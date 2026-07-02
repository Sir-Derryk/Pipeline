# Git Style Guidelines

This document regulates the branching strategy in Git and defines standard commit message formats to ensure a clean and transparent development history.

---

## 🌿 1. Branching Strategy: GitHub Flow

The **GitHub Flow** model is adopted as the primary branching strategy for collaboration in the UDE repository. It is simple to maintain and ideal for continuous integration.

### Core Rules:
1.  **Main Branch**:
    *   The `main` branch is always stable, tested, and ready for deployment.
    *   Direct commits to `main` are allowed only for minor administrative changes (e.g., fixing typos, updating documentation) followed by a push.
2.  **Feature and Bug Branches**:
    *   For any new task, feature, or bug fix, a separate branch is created from `main` with a descriptive name:
        *   `feature/parser-swig-implementation` (for new features)
        *   `bugfix/broken-sidebar-links` (for bug fixes)
        *   `docs/update-dev-guidelines` (for documentation updates)
3.  **Merging Changes**:
    *   After completing work on a task, a **Pull Request (PR)** is created from the feature branch into `main`.
    *   The code undergoes automated tests (if configured) and manual review.
    *   After PR approval, the branch is merged into `main` using **Squash and Merge** (to preserve a concise history) or standard merge.

---

## 💬 2. Commit Message Standard: Conventional Commits

All commit messages in the repository must strictly follow the **Conventional Commits** specification. This allows for automatic generation of change logs (ChangeLogs) and makes the project history easier to understand.

### Commit Structure:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Core Commit Types (`<type>`):
*   `feat`: Adding new functionality (e.g., `feat: add TypeScript parser for SWIG wrappers`).
*   `fix`: Fixing an error (e.g., `fix: resolve crash when parsing empty XML node`).
*   `docs`: Changes to documentation or rules only (e.g., `docs: refine code style rules`).
*   `style`: Formatting changes that do not affect logic (spaces, formatting, semicolons — e.g., `style: format index.ts with prettier`).
*   `refactor`: Code refactoring that neither adds a feature nor fixes a bug (e.g., `refactor: extract collector base class`).
*   `test`: Adding or modifying tests (e.g., `test: add unit tests for comment parser`).
*   `chore`: Updating build tasks, dependencies, linter configs, etc. (e.g., `chore: update typescript dependency to v5.4`).

### Example of a Good Commit Message:
```bash
feat(parser): add support for parsing Java multi-line doc-comments

Parsed Java comments are now converted into HTML-safe descriptions with preserved paragraphs.
```
