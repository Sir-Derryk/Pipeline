# Task: TSK-PAR-03 — Backward-Compatible Multi-Language Parser Facade

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement a unified, backward-compatible routing parser facade (`DoxygenXmlParser`) that inherits from a universal base parser (`BaseDoxygenParser`) and dynamically delegates parsing of C++, C#, Java, or Python XML files to language-specific parser subclasses based on configuration or auto-detection.
2. **Implementation Steps**:
   - Create and define `BaseDoxygenParser` inside `ude/parsers/doxygen/base.py`.
   - Subclass `DoxygenXmlParser` inside `ude/parsers/doxygen/__init__.py` (or `facade.py`) from `BaseDoxygenParser`.
   - Implement dynamic delegation to concrete parser subclasses (e.g., `CppDoxygenParser`, `CsharpDoxygenParser`, `JavaDoxygenParser`, `PythonDoxygenParser`) based on the provided `language` argument.
   - Implement dynamic language auto-detection using path analysis on the input XML/source directories if no explicit language is specified.
   - Maintain complete backward compatibility of import paths under the standard `ude.parsers.doxygen` module namespace.
   - Add structured docstring traceability:
     ```python
     """
     ...behavior details...

     Satisfies REQ-FUN-44
     """
     ```

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   - Write unit tests in `tests/test_parser_facade.py`.
   - Assert that instantiating `DoxygenXmlParser` with explicit language parameters routes parsing to correct subclass objects.
   - Assert that parser auto-detects language correctly when the language argument is omitted.
2. **TDD Green Phase**:
   - Implement routing and path analysis inside the facade.
3. **TDD Refactor Phase**:
   - Run `poetry run pytest tests/test_parser_facade.py` to ensure complete green status.

## 👥 Part 3: User Acceptance Scenario
1. **Run automated tests**:
   - `cd engine`
   - `poetry run pytest tests/test_parser_facade.py`
2. **Verify key task requirements**:
   - [ ] Verify that `DoxygenXmlParser` inherits from `BaseDoxygenParser` to maintain LSP compliance.
   - [ ] Confirm dynamic language auto-detection via directory structures.
   - [ ] Confirm backward-compatible imports under `ude.parsers.doxygen`.
