# Task: TSK-RND-04 — Sidebar Active Node Auto-Focus & Scroll-Top Alignment

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement dynamic navigation item auto-focus and top-aligned vertical scrolling on page load for both offline HTML help (`sidebar.js`) and Hugo templates (`single.html`) according to `REQ-FUN-31`.

2. **Implementation Steps**:
   * **Offline HTML Help (`sidebar.js`)**: Add scroll logic inside `DOMContentLoaded` after building and appending the tree in `engine/ude/templates/css/default/sidebar.js`. Find `.OdaDocTOCRow.active`, calculate its offset recursively relative to its container `#toctree`, and assign it to `toctree.scrollTop` to align it to the top.
   * **Hugo Static Site Layout (`single.html`)**: Add matching scroll logic inside `DOMContentLoaded` in `user-docs/hugo-site/layouts/_default/single.html`. Locate `.api-item.active`, check and expand its parent `.namespace-group` (removing `collapsed` class if present), calculate its recursive offset relative to `.left-sidebar`, and assign it to `sidebar.scrollTop`.
   * **Verification and Coverage**: Verify the correctness of these scripts and ensure that code coverage for the Python renderer remains strictly `>= 98%`.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Add a basic UI or DOM test verification if possible, or verify that the active classes are attached correctly.
2. **TDD Green Phase**:
   * Integrate the scroll-top javascript snippets inside both `sidebar.js` and `single.html` templates.
3. **TDD Refactor Phase**:
   * Ensure that the scrolling function is recursive to account for variable offsetParents, maintaining absolute robustness across various browsers.

## 👥 Part 3: User Acceptance Scenario
1. **Verify Standalone HTML Help**:
   * Compile the documentation locally using `generate_all.bat`.
   * Open any compiled HTML page in a browser offline.
   * Check that the sidebar tree expands the parent namespaces of the current page, focuses on the current active item, and scrolls it to the top of the sidebar viewport.

2. **Verify Hugo Static Site**:
   * Serve the Hugo site locally or access its compiled pages.
   * Navigate to any API page.
   * Confirm that the left sidebar automatically expands the parent namespace of the current entity page, focuses on the `.api-item.active`, and scrolls the left sidebar container so that the active item is aligned at the top.
