# Task: TSK-DAT-01 — Pydantic v2 IR Schema Validation

## 📌 Part 1: Implementation Guide
1. **Goal**: Create typed Pydantic schemas representing the language-agnostic Intermediate Representation (IR) of the codebase API catalog.
2. **Implementation Steps**:
   * Create file `ude/models.py`.
   * Define Pydantic v2 models mapping the structural code hierarchy:
     * `ProjectCatalog` — root container (contains a dictionary or list of namespaces).
     * `NamespaceEntity` — represents a namespace, package, or module scope.
     * `ClassEntity` — represents a class, interface, or struct (name, docstring, methods, fields).
     * `MethodEntity` — represents functions, methods, constructors (name, signature, parameters, return type, normalized docstring).
     * `ParameterField` — represents method parameter attributes (name, type, description).

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_models.py` executing two core validations:
     1. Constructing a valid `ProjectCatalog` object (nested classes, methods with parameters) is successful.
     2. Injecting invalid data types (e.g., passing an integer instead of a string to `fully_qualified_name`) triggers a validation error (`pydantic.ValidationError`).
   * Confirm the tests fail due to missing schema definitions.
2. **TDD Green Phase**:
   * Implement the models under `ude/models.py` inheriting from `pydantic.BaseModel` utilizing explicit type annotations.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_models.py
     ```
   * **Expected Success Result**: Tests pass successfully, demonstrating strict type validation and nested container parsing.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_models.py
   ```
   *Expected Result:* All assertions pass, confirming the accuracy and strict validation of the schema.

2. **Verify key task requirements**:
   * [ ] Verify the existence of `ude/models.py` containing the schemas: `ProjectCatalog`, `NamespaceEntity`, `ClassEntity`, `MethodEntity`, `ParameterField`.
   * [ ] Confirm that schemas are strictly typed and raise a `ValidationError` when supplied with incorrect attributes.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
