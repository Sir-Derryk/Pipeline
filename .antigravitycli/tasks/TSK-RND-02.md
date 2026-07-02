# Task: TSK-RND-02 — Standalone Offline HTML Documentation Compiler

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement a compiler utilizing Jinja2 templates to build structured API catalogs into offline-friendly, highly responsive standalone HTML documentation portals with dynamic sidebars and premium aesthetic layouts (`REQ-FUN-03`, `REQ-FUN-30`, `REQ-FUN-31`, `REQ-FUN-32`, `REQ-FUN-34`, `REQ-FUN-35`).

2. **Implementation Steps**:
   * Create file `ude/renderers/static_html.py` subclassing `HtmlRenderer` from `BaseRenderer`.
   * **CORS-Free Navigation Compile**: Compile the entire project's hierarchical ToC database into a nested JSON structure and serialize it as a global JavaScript variable assignment: `window.UDE_NAV_DATA = { ... };` inside a dedicated file named `nav_data.js`.
   * **Page Generation**: Ingest standard layouts from `ude/templates/` and generate static HTML files using physical flat-mapped filenames (`REQ-FUN-30`). Ensure all relative hyperlinks among entities resolve correctly.
   * **Asset Compilation**: The compiler must automatically copy the reference stylesheet `main.css` and all associated graphics (such as subtype indicator icons, e.g., `indicator-method-16.png`) from `sdk_refs/NewVersion/bimnv_api_cpp/` into the target output directory (`REQ-FUN-32`).
   * **Interactive Sidebar Features**:
     * Include a `<script>` tag in `index.html` loading `nav_data.js` and rendering the collapsible folder tree dynamically.
     * **Resize Splitter**: Include a draggable element `.OdaDocSplitter` which dynamically changes the width of the sidebar. Write Javascript listener to persist the selected width inside the browser's `localStorage` under the key `ude_sidebar_width` and apply it during page load.
     * **Real-time Search Filter**: Implement client-side keyup listener on `#sidebarSearch` input that matches search strings against entity labels, auto-expands parent folder nodes, and hides non-matching elements.
   * **Custom Catalog Links (`REQ-FUN-34`)**: Support injecting custom, user-defined catalog or index reference links (such as to the VitePress user guides) consistently inside the global navigation sidebar or footers of all compiled documentation types.
   * **No Empty Sections & Auto-Linking (`REQ-FUN-35`)**: Enforce that every category or group node in the sidebar tree corresponds to a real, navigable page (preventing empty collapsible headers that do not open any page) by mapping category nodes to their first child document or a dynamically generated index page.
   * **Standardized Entity Layouts**: Each output page must contain:
     * Header badge with entity-type designation (`[class]`, `[method]`, etc.).
     * Main description block styled with class `.OdaDocBrief`.
     * Metadata details panel `.OdaDocContainerTable` showing source file, scope, and parent scopes.
     * Code prototype block `.OdaDocCodeProto` containing Highlight.js tags.
     * Collapsible member tables with graphical icons (e.g. `indicator-method-16.png`).

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Create test file `tests/test_html_renderer.py`.
   * Write tests asserting:
     1. `nav_data.js` is generated with valid JSON structure assigned to `window.UDE_NAV_DATA`.
     2. Output HTML files include `.OdaDocBrief`, `.OdaDocContainerTable`, and `.OdaDocCodeProto` layout blocks.
     3. Cross-linked relative paths resolve correctly without broken targets.
   * Verify test failures.
2. **TDD Green Phase**:
   * Implement `HtmlRenderer` and associated assets and templates to pass all structure and JSON validation tests.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_html_renderer.py
     ```

## 👥 Part 3: User Acceptance Scenario
1. **Run automated tests**:
   ```bash
   cd engine
   poetry run pytest tests/test_html_renderer.py
   ```
   *Expected Result:* Clean pytest run with zero errors.

2. **Verify key task requirements**:
   * [ ] `nav_data.js` file is written, enabling оffline-friendly CORS-free navigation on `file:///` protocol.
   * [ ] Draggable splitter writes state to `localStorage` under `ude_sidebar_width`.
   * [ ] Sidebar includes `#sidebarSearch` filtering input.
   * [ ] The compiler automatically copies the reference `main.css` and visual indicator assets to the output directory, and generated pages render identically to `sdk_refs/NewVersion/`.
   * [ ] Pages feature standardized badges, `.OdaDocBrief`, `.OdaDocContainerTable`, and collapsible lists with indicators.
   * [ ] Custom catalog/index reference links are successfully injected inside sidebars or footers (`REQ-FUN-34`).
   * [ ] No empty sidebar sections are left; all collapsible nodes point to valid target index or child pages (`REQ-FUN-35`).
