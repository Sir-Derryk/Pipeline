# Task: TSK-NML-02 — Exclusion Filters and Hidden Code Blocks (DOM-IGNORE)

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement filtering rules to omit specified internal or private codebase sections from compiled catalogs using exclusion markers (`REQ-FUN-13`).
2. **Implementation Steps**:
   * Integrate exclusion filtering checks into `DoxygenXmlParser`:
     * Skip all entities (classes, methods, structures, or variables) enclosed within the range markers `DOM-IGNORE-BEGIN` and `DOM-IGNORE-END`.
     * Skip conditional blocks marked by Doxygen-specific tags `\cond`/`@cond` and `\endcond`/`@endcond`.
     * Skip any code entities containing `@internal` or `\internal` within their docstrings.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Create unit test file `tests/test_exclusions.py`.
   * Feed parser with XML mock files where:
     * A class is wrapped between `DOM-IGNORE-BEGIN` and `DOM-IGNORE-END` blocks.
     * A method is marked with the `@internal` tag.
   * Assert that the generated `ProjectCatalog` contains **absolutely no reference** to these excluded elements.
   * Verify test failure.
2. **TDD Green Phase**:
   * Update the XML parsing routines in `DoxygenXmlParser` to skip elements matching ignore conditions during ingestion.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_exclusions.py
     ```
   * **Expected Success Result**: Test suite is green, confirming complete removal of hidden or internal APIs at parser level.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_exclusions.py
   ```
   *Expected Result:* All tests pass successfully, verifying that internal, private, or ignore-tagged elements are omitted.

2. **Verify key task requirements**:
   * [ ] Verify the parsing engine filters out ignore-tagged code blocks.
   * [ ] Confirm that members inside `DOM-IGNORE-BEGIN` ... `DOM-IGNORE-END` boundaries or marked with `\cond` / `\internal` are absent from generated `ProjectCatalog` trees.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
