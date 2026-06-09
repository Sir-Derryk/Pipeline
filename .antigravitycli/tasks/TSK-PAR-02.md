# Task: TSK-PAR-02 — Doxygen XML Parser Engine (C++, C#, Java, Python)

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement the parser engine to read Doxygen XML outputs for C++, C#, Java, and Python, mapping entities into Intermediate Representation (IR) structures while filtering SWIG bindings and compiler export macros.
2. **Implementation Steps**:
   * Create `ude/parsers/doxygen.py`, subclassing `DoxygenXmlParser` from `BaseParser`.
   * **Traceability and Documenting Requirement**: Define explicit structured docstrings across `DoxygenXmlParser` and all inner parsing routines using the traceback pattern:
     ```python
     """
     ...behavior details...

     Satisfies REQ-FUN-02, REQ-FUN-19, REQ-FUN-20
     """
     ```
   * Implement parsing logic:
     * Ingest the main catalog manifest `index.xml` to locate all nested compound files (`class`, `struct`, `namespace`, etc.).
     * Recursively parse XML definitions utilizing `lxml` or standard `xml.etree`.
     * Extract packages/namespaces, classes/interfaces, methods (parameters, return types, visibilities), and docstrings.
     * **Support specific structural characteristics**:
       * Reconstruct nested namespaces and nested classes utilizing double colon separators `::` (e.g. C++ layout) inside the `ProjectCatalog`.
       * Correctly extract constructors and destructors (e.g., starting with `~`), ensuring no errors occur due to missing return values.
       * Resolve type aliases and `typedef` scopes.
       * Detect templates containing angle brackets `< >` in entity names (e.g. `Traits<Type::Value>`), ensuring subsequent renderers escape these characters to prevent compilation issues.
       * Automatically filter out compiler-specific export macros (e.g. `NWDBEXPORT`, `MAPEXPORT`).
       * Strip SWIG-specific wrapper members and fields (`swigCPtr`, `swigCMemOwn`, `Dispose()`, `getCPtr()`, etc.) if `exclude_swig_internals` is enabled in `ude_config.json`.
     * Map all validated attributes to a typed `ProjectCatalog` container.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_doxygen_parser.py`.
   * Feed parser with sample XML assets for C++, C#, Java, and Python, including custom macro and SWIG wrappers from `TSK-INF-02` (`class_with_macros.xml`, `class_swig_wrapper.xml`).
   * Write assertions to verify:
     * Accurate resolution of nested class trees and fully qualified names.
     * Type assertions for method signatures and variable declarations.
     * Export macros are stripped from the resulting entities (`REQ-FUN-19`).
     * SWIG internals are filtered out when the configuration option is set (`REQ-FUN-20`).
     * Reflection tests check for docstring traceability containing `Satisfies` lines.
   * Verify test failure.
2. **TDD Green Phase**:
   * Implement parsing logic in `doxygen.py`, mapping XML elements `<compounddef>` and `<memberdef>` into Pydantic models.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_doxygen_parser.py
     ```
   * **Expected Success Result**: Tests pass, verifying correct extraction of structural XML elements into typed IR catalogs with exact macro/SWIG filtration.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_doxygen_parser.py
   ```
   *Expected Result:* All assertions pass, confirming accurate structural parsing across target programming languages.

2. **Verify key task requirements**:
   * [ ] Verify that `DoxygenXmlParser` inside `ude/parsers/doxygen.py` successfully inherits from `BaseParser`.
   * [ ] Verify template angle bracket extraction and compiler export macro filtration.
   * [ ] Verify SWIG-specific members are removed from catalogs when configured.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
