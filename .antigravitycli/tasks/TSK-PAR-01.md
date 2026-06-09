# Task: TSK-PAR-01 — Abstract Contracts BaseParser, BaseRenderer and Exceptions

## 📌 Part 1: Implementation Guide
1. **Goal**: Define strict interfaces for parsers and renderers to support future direct AST parsers (like tree-sitter or libclang) without altering pipeline signatures (Recommendation 1), and establish UDE custom exceptions.
2. **Implementation Steps**:
   * Create file `ude/interfaces.py`.
   * Declare abstract classes utilizing Python's `abc` module:
     * `BaseParser` defining abstract method `.parse(self, input_path: str) -> ProjectCatalog`. The interface path parameter must support directories of XMLs as well as native code file paths for future ast frontends.
     * `BaseRenderer` defining abstract method `.render(self, catalog: ProjectCatalog, output_path: str)`.
   * **Traceability and Documenting Requirement**: Every interface, base class, and method must contain clear, structured docstrings outlining their behavior and featuring explicit traceability tags in the format:
     ```python
     """
     ...brief explanation...

     Satisfies REQ-FUN-XX
     """
     ```
     For `BaseParser`, trace with `Satisfies REQ-FUN-02`. For `BaseRenderer`, trace with `Satisfies REQ-FUN-03`.
   * Define exception hierarchy classes: `UdeException` (inheriting from `Exception`), `ParserError` (inheriting from `UdeException`), and `RendererError` (inheriting from `UdeException`). Document exceptions with traceable functional requirement references.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_interfaces.py`.
   * Assert:
     1. Attempting to directly instantiate `BaseParser()` or `BaseRenderer()` raises a `TypeError`.
     2. A concrete subclass of `BaseParser` that fails to implement `.parse()` raises a `TypeError` during instantiation.
     3. Reflection assertions verifying that the abstract classes and methods contain `Satisfies` tracing tags in their `__doc__` properties.
   * Verify tests fail.
2. **TDD Green Phase**:
   * Implement the base interfaces, exception classes, and complete traceability metadata inside `ude/interfaces.py`.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_interfaces.py
     ```
   * **Expected Success Result**: All tests pass, proving structural layout safety, trace alignment, and type contract restrictions.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_interfaces.py
   ```
   *Expected Result:* pytest verifies that attempts to directly instantiate abstract classes or incomplete subclasses are prevented.

2. **Verify key task requirements**:
   * [ ] Verify abstract classes `BaseParser` and `BaseRenderer` exist inside `ude/interfaces.py` using `abc.ABC` structures.
   * [ ] Verify custom exceptions `UdeException`, `ParserError`, and `RendererError` are declared.
   * [ ] Verify that all interfaces feature docstrings explicitly traced to requirement IDs (e.g., `Satisfies REQ-FUN-02`).

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
