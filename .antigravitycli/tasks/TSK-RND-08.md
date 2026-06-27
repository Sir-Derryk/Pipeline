# Task: TSK-RND-08 — Custom Page Nodes Compilation (Static, Inline, Redirect)

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement compile-time rendering logic for `static`, `inline`, and `redirect` nodes declared in the `"sidebar"` configuration, ensuring they are rendered alongside the `api_reference` root node on the same hierarchy level.

2. **Implementation Steps**:
   * **`static` Page Rendering**: When parsing a `static` node, read the specified external file path. If it is an HTML file, extract only the content situated inside the `<body>` tag. If it is a Markdown file, exclude any front-matter/SSG headers. Compile the extracted content using target layout templates and write it to the specified `output_name`.
   * **`inline` Page Rendering**: When parsing an `inline` node, write the embedded string content directly to the target output file `output_name` using templates (excluding layouts/decorative wrappers as per rules).
   * **`redirect` Node Rendering**: When building the navigation sidebar metadata (or `nav_data.js`), create a redirect node pointing to `target_url`. In HTML Help, the sidebar link points directly to the external/internal URL. In Hugo, compile a redirect/placeholder page containing meta-refresh or configure Hugo menus appropriately.
   * **TOC Sibling Ordering**: Align the root node of the Doxygen-compiled API Reference (`api_reference`) on the same level as these custom pages, strictly honoring the array ordering in the configuration.
   * **Traceability Tags**: Append docstring tags `Satisfies REQ-FUN-50` to all rendering methods.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write tests in `tests/test_render_custom_pages.py` defining a test sidebar configuration with `static`, `inline`, `api_reference`, and `redirect` items. Assert that rendering produces the static and inline pages with correct content extractions, and maps redirect nodes correctly at the sibling level.
   * Run the tests and verify that they fail.
2. **TDD Green Phase**:
   * Implement custom page parsing and compilation inside `HtmlRenderer` and `HugoMarkdownRenderer` pipelines to make the tests pass.
3. **TDD Refactor Phase**:
   * Clean up layout formatting and rendering routines. Verify statement coverage remains `>= 98%`.

## 👥 Part 3: User Acceptance Scenario
1. **Run full compilation**: Compile documentation via `generate_all.bat`.
2. **Check output structure**: Open the output directory and verify that custom pages (static and inline) are compiled, redirect links function correctly, and the sidebar contains neighbors for these custom pages alongside the API reference root.
