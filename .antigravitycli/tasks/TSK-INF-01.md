# Task: TSK-INF-01 — Environment Initialization and pytest Setup

## 📌 Part 1: Implementation Guide
1. **Goal**: Initialize the Python environment in the `engine/` submodule, configure the Poetry package manager, and prepare the pytest automatic testing framework.
2. **Implementation Steps**:
   * Change directory to `engine/` (the UDE core repository).
   * Initialize a Poetry project with `poetry init` (or create `pyproject.toml` manually).
   * Add core production dependencies:
     * `pydantic>=2.0`
     * `jinja2`
     * `lxml`
   * Add development dependencies:
     * `pytest`
     * `pytest-cov`
     * `black`
     * `mypy`
   * Create the basic directory structure:
     * `ude/` — core source code root.
     * `tests/` — test suite root.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Create test file `tests/test_harness.py`.
   * Write a test that verifies:
     * The `ude` package can be imported without errors.
     * The package version is readable and equal to `"0.1.0"`.
   * Run `poetry run pytest` (or `pytest`) and verify that the test fails (since core code is missing).
2. **TDD Green Phase**:
   * Create initialization file `ude/__init__.py`.
   * Declare the version string constant: `__version__ = "0.1.0"`.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest --cov=ude tests/
     ```
   * **Expected Success Result**: pytest finishes with exit code `0` (all tests green), and the console displays 100% coverage for `__init__.py`.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest --cov=ude tests/
   ```
   *Expected Result:* pytest finishes successfully (green status) returning code 0, and the coverage report shows 100% for `__init__.py`.

2. **Verify key task requirements**:
   * [ ] Verify the presence of `pyproject.toml` in `engine/` with the correct dependencies (`pydantic>=2.0`, `jinja2`, `lxml`, `pytest`, `pytest-cov`, `black`, `mypy`).
   * [ ] Verify the standard directory structure `ude/` and `tests/`.
   * [ ] Verify the presence of `ude/__init__.py` with the declared version constant `__version__ = "0.1.0"`.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
