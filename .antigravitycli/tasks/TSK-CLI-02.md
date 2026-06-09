# Task: TSK-CLI-02 — E2E Integration and Coverage Verification (>= 90%)

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement complete end-to-end integration tests to assert data flow and maintain codebase test statement coverage strictly `>= 90%` (`REQ-NFN-03`).
2. **Implementation Steps**:
   * Create `tests/test_integration_pipeline.py`.
   * Design E2E pipeline scripts:
     * Ingest sample source codes, coordinate the process collector, execute parsing, normalizations, and render target Markdown/HTML pages.
     * Verify that output files exist, feature accurate links, and have correct data parameters.
     * Expand the test suite until statement coverage verified by `pytest-cov` is `>= 90%`.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write E2E pipeline test structure. Assert coverage levels.
   * Run checks and verify test failure (due to incomplete code coverage).
2. **TDD Green Phase**:
   * Write complete tests verifying edge cases, error handlers, and pipeline variations.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest --cov=ude tests/
     ```
   * **Expected Success Result**: Test suite is green, and coverage report confirms statement coverage `>= 90%`.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest --cov=ude tests/
   ```
   *Expected Result:* All E2E scenarios pass successfully, and total statement coverage is `>= 90%`.

2. **Verify key task requirements**:
   * [ ] Verify integration test file `tests/test_integration_pipeline.py`.
   * [ ] Verify that statement coverage is `>= 90%`.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
