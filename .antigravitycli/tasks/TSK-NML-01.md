# Task: TSK-NML-01 — Docstring Normalizer to CommonMark Markdown

## 📌 Part 1: Implementation Guide
1. **Goal**: Standardize diverse raw docstring formats (Javadoc, Google Style, Doxygen, and Sphinx/RST) into uniform, clean CommonMark-compliant Markdown documentation blocks.
2. **Implementation Steps**:
   * Create file `ude/normalizer.py`.
   * Implement class `CommentNormalizer`:
     * Design regular expressions to parse parameter markers (`\param`, `@param`, `:param`, `:parameter`), return annotations (`eturn`, `@return`, `:return`, `:returns`), authors, and versions.
     * Support native Sphinx/RST-style docstrings widely found in SWIG-generated Python modules. This includes parsing `:param <name>: <desc>`, `:type <name>: <type_desc>`, `:return: <desc>`, and `:rtype: <type_desc>` tags.
     * Automatically map types from `:type` statements to their corresponding parameters and merge them into unified parameter metadata fields in the IR.
     * Extract these annotations as semantic metadata, populating individual argument metadata models inside the IR.
     * Strip block slashes, Javadoc decorations, and convert custom Doxygen tags into standard CommonMark layouts.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_normalizer.py` verifying:
     1. An annotation like `/** @param count Total size */` correctly extracts into parameter metadata (`count` -> `"Total size"`) while removing the Javadoc tag from the main docstring text.
     2. Doxygen comment tokens are stripped and normalized into standard CommonMark without raw compiler symbols.
     3. Sphinx/RST comments like `:param brep: The input boundary representation`, `:type brep: bool`, `:returns: True`, and `:rtype: bool` are correctly parsed, and types are mapped and merged cleanly.
   * Verify test failure.
2. **TDD Green Phase**:
   * Implement `CommentNormalizer` using robust regular expression string manipulations and formatting sanitizers.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_normalizer.py
     ```
   * **Expected Success Result**: Tests pass successfully, demonstrating clean extraction, type mapping, and formatting of diverse docstring styles.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_normalizer.py
   ```
   *Expected Result:* All test assertions pass, proving normalized markdown conversion.

2. **Verify key task requirements**:
   * [x] Verify class `CommentNormalizer` is declared inside `ude/normalizer.py`.
   * [x] Verify that parameter (`@param`/`\param` / `:param`) and return (`@return`/`eturn` / `:return`) tags are extracted as structured IR metadata fields.
   * [x] Confirm that Sphinx/RST type annotations (`:type`, `:rtype`) are parsed and mapped to parameter types and return types.
   * [x] Confirm that docstring bodies are stripped of legacy styling characters and formatted as standard CommonMark.

3. **Verify path portability**:
   * [x] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [x] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
