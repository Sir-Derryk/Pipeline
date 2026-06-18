# Task: TSK-RND-05 — Language-Specific Entity Layouts & Content Refinement

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement dynamic, language-specific entity layouts inside the static HTML reference generation engine to fully satisfy the visual representation guidelines (`REQ-FUN-32` and `REQ-FUN-35`).

2. **Implementation Steps**:
   * **Dynamic Config Loading**: Load language-specific `toc_<lang>.json` config files at runtime inside the renderer.
   * **Dynamic ToC Sorting & Pruning (`REQ-FUN-35`)**: Group namespace classes dynamically into non-empty virtual folders (e.g., *Classes*, *Structures*, *Interfaces*, *Exceptions*) as specified in the configuration rules. Prune folders with zero entities on-the-fly.
   * **Scope & Separators**: Adjust namespace and fully qualified name rendering inside Jinja2 `class_layout.html` to dynamically replace `::` with `.` for languages other than C++ (e.g., `cs`, `java`, `py`).
   * **Language-Specific Prototypes**: Refine the code declaration container `.OdaDocCodeProto` to format OOP class prototypes conforming to target language syntax:
     - **C++**: `class/struct Name : public Base { ... };` with members/fields inside.
     - **C#**: `public class/interface Name : Base { ... }` with members/fields inside.
     - **Java**: `public class/interface Name extends Base { ... }` with members/fields inside.
     - **Python**: `class Name(Base):` with fields represented inside `__init__(self)`.
   * **Verification and Coverage**: Add a comprehensive suite of unit/integration tests to ensure all four languages are correctly supported by the template engine, maintaining statement coverage strictly `>= 98%`.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Add test scenarios inside `engine/tests/test_html_renderer.py` asserting that C#, Java, and Python entities rendered under those configurations correctly display dot delimiters `.` in fully qualified names, correct language classes in code blocks, and appropriate OOP class/interface formatting keywords.
2. **TDD Green Phase**:
   * Update the templates and python renderer to support those dynamic parameters.
3. **TDD Refactor Phase**:
   * Clean up formatting and template logic, ensuring it remains simple, robust, and maintains `>= 98%` statement coverage.

## 👥 Part 3: User Acceptance Scenario
1. **Verify Generated HTML Layouts**:
   * Compile the reference documentation via `generate_all.bat`.
   * Open the generated C++ index and classes under `ude_output/bimnv_api_cpp/` and verify scope delimiters use `::` and prototype matches C++.
   * Open the generated C#, Java, or Python pages under `ude_output/` and verify that fully qualified names and scopes use `.` and prototypes use native language syntax.
