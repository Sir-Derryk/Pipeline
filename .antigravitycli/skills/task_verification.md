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

#### ⚠️ Pydantic Migration Regression Checklist
*(Mandatory gate — applies to any task touching `models.py` or its importers)*

Run these assertions before accepting the task as complete:

1. **Backward-compat alias test**: `python -c "from ude.models import ClassEntity, ClassModel; assert ClassEntity is ClassModel; print('OK')"` — must print `OK`.
2. **Old IR deserialization test**: Load a v1.0 `.json.gz` fixture that lacks `free_functions`, `enums`, `constants`, `type_aliases` fields. `ProjectCatalog.model_validate_json(old_data)` must succeed without `ValidationError`.
3. **Extra-field safety**: `ClassModel.model_validate({"name": "X", "fully_qualified_name": "Y", "unknown_v3_field": 99})` must succeed (requires `ConfigDict(extra="ignore")` on the model).
4. **Renderer string-access breakage**: After any `List[str]` → `List[SomeModel]` field change, run `grep -rn "\.fields\b" engine/ude/renderers/` and verify each hit accesses `.name` / `.type` attributes, not the field element directly as a string.

If any of the above checks fail, the task CANNOT be accepted regardless of overall pytest pass rate.

### 3. Architectural Traceability
*   *Review Question*: Does the task reference functional or non-functional requirements from the SRS? Does the specification require the implementation of docstring tracing strings directly in class and method code?
*   *Success Criterion*: Complete requirements tracing is present. Accept the following docstring tracing formats:
    - v1.0 code: `Satisfies REQ-FUN-XX`
    - v2.0 code: `Implements GAP-XX` or `Implements TASK-A.x.x` (from `.antigravitycli/v2_detailed_tasks.md`)
    Code that satisfies a v2.0 GAP item but references `REQ-FUN-XX` must be flagged for correction (stale reference, not a pass).

### 4. Safety & Guard Rails
*   *Review Question*: If the task performs dangerous operations (writing files to disk, recursive deletion of directories, running system processes via `subprocess`), are there strict defensive checks (guard clauses)? Must the code raise standard exceptions (e.g., `ValueError`, `PermissionError`) when passed invalid or potentially destructive paths (such as `/`, `.`, `..`)?
*   *Success Criterion*: A dedicated safety section is present in the specification and corresponding tests for exception raising under invalid arguments are implemented.

#### ⚠️ Renderer Factory Kwarg Forwarding Check
*(Mandatory gate — applies to any task touching `HtmlRenderer`, `HugoMarkdownRenderer`, or `LegacyRenderer`)*

Verify that `HtmlRenderer.__new__` signature includes `**kwargs` AND passes them through to the concrete subclass constructor. The verification commands:
```bash
grep -n "def __new__" engine/ude/renderers/static_html.py
grep -n "super().__init__" engine/ude/renderers/static_html.py
```
If `cache_manager` does not appear in either the `__new__` signature or is not forwarded, flag as 🔴 CRITICAL regardless of test results — the L2 cache will be silently disconnected from all renderers.

### 5. Path Portability & Isolation
*   *Review Question*: Is hardcoding of paths eliminated in the task? Are all paths to files and directories resolved dynamically relative to the configuration file (`ude_config.json`) or package directory, rather than relative to the process's Current Working Directory (CWD)?
*   *Success Criterion*: The implementation guarantees full portability of pipeline execution between the developer's local Windows OS and CI/CD servers under Linux without manual path edits.

---

## ⚙️ Workflow

When a user or system requests task verification (e.g., with the phrase *"Verify task TASK-A.1.3"*, *"Audit TASK-B.2.2"*, or legacy *"Verify TSK-INF-01"*):

1.  **Locate the Task Specification**: Accept either format:
    - **v2.0 atomic task** (current): Extract the task section matching the provided ID (e.g., `TASK-A.1.1`) from `.antigravitycli/v2_detailed_tasks.md`. Each task section begins with `#### TASK-<ID>` and ends at the next `####` heading.
    - **Legacy TSK file**: Read `.antigravitycli/tasks/TSK-XXX.md` directly.
    If neither location yields a task, halt and report: "Task [ID] not found. Verify the ID format and file location."
2.  **Component Audit**: Evaluate the specification or current code against the 5 criteria above, assigning ratings on a 10-point scale (where 10 is absolute compliance, and ratings below 7 require mandatory resolution in recommendations).
3.  **Local TDD Testing** (for code acceptance stage):
    *   Verify that tests run in isolation.
    *   Run tests locally and ensure they pass (`Green Phase`).
    *   Run code coverage calculation and verify compliance with the `>= 98%` limit:
        ```bash
        poetry run pytest --cov=ude tests/ --cov-report=term-missing
        ```
4.  **Formulate the Report**: Complete the evaluation matrix and provide clear recommendations for eliminating defects.
5.  **Publish Results** *(Consent-gated)*: Present the completed verification report in the chat. Then ask: "Shall I append these results to `design-docs/docs/srs/task_compliance.md`?" Only write upon explicit confirmation.

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
- **Code Coverage Percentage for Affected Files**: `[XX%]` (complies/does not comply with `>= 98%` requirement)
- **Docstrings Verification (Traceability)**: `[Verified: OK / Violated (description)]`
```

---

## ⚠️ Common Verification Pitfalls
*   **Ignoring TDD**: Accepting a task if tests were written *after* the implementation code, without capturing a failing state (RED Phase).
*   **Lack of Defensive Checks**: Approving collector or parser code without handling incorrect arguments, empty strings, or paths outside the project directory.
*   **Local Environment Dependency**: Writing tests that pass successfully on the developer's machine but fail in CI/CD due to path separators (`\` vs `/`) or hardcoded drive letters (`D:\`).
*   **Dogfooding Scope Spillage**: Approving task specifications or implementations that hardcode project-specific assets (e.g., UDE's own website folders, logos, or `ude_portal_blueprint.md` links) directly inside the universal engine code. All such dependencies must be fully configurable and injected from target configurations.
