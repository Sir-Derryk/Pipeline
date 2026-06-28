---
name: docomatic-semantics-analysis
description: >-
  Language-specific SOP and automated script workflow for analyzing multiple Doc-O-Matic 
  examples of a single target language (C++, C#, Java, etc.) to reconstruct and document 
  its unique Table of Contents (ToC) hierarchy, entity mappings, and rules.
---

# Skill: Language-Specific Doc-O-Matic Semantics Analysis & ToC Recovery

## 🎯 General Description
This skill defines the methodology (SOP) and automation workflow to reverse-engineer and recover the Table of Contents (ToC) structure, logical hierarchy, and file-mapping rules **specifically for a single target programming language** (e.g., C++, C#, or Java) by analyzing and synthesizing findings from **multiple documentation examples** generated for that language.

By running this skill for a chosen language, the assistant will run bulk scripts across all available HTML directories of that language, analyze representative files, resolve inconsistencies between examples (e.g., if one example has functions and another does not), and produce a unified language-specific specification in both human-readable Markdown and machine-readable JSON/YAML.

---

## ⚙️ Workflow for Target Language Analysis

When requested to analyze Docomatic's semantics or reconstruct the ToC for a specific language (e.g., *"Analyze C++ Docomatic examples to recover its ToC rules"*, *"Analyze C# SWIG examples"*):

### 1. Phase 1: Language-Specific Bulk Scraping
The canonical scraper lives at `Tests/docomatic_scraper.py`. Create it on first use if absent; update it in-place on subsequent runs — never generate a new per-session copy. The script must be parameterized via CLI flags:

```bash
poetry run python Tests/docomatic_scraper.py \
  --language cpp \
  --folders "reference/FacetModeler_API_CPP" "reference/oda_bimnv_cpp_docs" \
  --output-dir TOCStructures/
```

Pass `--dry-run` to print findings to stdout without writing any files (useful for quick inspection without triggering consent-first gating).

The script should traverse **all provided reference folders of the target language** and collect:
* Unique filename prefixes starting with `!!`.
* Distinct member types found in `!!MEMBERTYPE_` files.
* File naming conventions and translation tokens.
* Complete lists of detected entity types (namespaces, classes, structs, enums, methods, functions, variables, typedefs, properties, delegates, indexers, etc.) and verify which examples contain them.

### 2. Phase 2: Targeted Semantics & HTML Layout Inspection
The assistant must inspect a minimal, representative sample of files across the language examples to verify the HTML layout:
* **Classes / Interfaces Index**: Inspect one `!!CLASSES_` file to see how classes and interfaces of this language are listed in tables.
* **Structs / Enums Index**: Inspect one `!!RECORDS_` file to understand how records/structs/enums are presented.
* **Class Members Index**: Inspect one `!!MEMBERTYPE_` file of a common type (e.g., `Methods` or `Fields`) to confirm the inner list structure.
* **Overload Dispatcher**: Inspect one `!!OVERLOADED_` file to see how constructors or methods with multiple signatures are represented for this language.

### 3. Phase 3: Synthesis of Language-Specific ToC Rules
The assistant must compare the findings from all analyzed folders of the chosen language to formulate a unified ruleset:
* **Unified Scope Hierarchy**: Define how scopes are nested (e.g., how nested namespaces or nested classes are grouped for this language).
* **Flat-Mapping Filename Rules**: Establish the exact rules of translating logical paths (using double colons `::` for C++ or dots `.` for C#/Java) and parameter symbols (`*`, `&`, `<`) into flat filenames on disk.
* **Optional/Conditional Entities**: Document entities that are optional (e.g., in C++ some examples might have free functions or global variables, while others don't; in C# / Java, free functions are absent, but there may be properties or indexers).
* **Optionality Decision Rule**: An entity type is classified as OPTIONAL if it is absent in ≥ 50% of the analyzed language folders. An entity type is classified as CONDITIONAL if it is present in some folders but absent in others without a structural rule explaining the absence. Document the decision rationale for each optional entity type in the generated `toc_<lang>.md`.

### 4. Phase 4: Reconstructed Outputs Generation *(Consent-gated)*
Present the recovered ToC specification in the chat first. Then ask:
> "Shall I write `TOCStructures/toc_<lang>.md` and `TOCStructures/toc_<lang>.json` to disk?"
Only proceed with file creation upon explicit confirmation. Never auto-write.

For the analyzed language, the assistant must generate two files in the workspace (using `toc_<lang>.md` and `toc_<lang>.json`):

1. **Human-Readable Specification** (`toc_<lang>.md` inside `TOCStructures/`):
   * Detailed logical tree representation of the ToC hierarchy.
   * Path-to-filename translation table with examples.
   * Specification of virtual folder groupings (e.g., "Classes", "Methods", "Properties").
   * Link to the machine-readable specification.

2. **Machine-Readable Specification** (`toc_<lang>.json` or `.yaml` inside `TOCStructures/`):
   * Contains the exact recovered algorithmic JSON representation of the language's ToC structure (see schema below).

---

## 📄 Target Language Algorithmic Schema (JSON/YAML)

The recovered JSON/YAML specification for the target language must follow this clean, algorithmic schema:

```json
{
  "language": "cpp",                        // Target language (cpp, cs, java, etc.)
  "recovered_toc_algorithm": {
    "file_naming_rules": {
      "namespace_separator": "__",
      "class_member_separator": "__",
      "method_overload_marker": "@",
      "special_characters_translation": {
        "*": "_ptr",
        "&": "_ref",
        " ": "_",
        "<": "_lt_",
        ">": "_gt_"
      }
    },
    "logical_toc_hierarchy": {
      "root_node_title": "API Reference (C++)",
      "schema_version": "2.0",
      "note": "Fields marked (v2.0+) require GAP-03 typed IR models. On v1.0 IR, these virtual folders will be empty and must be omitted from the rendered ToC.",
      "virtual_group_folders": {
        "namespace_level": [
          "Classes",
          "Structs_and_Enums",
          "Functions",
          "Types",
          "Variables",
          "Constants"
        ],
        "class_level": [
          "Methods",
          "Properties",
          "Fields",
          "Operators",
          "Nested_Classes",
          "TypeAliases",
          "Constants"
        ]
      },
      "entity_placement_rules": {
        "constructors": "Placed at the top of the class node, before any virtual folders",
        "destructors": "Placed immediately after constructors",
        "methods": "Grouped inside 'Methods' virtual folder",
        "operators": "Grouped inside 'Operators' virtual folder"
      }
    },
    "aggregating_file_patterns": {
      "global_symbol_index": "^!!SYMREF\\.html$",
      "classes_index": "^!!CLASSES_(?P<scope>.+)\\.html$",
      "records_index": "^!!RECORDS_(?P<scope>.+)\\.html$",
      "functions_index": "^!!FUNCTIONS_(?P<scope>.+)\\.html$",
      "types_index": "^!!TYPES_(?P<scope>.+)\\.html$",
      "variables_index": "^!!VARIABLES_(?P<scope>.+)\\.html$",
      "class_members_index": "^!!MEMBERTYPE_(?P<member_type>[A-Za-z_]+)_(?P<class_scope>.+)\\.html$",
      "constructor_overloads_dispatcher": "^!!OVERLOADED_(?P<class_name>[A-Za-z0-9_]+)_(?P<class_scope>.+)\\.html$",
      "method_overloads_dispatcher": "^!!OVERLOADED_Methods_(?P<method_name>[A-Za-z0-9_]+)_(?P<class_scope>.+)\\.html$"
    }
  }
}
```

---

## 🛠️ Canonical Scraper Contract

The scraper at `Tests/docomatic_scraper.py` must satisfy this interface contract (implement on first creation; maintain on all subsequent updates — never recreate as a per-session ad-hoc script):

**Required CLI flags:**
* `--language <cpp|cs|java|py>` — target language (required)
* `--folders <path1> [<path2> ...]` — reference HTML directories (required, 1+)
* `--output-dir <dir>` — where to write `toc_<lang>.json` (required for write mode)
* `--dry-run` — print findings to stdout only; NO files written (consent-first safe)

**Required output structure:**
* When `--dry-run`: print a JSON summary to stdout with keys `entity_types`, `filename_prefixes`, `member_types`, `total_files_scanned`.
* When writing: produce `<output-dir>/toc_<lang>.json` conforming to the schema in §Target Language Algorithmic Schema above.

**Implementation approach:**
* Directory traversal matching file patterns against the `aggregating_file_patterns` regex map defined in the JSON schema.
* Compile a matrix of found entities across all `--folders` to identify commonalities and differences among language-specific examples.
* Use `argparse` for all CLI arguments — no positional arguments, no interactive input.
