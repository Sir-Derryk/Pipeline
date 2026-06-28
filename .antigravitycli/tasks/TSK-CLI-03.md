# Task: TSK-CLI-03 — Multi-Target Orchestration Engine

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement the master orchestrator to parse decentral target configurations, resolve portable paths, coordinate collectors, parsers, and renderers, and enforce error handling policies (`REQ-FUN-23`, `REQ-FUN-24`, `REQ-FUN-25`, `REQ-FUN-28`, `REQ-FUN-29`).
2. **Implementation Steps**:
   * Create `ude/orchestrator.py` defining class `UdeOrchestrator`.
   * Implement orchestration flows:
     * Read `ude_global.json` and decentral target configuration files `ude_config.json`.
     * Establish absolute paths by mapping relative paths relative to target configuration parent folders, verifying execution portability across developer workstations and CI agents.
     * Sequence executions: trigger Collector ➡️ Parse raw outputs to IR ➡️ Render IR blocks to destination outputs.
     * Enforce `error_policy` configurations: `fail-fast` terminates processes on error, while `continue-on-error` logs warnings but continues compilation.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_orchestrator.py`.
   * Feed configuration assets mapping a mock compile job and execute. Verify assertions fail.
   * Verify path portability by running orchestrations from alternative current working directories (CWDs) and asserting paths resolve relative to configurations.
2. **TDD Green Phase**:
   * Implement `UdeOrchestrator` orchestrating compilation flows and paths resolution.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_orchestrator.py
     ```
   * **Expected Success Result**: Tests pass successfully, verifying that the orchestrator loads configurations, handles error policies, and runs sequentially.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_orchestrator.py
   ```
   *Expected Result:* All tests pass, proving correct workflow sequencing and path resolutions.

2. **Verify key task requirements**:
   * [ ] Verify class `UdeOrchestrator` inside `ude/orchestrator.py`.
   * [ ] Confirm that relative path configs are parsed and resolved relative to their respective config files location.
   * [ ] Verify orchestration flows execute correctly across diverse current working directories.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
