# Task: TSK-RND-01 — Hugo/Docusaurus Markdown Renderer & Front-Matter

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement a renderer to translate Intermediate Representation (IR) structures into Markdown documents containing YAML/TOML metadata front-matter, optimized for static site generators (Docusaurus, Hugo) (`REQ-FUN-03`, `REQ-FUN-04`).
2. **Implementation Steps**:
   * Create file `ude/renderers/hugo_markdown.py` subclassing `HugoMarkdownRenderer` from `BaseRenderer`.
   * Implement rendering structures:
     * Translate namespaces and classes into individual Markdown pages.
     * Inject front-matter headers (YAML/TOML block specifying `title`, `sidebar_position`, `id`).
     * Structure method signature profiles, arguments, types, and return values into markdown tables.
     * **Angle Bracket Escaping**: To prevent layout breakage or tag errors inside Docusaurus/Hugo, detect template symbols `< >` (e.g. C++ templates in class names) and convert them to escaped formats `&lt;` and `&gt;`.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_hugo_renderer.py` asserting:
     1. Output files feature correct front-matter headers.
     2. Class names containing template parameters (e.g. `ExchangeTraits<Type>`) are escaped into output streams as `ExchangeTraits&lt;Type&gt;`.
   * Verify test failure.
2. **TDD Green Phase**:
   * Implement `HugoMarkdownRenderer` utilizing template schemas and strict escaping routines.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_hugo_renderer.py
     ```
   * **Expected Success Result**: Tests compile successfully, verifying output document structures, metadata generation, and escaping rules.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_hugo_renderer.py
   ```
   *Expected Result:* pytest runs successfully (green status), proving formatting compliance.

2. **Verify key task requirements**:
   * [ ] Verify class `HugoMarkdownRenderer` is implemented under `ude/renderers/hugo_markdown.py`.
   * [ ] Confirm that template characters (`<` and `>`) are converted to `&lt;` and `&gt;`.
   * [ ] Verify that rendered files feature correct metadata header headers (YAML/TOML front-matter).

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
