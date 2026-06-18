# Tests/run_regression_tests.py
# Regression testing runner using portable frozen baselines.

import os
import sys
import json
import gzip
import filecmp
import shutil
from pathlib import Path
from typing import Tuple, List

TESTS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = TESTS_DIR.parent
ENGINE_DIR = WORKSPACE_ROOT / "engine"

sys.path.insert(0, str(ENGINE_DIR))

from ude.parsers.doxygen import DoxygenXmlParser
from ude.renderers.static_html import HtmlRenderer
from ude.renderers.hugo_markdown import HugoMarkdownRenderer
from ude.models import ProjectCatalog

PROJECTS = [
    # FacetModeler Suite (Mandatory)
    {"id": "facetmodeler_api_cpp", "lang": "cpp"},
    {"id": "facetmodeler_api_cs", "lang": "cs"},
    {"id": "facetmodeler_api_java", "lang": "java"},
    {"id": "facetmodeler_api_py", "lang": "py"},
    # BimNv Suite (Run if baseline exists)
    {"id": "bimnv_api_cpp", "lang": "cpp"},
    {"id": "bimnv_api_cs", "lang": "cs"},
    {"id": "bimnv_api_java", "lang": "java"},
    {"id": "bimnv_api_py", "lang": "py"},
]

def compare_directories(dir1: Path, dir2: Path) -> List[str]:
    """Recursively compares two directories and returns differences."""
    diff_files = []
    dcmp = filecmp.dircmp(dir1, dir2)
    
    def _check_dcmp(sub_dcmp, relative_path=""):
        for f in sub_dcmp.left_only:
            diff_files.append(f"Missing in baseline: {os.path.join(relative_path, f)}")
        for f in sub_dcmp.right_only:
            diff_files.append(f"Extra file found: {os.path.join(relative_path, f)}")
        for f in sub_dcmp.diff_files:
            f1_path = Path(sub_dcmp.left) / f
            f2_path = Path(sub_dcmp.right) / f
            with open(f1_path, "r", encoding="utf-8", errors="ignore") as f1, \
                 open(f2_path, "r", encoding="utf-8", errors="ignore") as f2:
                c1 = f1.read().replace("\r\n", "\n")
                c2 = f2.read().replace("\r\n", "\n")
                if c1 != c2:
                    diff_files.append(f"Content mismatch: {os.path.join(relative_path, f)}")
                    
        for sub_name, sub_sub_dcmp in sub_dcmp.subdirs.items():
            _check_dcmp(sub_sub_dcmp, os.path.join(relative_path, sub_name))
            
    _check_dcmp(dcmp)
    return diff_files

def run_project_test(p_id: str, lang: str, temp_out_root: Path) -> Tuple[bool, str]:
    xml_baseline = TESTS_DIR / "baseline" / "xml" / p_id
    catalog_baseline_file = TESTS_DIR / "baseline" / "ir" / f"{p_id}.json.gz"
    html_baseline = TESTS_DIR / "baseline" / "html" / p_id
    hugo_baseline = TESTS_DIR / "baseline" / "hugo_md" / p_id
    
    if not xml_baseline.exists() or not catalog_baseline_file.exists():
        return True, "SKIPPED (Baselines not found)"
        
    print(f"\n[TEST] Running regression checks for: {p_id}")
    
    # Define languages
    lang_map = {
        "cpp": "cpp",
        "cs": "csharp",
        "java": "java",
        "py": "python"
    }
    language = lang_map.get(lang, "cpp")
    
    # --- PHASE 1: Parse xml_baseline and compare Pydantic models ---
    try:
        parser = DoxygenXmlParser()
        new_catalog = parser.parse(str(xml_baseline))
        
        # Load and decompress baseline model
        with gzip.open(catalog_baseline_file, "rt", encoding="utf-8") as f:
            baseline_data = json.load(f)
            
        new_catalog_data = json.loads(new_catalog.model_dump_json())
        
        # Mismatch checking
        if baseline_data != new_catalog_data:
            b_namespaces = {n["name"] for n in baseline_data.get("namespaces", [])}
            n_namespaces = {n["name"] for n in new_catalog_data.get("namespaces", [])}
            if b_namespaces != n_namespaces:
                return False, f"Parser Mismatch (Namespaces diff: {b_namespaces ^ n_namespaces})"
            return False, "Parser Mismatch (Internal JSON contents differ)"
            
        print("  -> L1 Parsing check: PASSED (Models are identical)")
    except Exception as e:
        return False, f"Parser Stage Exception: {e}"
        
    # Load catalog for render tests
    try:
        with gzip.open(catalog_baseline_file, "rt", encoding="utf-8") as f:
            raw_json = f.read()
        catalog_to_render = ProjectCatalog.model_validate_json(raw_json)
    except Exception as e:
        return False, f"Baseline catalog load error: {e}"
        
    # --- PHASE 2: HTML Renderer comparison ---
    if html_baseline.exists():
        try:
            temp_out_html = temp_out_root / "html" / p_id
            if temp_out_html.exists():
                shutil.rmtree(temp_out_html)
            temp_out_html.mkdir(parents=True, exist_ok=True)
            
            assets_src_dir = ENGINE_DIR / "ude/templates/css/default"
            html_renderer = HtmlRenderer(language=language, assets_src_dir=str(assets_src_dir))
            html_renderer.render(catalog_to_render, str(temp_out_html))
            
            differences = compare_directories(temp_out_html, html_baseline)
            if differences:
                print("  [ERROR] HTML Renderer output mismatches:")
                for d in differences[:10]:
                    print(f"    - {d}")
                if len(differences) > 10:
                    print(f"    ... and {len(differences) - 10} more differences.")
                return False, f"HTML Renderer Mismatch ({len(differences)} differences found)"
                
            print("  -> L2 HTML Rendering check: PASSED (HTML files are identical)")
        except Exception as e:
            return False, f"HTML Renderer Exception: {e}"
            
    # --- L3: Hugo Markdown Renderer comparison ---
    if hugo_baseline.exists():
        try:
            temp_out_hugo = temp_out_root / "hugo_md" / p_id
            if temp_out_hugo.exists():
                shutil.rmtree(temp_out_hugo)
            temp_out_hugo.mkdir(parents=True, exist_ok=True)
            
            hugo_renderer = HugoMarkdownRenderer(language=language)
            hugo_renderer.render(catalog_to_render, str(temp_out_hugo))
            
            differences = compare_directories(temp_out_hugo, hugo_baseline)
            if differences:
                print("  [ERROR] Hugo Markdown Renderer output mismatches:")
                for d in differences[:10]:
                    print(f"    - {d}")
                if len(differences) > 10:
                    print(f"    ... and {len(differences) - 10} more differences.")
                return False, f"Hugo Markdown Renderer Mismatch ({len(differences)} differences found)"
                
            print("  -> L3 Hugo MD Rendering check: PASSED (Markdown files are identical)")
        except Exception as e:
            return False, f"Hugo MD Renderer Exception: {e}"
            
    return True, "PASSED"

def main():
    print("=" * 60)
    print("Running 3-tier Regression Testing Suite...")
    print("=" * 60)
    
    temp_out_root = WORKSPACE_ROOT / "ude_output_test_temp"
    if temp_out_root.exists():
        shutil.rmtree(temp_out_root)
    temp_out_root.mkdir(parents=True, exist_ok=True)
    
    failed = 0
    passed = 0
    skipped = 0
    
    try:
        for p in PROJECTS:
            success, status = run_project_test(p["id"], p["lang"], temp_out_root)
            if "SKIPPED" in status:
                skipped += 1
                print(f"[SKIP] {p['id']}: {status}")
            elif success:
                passed += 1
                print(f"[OK]   {p['id']}: {status}")
            else:
                failed += 1
                print(f"[FAIL] {p['id']}: {status}")
                
        print("\n" + "=" * 60)
        print(f"TEST RESULTS: {passed} PASSED, {failed} FAILED, {skipped} SKIPPED")
        print("=" * 60)
        
        if failed > 0:
            sys.exit(1)
            
    finally:
        # Safe Cleanup
        if temp_out_root.exists():
            shutil.rmtree(temp_out_root)

if __name__ == "__main__":
    main()
