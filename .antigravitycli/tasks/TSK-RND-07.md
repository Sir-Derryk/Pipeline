# Task: TSK-RND-07 — Renderer-Specific JSON TOC Configs Loader & Migration

## 📌 Part 1: Implementation Guide
1. **Goal**: Refactor the TOC configuration loading mechanism to resolve and load dedicated `toc_<RendererClassName>.json` configuration files for each of the 16 concrete renderer subclass implementations instead of language-specific `toc_<lang>.json` configurations. Update and migrate all JSON structures in `engine/ude/templates/SidebarStructures/default/` to the new Option A array format under the `"sidebar"` key, wrapping Doxygen parsing/mapping rules inside an `api_reference` node.

2. **Implementation Steps**:
   * **Refactor Loader**: Update `_get_toc_filename()` in each of the 16 concrete subclasses of `HtmlRenderer`, `HugoMarkdownRenderer`, `LegacyHtmlRenderer`, and `LegacyHugoMarkdownRenderer` (located in `static_html.py`, `hugo_markdown.py`, and `legacy.py`) to return `toc_<RendererClassName>.json` (e.g., `toc_CppHtmlRenderer.json`).
   * **TOC JSON Configurations Migration**: Create and populate the 16 configuration files in `engine/ude/templates/SidebarStructures/default/`. Migrate existing Doxygen mapping schemas under a single array item of type `"api_reference"`.
   * **TOC Parser Refactoring**: Update the JSON TOC loading/initialization code in the base renderers to parse the `"sidebar"` array, extract the `api_reference` configuration, and supply it to the existing Doxygen catalog structuring parser.
   * **Traceability Tags**: Append docstring tags `Satisfies REQ-FUN-50` to all updated methods.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit tests in `tests/test_toc_loader.py` asserting that each subclass renderer correctly resolves its dedicated `toc_<RendererClassName>.json` path and loads the JSON layout successfully.
   * Run the tests and verify that they fail due to missing configuration files.
2. **TDD Green Phase**:
   * Create all 16 `toc_*.json` files and complete the loader code refactoring to make all tests pass.
3. **TDD Refactor Phase**:
   * Clean up the parsing and loading code and verify that total test statement coverage remains `>= 98%`.

## 👥 Part 3: User Acceptance Scenario
1. **Orchestrator Execution**:
   * Verify that compiling SDK targets successfully resolves and loads `toc_<RendererClassName>.json` files from the default configuration templates without warnings or file access crashes.
