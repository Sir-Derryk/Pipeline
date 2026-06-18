# Code Style Standards

This document establishes unified rules for formatting and styling code in the UDE project for the **Python** and **TypeScript** languages, and also defines the status of raw **C++** source code.

---

## 🐍 1. Python Code Style

All components written in Python must strictly comply with the **PEP 8** recommendations.

### Quality Control Tools:
*   **Formatting**: **Black** (automatic formatting to standard).
    - Line Length: **88 characters** by default (or **120 characters** for long expressions, if agreed in the project configuration).
*   **Linter**: **Flake8** (static analysis of potential errors and style violations).

### Naming Conventions:
*   **Classes**: `PascalCase` (e.g., `MetadataCollector`, `HtmlParser`).
*   **Functions and Methods**: `snake_case` (e.g., `collect_metadata()`, `parse_file()`).
*   **Variables**: `snake_case` (e.g., `file_path`, `output_directory`).
*   **Global Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_BUFFER_SIZE`, `MAX_RETRIES`).
*   **Private Members (logically)**: prefixed with a single underscore `_snake_case` (e.g., `_cache_data`).

---

## ⚡ 2. TypeScript Code Style

TypeScript components must be written using modern standards and auto-formatting utilities.

### Quality Control Tools:
*   **Linter**: **ESLint** (verifying code quality, preventing potential bugs, maintaining syntax purity).
*   **Formatting**: **Prettier** (standardizing formatting for braces, semicolons, and indents).
    - Line Length: **100 characters** by default.

### Naming Conventions:
*   **Classes**: `PascalCase` (e.g., `OrchestratorService`, `TemplateEngine`).
*   **Interfaces**: prefixed with `I` in `PascalCase` or standard `PascalCase` (e.g., `IParserOptions` or `ParserConfig`).
*   **Functions and Methods**: `camelCase` (e.g., `renderPage()`, `loadConfig()`).
*   **Variables**: `camelCase` (e.g., `sourcePath`, `cacheManager`).
*   **Constants**: `UPPER_SNAKE_CASE` (e.g., `PORT`, `API_URL`).

---

## ⚙️ 3. C++ Source Code Baseline

For C++ modules that are processed by the pipeline, standard Doxygen structures are supported. The source code formatting does not strictly depend on PEP 8 or Prettier but must use clean, readable commenting structures (e.g., Qt-style or Javadoc-style comments) to allow the Doxygen parser to successfully extract descriptive attributes.
