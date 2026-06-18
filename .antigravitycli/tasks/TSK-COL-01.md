# Task: TSK-COL-01 — BaseCollector Interface and DoxygenXmlCollector

## 📌 Part 1: Implementation Guide
1. **Goal**: Set up a pre-processing compilation tier to trigger external Doxygen commands, generating raw XML assets, and ensuring guaranteed secure removal of temporary workspace folder directories (`REQ-FUN-01`, `REQ-FUN-22`).
2. **Implementation Steps**:
   * Define interface `BaseCollector` inside `ude/interfaces.py` exposing:
     * `validate_environment(self, config_path: Path) -> None` (validates executable paths).
     * `collect(self, config_path: Path) -> Path` (runs compilation, returning the path to temporary XML folders).
     * `cleanup(self, temp_path: Path) -> None` (cleans up temporary workspaces).
   * Create `ude/collectors/doxygen.py` and implement subclass `DoxygenXmlCollector(BaseCollector)`:
     * `validate_environment`: Asserts availability of Python and `doxygen` binaries in PATH (or paths defined in `ude_global.json`), checks for localized `Doxyfile` templates, and asserts existence of source files directories `src_dir`.
     * `collect`: Spawns the Doxygen process utilizing `subprocess.run`, generating custom localized Doxygen configurations dynamically per target language (`cpp` / `cs` / `java` / `python`), applying appropriate parameters (such as file glob mappings `**/*.cs` or `OPTIMIZE_OUTPUT_JAVA = YES`), and directing output XML streams to dedicated, isolated temp folders under the target product directory.
     * `cleanup`: Recursively and safely removes the specified temporary folder. **CRITICAL WARNING (Guard Rails)**: To protect filesystems, the `cleanup` routine must enforce strict guard clauses. Raise a `ValueError` if the supplied path:
       * Is empty, null, or a root directory (`/`, `C:\`, `D:\`, etc.).
       * Points to the current directory (`.`) or parent directory (`..`).
       * Resolves to paths outside the project's temporary directory or working tree.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_doxygen_collector.py`.
   * Prepare mock collector verification scenarios. Verify assertions fail.
   * Add a specific test checking the `cleanup` guard rails by passing forbidden paths (`/`, `""`, `.`) and asserting they raise `ValueError`.
2. **TDD Green Phase**:
   * Implement `DoxygenXmlCollector` with strict path validation policies.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_doxygen_collector.py
     ```
   * **Expected Success Result**: Tests successfully mock Doxygen execution, verify environment checks, and assert that `cleanup` behaves securely.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_doxygen_collector.py
   ```
   *Expected Result:* pytest runs green, asserting environment checks, execution, and secure directory clean-up boundaries.

2. **Verify key task requirements**:
   * [ ] Verify that `DoxygenXmlCollector` is declared inside `ude/collectors/doxygen.py` inheriting from `BaseCollector`.
   * [ ] Verify that `cleanup` blocks attempts to delete root, relative, or system paths, raising a `ValueError`.
   * [ ] Confirm the collector triggers Doxygen as a subprocess, outputting XML structures to an isolated temporary directory.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
