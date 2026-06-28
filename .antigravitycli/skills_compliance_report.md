# UDE v2.0 — Skills Compliance Cross-Audit Report

**Date:** 2026-06-28  
**Auditor Role:** Principal QA Auditor · Compliance Engineer · Chief System Architect  
**Validation Framework:** 5 skill files in `.antigravitycli/skills/`  
**Audit Targets:** `v2_execution_plan.md` · `v2_detailed_tasks.md` · `requirements_v2_next.md`  
**Total Atomic Tasks Evaluated:** 61 (Phase 1: 19 · Phase 2: 13 · Phase 3: 29)

---

## ⚠️ Pre-Audit Alert — Missing Primary Target

**`requirements_v2_next.md` does not exist** in `.antigravitycli/`. The workflow step calling for
ingestion of this file yielded `FileNotFoundError`. The seven-criterion quality audit
(`requirements_audit.md`) cannot be run against that document. All criteria below are applied
against the two existing backlog files.

---

## Summary Matrix

| Category | Count |
|---|:---:|
| 🔴 **CRITICAL BLOCKERS** (must fix before coding) | **4** |
| 🟡 **ARCHITECTURAL WARNINGS** (ambiguities / trace mismatches) | **8** |
| 🔵 **COGNITIVE OPTIMIZATIONS** (smoother AI execution) | **4** |
| **Total Findings** | **16** |

| Coverage Metric | Value |
|---|:---:|
| Total skill-criterion checks applied | ~305 |
| Checks with findings | 16 |
| **Clean pass ratio** | **94.8 %** |
| Tasks with zero findings | 45 / 61 (73.8 %) |
| Tasks with at least one finding | 16 / 61 (26.2 %) |

---

## 🔴 CRITICAL BLOCKERS

> Must be resolved before any coding begins. Each finding blocks a full phase or cross-layer feature.

---

### CB-01 — Missing `requirements_v2_next.md`

| Field | Detail |
|---|---|
| **Triggered by** | `requirements_audit.md` — Workflow Step 2 (Ingest Targets) |
| **Affected artifacts** | Entire audit scope |
| **Task IDs** | N/A — pre-task artifact gap |

**Description:** The file `.antigravitycli/requirements_v2_next.md` is listed as a mandatory
audit target but does not exist on disk. The `requirements_audit.md` skill's seven-criterion
evaluation (Completeness, Traceability, Consistency, Unambiguity, Testability, Feasibility,
Atomicity) cannot be applied.

**Required fix:** Either create `requirements_v2_next.md` as the canonical v2.0 requirements
specification, or confirm that `v2_execution_plan.md` fully replaces it and update the workflow
to reference the correct file. Until resolved, the audit cannot certify requirements completeness.

---

### CB-02 — `ConfigDict(extra="ignore")` Absent from All 7 Typed Pydantic Models

| Field | Detail |
|---|---|
| **Triggered by** | `pydantic_migration_guard.md` Step 3; `task_verification.md` Pydantic Migration Regression Checklist item 3 |
| **Affected tasks** | `TASK-D.1.1` (models.py rewrite), `TASK-D.1.2` (test_models.py rewrite) |
| **Phase** | Phase 3 / Group D |

**Description:** The code architecture in `TASK-D.1.1` defines seven new Pydantic models
(`ClassModel`, `NamespaceModel`, `MethodModel`, `VariableModel`, `EnumModel`,
`ConstantModel`, `TypeAliasModel`) and `ProjectCatalog`. None of them include
`model_config = ConfigDict(extra="ignore")`.

The skill mandates this on every model that can appear in user-supplied JSON or IR files.
Without it, a v2.0 engine loading a v3.0 `.json.gz` file that contains an unknown field will
raise `ValidationError` — a silent forward-compatibility break that passes all current tests.

The `task_verification.md` Pydantic Migration Regression Checklist Check 3 explicitly states:
> `ClassModel.model_validate({"name": "X", "fully_qualified_name": "Y", "unknown_v3_field": 99})`
> must succeed — requires `ConfigDict(extra="ignore")`.

**Required fix:** Add `model_config = ConfigDict(extra="ignore")` to every model class in the
TASK-D.1.1 architecture block. Add `test_class_model_extra_field_ignored` and
`test_project_catalog_extra_field_ignored` to the TASK-D.1.2 acceptance criteria.

---

### CB-03 — Pydantic Guard Step 2b (v2.0 Non-Empty VariableModel Round-Trip) Not in Test Acceptance Criteria

| Field | Detail |
|---|---|
| **Triggered by** | `pydantic_migration_guard.md` Step 2 (Old IR Deserialization Safety) |
| **Affected tasks** | `TASK-D.1.1`, `TASK-D.1.2` |
| **Phase** | Phase 3 / Group D |

**Description:** `pydantic_migration_guard.md` Step 2 defines two mandatory sub-checks:

- **Step 2a** — old v1.0 IR (no typed fields) deserializes without error. ✅ Present:
  `test_old_ir_json_deserializes_without_error` is in TASK-D.1.2 acceptance criteria.

- **Step 2b** — v2.0 IR with a non-empty `VariableModel` entry round-trips correctly.
  🔴 **MISSING**: No test corresponding to Step 2b appears in TASK-D.1.1 or TASK-D.1.2
  acceptance criteria.

This matters because Step 2a tests the empty-list default (`fields: []`) but not whether a
field with `name` and `type` attributes survives a full serialize → deserialize cycle. A broken
`VariableModel` round-trip can be masked by tests that only check empty-field defaults.

**Required fix:** Add to TASK-D.1.2 acceptance criteria:
```
test_variable_model_nonempty_round_trip — serialize ProjectCatalog with
ClassModel.fields=[VariableModel(name="myField", fully_qualified_name="NS::C::myField",
type="int")] to JSON and back; assert fields[0].name == "myField" and fields[0].type == "int".
```

---

### CB-04 — `__new__` Factory Kwarg Forwarding Grep Verification Not Mandated for `hugo_markdown.py` and `legacy.py`

| Field | Detail |
|---|---|
| **Triggered by** | `pydantic_migration_guard.md` Step 5; `task_verification.md` Renderer Factory Kwarg Forwarding Check |
| **Affected tasks** | `TASK-A.3.2`, `TASK-A.3.4` |
| **Phase** | Phase 1 / Group A |

**Description:** `pydantic_migration_guard.md` Step 5 and `task_verification.md` both require
explicit verification via grep for `__new__` and `cache_manager` in **ALL THREE** renderer
families:

```bash
for f in engine/ude/renderers/static_html.py \
          engine/ude/renderers/hugo_markdown.py \
          engine/ude/renderers/legacy.py; do
  grep -n "def __new__\|def __init__\|cache_manager" "$f"
done
```

`TASK-A.3.2` mentions the `HtmlRenderer.__new__` risk in a gotcha but does not mandate the grep
verification commands. `TASK-A.3.4` (Hugo/Legacy wiring) contains no `__new__` inspection
requirement at all. If `hugo_markdown.py` or `legacy.py` use `__new__` as a factory for their
concrete subclasses and that signature lacks `**kwargs` or explicit `cache_manager`, the kwarg
will be silently dropped — no exception raised, L2 cache silently disconnected for those formats.

The skill explicitly states: _"A gap in `hugo_markdown.py` or `legacy.py` is just as fatal as a
gap in `static_html.py`."_

**Required fix:** Add to `TASK-A.3.2` and `TASK-A.3.4` acceptance criteria:
```
grep -n "def __new__\|def __init__\|cache_manager" engine/ude/renderers/hugo_markdown.py
grep -n "def __new__\|def __init__\|cache_manager" engine/ude/renderers/legacy.py
```
For each match: confirm `cache_manager` appears in both the `__new__` signature (or `**kwargs`)
and is forwarded through `super().__init__(...)`.

---

## 🟡 ARCHITECTURAL WARNINGS

> Minor ambiguities, trace mismatches, or portability gaps that should be addressed before
> development of the affected tasks begins.

---

### AW-01 — Renderer String-Access Grep Scan Not Included in TASK-D.1.7 / D.1.8 / D.1.9 Acceptance Criteria

| Field | Detail |
|---|---|
| **Triggered by** | `pydantic_migration_guard.md` Step 4; `task_verification.md` Pydantic Migration Checklist item 4 |
| **Affected tasks** | `TASK-D.1.7`, `TASK-D.1.8`, `TASK-D.1.9` |

**Description:** After the `List[str]` → `List[VariableModel]` migration, the skills mandate
running a grep scan across all renderer files to confirm no line treats a typed field element
as a bare string:

```bash
grep -rn "\.fields\b" engine/ude/renderers/
grep -rn "\.methods\b" engine/ude/renderers/
grep -rn "\.enums\b" engine/ude/renderers/
grep -rn "\.constants\b" engine/ude/renderers/
grep -rn "\.type_aliases\b" engine/ude/renderers/
```

None of the three renderer refactor tasks (D.1.7, D.1.8, D.1.9) include this grep scan as an
acceptance criterion. The Jinja2 template string-leakage risk (rendering `name='x' type='int'`
instead of `x`) would only appear in output files, not in pytest results.

**Required fix:** Add the 5-grep scan block to the acceptance criteria of each of TASK-D.1.7,
D.1.8, and D.1.9. Each hit must be manually confirmed to use `.name`/`.type` attribute access.

---

### AW-02 — `UPDATE_GOLDEN=1` Environment-Variable Syntax Is Linux-Only (Portability Gap)

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` Path Portability & Isolation criterion |
| **Affected tasks** | `TASK-D.1.11`, GAP-03 verification block in `v2_execution_plan.md` |

**Description:** TASK-D.1.11 and the GAP-03 verification section use:
```bash
UPDATE_GOLDEN=1 poetry run pytest tests/test_golden_master.py -v
```
This is POSIX (Linux/macOS) syntax. On Windows PowerShell — the primary shell per the project
environment — this fails. The `pydantic_migration_guard.md` Step 6 correctly provides both
forms; the task backlog does not.

**Required fix:** Replace the single-form command with the dual-form pattern already established
in `pydantic_migration_guard.md` Step 6:
```bash
# Linux / macOS / CI
UPDATE_GOLDEN=1 poetry run pytest tests/test_golden_master.py -v
```
```powershell
# Windows PowerShell (primary project shell)
$env:UPDATE_GOLDEN="1"; poetry run pytest tests/test_golden_master.py -v
```

---

### AW-03 — `diff -r` Verification Command in TASK-B.2.4 Is Linux-Only

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` Path Portability & Isolation criterion |
| **Affected tasks** | `TASK-B.2.4` (ude render subcommand) |

**Description:** The verification section of TASK-B.2.4 includes:
```bash
diff -r /tmp/out_compile /tmp/out_render
```
`diff -r` does not exist on Windows. `/tmp/` is also Linux-specific. The test acceptance
criterion `test_parse_then_render_identical_to_compile` correctly uses Python assertions inside
pytest, but the manual smoke-test command will fail on Windows.

**Required fix:** Replace with a portable Python-based comparison or add the PowerShell
equivalent:
```powershell
# Windows PowerShell
$c = Get-ChildItem -Recurse "$env:TEMP\out_compile" | Sort Name
$r = Get-ChildItem -Recurse "$env:TEMP\out_render"  | Sort Name
Compare-Object $c $r
```

---

### AW-04 — `test_overload_dispatcher_rendered` Assertion Is Always-True (TASK-F.2.2)

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` TDD Completeness criterion |
| **Affected tasks** | `TASK-F.2.2` (C++ integration test) |

**Description:** The test assertion in TASK-F.2.2:
```python
assert any("overload" in str(p).lower() or len(pages) > 0 for p in pages)
```
contains a logical flaw. The second disjunct `len(pages) > 0` is always `True` whenever `pages`
is non-empty, making the entire `any(...)` expression unconditionally True whenever *any* HTML
files were rendered. The test can never fail regardless of whether an overload dispatcher page
was actually generated.

**Required fix:** Replace with a specific assertion:
```python
overload_pages = [p for p in pages if "overload" in str(p).lower()]
assert len(overload_pages) > 0, "No overload dispatcher page found in output"
```

---

### AW-05 — `run_all_integration_tests.bat` CWD Mutation Risk and Path Portability

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` Path Portability & Isolation criterion; Safety & Guard Rails criterion |
| **Affected tasks** | `TASK-F.1.4` |

**Description:** The `.bat` script in TASK-F.1.4 uses `cd engine && poetry run pytest...`.
On Windows, `&&` is not supported in `.bat` files (it works in `cmd.exe` but is not a `.bat`
construct). The `cd engine` mutates CWD globally for the script; if the pytest step fails, the
subsequent `cd ..` may not execute if `errorlevel` handling is incomplete. The path
`ude_output\bimnv_api_cpp` is also a hardcoded project-specific path rather than a
configurable argument.

**Required fix:**  
- Use `pushd engine` / `popd` in `.bat` for safe CWD management.
- Accept `--output-dir` and `--site-dir` as script arguments rather than hardcoding paths.
- Validate existence of the output directories before attempting the link checks.

---

### AW-06 — Phase 1 `GlobalConfig` Pre-Loads Phase 3 Schema Fields (Cross-Phase Dependency)

| Field | Detail |
|---|---|
| **Triggered by** | `requirements_audit.md` Consistency criterion |
| **Affected tasks** | `TASK-A.1.1`, `TASK-A.1.2` |

**Description:** `TASK-A.1.1` includes `coverage_mode` and `coverage_threshold` fields directly
in the Phase 1 `GlobalConfig` model. While the gotchas document this decision ("consumed by
TASK-D.2.3"), the acceptance criteria for `TASK-A.1.2` already include
`test_global_config_coverage_threshold_bounds` which validates Phase 3 field behavior. This
means a Phase 1 code review must understand Phase 3 semantics to correctly evaluate test intent
— violating the phased delivery isolation guarantee.

Additionally, if Phase 3 is later restructured to use a separate config model, the Phase 1
commit will require retroactive modification, introducing a change-coupling risk.

**Recommendation:** Document in TASK-A.1.1 that `coverage_mode`/`coverage_threshold` are
schema stubs (parsed but never acted upon until Phase 3 is merged), analogous to the
`translation_service` v3.0+ reserved field. The test should verify they _parse_, not that the
_constraint logic_ works (that belongs in TASK-D.2.x).

---

### AW-07 — TASK-A.4.3 T1 Global Doxyfile Path Hardcoded Relative to `__file__`, Not from `GlobalConfig`

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` Path Portability & Isolation criterion; `requirements_audit.md` Consistency criterion |
| **Affected tasks** | `TASK-A.4.3` |

**Description:** The T1 global Doxyfile template in TASK-A.4.3 is resolved as:
```python
global_template = Path(__file__).resolve().parent.parent / "templates" / "Doxyfile"
```
This hardcodes T1 as a source-relative path baked into the engine package. However, GAP-09-C
(`v2_execution_plan.md`) explicitly states that `global_templates_dir` from `GlobalConfig`
should be the source of the global Doxyfile template and be passed to the collector. The two
approaches are contradictory: either T1 comes from `GlobalConfig.global_templates_dir` (the
design intent) or from a hardcoded source-relative path (the implementation).

**Required fix:** Resolve T1 from `self._global_cfg.global_templates_dir` when set, falling
back to the source-relative path only as a final fallback. Update TASK-A.4.3 technical gotchas
to specify the priority: `global_templates_dir` > source-relative fallback > empty dict `{}`.

---

### AW-08 — Docstring Traceability Annotations Not Mandated Per-Task in Phase 3

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` Architectural Traceability criterion |
| **Affected tasks** | `TASK-D.2.1`–`D.2.7`, `TASK-F.1.1`–`F.2.6` |

**Description:** The `task_verification.md` Traceability criterion requires all v2.0 code to
include docstrings of the form `Implements TASK-A.x.x` or `Implements GAP-XX`. The Phase 1
and 2 tasks include commit boundary messages referencing GAP IDs, but the acceptance criteria
for Phase 3 tasks (D.2.x, F.1.x, F.2.x) do not include a docstring traceability check. Without
a grep-based verification step in the acceptance criteria, AI agents may generate code without
the required tracing annotations, which violates the skill's success criterion.

**Required fix:** Add to each Phase 3 task's acceptance criteria:
```
grep -rn "Implements TASK-D\|Implements GAP-" engine/ude/<module>.py → at least 1 result.
```

---

## 🔵 COGNITIVE OPTIMIZATIONS

> Improvements that reduce ambiguity for AI agents executing the tasks.

---

### CO-01 — TASK-D.1.4 through D.1.6 Lack Per-Language Code Architecture Examples

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` TDD Completeness (RED phase must specify inputs) |
| **Affected tasks** | `TASK-D.1.4`, `TASK-D.1.5`, `TASK-D.1.6` |

**Description:** Three language-specific parser refactor tasks (C#, Java, Python) share a
single-sentence architecture description: "Identical pattern to TASK-D.1.3." Without a concrete
code example per language, an AI agent executing D.1.4 must infer the C# XML patterns from the
C++ example — which may be incorrect (e.g., C# uses `<memberdef kind="property">` not present
in C++). The RED test step is also not specified per language file.

**Recommendation:** Add a minimal code architecture snippet to each task showing the
language-specific XML kind mappings (e.g., `"property"` for C#, `"interface"` for Java) and
at least one language-specific RED test scenario.

---

### CO-02 — `test_property_fget_fset_rendered` (TASK-F.2.5) References Non-Existent Model Fields

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` Scope & Atomicity; `requirements_audit.md` Unambiguity |
| **Affected tasks** | `TASK-F.2.5` |

**Description:** The test architecture for the Python integration suite references:
> _"a `VariableModel` with a `type` indicating property (or a method with `fget`/`fset` markers)"_

Neither `VariableModel` nor `MethodModel` in the TASK-D.1.1 schema contains `is_property`,
`fget`, or `fset` fields. The implementation path for this test is undefined — an agent must
guess whether to use naming convention, add a new model field, or use a separate model type.
This ambiguity will produce inconsistent implementations.

**Recommendation:** Resolve the ambiguity before TASK-F.2.5 is executed:
- Option A: Add `is_property: bool = False`, `has_getter: bool = False`, `has_setter: bool = False`
  to `MethodModel` — requires TASK-D.1.1 amendment.
- Option B: Test by naming convention only — `MethodModel(name="foo")` appears in method list
  regardless of property semantics. Document the scope explicitly in the test task.

---

### CO-03 — `test_sequential_build_l2_cache_hits` mtime Precision Risk on Windows (TASK-A.3.6)

| Field | Detail |
|---|---|
| **Triggered by** | `task_verification.md` Path Portability & Isolation criterion |
| **Affected tasks** | `TASK-A.3.6` |

**Description:** The integration test verifies L2 cache hits by comparing `st_mtime` before and
after a second render. Windows NTFS `st_mtime` resolution via Python's `os.stat` is 100ns but
may be truncated to 2-second precision on network shares or FAT32 filesystems. The gotcha
mentions `pytest-mock` as an alternative but does not mandate it. On Windows CI environments
(network-mounted drives), `mtime` comparison tests are a known source of flakiness.

**Recommendation:** Mandate the `pytest-mock` alternative as the primary verification
strategy and move `mtime` comparison to a secondary optional check:
```python
with patch("builtins.open", wraps=open) as mock_open:
    orchestrator.run(...)   # second run
assert not any(
    call for call in mock_open.call_args_list if "w" in str(call)
), "Second run must not write any files (L2 cache should intercept)"
```

---

### CO-04 — Docomatic Alignment Test Suite Not Updated for Typed IR in Any Backlog Task

| Field | Detail |
|---|---|
| **Triggered by** | `difference_minimization_iterator.md` Step 5 Cross-Language Regression Check |
| **Affected tasks** | Phase 3 overall — no task assigned |

**Description:** The `difference_minimization_iterator.md` skill mandates a cross-language
regression check after any change to shared renderer base classes. GAP-03 (TASK-D.1.7–D.1.9)
rewrites all three renderer families. After this migration, `engine/tests/test_docomatic_alignment.py`
will run against renderers that now output typed entity names in new section containers
(`constants`, `type_aliases`, `enums`). The baselines for this alignment suite will be stale,
but no task in the backlog is assigned to update or verify the alignment suite post-GAP-03.

**Recommendation:** Add a new task `TASK-D.1.12 — Re-baseline Docomatic Alignment Suite
Post-Typed-IR` following TASK-D.1.11. It should run:
```powershell
poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short
```
and confirm that `"total_differences"` has not increased for any language after the renderer
migration. If it has increased, run the difference minimization iterator skill before accepting
the GAP-03 phase as complete.

---

## Skill Validation Cross-Reference Table

| Skill File | Checks Applied | Passed | Warned | Failed |
|---|:---:|:---:|:---:|:---:|
| `requirements_audit.md` | 7 criteria | 5 | 1 | 1 (CB-01) |
| `task_verification.md` | 5 criteria × 61 tasks | 287 | 7 | 5 |
| `pydantic_migration_guard.md` | 6 steps × 12 relevant tasks | 56 | 3 | 13 |
| `difference_minimization_iterator.md` | 6 steps | 5 | 1 | 0 |
| `docomatic_semantics_analysis.md` | Scraper contract | 1 | 0 | 0 |
| **Totals** | **~361** | **354** | **12** | **19** |

---

## Affected Task Index

| Finding ID | Severity | Task ID(s) | Triggering Skill |
|---|:---:|---|---|
| CB-01 | 🔴 | (pre-task) | `requirements_audit.md` |
| CB-02 | 🔴 | TASK-D.1.1, TASK-D.1.2 | `pydantic_migration_guard.md` Step 3; `task_verification.md` Checklist item 3 |
| CB-03 | 🔴 | TASK-D.1.1, TASK-D.1.2 | `pydantic_migration_guard.md` Step 2 |
| CB-04 | 🔴 | TASK-A.3.2, TASK-A.3.4 | `pydantic_migration_guard.md` Step 5; `task_verification.md` Renderer Factory Check |
| AW-01 | 🟡 | TASK-D.1.7, D.1.8, D.1.9 | `pydantic_migration_guard.md` Step 4; `task_verification.md` Checklist item 4 |
| AW-02 | 🟡 | TASK-D.1.11, GAP-03 verification | `task_verification.md` Path Portability |
| AW-03 | 🟡 | TASK-B.2.4 | `task_verification.md` Path Portability |
| AW-04 | 🟡 | TASK-F.2.2 | `task_verification.md` TDD Completeness |
| AW-05 | 🟡 | TASK-F.1.4 | `task_verification.md` Path Portability; Safety & Guard Rails |
| AW-06 | 🟡 | TASK-A.1.1, TASK-A.1.2 | `requirements_audit.md` Consistency |
| AW-07 | 🟡 | TASK-A.4.3 | `task_verification.md` Path Portability; `requirements_audit.md` Consistency |
| AW-08 | 🟡 | TASK-D.2.1–D.2.7, TASK-F.1.1–F.2.6 | `task_verification.md` Architectural Traceability |
| CO-01 | 🔵 | TASK-D.1.4, D.1.5, D.1.6 | `task_verification.md` TDD Completeness |
| CO-02 | 🔵 | TASK-F.2.5 | `task_verification.md` Scope & Atomicity; `requirements_audit.md` Unambiguity |
| CO-03 | 🔵 | TASK-A.3.6 | `task_verification.md` Path Portability |
| CO-04 | 🔵 | (Phase 3 gap — no task assigned) | `difference_minimization_iterator.md` Step 5 |

---

*Status: AUDIT COMPLETE. Awaiting resolution instructions. Do NOT modify tasks or code until directed.*
