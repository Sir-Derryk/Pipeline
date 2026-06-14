# Task: TSK-RND-06 — Hugo Flatter Sidebar & Namespace Index Tables

## 📌 Part 1: Implementation Guide
1. **Goal**: Refactor the Hugo markdown rendering engine to support flatter directory structures (completely omitting intermediate grouping directories like "Classes", "Structures", "Interfaces") and dynamically generate Markdown index pages (`_index.md`) for namespaces featuring structured summary tables (`REQ-FUN-35`).

2. **Implementation Steps**:
   * **Flatter Folder Mapping**: Update `HugoMarkdownRenderer` in `engine/ude/renderers/hugo_markdown.py` to write class and structure pages directly under their parent namespace directory without creating intermediate visual category subdirectories.
   * **Namespace Index Generation**: For every unique logical Namespace parsed in the catalog, dynamically compile a dedicated Markdown index file named `_index.md` inside its corresponding subdirectory.
   * **Summary Tables**: The generated `_index.md` namespace page must contain a highly readable Markdown table listing all child entities nested in this namespace.
     * The table must have columns: `Entity Name` (formatted as a relative clickable Markdown link pointing to its respective class/struct document page) and `Description` (extracting the CommonMark brief description `.OdaDocBrief` from the IR).
   * **Verification & E2E Validation**: Extend `tests/test_hugo_renderer.py` to assert that:
     1. Namespace `_index.md` files are successfully written.
     2. Relative paths inside tables resolve correctly.
     3. Virtual category grouping folders are not created in Hugo output.
     Ensure total Python renderer test coverage remains `>= 98%`.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit tests inside `tests/test_hugo_renderer.py` verifying that:
     - Directory tree generation for Hugo does not contain empty folder intermediates.
     - An `_index.md` is compiled for `FacetModeler` with a table linking to `class_FacetModeler__Body.md`.
   * Run tests and verify failure.
2. **TDD Green Phase**:
   * Implement flatter hierarchy rendering and namespace index compilation inside `hugo_markdown.py`.
3. **TDD Refactor Phase**:
   * Run pytest to verify all tests pass with code coverage `>= 98%`.

## 👥 Part 3: User Acceptance Scenario
1. **Verify Generated Hugo Content**:
   * Execute the full pipeline via `generate_all.bat`.
   * Open the output directory for Hugo and check that namespace folders (like `bimnv_cpp/`) contain direct entity files and a dynamic `_index.md`.
   * Verify that `_index.md` contains a markdown table representing all child classes with relative links and descriptions.
