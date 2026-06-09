# Task: TSK-RND-02 — Standalone Offline HTML Documentation Compiler

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement a compiler using Jinja2 templates to compile structured API catalogs into offline-friendly, responsive HTML documentation portals (`REQ-FUN-03`).
2. **Implementation Steps**:
   * Create file `ude/renderers/static_html.py` subclassing `HtmlRenderer` from `BaseRenderer`.
   * Structure the renderer:
     * Ingest localized HTML/CSS templates under `ude/templates/`.
     * Render the entire catalog hierarchy as cross-linked HTML documents.
     * Construct a responsive navigation sidebar mapping namespaces and classes.
     * Deliver CSS layouts as standalone assets directly written to output paths.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Create test file `tests/test_html_renderer.py`.
   * Write tests asserting:
     1. HTML assets are correctly written to directories.
     2. Page structures feature correct sidebar navigation tags.
     3. Cross-linked class references resolve cleanly (internal relative hyperlinks).
   * Verify test failure.
2. **TDD Green Phase**:
   * Implement `HtmlRenderer` using structured Jinja2 templates and assets.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_html_renderer.py
     ```
   * **Expected Success Result**: All tests pass, verifying compiled static files, menu components, and relative navigations.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_html_renderer.py
   ```
   *Expected Result:* All assertions pass, confirming the standalone compilation.

2. **Verify key task requirements**:
   * [ ] Verify `HtmlRenderer` is implemented inside `ude/renderers/static_html.py`.
   * [ ] Verify compiled assets feature responsive design templates and sidebar navigations.
   * [ ] Verify all cross-references resolve cleanly as offline-compatible links.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
