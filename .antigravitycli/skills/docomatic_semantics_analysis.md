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
To process large amounts of data across multiple SDK directories for the chosen language, the assistant must run a Python scraper script. The script should traverse **all provided reference folders of the target language** (e.g., for C++: `FacetModeler_API_CPP/` and `oda_bimnv_cpp_docs/`) and collect:
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

### 4. Phase 4: Reconstructed Outputs Generation
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
      "virtual_group_folders": {
        "namespace_level": ["Classes", "Structs_and_Enums", "Functions", "Types", "Variables"],
        "class_level": ["Methods", "Properties", "Fields", "Operators", "Nested_Classes"]
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

## 🛠️ Automated Scraper Design
During Phase 1, the assistant must generate an ad-hoc Python scraper inside the scratch directory. The script must be parameterized by:
* `TARGET_LANGUAGE_FOLDERS`: List of paths to the target language examples.
* `SEPARATOR_SYMBOLS`: Naming symbols to analyze.

The script must perform directory traversal, match file patterns against regex, and compile a matrix of found entities to identify commonalities and differences among the language-specific folders.
