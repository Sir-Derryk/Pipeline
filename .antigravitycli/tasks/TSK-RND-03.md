# Task: TSK-RND-03 — Sidebar Navigation Refactoring & Namespace Landing Pages

## 📌 Part 1: Implementation Guide
1. **Goal**: Refactor the standalone HTML compiler sidebar tree to eliminate pageless category folders and implement dedicated index landing pages for all logical namespaces (`REQ-FUN-32`, `REQ-FUN-35`).

2. **Implementation Steps**:
   * **Pageless Node Elimination**: Refactor `engine/ude/renderers/static_html.py` to remove the redundant `Classes` grouping node (`classes_group`) from `nav_tree`. Ensure any collapsible directories in the sidebar map directly to a valid page on disk.
   * **Namespace Landing Pages**: Automatically generate a dedicated landing index page (`namespace_{ns_id}.html`) for every logical namespace/package parsed in the project.
   * **Namespace Template**: Develop a clean standard Jinja2 template (`engine/ude/templates/namespace.html`) detailing all enclosing members (classes, structs, global methods) with high-fidelity indicator icons.
   * **E2E Integration & Verification**: Extend test suites in `tests/test_html_renderer.py` to assert the presence of namespace files and correctness of category links, keeping total statement coverage strictly >= 98%.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Add test assertions checking that every sidebar folder node has a valid non-empty `href` and namespace index pages are successfully rendered.
   * Verify test failures.
2. **TDD Green Phase**:
   * Refactor rendering engine to output namespace landing pages and remove pageless collapsible nodes.
3. **TDD Refactor Phase**:
   * Ensure statement coverage remains `>= 98%` and code style conforms to standards.

## 👥 Part 3: User Acceptance Scenario
1. **Run automated tests**:
   ```bash
   poetry run pytest tests/test_html_renderer.py
   ```
   *Expected Result:* All tests pass, and coverage is >= 98%.

2. **Verify requirements**:
   * [ ] Redundant `Classes` folders are removed from sidebar trees.
   * [ ] Every logical namespace generates its own `namespace_*.html` index page.
   * [ ] All collapsible sidebar elements are active and clickable, resolving to valid pages.
