# 📂 Chapter 3: Configurations Reference — Detailed Structure Blueprint

This document details the page tree and hierarchical heading structure for **Chapter 3: Configurations Reference** of the UDE VitePress Guides.

---

## 🗺️ Page Tree

```text
Chapter 3: Configurations Reference (/guides/)
├── global-settings.md          # Global orchestration configurations (ude_global.json).
└── target-settings.md          # Decentralized pipeline target configurations (ude_config.json).
```

---

## 📑 Page & Heading Hierarchies

### 📄 Page 1: `global-settings.md`

#### # Global System Configurations
*   *Description*: Reference manual for the centralized system settings file (`ude_global.json`).

#### ## 📋 File Schema Overview
*   *Description*: Main parameters and structure of the global configurations file.

#### ## ⚙️ Configuration Properties
*   *Description*: Detailed breakdown of key system settings.
    *   ### ### 1. Logging and Verbosity (`logging`)
        *   *Description*: Severity levels (DEBUG, INFO, WARNING, ERROR) and stderr/stdout destinations.
    *   ### ### 2. Cache Databases (`caching`)
        *   *Description*: Active toggles for L1 parsing caches and L2 rendering caches.
    *   ### ### 3. Directory Guard Rails (`guards`)
        *   *Description*: Strict boundaries to protect system folders from deletion.
        *   *Traceability*: Traces to **`REQ-FUN-22`** (Safe Directories Cleanup Guard Rails).

#### ## 📂 Default Configuration File Example
*   *Description*: Code block containing a fully documented template of `ude_global.json`.

---

### 📄 Page 2: `target-settings.md`

#### # Target Pipeline Configurations
*   *Description*: Specifications for defining individual, decentralized compilation targets.

#### ## 📐 Decentralized Configuration Strategy
*   *Description*: Rationale behind target-level configurations (`product.json` and `ude_config.json`) instead of one giant monolith config.

#### ## 📑 Target Config Schema Specifications
*   *Description*: Key configuration sections.
    *   ### ### 1. Codebase Metadata (`product`)
        *   *Description*: Product name, version, and default namespace.
    *   ### ### 2. Collector Specifications (`collector`)
        *   *Description*: Output paths for Doxygen XML directories and preprocessor flags.
    *   ### ### 3. Parser Specifications (`parser`)
        *   *Description*: Active exclusion lists and SWIG helper omissions.
    *   ### ### 4. Renderer Specifications (`renderer`)
        *   *Description*: Target output folder paths, Hugo Markdown vs Standalone HTML toggles, and Jinja2 templates.

#### ## 🔄 Relative Path Resolution Rules
*   *Description*: How UDE ensures path portability by resolving relative directories relative to the configuration file's physical parent folder.
    *   *Traceability*: Traces to Functional Requirement **`REQ-FUN-12`** (Path Portability and Resolution).

#### ## 📑 Complete Target Template (Example)
*   *Description*: Real-world code sample of a `ude_config.json` target configurations file.
