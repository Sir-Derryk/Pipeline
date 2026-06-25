# Tests/prepare_baseline.py
# Automatic Golden Master baseline preparation script.
# Stores portable regression baselines in the Tests/baseline/ folder.

import os
import sys
import json
import gzip
import shutil
import argparse
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = TESTS_DIR.parent
ENGINE_DIR = WORKSPACE_ROOT / "engine"

# Inject local engine folder to python path
sys.path.insert(0, str(ENGINE_DIR))

from ude.collectors.doxygen import DoxygenXmlCollector
from ude.parsers.doxygen import DoxygenXmlParser
from ude.renderers.static_html import HtmlRenderer
from ude.renderers.hugo_markdown import HugoMarkdownRenderer
from ude.orchestrator import UdeOrchestrator

# Target Projects Configurations
FACETMODELER_PROJECTS = [
    {"id": "facetmodeler_api_cpp", "config": WORKSPACE_ROOT / "ude_projects/FacetModeler/facetmodeler_api_cpp/ude_doc_config.json", "lang": "cpp"},
    {"id": "facetmodeler_api_cs", "config": WORKSPACE_ROOT / "ude_projects/FacetModeler/facetmodeler_api_cs/ude_doc_config.json", "lang": "cs"},
    {"id": "facetmodeler_api_java", "config": WORKSPACE_ROOT / "ude_projects/FacetModeler/facetmodeler_api_java/ude_doc_config.json", "lang": "java"},
    {"id": "facetmodeler_api_py", "config": WORKSPACE_ROOT / "ude_projects/FacetModeler/facetmodeler_api_py/ude_doc_config.json", "lang": "py"},
]

BIMNV_PROJECTS = [
    {"id": "bimnv_api_cpp", "config": WORKSPACE_ROOT / "ude_projects/bimnv/bimnv_api_cpp/ude_doc_config.json", "lang": "cpp"},
    {"id": "bimnv_api_cs", "config": WORKSPACE_ROOT / "ude_projects/bimnv/bimnv_api_cs/ude_doc_config.json", "lang": "cs"},
    {"id": "bimnv_api_java", "config": WORKSPACE_ROOT / "ude_projects/bimnv/bimnv_api_java/ude_doc_config.json", "lang": "java"},
    {"id": "bimnv_api_py", "config": WORKSPACE_ROOT / "ude_projects/bimnv/bimnv_api_py/ude_doc_config.json", "lang": "py"},
]

MOCK_PROJECTS = [
    {"id": "mock_api_cpp", "config": WORKSPACE_ROOT / "ude_projects/mock/mock_api_cpp/ude_doc_config.json", "lang": "cpp"},
    {"id": "mock_api_cs", "config": WORKSPACE_ROOT / "ude_projects/mock/mock_api_cs/ude_doc_config.json", "lang": "cs"},
    {"id": "mock_api_java", "config": WORKSPACE_ROOT / "ude_projects/mock/mock_api_java/ude_doc_config.json", "lang": "java"},
    {"id": "mock_api_py", "config": WORKSPACE_ROOT / "ude_projects/mock/mock_api_py/ude_doc_config.json", "lang": "py"},
]


# Track current project being compiled for our hooks
global_current_project_id = None
global_current_project_lang = None

# 1. Monkeypatch Cleanup to intercept Doxygen XMLs
original_cleanup = DoxygenXmlCollector.cleanup

def custom_cleanup(self, temp_xml_dir):
    global global_current_project_id
    xml_src = temp_xml_dir / "xml"
    if xml_src.exists() and global_current_project_id:
        xml_dest = TESTS_DIR / "baseline" / "xml" / global_current_project_id
        if xml_dest.exists():
            shutil.rmtree(xml_dest)
        shutil.copytree(xml_src, xml_dest)
        print(f"  [XML Baseline] Successfully saved to {xml_dest}")
    original_cleanup(self, temp_xml_dir)

DoxygenXmlCollector.cleanup = custom_cleanup

# 2. Monkeypatch Parsing to intercept Pydantic IR Catalogs (Gzip format)
# We also render BOTH HTML and Hugo MD formats on-the-fly from the parsed catalog!
original_parse = DoxygenXmlParser.parse

def custom_parse(self, xml_dir_path):
    global global_current_project_id, global_current_project_lang
    catalog = original_parse(self, xml_dir_path)
    if global_current_project_id:
        # Save compressed JSON/IR
        catalog_dest_dir = TESTS_DIR / "baseline" / "ir"
        catalog_dest_dir.mkdir(parents=True, exist_ok=True)
        catalog_dest = catalog_dest_dir / f"{global_current_project_id}.json.gz"
        
        json_data = catalog.model_dump_json(indent=2)
        with gzip.open(catalog_dest, "wt", encoding="utf-8") as f:
            f.write(json_data)
        print(f"  [IR Baseline] Successfully saved compressed Gzip to {catalog_dest}")
        
        # Determine language identifier
        lang_map = {
            "cpp": "cpp",
            "cs": "csharp",
            "java": "java",
            "py": "python"
        }
        language = lang_map.get(global_current_project_lang, "cpp")
        
        # --- HTML RENDERING ---
        html_dest = TESTS_DIR / "baseline" / "html" / global_current_project_id
        if html_dest.exists():
            shutil.rmtree(html_dest)
        html_dest.mkdir(parents=True, exist_ok=True)
        
        assets_src_dir = ENGINE_DIR / "ude/templates/css/default"
        html_renderer = HtmlRenderer(language=language, assets_src_dir=str(assets_src_dir))
        html_renderer.render(catalog, str(html_dest))
        print(f"  [HTML Baseline] Successfully rendered HTML to {html_dest}")
        
        # --- HUGO MD RENDERING ---
        hugo_dest = TESTS_DIR / "baseline" / "hugo_md" / global_current_project_id
        if hugo_dest.exists():
            shutil.rmtree(hugo_dest)
        hugo_dest.mkdir(parents=True, exist_ok=True)
        
        hugo_renderer = HugoMarkdownRenderer(language=language)
        hugo_renderer.render(catalog, str(hugo_dest))
        print(f"  [Hugo MD Baseline] Successfully rendered Hugo Markdown to {hugo_dest}")
        
    return catalog

DoxygenXmlParser.parse = custom_parse

def main():
    parser = argparse.ArgumentParser(description="Prepare UDE test baselines.")
    parser.add_argument(
        "--suite",
        choices=["facetmodeler", "both", "mock", "all"],
        default="facetmodeler",
        help="Which projects suite to run. Default is facetmodeler."
    )
    args = parser.parse_args()
    
    projects_to_run = []
    if args.suite == "facetmodeler":
        projects_to_run = FACETMODELER_PROJECTS
    elif args.suite == "both":
        projects_to_run = FACETMODELER_PROJECTS + BIMNV_PROJECTS
    elif args.suite == "mock":
        projects_to_run = MOCK_PROJECTS
    elif args.suite == "all":
        projects_to_run = FACETMODELER_PROJECTS + BIMNV_PROJECTS + MOCK_PROJECTS

        
    print("=" * 60)
    print(f"Preparing 3-Tier Golden Master baseline (Suite: {args.suite.upper()})...")
    print("=" * 60)
    
    # Initialize standard Orchestrator
    orchestrator = UdeOrchestrator()
    
    for p in projects_to_run:
        global global_current_project_id, global_current_project_lang
        global_current_project_id = p["id"]
        global_current_project_lang = p["lang"]
        
        print(f"\n[BUILD] Processing project: {p['id']}")
        
        # Run standard generation pipeline
        success = orchestrator.run_target(p["config"])
        if not success:
            print(f"[ERROR] Failed to run orchestrator for {p['id']}")
            sys.exit(1)
            
    print("\n" + "=" * 60)
    print("[SUCCESS] Portables baselines prepared and stored in Tests/baseline/ successfully.")
    print("=" * 60)

if __name__ == "__main__":
    main()
