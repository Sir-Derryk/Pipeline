# Task: TSK-CLI-01 — Non-Interactive CLI Interface (argparse)

## 📌 Part 1: Implementation Guide
1. **Goal**: Build a console CLI interface for seamless integration and non-interactive compiler execution inside CI/CD environments (`REQ-FUN-07`, `REQ-BUS-09`).
2. **Implementation Steps**:
   * Create `ude/cli.py` as the primary entry point.
   * Use the `argparse` module to define switches:
     * `--config`, `-c` (path to target project configuration templates, e.g. `ude_config.json`).
     * `--input`, `-i` (override value for source paths defined in configurations as `src_dir`).
     * `--output`, `-o` (override value for destination targets defined in configurations as `output_dir`).
     * `--format`, `-f` (override value for output formats: `hugo_markdown` or `html`).
   * Implement validation routing:
     * Ingest target `ude_config.json` structures.
     * Ascend tree scopes to find `product.json` files to enrich catalog metadata details.
     * Dynamic resolution of relative path properties (`src_dir`, `output_dir`) relative strictly to the configuration file's physical parent folder (`REQ-FUN-29`).
   * Catch all exceptions: Output condensed, clear error summaries directly to `sys.stderr` and exit processes returning non-zero codes (like `1`), while successful executions exit returning code `0`.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write test file `tests/test_cli.py`.
   * Use `pytest` to simulate console executions (monkeypatching `sys.argv`).
   * Assert:
     1. Standard runs containing valid configurations exit throwing `SystemExit` code `0`.
     2. Runs containing invalid formats or paths exit returning non-zero values (e.g. `1` or `2`).
   * Verify test failure.
2. **TDD Green Phase**:
   * Implement argument processing inside `cli.py` and hook parser/renderer chains together.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_cli.py
     ```
   * **Expected Success Result**: Test suite is green, verifying CLI commands process arguments, catch exceptions, and return exact status exit codes.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_cli.py
   ```
   *Expected Result:* pytest runs green, asserting argument handling and exit status codes.

2. **Verify key task requirements**:
   * [ ] Verify `ude/cli.py` parses commands `--config`, `--input`, `--output`, `--format` via `argparse`.
   * [ ] Verify that source paths resolve strictly relative to configuration files physical directory positions.
   * [ ] Verify process exit status codes: `0` on success and non-zero on error.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
