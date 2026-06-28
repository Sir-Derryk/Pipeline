# Task: TSK-RND-01 — Hugo/Docusaurus Markdown Renderer & Front-Matter

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement a renderer to translate Intermediate Representation (IR) structures into Markdown documents containing YAML/TOML metadata front-matter, optimized for static site generators like Docusaurus and Hugo, enforcing language-specific Flat-Mapping naming rules (`REQ-FUN-03`, `REQ-FUN-04`, `REQ-FUN-30`, `REQ-FUN-31`, `REQ-FUN-32`).

2. **Implementation Steps**:
   * Create file `ude/renderers/hugo_markdown.py` subclassing `HugoMarkdownRenderer` from `BaseRenderer`.
   * **Logical TOC Compile**: Traverse the nested `ProjectCatalog` hierarchy and resolve logical parent-child paths for each entity based on its language (C++, C#, Java, Python) rules.
   * **Front-Matter Injection**: Inject YAML block headers at the top of each Markdown file with keys:
     * `title`: Name of the entity.
     * `sidebar_position`: Numeric weight of the entity in the ToC tree.
     * `parent`: Logical parent entity path (to support Docusaurus/Hugo menu nesting).
   * **Flat-Mapping Filename Resolution**: Translate logical API paths to physical, safe flat disk filenames:
     * *C++*: Use double underscores `__` for namespaces and scopes, `@` for overloaded parameter list types (with pointers `*` mapped to `_ptr`, references `&` to `_ref`, brackets `<` to `_lt_` / `>` to `_gt_`).
     * *C#*: Scope levels and nested classes separated by `__`, overloads by `@`.
     * *Java*: Packages separated by single underscore `_`, nested scopes by `__`, overloads by `@`.
     * *Python*: Modules/packages and class scopes separated by single underscore `_`, member methods/properties by `__`, overloads by `@` (e.g. `ude_parsers_doxygen_DoxygenXmlParser__parse_file@str.md`).
   * **Angle Bracket Escaping**: Inside Markdown contents, detect and escape angle brackets `< >` for template declarations into `&lt;` and `&gt;` to prevent rendering conflicts in MDX/Docusaurus.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_hugo_renderer.py` asserting:
     1. Flat-mapping translations result in exact expected filenames (e.g. `FacetModeler__Body__faceCount.md` for C++, and `ude_parsers_doxygen_DoxygenXmlParser__parse_file@str.md` for Python).
     2. Metadata headers contain correct YAML structure with `title`, `sidebar_position`, and `parent`.
     3. Brackets in template-rich class declarations (e.g. `Traits<Type>`) are escaped into MDX safe format `Traits&lt;Type&gt;`.
   * Verify test failures.
2. **TDD Green Phase**:
   * Implement `HugoMarkdownRenderer` logic to satisfy all flat-mapping, metadata mapping, and escaping checks.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_hugo_renderer.py
     ```
   * Ensure statement coverage for `hugo_markdown.py` is `>= 90%`.

## 👥 Part 3: User Acceptance Scenario
1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_hugo_renderer.py
   ```
   *Expected Result:* All tests are green.

2. **Verify key task requirements**:
   * [ ] Flat-mapped names are generated correctly for C++, C#, Java, and Python.
   * [ ] Angle brackets `< >` in code declarations are properly escaped as XML entities.
   * [ ] Markdown documents begin with a valid, clean YAML front-matter metadata block.
