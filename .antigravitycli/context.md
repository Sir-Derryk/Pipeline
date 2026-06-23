# Universal Documentation Engine (UDE) — Project Context

## 🎯 Project Core
An extensible, pipeline-based software tool for technical documentation generation. It ingests source code metrics and layouts (via exported Doxygen XML), parses its structure and comments, maps them into an internal, language-agnostic Intermediate Representation (IR), and renders them into static website content (Markdown for Hugo/Docusaurus), standalone offline HTML pages, or structured data (RAG JSON/XML).

## 🛠️ Technology Stack
- **Implementation Language**: Python
- **Coding Style**: PEP 8 (standards defined in `.antigravitycli/styles/code_style.md`)
- **Key Dependencies**: `lxml` / `xml.etree` (XML Parsing), `Jinja2` (Templating Engine)
- **Primary Source Input**: Doxygen XML
- **Testing Framework**: pytest (standards defined in `testing_style.md`)

## 📐 UDE Portal Architecture
The project is structured as an "umbrella" repository linking specialized Git Submodules:

```text
Pipeline/ (Umbrella Repository)
├── design-docs/            # [Git Submodule] https://github.com/Sir-Derryk/ude-design-docs.git
│                           # Pipeline #1: Project Knowledge Base (BRD, SRS, SDD) -> Docusaurus (fully versioned)
├── engine/                 # [Git Submodule] https://github.com/Sir-Derryk/universal-document-engine.git
│                           # Core UDE Source Code (Python; no internal Git-versioning of compiled API reference docs)
└── user-docs/              # [Git Submodule] https://github.com/Sir-Derryk/ude-user-docs.git
                            # User/Admin Guides and Portal (VitePress — premium layout and design)
```

### UDE Publisher Pipelines and Triggers:
1. **Pipeline #1 (Project Documentation)**: 
   - *Trigger*: Commits in `design-docs/**` or updates under `.antigravitycli/**`.
   - *Result*: Compiles the design knowledge base using **Docusaurus** (isolated search and full versioning of the architecture).
2. **Pipeline #2 (User Documentation)**: 
   - *Trigger*: Commits in `user-docs/content/**` (User/Admin Guides).
   - *Result*: Compiles public manuals using **VitePress** (premium aesthetics, instant client-side SPA navigation).
3. **Pipeline #3 (API Reference)**: 
   - *Trigger*: Commits in core source code (`engine/**`).
   - *Result*: Generates API Reference on-the-fly (runs UDE compiler over source code/XML to output static Markdown/HTML/RAG JSON directly, avoiding any Git history noise or PR bloat).

## 📋 Document Development Status
- [x] BRD (Business Requirements Document) — *Updated & Completed (covers C++/C#/Java/Python, expanded XML/AST inputs and HTML/Markdown/RAG JSON outputs, addresses automation pain points and EOL tools, moves versioning strictly to project-docs level)*
- [x] SRS (Software Requirements Specification) — *Updated & Synchronized with the new BRD*
- [x] SDD (Software Design Document) — *Updated & Detailed (adds BaseParser/BaseRenderer class contracts, decentralized hierarchical JSON configurations, and Doxygen automation)*
- [x] User Guide & Admin Deployment Guides — *Completed (Comprehensive 4-chapter manuals written in VitePress portal, verified build integrity)*

## ❓ Architectural Decisions & Open Issues (Decision Log)

### ✅ Agreed Decisions (Q&A):
* **Question 1 (Section 2.2 — Pain Points)**: All 18 user-selected pain points have been integrated and detailed across 6 core categories (A-F) in the BRD.
* **Question 2 (Section 1.2 — Business Goals)**: Defined and approved 7 quantitative quality metrics (performance handling 10,000 entities across 1,000 files in under 5 seconds, 100% clean Git, AI-driven code completion with manual validation, incremental AI translation caching, RAG JSON exports, compilation token cost reporting, and documentation coverage auditing).
* **Question 1.1 (Initial Parsing Scope)**: For version 1.0, UDE limits its scope to parsing raw XML structures produced by Doxygen. The boundaries of extracted entities in the IR completely match Doxygen XML schemas and capabilities.
* **Question 1.2 (Future Direct Parsers)**: In subsequent releases, UDE will introduce specialized native code parsers utilizing `libclang`, `tree-sitter`, native ASTs (e.g., Python's `ast` module), or `regexp`, reinforcing the need for strict parsing level isolation via the abstract `BaseParser`.
* **Question 2.1 (Translation Cache Synchronization in Git) [DEFERRED - FUTURE PHASES (v2.0+)]**: Merge conflicts and pipeline race conditions in CI/CD are resolved using role-based access control. Standard developers (in feature branches) run parsing and translation in *Read-Only* mode (reading from the repository cache without writing back). Cache updates are performed strictly inside a protected CI/CD environment or by a dedicated Translation Manager account utilizing repository secrets and protected Git `CODEOWNERS` configurations. (This feature is deferred to future releases).
* **Question 2.2 (Server-Side Push Gating and Context Extraction)**: During commits of undocumented code, the UDE gate supports 4 execution modes: `reject-undocumented` (strictly blocks merges via standard read-only verification), `allow-undocumented` (prints warnings but allows merge), `auto-document` (invokes write-enabled `ude-enrich` to generate English docstrings and write them back), and `verify-document` (generates non-blocking draft PR suggestions for review). The default language for all docstrings is English. To ensure accurate docstrings, the LLM receives function declarations and bodies. Local developer runs operate in offline mode by default to protect API budgets.
* **Question 2.3 (Asynchronous Localization and XLIFF Support) [DEFERRED - FUTURE PHASES (v2.0+)]**: Localization verification is non-blocking. Draft AI translations are generated in the background strictly after a successful merge into `master`, preventing translation cost overhead for short-lived feature branches. Unverified pages display fallback English text or an "AI-translated draft" banner. Translation managers can export source text to `.xlf` format, send to translation partners, and import verified results. (This feature is deferred to future releases).
* **Question 3 (Configuration, Local Automation, Caching, and Portability)**:
  1. **Decentralized & Hierarchical Config Merging**: Agreed on a decentralized configuration structure. System configurations are defined in `ude_global_config.json` (logging, caching, fallback policies). Target projects define local `ude_doc_config.json` configurations. The orchestrator walks up the directory tree to find `ude_global_config.json` and performs a flat-merge (`config = {**resolved_global_config, **config}`), allowing target-specific options to override global ones.
  2. **Doxygen-Backend and Sequential Doxyfile Assembly**: Doxygen acts as the preprocessor for all languages in v1.0. To build the Doxyfile used during parsing, a three-stage sequential merge model is executed: first, a global template (`engine/ude/templates/Doxyfile`) containing default performance parameters (`NUM_PROC_THREADS`, `LOOKUP_CACHE_SIZE`, `XML_PROGRAMLISTING`) is loaded; second, a project-specific template (defined in `ude_doc_config.json`) is appended to override defaults; third, dynamic runtime-specific entries (such as `INPUT`, `OUTPUT_DIRECTORY`, etc.) are appended. The collector validates the environment (`validate_environment`) and executes a guaranteed clean-up routine under `try...finally` using strict guard rails (preventing deletion of `/`, `.`, or `..`).
  3. **Batch Automation and Preflight Checks**: Three levels of batch files are used: `engine/generate_all.bat`, `engine/generate_<product>.bat`, and target-specific `generate_docs.bat` files. They verify Python on the host (exiting with code 5 if missing) and auto-install missing packages (`pydantic`, `lxml`, `jinja2`) via `pip install` before executing the orchestrator.
  4. **Target Isolation and IR Compression**: Intermediate representation (`intermediate_representation.json.gz`) and cache databases (`.build_cache.json.gz`) are isolated inside product-specific subfolders (e.g., `ude/Bimnv/bimnv_cpp/`), keeping the output folder clean. IR files are compressed using Gzip.
  5. **Two-Level Incremental Build Cache**:
     - *Parsing (L1)*: Tracks mtime and contents hash of XML files. If unchanged, loads cached IR directly.
     - *Rendering (L2)*: Compares IR signature hash and Jinja2 templates. If unchanged, skips writing target files.
  6. **Path Portability & Combined Output Resolution**: Raw paths must not be hardcoded in Python modules. All configurations specify paths relative to their respective configuration files. Furthermore, if `output_base_dir` and `output_subdir` are present, the engine combines them into a single absolute path (`out_dir = base_dir_ref / output_base_dir / output_subdir`), falling back to standard `output_dir` if either is absent, ensuring 100% path portability and backward compatibility.
* **Question 4 (Git Repository Folder Structure & Gitignores Cleanup)**:
  1. **Source Code Exclusion**: The local `/src` directory contains C++ source files, which are strictly outside of version control and must remain ignored.
  2. **Precise UDE Exclusions**: Replaced the global `/ude` folder ignore with precise rules ignoring build outputs (Doxygen intermediate XML folders, generated HTML folders, `.json.gz` files, and `.build_cache.json` files) across all product directories (`bimnv`, `facetmodeler`, `iges`, `map`). This ensures that product configurations (such as `ude_sdk_config.json` and `ude_doc_config.json`) are correctly tracked by Git, while dynamic build outputs remain excluded.
  3. **Specification Files Cleanup**: Staged the deletion of 5 obsolete legacy specification files from the parent root repository (`chapter_1_quick_start_structure.md`, `chapter_2_coding_standards_structure.md`, `chapter_3_configurations_structure.md`, `chapter_4_case_study_structure.md`, `ude_portal_blueprint.md`).
  4. **Submodule Gitignore Upgrade**: Configured ignores for `hugo-site/public/`, `hugo-site/.hugo_build.lock`, and temporary `engine/` symlink in `user-docs/.gitignore`.

### ⏳ Open Issues (Awaiting Discussion):
* **Question 5.1 (Single Sign-On (SSO) for Documentation Portals)**: Resolving SSO routing for static sites (Docusaurus and VitePress) hosted on GitHub Pages. Discussion deferred on custom domain routing via Cloudflare Zero Trust Access with OIDC/OAuth providers.

## 🗺️ Current Roadmap & Status
- [x] Hierarchical doc tree refactoring and clean layout division.
- [x] Added Roadmap and Document Version History section starting with version 0.1 (Requirements).
- [x] Configured Docusaurus version selector dropdown (`docsVersionDropdown`).
- [x] Upgraded old legacy admonitions to modern syntax in 11 files.
- [x] Designed core class contracts (`BaseParser`, `BaseRenderer`, exceptions, and CLI interfaces).
- [x] Verified Docusaurus compilation integrity (compiled successfully).
- [x] Set up decentralized target directory structure under `ude/` for BimNv, FacetModeler, IGES, and Map.
- [x] Completely removed `toc.yaml` files from requirements and folder structures.
- [x] Updated Requirements Quality Audit report using the 10-point scorecard.
- [x] Expanded, verified, and detailed the developer TDD task specifications under `.antigravitycli/tasks/`.
- [x] Integrated requirements audit recommendations into the task checklists.
- [x] Aligned Gantt milestone schedules (`schedule.md` and `active_plan.md`) with task modifications.
- [x] Freeze/save version 0.3 of specifications and transition current development focus to version 0.4 ("Documentation").
- [x] Prepare local Python development environment (virtual environment, poetry/pip, pytest) to begin core module coding.
- [x] Implement TSK-PAR-02 (Doxygen XML Parser Engine) with 100% test coverage and update compliance registries.
- [x] Implement TSK-COL-01 (BaseCollector Interface and DoxygenXmlCollector) with 95% statement coverage and safe cleanup guard rails.
- [x] Implement TSK-NML-01 (Docstring Normalizer to CommonMark Markdown) with 100% statement coverage and Javadoc/Doxygen/Google support.
- [x] Implement TSK-NML-02 (Exclusion Filters and Hidden Code Blocks) with 100% statement coverage and support for DOM-IGNORE, cond, and internal.
- [x] Implement TSK-RND-01 (Hugo Markdown Renderer & Front-Matter Metadata) with 100% statement coverage.
- [x] Implement TSK-RND-02 (Standalone Static HTML Compiler) with 100% statement coverage.
- [x] Implement TSK-RND-03 (Sidebar Navigation Refactoring & Namespace Landing Pages) with 100% statement coverage.
- [x] Implement TSK-CLI-01 (Non-Interactive CLI Command Processor) with 100% statement coverage.
- [x] Implement TSK-CLI-03 (Multi-Target Orchestration Engine) with 100% statement coverage.
- [x] Implement TSK-CLI-02 (E2E Integration Testing & Coverage Verification) with 100% statement coverage.
- [x] Configure and implement UDE Publisher (combined VitePress + Hugo publication pipeline with cross-repo automated triggers).
- [x] Standardize and unify visual appearance and design theme across all three documentation portals (Docusaurus, VitePress, Hugo) to make them completely cohesive, utilizing matching fonts (Inter + JetBrains Mono) and brand color palettes.
- [x] Freeze/save version 0.4 of specifications and transition current development focus to version 0.5 ("Testing documentation").
- [x] Analyze and clean up Git folder structures and `.gitignore` files in parent repository and submodules.
- [x] Create root-level folder 'ude_output', update all 11 sub-projects to target 'ude_output/' subfolders, and configure bat files to generate only HTML help.
- [x] Develop Table of Contents (toc_py.md) and machine-readable parser rules (toc_py.json) for Python, matching C++ and C# quality standards.
- [x] Implement active navigation item auto-focus and vertical scroll-top alignment (TSK-RND-04) for standalone HTML and Hugo layouts, synchronizing all specifications.
- [x] Implement language-specific entity layouts, dynamic ToC sorting and pruning (TSK-RND-05) with 100% statement coverage.
- [x] Implement Python SWIG wrapper docstring normalization (Sphinx/RST parsing) and logical parameter merging to produce clean HTML documentation tables.
# Universal Documentation Engine (UDE) — Project Context

## 🎯 Project Core
An extensible, pipeline-based software tool for technical documentation generation. It ingests source code metrics and layouts (via exported Doxygen XML), parses its structure and comments, maps them into an internal, language-agnostic Intermediate Representation (IR), and renders them into static website content (Markdown for Hugo/Docusaurus), standalone offline HTML pages, or structured data (RAG JSON/XML).

## 🛠️ Technology Stack
- **Implementation Language**: Python
- **Coding Style**: PEP 8 (standards defined in `.antigravitycli/styles/code_style.md`)
- **Key Dependencies**: `lxml` / `xml.etree` (XML Parsing), `Jinja2` (Templating Engine)
- **Primary Source Input**: Doxygen XML
- **Testing Framework**: pytest (standards defined in `testing_style.md`)

## 📐 UDE Portal Architecture
The project is structured as an "umbrella" repository linking specialized Git Submodules:

```text
Pipeline/ (Umbrella Repository)
├── design-docs/            # [Git Submodule] https://github.com/Sir-Derryk/ude-design-docs.git
│                           # Pipeline #1: Project Knowledge Base (BRD, SRS, SDD) -> Docusaurus (fully versioned)
├── engine/                 # [Git Submodule] https://github.com/Sir-Derryk/universal-document-engine.git
│                           # Core UDE Source Code (Python; no internal Git-versioning of compiled API reference docs)
└── user-docs/              # [Git Submodule] https://github.com/Sir-Derryk/ude-user-docs.git
                            # User/Admin Guides and Portal (VitePress — premium layout and design)
```

### UDE Publisher Pipelines and Triggers:
1. **Pipeline #1 (Project Documentation)**: 
   - *Trigger*: Commits in `design-docs/**` or updates under `.antigravitycli/**`.
   - *Result*: Compiles the design knowledge base using **Docusaurus** (isolated search and full versioning of the architecture).
2. **Pipeline #2 (User Documentation)**: 
   - *Trigger*: Commits in `user-docs/content/**` (User/Admin Guides).
   - *Result*: Compiles public manuals using **VitePress** (premium aesthetics, instant client-side SPA navigation).
3. **Pipeline #3 (API Reference)**: 
   - *Trigger*: Commits in core source code (`engine/**`).
   - *Result*: Generates API Reference on-the-fly (runs UDE compiler over source code/XML to output static Markdown/HTML/RAG JSON directly, avoiding any Git history noise or PR bloat).

## 📋 Document Development Status
- [x] BRD (Business Requirements Document) — *Updated & Completed (covers C++/C#/Java/Python, expanded XML/AST inputs and HTML/Markdown/RAG JSON outputs, addresses automation pain points and EOL tools, moves versioning strictly to project-docs level)*
- [x] SRS (Software Requirements Specification) — *Updated & Synchronized with the new BRD*
- [x] SDD (Software Design Document) — *Updated & Detailed (adds BaseParser/BaseRenderer class contracts, decentralized hierarchical JSON configurations, and Doxygen automation)*
- [x] User Guide & Admin Deployment Guides — *Completed (Comprehensive 4-chapter manuals written in VitePress portal, verified build integrity)*

## ❓ Architectural Decisions & Open Issues (Decision Log)

### ✅ Agreed Decisions (Q&A):
* **Question 1 (Section 2.2 — Pain Points)**: All 18 user-selected pain points have been integrated and detailed across 6 core categories (A-F) in the BRD.
* **Question 2 (Section 1.2 — Business Goals)**: Defined and approved 7 quantitative quality metrics (performance handling 10,000 entities across 1,000 files in under 5 seconds, 100% clean Git, AI-driven code completion with manual validation, incremental AI translation caching, RAG JSON exports, compilation token cost reporting, and documentation coverage auditing).
* **Question 1.1 (Initial Parsing Scope)**: For version 1.0, UDE limits its scope to parsing raw XML structures produced by Doxygen. The boundaries of extracted entities in the IR completely match Doxygen XML schemas and capabilities.
* **Question 1.2 (Future Direct Parsers)**: In subsequent releases, UDE will introduce specialized native code parsers utilizing `libclang`, `tree-sitter`, native ASTs (e.g., Python's `ast` module), or `regexp`, reinforcing the need for strict parsing level isolation via the abstract `BaseParser`.
* **Question 2.1 (Translation Cache Synchronization in Git) [DEFERRED - FUTURE PHASES (v2.0+)]**: Merge conflicts and pipeline race conditions in CI/CD are resolved using role-based access control. Standard developers (in feature branches) run parsing and translation in *Read-Only* mode (reading from the repository cache without writing back). Cache updates are performed strictly inside a protected CI/CD environment or by a dedicated Translation Manager account utilizing repository secrets and protected Git `CODEOWNERS` configurations. (This feature is deferred to future releases).
* **Question 2.2 (Server-Side Push Gating and Context Extraction)**: During commits of undocumented code, the UDE gate supports 4 execution modes: `reject-undocumented` (strictly blocks merges via standard read-only verification), `allow-undocumented` (prints warnings but allows merge), `auto-document` (invokes write-enabled `ude-enrich` to generate English docstrings and write them back), and `verify-document` (generates non-blocking draft PR suggestions for review). The default language for all docstrings is English. To ensure accurate docstrings, the LLM receives function declarations and bodies. Local developer runs operate in offline mode by default to protect API budgets.
* **Question 2.3 (Asynchronous Localization and XLIFF Support) [DEFERRED - FUTURE PHASES (v2.0+)]**: Localization verification is non-blocking. Draft AI translations are generated in the background strictly after a successful merge into `master`, preventing translation cost overhead for short-lived feature branches. Unverified pages display fallback English text or an "AI-translated draft" banner. Translation managers can export source text to `.xlf` format, send to translation partners, and import verified results. (This feature is deferred to future releases).
* **Question 3 (Configuration, Local Automation, Caching, and Portability)**:
  1. **Decentralized Config and Three-Level Pipelines**: Agreed on a decentralized structure under `ude/`. System configurations are defined in `ude_global_config.json` (logging, caching, fallback policies). Products contain `ude_sdk_config.json` (metadata). Targets contain `ude_doc_config.json` defining individual `collector`, `parser`, and `renderer` options.
  2. **Doxygen-Backend and Resource Management**: Doxygen acts as the preprocessor for all languages in v1.0. The collector validates the environment (`validate_environment`) and executes a guaranteed clean-up routine under `try...finally` using strict guard rails (preventing deletion of `/`, `.`, or `..`).
  3. **Batch Automation and Preflight Checks**: Three levels of batch files are used: `engine/generate_all.bat`, `engine/generate_<product>.bat`, and target-specific `generate_docs.bat` files. They verify Python on the host (exiting with code 5 if missing) and auto-install missing packages (`pydantic`, `lxml`, `jinja2`) via `pip install` before executing the orchestrator.
  4. **Target Isolation and IR Compression**: Intermediate representation (`intermediate_representation.json.gz`) and cache databases (`.build_cache.json.gz`) are isolated inside product-specific subfolders (e.g., `ude/Bimnv/bimnv_cpp/`), keeping the output folder `output_dir` clean. IR files are compressed using Gzip.
  5. **Two-Level Incremental Build Cache**:
     - *Parsing (L1)*: Tracks mtime and contents hash of XML files. If unchanged, loads cached IR directly.
     - *Rendering (L2)*: Compares IR signature hash and Jinja2 templates. If unchanged, skips writing target files.
  6. **Path Portability**: Raw paths must not be hardcoded in Python modules. All configurations specify paths relative to their respective configuration files, and the orchestrator dynamically resolves them to absolute paths during execution.
* **Question 4 (Git Repository Folder Structure & Gitignores Cleanup)**:
  1. **Source Code Exclusion**: The local `/src` directory contains C++ source files, which are strictly outside of version control and must remain ignored.
  2. **Precise UDE Exclusions**: Replaced the global `/ude` folder ignore with precise rules ignoring build outputs (Doxygen intermediate XML folders, generated HTML folders, `.json.gz` files, and `.build_cache.json` files) across all product directories (`bimnv`, `facetmodeler`, `iges`, `map`). This ensures that product configurations (such as `ude_sdk_config.json` and `ude_doc_config.json`) are correctly tracked by Git, while dynamic build outputs remain excluded.
  3. **Specification Files Cleanup**: Staged the deletion of 5 obsolete legacy specification files from the parent root repository (`chapter_1_quick_start_structure.md`, `chapter_2_coding_standards_structure.md`, `chapter_3_configurations_structure.md`, `chapter_4_case_study_structure.md`, `ude_portal_blueprint.md`).
  4. **Submodule Gitignore Upgrade**: Configured ignores for `hugo-site/public/`, `hugo-site/.hugo_build.lock`, and temporary `engine/` symlink in `user-docs/.gitignore`.

### ⏳ Open Issues (Awaiting Discussion):
* **Question 5.1 (Single Sign-On (SSO) for Documentation Portals)**: Resolving SSO routing for static sites (Docusaurus and VitePress) hosted on GitHub Pages. Discussion deferred on custom domain routing via Cloudflare Zero Trust Access with OIDC/OAuth providers.

## 🗺️ Current Roadmap & Status
- [x] Hierarchical doc tree refactoring and clean layout division.
- [x] Added Roadmap and Document Version History section starting with version 0.1 (Requirements).
- [x] Configured Docusaurus version selector dropdown (`docsVersionDropdown`).
- [x] Upgraded old legacy admonitions to modern syntax in 11 files.
- [x] Designed core class contracts (`BaseParser`, `BaseRenderer`, exceptions, and CLI interfaces).
- [x] Verified Docusaurus compilation integrity (compiled successfully).
- [x] Set up decentralized target directory structure under `ude/` for BimNv, FacetModeler, IGES, and Map.
- [x] Completely removed `toc.yaml` files from requirements and folder structures.
- [x] Updated Requirements Quality Audit report using the 10-point scorecard.
- [x] Expanded, verified, and detailed the developer TDD task specifications under `.antigravitycli/tasks/`.
- [x] Integrated requirements audit recommendations into the task checklists.
- [x] Aligned Gantt milestone schedules (`schedule.md` and `active_plan.md`) with task modifications.
- [x] Freeze/save version 0.3 of specifications and transition current development focus to version 0.4 ("Documentation").
- [x] Prepare local Python development environment (virtual environment, poetry/pip, pytest) to begin core module coding.
- [x] Implement TSK-PAR-02 (Doxygen XML Parser Engine) with 100% test coverage and update compliance registries.
- [x] Implement TSK-COL-01 (BaseCollector Interface and DoxygenXmlCollector) with 95% statement coverage and safe cleanup guard rails.
- [x] Implement TSK-NML-01 (Docstring Normalizer to CommonMark Markdown) with 100% statement coverage and Javadoc/Doxygen/Google support.
- [x] Implement TSK-NML-02 (Exclusion Filters and Hidden Code Blocks) with 100% statement coverage and support for DOM-IGNORE, cond, and internal.
- [x] Implement TSK-RND-01 (Hugo Markdown Renderer & Front-Matter Metadata) with 100% statement coverage.
- [x] Implement TSK-RND-02 (Standalone Static HTML Compiler) with 100% statement coverage.
- [x] Implement TSK-RND-03 (Sidebar Navigation Refactoring & Namespace Landing Pages) with 100% statement coverage.
- [x] Implement TSK-CLI-01 (Non-Interactive CLI Command Processor) with 100% statement coverage.
- [x] Implement TSK-CLI-03 (Multi-Target Orchestration Engine) with 100% statement coverage.
- [x] Implement TSK-CLI-02 (E2E Integration Testing & Coverage Verification) with 100% statement coverage.
- [x] Configure and implement UDE Publisher (combined VitePress + Hugo publication pipeline with cross-repo automated triggers).
- [x] Standardize and unify visual appearance and design theme across all three documentation portals (Docusaurus, VitePress, Hugo) to make them completely cohesive, utilizing matching fonts (Inter + JetBrains Mono) and brand color palettes.
- [x] Freeze/save version 0.4 of specifications and transition current development focus to version 0.5 ("Testing documentation").
- [x] Analyze and clean up Git folder structures and `.gitignore` files in parent repository and submodules.
- [x] Create root-level folder 'ude_output', update all 11 sub-projects to target 'ude_output/' subfolders, and configure bat files to generate only HTML help.
- [x] Develop Table of Contents (toc_py.md) and machine-readable parser rules (toc_py.json) for Python, matching C++ and C# quality standards.
- [x] Implement active navigation item auto-focus and vertical scroll-top alignment (TSK-RND-04) for standalone HTML and Hugo layouts, synchronizing all specifications.
- [x] Implement language-specific entity layouts, dynamic ToC sorting and pruning (TSK-RND-05) with 100% statement coverage.
- [x] Implement Python SWIG wrapper docstring normalization (Sphinx/RST parsing) and logical parameter merging to produce clean HTML documentation tables.
- [x] Implement Hugo flatter sidebar layouts, namespace indices, and standalone HTML Python category index landing pages (TSK-RND-06) satisfying REQ-FUN-35 with 100% statement coverage.
- [x] Fix Hugo nested directory permalinks to resolve CI verification script (verify_pages.py) failures.
- [x] Fix VitePress client-side router 404 interception for Hugo-compiled API pages.
- [x] Refactor Hugo Markdown output structure to match the nested logical folder hierarchy of HTMLRenderer based on language-specific JSON configs (with virtual grouping and on-the-fly pruning of empty groups).
- [x] Fixed Hugo sidebar category folder navigation links, layout footers, and resolved nested table summary leakage by implementing description front-matter on all generated index files.
- [x] Standardize and unify entity topic names in both static HTML and Hugo Markdown renderers to "<EntityID> <EntityType>" format in sidebar, breadcrumbs, and content sections (TSK-RND-08).
- [x] Achieve 100% E2E test coverage across all modules (including edge-cases, error fallbacks, and flat rendering paths) with all 190 integration and unit tests passing successfully.
- [x] Remove code-style backticks from index titles and sidebar labels, and filter out remarks, see-also, and detailed blocks from Hugo namespace/category indices to show clean briefs.
- [x] Establish a portable 3-tier Golden Master baseline and automated regression test suite under `Tests/` (for FacetModeler and BimNv) validating 100% parser IRs, static HTML rendering, and Hugo Markdown outputs.
- [x] Document and specify the 4 specialized post-build integration and artifact validation tests in `design-docs/docs/srs/integration_tests_specification.md` and link them relatively from functional requirements (`REQ-FUN-48`, `REQ-FUN-49`) and the quality audit report.
- [x] Modularize Signature Formatter strategies, separate HTML templates by language, and subdivide Doxygen XML parser into clean, decoupled packages, passing all unit tests and achieving 100% byte-for-byte identical output with the Golden Master baseline.
- [x] Remove the Golden Master baseline directory (`Tests/baseline/`) from version control (adding it to `.gitignore`) to permanently delete it from GitHub.
- [x] Enhance statement coverage of the core parsing and routing engines to 98% by adding unit tests for namespace edge cases and language auto-detection.
- [x] Refactor sidebar navigation to flat-render global scope entities, remove the dedicated Global Namespace page, combine fields/structures/enums into a single category, and sort actual namespaces first (TSK-RND-11).
- [x] Implement isolated Docomatic Output Loaders (HtmlOutputLoader and HugoMarkdownOutputLoader) and Alignment Allowances Engine to verify 100% semantic and structural alignment between UDE outputs and legacy Docomatic results (Mock SDK).
- [x] Integrate automated allowance file updating via UPDATE_ALLOWANCES=1 env flag to auto-generate baseline deviations, achieving a 100% green alignment suite with 99% statement coverage.
- [x] Implement total discrepancy counter headers ("total_differences") at the beginning of Docomatic JSON difference files.
- [x] Implement support for file exceptions lists inside Golden Master regression tests to bypass failures when differences occur only in excepted files.
- [x] Refactor Golden Master regression tests (`test_golden_master.py`) into an extensible registry-based system (`PIPELINE_COMPLEXES`) to support multiple parser-renderer complexes.
- [x] Implement regression baselines validation and generation for LegacyHtmlRenderer and LegacyHugoMarkdownRenderer under dedicated subfolders (`html_legacy` and `markdown_legacy`) across C++, C#, and Java.
- [x] Rename and integrate the Docomatic search script as `oda_search.js` inside CSS default templates and standard HTML layout templates for C++, C#, Java, and Python, positioning the search elements at the right-aligned section of the breadcrumbs bar.
- [x] Enforce strict layout template existence gating by raising a `RendererError` when assets or templates are missing on disk, completely removing the `dummy_assets` fallback.
