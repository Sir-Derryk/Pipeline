---
name: task-verification
description: >-
  Automated task verification skill (TSK) for compliance with 
  TDD methodology, coding standards, architectural safety, and coverage completeness.
---

# Skill: Task Verification SOP

## 🎯 General Description
This skill is designed for automatic and semi-automatic verification of technical task specifications (TSK files) before development begins, as well as for verifying the quality of the completed implementation during task submission. Using this standard eliminates the risks of missed requirements, security vulnerabilities, and "blind" coding without tests.

---

## 🔍 Five Technical Task (TSK) Quality Criteria

Each task during specification audit or code acceptance must be evaluated against the following criteria:

### 1. Scope & Atomicity
*   *Review Question*: Does the task solve exactly one indivisible technical problem within its component? Is there any "feature creep" or mixing of universal engine logic with project-specific documentation portal configurations (dogfooding)?
*   *Success Criterion*: The task specification describes a strictly limited set of changes in one or two related modules, with clear boundaries between universal engine CLI/source code and site-specific manuals/assets.

### 2. TDD Completeness
*   *Review Question*: Are the failure (**RED**) and success (**GREEN**) phases described in detail? Are the target test files, input datasets, and specific assertions specified?
*   *Success Criterion*: A clear test execution command and deterministic expected results are provided for both phases.

### 3. Architectural Traceability
*   *Review Question*: Does the task reference functional or non-functional requirements from the SRS (`REQ-FUN-XX` / `REQ-NFN-XX`)? Does the specification require the implementation of docstrings with tracing strings like `Satisfies REQ-FUN-XX` directly in class and method code?
*   *Success Criterion*: Complete requirements tracing is present in the specification, and the verification of docstring metadata in the code is mandatory.

### 4. Safety & Guard Rails
*   *Review Question*: If the task performs dangerous operations (writing files to disk, recursive deletion of directories, running system processes via `subprocess`), are there strict defensive checks (guard clauses)? Must the code raise standard exceptions (e.g., `ValueError`, `PermissionError`) when passed invalid or potentially destructive paths (such as `/`, `.`, `..`)?
*   *Success Criterion*: A dedicated safety section is present in the specification and corresponding tests for exception raising under invalid arguments are implemented.

### 5. Path Portability & Isolation
*   *Review Question*: Is hardcoding of paths eliminated in the task? Are all paths to files and directories resolved dynamically relative to the configuration file (`ude_config.json`) or package directory, rather than relative to the process's Current Working Directory (CWD)?
*   *Success Criterion*: The implementation guarantees full portability of pipeline execution between the developer's local Windows OS and CI/CD servers under Linux without manual path edits.

---

## ⚙️ Workflow

When a user or system requests task verification (e.g., with the phrase *"Verify task execution TSK-INF-01"* or *"Audit specification TSK-PAR-02"*):

1.  **Analyze Specification**: Read the task file at `.antigravitycli/tasks/TSK-XXX.md`.
2.  **Component Audit**: Evaluate the specification or current code against the 5 criteria above, assigning ratings on a 10-point scale (where 10 is absolute compliance, and ratings below 7 require mandatory resolution in recommendations).
3.  **Local TDD Testing** (for code acceptance stage):
    *   Verify that tests run in isolation.
    *   Run tests locally and ensure they pass (`Green Phase`).
    *   Run code coverage calculation (`pytest --cov=ude tests/`) and verify compliance with the `>= 90%` limit.
4.  **Formulate the Report**: Complete the evaluation matrix and provide clear recommendations for eliminating defects.
5.  **Publish Results in Documentation**: After successful task verification, update the aggregated compliance registry in the project documentation at `design-docs/docs/srs/task_compliance.md`, specifying the actual TDD status, code coverage percentage, safety status, and overall acceptance outcome.

---

## 📄 Output Template

The response must be generated strictly in the following format:

```markdown
# Task Verification Report: [Task ID — Title]

## 📊 Quality Evaluation Matrix

| Quality Criterion | Status | Score (1-10) | Key Findings and Observations |
| :--- | :---: | :---: | :--- |
| **Scope & Atomicity** | 🟢/🟡/🔴 | [1-10] | [Description] |
| **TDD Completeness** | 🟢/🟡/🔴 | [1-10] | [Description] |
| **Traceability** | 🟢/🟡/🔴 | [1-10] | [Description] |
| **Safety & Guard Rails** | 🟢/🟡/🔴 | [1-10] | [Description] |
| **Path Portability** | 🟢/🟡/🔴 | [1-10] | [Description] |

*Status Scale: 🟢 Excellent (100% compliant), 🟡 Requires Revision (minor risks), 🔴 Critical Defect (blocks development).*
*Scores below 7 require mandatory resolution in recommendations.*

## 🔍 Detailed Findings and Recommendations
*   **Observation 1 ([Criterion])**: Problem description in the specification or code. *Recommendation*: Specific steps for resolution or code review.
*   **Observation 2 ([Criterion])**: Problem description. *Recommendation*: How to rewrite it.

## 🧪 TDD Testing Results (for code acceptance stage)
- **Test Status**: `[Passed / Failed]`
- **Executed Command**: `poetry run pytest tests/test_...py`
- **Code Coverage Percentage for Affected Files**: `[XX%]` (complies/does not comply with `>= 90%` requirement)
- **Docstrings Verification (Traceability)**: `[Verified: OK / Violated (description)]`
```

---

## ⚠️ Common Verification Pitfalls
*   **Ignoring TDD**: Accepting a task if tests were written *after* the implementation code, without capturing a failing state (RED Phase).
*   **Lack of Defensive Checks**: Approving collector or parser code without handling incorrect arguments, empty strings, or paths outside the project directory.
*   **Local Environment Dependency**: Writing tests that pass successfully on the developer's machine but fail in CI/CD due to path separators (`\` vs `/`) or hardcoded drive letters (`D:\`).
*   **Dogfooding Scope Spillage**: Approving task specifications or implementations that hardcode project-specific assets (e.g., UDE's own website folders, logos, or `ude_portal_blueprint.md` links) directly inside the universal engine code. All such dependencies must be fully configurable and injected from target configurations.
