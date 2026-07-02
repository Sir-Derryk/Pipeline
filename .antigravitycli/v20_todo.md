# UDE v2.0 — Consolidated Task Plan

> **Document:** `ToDo/v20_todo.md`  
> **Date:** 2026-06-29  
> **Sources:**  
> - `.antigravitycli/v2_execution_plan.md` — technical phase plan (GAP-09 → GAP-12 → GAP-07 → GAP-11 → GAP-05 → GAP-01 → GAP-03 → GAP-10 → GAP-31 → GAP-32)  
> - `ToDo/RepoStruct_ToDo.md` — repository structure  
> - `ToDo/CICD_ToDo.md` — CI/CD migration  
> - `ToDo/ActivitiesReqs_ToDo.md` — pipeline requirements  
> - `ToDo/ActivitiesDoc_ToDo.md` — pipeline documentation  
> - `ToDo/DocReqs_ToDo.md` — technical documentation requirements  
> - `ToDo/UserDocs_ToDo.md` — user documentation  
> - `ToDo/Tests_ToDo.md` — testing and quality assurance plan  
>
> **TDD Invariant (mandatory for every commit):**  
> Red → Green → Refactor · Coverage gate ≥ 98% · No step is checked off without passing tests

---

## Symbols

| Marker | Meaning |
|--------|---------|
| 🔴 | Blocks the next step / critical |
| 🟡 | Important for v2.0 / required before release |
| 🟢 | Desirable / can be parallelized |
| ⚡ | Depends on completion of the previous step |
| `[GAP-XX]` | Link to GAP from `v2_execution_plan.md` |
| `[AD-XXX]` | Link to task from `ActivitiesDoc_ToDo.md` |
| `[AR-XXX]` | Link to task from `ActivitiesReqs_ToDo.md` |
| `[DR-XXX]` | Link to task from `DocReqs_ToDo.md` |
| `[UD-XXX]` | Link to task from `UserDocs_ToDo.md` |
| `[RS-TX]` | Link to task from `RepoStruct_ToDo.md` |
| `[CI-X.Y]` | Link to task from `CICD_ToDo.md` |

---

## Section 0 — Repository and Environment Preparation

> **Goal:** Set up the repository in order before starting v2.0 implementation. Executed once. Does not block Phase 1 completely but reduces technical debt.

### 0.1 baseline Verification of v1.0 State (TDD: Baseline)

> Executed first — before any physical changes to the repository. Guarantees that any subsequent regression is diagnosed relative to the certified green baseline.

- [x] **[TST-0.1]** 🔴 **[Python]** Ensure all 209 engine tests pass: `poetry run pytest engine/tests/ -v` ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [x] **[TST-0.2]** 🔴 **[Python]** Confirm coverage ≥ 98%: `poetry run pytest --cov=ude --cov-report=term-missing` (or `grep TOTAL`) ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [x] **[TST-0.3]** 🔴 **[Python]** Record baseline metrics (number of tests, % coverage, run time) in `ToDo/Tests_ToDo.md` ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [x] **[TST-0.4]** 🟡 **[Python]** Run performance benchmark: `poetry run pytest tests/test_performance_benchmark.py -v` — make sure it executes in ≤ 5 s for 1000 classes ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [x] **[TST-0.5]** 🟡 **[Python]** Generate HTML coverage report: `poetry run pytest --cov=ude --cov-report=html` ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [x] **[TST-0.6]** 🟡 **[Python]** Identify modules with coverage < 98% and record gaps in `Tests_ToDo.md` ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [x] **[TST-0.7]** 🟢 **[Python]** Create test `test_coverage_gate.py` with CI-ready parameter `--cov-fail-under=98` ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

### 0.2 Repository Structural Changes

> Executed strictly after fixing baseline (0.1). Most tasks are safe for tests; the exception is RS-T9 (medium risk, requires synchronous updates of imports and scripts).

- [x] **[RS-T1]** 🔴 Commit uncommitted architectural documents: `CICD.md`, `RepoStruct.md`, `RepoStruct_ToDo.md` ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T1] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [x] **[RS-T2]** 🔴 Delete `FutureImprovements/` — 4 files without value (`doxygen_cpp.py`, `cpp_signature_formatter.py`, `legacy_cpp_sidebar.json`, `cpp_class_layout.html`) ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T2] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [x] **[RS-T3]** 🔴 Document the `ude_` prefix convention for root directories in `CLAUDE.md` ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T3] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [x] **[RS-T4]** 🟡 Rename `/refs/` → `/sdk_refs/` in `.gitignore` (resolves conflict with git terminology) ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T4] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [x] **[RS-T5]** 🟡 Move utilities `compress_history.bat`, `compress_history.ps1`, `run_swig.bat` to `scripts/` ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T5] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [x] **[RS-T6]** 🟢 Merge `Tests/` + `LoadTest/` → `ude_tests/regression/` + `ude_tests/load/`; update paths in `.github/workflows/integration_tests.yml` ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T6] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[RS-T7]** 🟢 Verify redundancy of `.gitignore` rules for `ude_projects/` — run generation, check `git status` ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T7] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[RS-T8]** 🟢 Audit `make_release.py` — understand ODA compatibility logic (prerequisite for RS-T9) ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T8] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[RS-T9]** 🟢 **[MEDIUM RISK]** Rename `main/` → `sdk_sources/` after RS-T8 — requires synchronous updates of Python imports, build scripts, and IDE settings ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T9] ──► [Model: Antigravity - Gemini 3.5 Flash (High)]
- [ ] **[RS-T10]** 🟢 Rename umbrella branch `master` → `main` (requires coordination with CI/CD) ──► [Source: ToDo/RepoStruct_ToDo.md #RS-T10] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]

### 0.3 Code Documentation Requirements (applied from this point forward)

- [ ] **[DR-NEW-04]** 🟡 Fix file naming rule in `CLAUDE.md`: kebab-case for `user-docs/`, snake_case for `.antigravitycli/` ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[DR-NEW-21]** 🟡 Establish rule: every new GitHub Actions workflow begins with a comment block (purpose, triggers, secrets, execution time) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-21] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-20]** 🟡 Introduce rule: every new `TASK-*.md` contains a `Related Docs` field — files in user-docs/design-docs requiring updates ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-20] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

> ⚠️ **Immediately active rules from Section 8 (🔴):** DR-NEW-01 (markdownlint in CI), DR-NEW-06 (Mermaid diagrams), DR-NEW-10/11 (link rules), DR-NEW-22–25 (secrets and workflow env), DR-NEW-29 (Docusaurus build gate), DR-NEW-32 (CLI smoke test in CI). Details in Section 8.

### 0.4 Refactoring and Auditing Existing Test Base (TDD: Refactor)

- [ ] **[TST-0.8]** 🔴 **[Python]** In `engine/tests/test_orchestrator.py`: replace all occurrences of `"ude_global.json"` → `"ude_global_config.json"`, `"ude_config.json"` → `"ude_doc_config.json"` ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[TST-0.9]** 🔴 **[Python]** In `engine/tests/test_integration_pipeline.py`: perform similar replacements ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[TST-0.10]** 🔴 **[Python]** In `engine/tests/test_doxygen_collector.py`: perform similar replacements ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[TST-0.11]** 🟡 **[Python]** Update docstring comments in `engine/ude/interfaces.py` and `engine/ude/collectors/doxygen.py` ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-0.12]** 🟡 **[Python]** Run `poetry run pytest engine/tests/ -v` after replacements — ensure 0 failed ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-0.13]** 🔴 **[Python]** In `engine/tests/` find all `caplog` assertions with `"ude.renderers"` from `interfaces.py` ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-0.14]** 🔴 **[Python]** Update found assertions: `"ude.renderers"` → `"ude.interfaces"` (HC-05 logger fix) ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-0.15]** 🔴 **[Python]** Ensure tests pass after fix ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[TST-0.17]** 🟡 **[Python]** Add helper function `_write_test_config(tmp_path, **kwargs) -> Path` for temporary configurations ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-0.18]** 🟢 **[Python]** Add factory `_make_mock_catalog` to create a synthetic `ProjectCatalog` ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

---

## Section 1 — Phase 1: Engine Infrastructure

> **Strategic Order:** GAP-09 → (GAP-12 ‖ GAP-07) → GAP-11  
> GAP-12 and GAP-07 both depend only on GAP-09 and can execute in parallel. GAP-11 is independent of GAP-12/07 and runs last in the phase.

### 1.1 GAP-09 — Activation of GlobalConfig Fields `[REQ-V2-01]`

> **Goal:** Make all fields in `ude_global_config.json` operationally active via a Pydantic model.

**Tests (RED — write first):**

- [ ] **[TST-1.1]** 🔴 **[Python]** Write test `test_global_config_defaults` — empty JSON produces all defaults ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.2]** 🔴 **[Python]** Write test `test_global_config_full_round_trip` — all fields round-trip through `from_file()` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.3]** 🔴 **[Python]** Write test `test_global_config_unknown_keys_ignored` — extra keys do not cause ValidationError ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.4]** 🔴 **[Python]** Write test `test_global_config_missing_file_raises` — FileNotFoundError when file is missing ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.5]** 🔴 **[Python]** Write test `test_global_config_bad_json_raises` — ValueError on invalid JSON ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.6]** 🔴 **[Python]** Write test `test_global_config_coverage_threshold_parses` — threshold 0.85 is accepted without error ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.7]** 🔴 **[Python]** Write test `test_global_config_coverage_threshold_bounds` — threshold 1.5 → ValidationError ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.8]** 🔴 **[Python]** Write test `test_apply_global_cfg_env_injects_path` — doxygen_path is added to PATH ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.9]** 🔴 **[Python]** Write test `test_apply_global_cfg_env_idempotent` — double call does not duplicate path in PATH ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.10]** 🔴 **[Python]** Write test `test_apply_global_cfg_env_noop_when_none` — doxygen_path=None does not change PATH ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.11]** 🟡 **[Python]** Write test `test_orchestrator_stores_global_cfg_instance` — orchestrator._global_cfg contains GlobalConfig instance ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.12]** 🟡 **[Python]** Write test `test_orchestrator_sets_path_from_doxygen_path` — mock subprocess.run; doxygen_path is injected before running doxygen ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.13]** 🟡 **[Python]** Write test `test_orchestrator_cache_root_resolved_absolute` — cache_root_dir is resolved to an absolute path ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Implementation (GREEN):**

- [ ] ⚡ 🔴 Create `engine/ude/config.py` — `GlobalConfig(BaseModel)` with fields `doxygen_path`, `log_level`, `log_file`, `cache_root_dir`, `global_templates_dir`, `error_policy`, `translation_service`, `coverage_mode`, `coverage_threshold`; factory `from_file()`; `ConfigDict(extra="ignore")` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Replace raw `json.load` in `UdeOrchestrator.__init__()` with `GlobalConfig.from_file()`, store as `self._global_cfg` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 In `run_target()`: inject `doxygen_path` into env, resolve `global_templates_dir` and `cache_root_dir` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 In `cli.py:run_pipeline()`: replace raw `json.load` with `GlobalConfig.from_file()` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Resolve all paths in `GlobalConfig` relative to the parent directory of the config file, not CWD ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-09] ──► [Model: Claude Code - Sonnet 3.6]

**Verification:**
```bash
poetry run pytest tests/test_config.py -v --tb=short
# Expected: 6/6 PASSED
poetry run pytest --cov=ude --cov-report=term-missing | grep TOTAL
# Expected: ≥ 98%
```

**Commit:** `feat(config): add GlobalConfig pydantic model with from_file() factory`

---

### 1.2 GAP-12 — Unified Logging `[REQ-V2-02]`

> **Prerequisite:** GAP-09 completed. Can run in parallel with GAP-07 (1.3).

**Tests (RED):**

- [ ] **[TST-1.14]** 🔴 **[Python]** Write test `test_logging_setup_stderr_only` — log_file=None → exactly 1 StreamHandler ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.15]** 🔴 **[Python]** Write test `test_logging_setup_with_log_file` — log_file → 2 handlers, file created on disk ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.16]** 🔴 **[Python]** Write test `test_logging_setup_level_debug` — log_level="DEBUG" → logger.level == DEBUG ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.17]** 🔴 **[Python]** Write test `test_logging_setup_invalid_level` — VERBOSE (invalid) level falls back to WARNING without crashing ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.18]** 🔴 **[Python]** Write test `test_logging_setup_idempotent` — double call does not accumulate StreamHandlers ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Claude Code - Sonnet 3.6]

**Implementation (GREEN):**

- [ ] ⚡ 🔴 In `engine/ude/interfaces.py` line 8: `"ude.renderers"` → `"ude.interfaces"` (HC-05) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] ⚡ 🔴 Add `logging_setup(cfg: GlobalConfig) -> None` in `engine/ude/config.py` with `root.handlers.clear()` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Call `logging_setup(self._global_cfg)` in `UdeOrchestrator.__init__()` after `from_file()` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Call `logging_setup(global_cfg)` in `cli.py:run_pipeline()` immediately after loading config ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🟡 Find all tests with assert `"ude.renderers"` from `interfaces.py` and update them ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-12] ──► [Model: Antigravity - Gemini 3.5 Flash (High)]

**Verification:**
```bash
poetry run pytest tests/test_config.py -v -k "logging"
# Expected: 4/4 PASSED
```

**Commit:** `feat(config): add unified logging_setup(); fix HC-05 logger label`

---

### 1.3 GAP-07 — Activation of L2 Render Cache `[REQ-V2-03]`

> **Prerequisite:** GAP-09 completed (requires `cache_root_dir` from `GlobalConfig`). Can run in parallel with GAP-12 (1.2).

**Tests (RED):**

- [ ] **[TST-1.19]** 🔴 **[Python]** Write test `test_compute_template_hash_stable` — hash is stable across repeat calls ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.20]** 🔴 **[Python]** Write test `test_compute_template_hash_changes_on_content_change` — modifying template changes its hash ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.21]** 🔴 **[Python]** Write test `test_compute_template_hash_empty_dir` — empty directory → "" ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.22]** 🔴 **[Python]** Write test `test_compute_template_hash_missing_dir` — non-existent directory → "" ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.23]** 🔴 **[Python]** Write test `test_l2_html_cache_hit_skips_write` — repeat render does not overwrite file (spy on open) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.24]** 🔴 **[Python]** Write test `test_l2_html_cache_miss_on_catalog_change` — mutating a method in catalog invalidates cache ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.25]** 🔴 **[Python]** Write test `test_l2_html_cache_miss_on_template_change` — modifying Jinja2 template invalidates cache ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.26]** 🔴 **[Python]** Write test `test_l2_html_cache_disabled_when_no_manager` — cache_manager=None → files always written (v1.0) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.27]** 🔴 **[Python]** Write test `test_l2_hugo_cache_hit_skips_write` — analog of L2 cache for Hugo renderer ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.28]** 🔴 **[Python]** Write test `test_l2_legacy_cache_hit_skips_write` — analog of L2 cache for Legacy renderer ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.29]** 🟡 **[Python]** Write test `test_sequential_build_l2_cache_hits` — integration: no writes occur during second orchestrator.run() ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.30]** 🔴 **[Python]** Perform grep audit (CB-04): ensure `cache_manager` is declared in `__new__` and forwarded to `super().__init__()` of renderers ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-1.31]** 🔴 **[Python]** Write test `test_cache_manager_forwarded_through_new_hugo` — HugoMarkdownRenderer stores `_cache_mgr` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-1.32]** 🔴 **[Python]** Write test `test_cache_manager_forwarded_through_new_legacy` — LegacyRenderer stores `_cache_mgr` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]

**Implementation (GREEN):**

- [ ] ⚡ 🔴 Verify/implement `BuildCacheManager` in `engine/ude/storage.py` — methods `is_render_stale()`, `update()`, `save()` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Add `compute_template_hash(template_dir: Path) -> str` in `storage.py` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Resolve `cache_dir` in `UdeOrchestrator.run_target()` from `GlobalConfig.cache_root_dir` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Pass `cache_dir` to renderer constructor; update `BaseRenderer.__init__()` — parameter `cache_dir: Optional[Path] = None` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 In `BaseRenderer.render()`: before writing each file, check L2 cache; on HIT skip write and log DEBUG `"[L2 cache HIT]"` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Ensure: `cache_manager` kwarg is forwarded through `__new__` of all three renderer families (`static_html`, `hugo_markdown`, `legacy`) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-07] ──► [Model: Claude Code - Sonnet 3.6]

**Verification:**
```bash
poetry run pytest tests/test_caching.py -v
# Expected: all L2 tests PASSED
# The second run must log "[L2 cache HIT]" for unchanged entities
```

**Commit:** `feat(cache): wire L2 render cache into BaseRenderer.render()`

---

### 1.4 GAP-11 — Doxyfile 3-Tier Key-Level Merge `[REQ-V2-04]`

> **Prerequisite:** No hard dependency on GAP-09/12/07, but executed after them.

**Tests (RED — TDD):**

- [ ] **[TST-1.33]** 🔴 **[Python]** Write test `test_parse_basic` — parsing simple Key = Value pairs in Doxyfile ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.34]** 🔴 **[Python]** Write test `test_parse_skip_comments_and_blanks` — `#` comments and empty lines are ignored ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.35]** 🔴 **[Python]** Write test `test_parse_continuation_lines` — line continuations via backslash `\` are collapsed into one line ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.36]** 🔴 **[Python]** Write test `test_parse_value_with_equals` — values containing `=` (e.g. PREDEFINED) are parsed correctly ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.37]** 🔴 **[Python]** Write test `test_serialize_round_trip` — parse -> serialize -> parse preserves keys in alphabetical order ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.38]** 🔴 **[Python]** Write test `test_merge_t2_overrides_t1` — override T1 keys with values from T2 ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.39]** 🔴 **[Python]** Write test `test_merge_t3_overrides_t2` — override T2 keys with values from T3 ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.40]** 🔴 **[Python]** Write test `test_merge_debug_log_on_conflict` — T2 vs T1 conflict logs a DEBUG message ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.41]** 🔴 **[Python]** Write test `test_merge_missing_tiers` — graceful degradation of merge when T1/T2 are missing ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.42]** 🟡 **[Python]** Write test `test_collector_uses_merged_doxyfile` — mock subprocess.run; target Doxyfile contains T3 keys exactly once ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-1.43]** 🟡 **[Python]** Write test `test_collector_t3_overrides_t2_key` — target Doxyfile specifies GENERATE_HTML=YES, merge overrides to NO ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Implementation (GREEN):**

- [ ] ⚡ 🔴 Create `engine/ude/collectors/doxyfile.py` — `parse_doxyfile()`, `serialize_doxyfile()`, `merge_doxyfile_tiers(t1, t2, t3) -> dict` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 In `engine/ude/collectors/doxygen.py`: replace concatenation of 3 files with `parse_doxyfile` + `merge_doxyfile_tiers` + `serialize_doxyfile` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🟡 Ensure: if `global_templates_dir` is missing → T1 = `{}` (merge degrades to T2+T3) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] ⚡ 🟡 Backward compatibility: `doxyfile_template` in `ude_doc_config.json` continues to work ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-11] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Verification:**
```bash
poetry run pytest tests/test_doxyfile.py -v
# Expected: 8/8 PASSED
poetry run pytest --cov=ude --cov-report=term-missing | grep TOTAL
# Expected: ≥ 98%
```

**Commit:** `feat(collector): replace doxyfile concatenation with 3-tier key-level merge`

---

### 1.5 Phase 1 Environment Provisions (CI/CD security gate)

- [ ] **[AR-GAP-02]** 🔴 Add `permissions:` block in `integration_tests.yml`: `contents: read`, `checks: write`, `actions: read` ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AR-GAP-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-SEC-01]** 🔴 Pin `actions/checkout` version (pinned semver-tag) ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-SEC-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-SEC-02]** 🔴 Pin `actions/setup-python` version (pinned semver-tag) ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-SEC-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-SEC-03]** 🔴 Pin `peaceiris/actions-hugo` version (specific version, not `latest`) ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-SEC-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-SEC-07]** 🔴 Remove fallback `|| github.token` — workflow must fail explicitly without PAT ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-SEC-07] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-ISO-01]** 🟡 Switch `pip install` to virtual environment in CI runner ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-ISO-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-ISO-02]** 🟡 Move `PYTHONPATH: engine` to the job-level `env:` section ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-ISO-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

---

## Section 2 — Phase 2: Library API and CLI Unification

> **Strategic Order:** GAP-05 → GAP-01  
> **Prerequisite:** Phase 1 fully completed.

### 2.1 GAP-05 — UdeOrchestrator Public Library API `[REQ-V2-05]`

**Tests (RED):**

- [ ] **[TST-2.1]** 🔴 **[Python]** Write test `test_orchestrator_parse_returns_catalog` — `orchestrator.parse()` returns ProjectCatalog ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-2.2]** 🔴 **[Python]** Write test `test_orchestrator_parse_skips_collector_when_xml_exists` — repeated run does not invoke DoxygenXmlCollector.collect ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-2.3]** 🔴 **[Python]** Write test `test_orchestrator_render_produces_files` — `orchestrator.render()` creates HTML/Markdown files in out_dir ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-2.4]** 🔴 **[Python]** Write test `test_orchestrator_render_respects_format_config` — renderer format selection (static_html / hugo_markdown) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-2.5]** 🔴 **[Python]** Write test `test_orchestrator_run_end_to_end` — `orchestrator.run()` returns True on success, generates files ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-2.6]** 🔴 **[Python]** Write test `test_run_target_is_alias` — run_target() invokes run() for backward compatibility ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[TST-2.7]** 🔴 **[Python]** Write test `test_orchestrator_run_returns_false_on_missing_config` — missing config returns False ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-2.8]** 🟡 **[Python]** Write test `test_resolve_config_returns_merged_dict` — correct priorities when merging global/sdk/doc configs ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-2.9]** 🟡 **[Python]** Write test `test_resolve_config_graceful_sidebar_missing` — missing `sidebar.toml` does not raise error ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-2.10]** 🟡 **[Python]** Write test `test_resolve_config_sidebar_static_paths_absolute` — static paths from sidebar.toml are converted to absolute ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-2.11]** 🟡 **[Python]** Write test `test_deep_merge_importable_from_both_modules` — importing `deep_merge` works from both `cli.py` and `orchestrator.py` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Implementation (GREEN):**

- [ ] ⚡ 🔴 Move `deep_merge()` and `find_product_json()` from `cli.py` → `orchestrator.py` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Update import in `cli.py`: `from ude.orchestrator import deep_merge, find_product_json` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] ⚡ 🔴 Add `resolve_config(doc_config_path, global_cfg) -> tuple[dict, Path]` in `orchestrator.py` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Implement public method `parse(config, config_dir) -> ProjectCatalog` on `UdeOrchestrator` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Implement public method `render(catalog, config, config_dir, out_dir) -> None` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Implement public method `run(doc_config_path) -> bool` — end-to-end shortcut ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Make `run_target()` a thin alias calling `run()` for backward compatibility ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] ⚡ 🔴 Simplify `cli.py:run_pipeline()` to: load GlobalConfig → instantiate orchestrator → call `run()` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🟡 v1.0 flat CLI flags (`--global-config`, `--sdk-config`, `--doc-config`, `--input`, `--output`, `--format`) work identically ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-05] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Smoke test:**
```bash
python -c "from ude.orchestrator import UdeOrchestrator; o = UdeOrchestrator(); print(dir(o))"
# parse, render, run — present in output
```

**Commit:** `refactor(orchestrator): expose public parse/render/run API; slim cli.py`

---

### 2.2 GAP-01 — CLI Subcommands `[REQ-V2-06]`

> **Prerequisite:** GAP-05 completed.

**Tests (RED):**

- [ ] ⚡ 🔴 Supplement `engine/tests/test_cli.py` with 6 new tests: ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-01] ──► [Model: Claude Code - Sonnet 3.6]
  - `test_compile_subcommand_delegates_to_run`
  - `test_parse_subcommand_creates_ir_file`
  - `test_render_subcommand_from_ir_file`
  - `test_flat_flags_still_work` — backward compat
  - `test_parse_then_render_output_identical_to_compile`
  - `test_audit_subcommand_reachable` — returns non-zero (stub), does not crash argparse

**Implementation (GREEN):**

- [ ] ⚡ 🔴 Restructure `main()` in `cli.py` — `parser.add_subparsers(dest="command")`; if `args.command is None` — fallback to v1.0 flat ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-01] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Implement subcommand `ude compile` — behavior identical to v1.0 flat ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-01] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Implement subcommand `ude parse` — argument `--output-ir`, prints JSON summary to stdout ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-01] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Implement subcommand `ude render` — argument `--input-ir`, loads IR and renders ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-01] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Implement subcommand `ude audit` — shell stub raising `NotImplementedError` (full implementation in GAP-10) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-01] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🟡 `ude compile --doc-config X` and `ude --doc-config X` produce byte-identical output ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-01] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Verification:**
```bash
poetry run pytest tests/test_cli.py -v
# All tests PASSED
```

**Commit:** `feat(cli): add compile/parse/render/audit subcommands; keep v1.0 flat interface`

---

### 2.3 CLI Documentation for User Docs

- [ ] **[UD-CLI-01]** 🟡 Create `user-docs/docs/reference/cli-reference.md` ──► [Source: ToDo/UserDocs_ToDo.md #UD-CLI-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[UD-CLI-02]** 🟡 Document v1.0 flat interface (backward compat) ──► [Source: ToDo/UserDocs_ToDo.md #UD-CLI-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[UD-CLI-03]** 🟡 Document `ude compile` — arguments, examples, exit codes ──► [Source: ToDo/UserDocs_ToDo.md #UD-CLI-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[UD-CLI-04]** 🟡 Document `ude parse` — `--output-ir`, JSON summary format ──► [Source: ToDo/UserDocs_ToDo.md #UD-CLI-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[UD-CLI-05]** 🟡 Document `ude render` — `--input-ir`, decoupled pipeline ──► [Source: ToDo/UserDocs_ToDo.md #UD-CLI-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[UD-CLI-06]** 🟡 Document `ude audit` (stub in v2.0) — modes, exit codes ──► [Source: ToDo/UserDocs_ToDo.md #UD-CLI-06] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[UD-CLI-07]** 🟡 Add exit codes table: 0 (success), 1 (error), 2 (audit fail) ──► [Source: ToDo/UserDocs_ToDo.md #UD-CLI-07] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[UD-CLI-08]** 🟢 Add examples of pipelined `ude parse` + `ude render` ──► [Source: ToDo/UserDocs_ToDo.md #UD-CLI-08] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 2.4 CI Transition Gate for CLI

- [ ] **[CI-4.4]** 🟡 Add CLI backward compatibility smoke test to `generate-api-ref.yml`: `ude --help`, `ude compile --help`, `ude parse --help`, `ude render --help`, `ude audit --help` ──► [Source: ToDo/CICD_ToDo.md #CI-4.4] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-4.4]** 🟡 After implementing GAP-01: update the compilation step in CI from flat CLI to `ude compile --all --output`; verify byte-identical output between v1.0 and v2.0 before switching ──► [Source: ToDo/CICD_ToDo.md #CI-4.4] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

---

## Section 3 — Phase 3 / Track D: Typed IR

> **Prerequisite:** GAP-01 completed (`ude audit` stub is available).  
> **Attention:** The most extensive part of v2.0. Affects all pipeline layers.  
> **Order:** GAP-03 → GAP-10

### 3.1 GAP-03 — Typed Entity Models `[REQ-V2-07]`

**Tests (RED — write before modifying models.py):**

- [ ] **[TST-3.1]** 🔴 **[Python]** Write test `test_project_catalog_has_project_name_and_version` — project name and version round-trip through JSON ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.2]** 🔴 **[Python]** Write test `test_class_model_fields_are_variable_models` — class fields contain instances of VariableModel, not strings ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.3]** 🔴 **[Python]** Write test `test_old_ir_json_deserializes_without_error` — deserializing v1.0 IR without new fields succeeds ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.4]** 🔴 **[Python]** Write test `test_variable_model_nonempty_round_trip` — non-empty fields in VariableModel encode/decode correctly ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.5]** 🔴 **[Python]** Write test `test_class_model_extra_field_ignored` — extra fields are stripped during validation of ClassModel ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.6]** 🔴 **[Python]** Write test `test_project_catalog_extra_field_ignored` — extra fields are stripped during validation of ProjectCatalog ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.7]** 🔴 **[Python]** Write test `test_backward_compat_alias` — alias `ClassEntity is ClassModel` returns True ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.8]** 🔴 **[Python]** Write test `test_7_model_round_trip` — round-trip of catalog containing all 7 new models ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.9]** 🟡 **[Python]** Write test `test_method_model_overloads` — `MethodModel.overloads` contains a list of `OverloadModel` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-3.10]** 🟡 **[Python]** Write test `test_enum_model_values` — `EnumModel.values` contains `List[str]` values ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-3.11]** 🟡 **[Python]** Write test `test_constant_model_has_value` — `ConstantModel.value` serializes as `null` if the value is `None` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-3.12]** 🟡 **[Python]** Write test `test_type_alias_model_round_trip` — correctness of `TypeAliasModel` serialization/deserialization ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Implementation of `models.py` (GREEN):**

- [ ] ⚡ 🔴 Completely replace `engine/ude/models.py` — 7 models: `ParameterModel`, `OverloadModel`, `MethodModel`, `EnumModel`, `VariableModel`, `ConstantModel`, `TypeAliasModel`, `ClassModel`, `NamespaceModel`, `ProjectCatalog` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 Add `project_name: str = ""` and `version: str = ""` to `ProjectCatalog` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 Global search and replace: `NamespaceEntity` → `NamespaceModel` across codebase ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 Commit `models.py` in isolation — before modifying parsers and renderers ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]

**Parser Refactoring:**

- [ ] ⚡ 🔴 `engine/ude/parsers/doxygen.py` — `ClassEntity(...)` → `ClassModel(...)`; `NamespaceEntity(...)` → `NamespaceModel(...)`; `MethodEntity` → `MethodModel`; `ParameterField` → `ParameterModel` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 `doxygen_csharp.py`, `doxygen_java.py`, `doxygen_python.py`, `doxygen_base.py`, `doxygen_router.py` — similar refactoring ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 Populate new typed lists (`VariableModel`, `ConstantModel`, `EnumModel`) with data from Doxygen XML; on missing metadata → `None`, do not delete the entity ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 After each file: `poetry run pytest tests/test_doxygen_parser.py` (catch regressions early) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]

**Renderer Refactoring:**

- [ ] ⚡ 🔴 `engine/ude/renderers/static_html.py` — replace attributes of `ClassEntity` with new models; `entity.fields` (was `List[str]`) → iterate as `List[VariableModel]` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 `hugo_markdown.py` — similar refactoring ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 `legacy.py` — similar refactoring ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🟡 Add rendering of `entity.enums`, `entity.constants`, `entity.type_aliases` inside existing page sections (without layout changes — v3.0+) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Storage and Tests Refactoring:**

- [ ] ⚡ 🔴 `engine/ude/storage.py` — add round-trip test of 7-model structure through gzip ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 Update `test_doxygen_parser.py`, `test_html_renderer.py`, `test_hugo_renderer.py`, `test_legacy_renderer.py`, `test_integration_pipeline.py` for new scheme ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 Regenerate golden master baselines (`UPDATE_GOLDEN=1 poetry run pytest tests/test_golden_master.py`) — only after confirming `git diff --stat` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 Rerun Docomatic alignment suite (`test_docomatic_alignment.py`); verify that `"total_differences"` did not increase for unaffected languages ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]

**Refactoring Existing Tests for v2.0 Models:**

- [ ] **[TST-3.13]** 🔴 **[Python]** In `test_doxygen_parser.py`: update assertions for `entity.fields` (access via `.name`, not string indices) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.14]** 🔴 **[Python]** In `test_doxygen_parser.py`: add test `test_parser_populates_enum_model` (Kind="enum" in XML parses to `EnumModel`) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.15]** 🔴 **[Python]** In `test_doxygen_parser.py`: add test `test_parser_populates_constant_model` (Kind="variable" static=yes -> `ConstantModel`) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.16]** 🔴 **[Python]** In `test_html_renderer.py`: update test fixtures for ClassModel with VariableModel ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.17]** 🔴 **[Python]** In `test_hugo_renderer.py`: update test fixtures similarly ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.18]** 🔴 **[Python]** In `test_legacy_renderer.py`: update test fixtures similarly ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.19]** 🔴 **[Python]** Verify absence of direct `.fields` references in renderers using grep (Guard Step 4) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[TST-3.20]** 🔴 **[Python]** Run `test_doxygen_parser.py` and all integration tests to verify changes ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]

**Verification of Pydantic Compatibility (CB-02, CB-03 from `skills_compliance_report.md`):**

- [ ] ⚡ 🔴 Verify existence of `model_config = ConfigDict(extra="ignore")` on EVERY typed Pydantic model in `engine/ude/models.py` (CB-02): `ParameterModel`, `OverloadModel`, `MethodModel`, `EnumModel`, `VariableModel`, `ConstantModel`, `TypeAliasModel`, `ClassModel`, `NamespaceModel`, `ProjectCatalog` — absence on even one makes loading v3.0+ IR files incompatible (`ValidationError` on unknown fields); run: `grep -c "extra=\"ignore\"" engine/ude/models.py` — must return ≥ 10 ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] ⚡ 🔴 Write test `test_variable_model_nonempty_round_trip` (CB-03 — Pydantic Guard Step 2b): create `ProjectCatalog` with `ClassModel(fields=[VariableModel(name="myField", fully_qualified_name="NS::C::myField", type="int")])`, serialize to JSON and back; verify `fields[0].name == "myField"` and `fields[0].type == "int"` — test verifies non-empty VariableModel round-trip, which is not covered by `test_old_ir_json_deserializes_without_error` (checks only empty defaults) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🔴 **[TASK-D.1.12]** After completing TASK-D.1.9 (refactoring `legacy.py`): execute Docomatic alignment re-baseline check — `poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short`; if `"total_differences"` increased for any language (C++, C#, Java) compared to pre-GAP-03 baseline — apply SOP `.antigravitycli/skills/difference_minimization_iterator.md` Step 5 until differences are restored; GAP-03 is not completed without explicit confirmation of zero delta in differences (CO-04) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Claude Code - Opus 3.8]
- [ ] ⚡ 🟡 When regenerating golden master on Windows, use the PowerShell command form (AW-02 — portability): `$env:UPDATE_GOLDEN = "1"; poetry run pytest engine/tests/test_golden_master.py -v` — Linux form `UPDATE_GOLDEN=1 poetry run pytest ...` does not work in PowerShell and is unsuitable for CI matrices with Windows runners ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-03] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Coverage checkpoint:**
```bash
poetry run pytest --cov=ude --cov-report=term-missing | grep TOTAL
# Expected: ≥ 98%
```

**Commit:** `feat(models): replace ClassEntity with 7 typed Pydantic models (GAP-03)`

---

### 3.2 GAP-10 — Documentation Coverage Gate `[REQ-V2-08]`

> **Prerequisite:** GAP-03 (typed IR) and GAP-01 (ude audit stub) completed.

**Tests (RED):**

- [ ] **[TST-3.21]** 🔴 **[Python]** Write test `test_full_coverage_catalog` — 100% documented entities yields coverage == 1.0 ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.22]** 🔴 **[Python]** Write test `test_zero_coverage_catalog` — 0% documented entities (docstrings = None) → coverage == 0.0 ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.23]** 🔴 **[Python]** Write test `test_mixed_coverage` — partial documentation (e.g. 3 of 4 methods → coverage == 0.75) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.24]** 🔴 **[Python]** Write test `test_reject_mode_exits_nonzero` — `ude audit` in `reject-undocumented` mode exits with code 2 when coverage is below threshold ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-3.25]** 🔴 **[Python]** Write test `test_allow_mode_exits_zero` — `ude audit` in `allow-undocumented` mode exits with code 0 even with 0% coverage ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] **[TST-3.26]** 🔴 **[Python]** Write test `test_audit_output_contains_table` — audit output contains formatted markdown table of coverage ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-3.27]** 🟡 **[Python]** Write test `test_coverage_gate_runs_on_compile` — coverage gate runs inside `ude compile` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-3.28]** 🟡 **[Python]** Write test `test_coverage_gate_absent_on_parse` — `ude parse` does not perform coverage audit ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-3.29]** 🟡 **[Python]** Write test `test_coverage_gate_absent_on_render` — `ude render` does not perform coverage audit ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-3.30]** 🟡 **[Python]** Verify presence of trace docstring annotations `Implements TASK-D` / `Implements GAP-` in all new Phase 3 modules using grep ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-3.31]** 🟡 **[Python]** Perform same check on Windows PowerShell (AW-08 check) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-3.32]** 🟡 **[Python]** Write test `test_phase3_modules_have_traceability_docstrings` — programmatic analysis of module AST for Implements annotations ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Implementation (GREEN):**

- [ ] ⚡ 🔴 Create `engine/ude/coverage.py` — models `EntityCoverage`, `CoverageReport`; function `compute_coverage(catalog: ProjectCatalog) -> CoverageReport` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Extend `GlobalConfig` in `config.py`: `coverage_mode` and `coverage_threshold` become active (were stubs in TASK-A.1.1) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Implement `ude audit` handler in `cli.py` — calls `orchestrator.parse()` + `compute_coverage()` + prints table + applies mode policy ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 In `UdeOrchestrator.run()`: after rendering, call `apply_coverage_gate(catalog, self._global_cfg)` — only for `ude compile` and `ude audit`, NOT for `ude parse` and `ude render` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Sonnet 3.6]
- [ ] ⚡ 🔴 Coverage gate active only on branch `main` in CI (conditional `if: github.ref == 'refs/heads/main'`) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-10] ──► [Model: Claude Code - Opus 3.8]

**Verification:**
```bash
poetry run pytest tests/test_coverage.py -v
# All PASSED
ude audit --doc-config path/to/ude_doc_config.json --mode allow-undocumented
# Prints coverage table; exit 0
ude audit --doc-config path/to/ude_doc_config.json --mode reject-undocumented --threshold 0.99
# Exit 2 if coverage < 99%
```

**Commit:** `feat(coverage): implement ude audit coverage gate (GAP-10)`

### 3.3 CI gate for GAP-10

- [ ] **[CI-4.3]** 🟡 After implementing GAP-10: add step in `generate-api-ref.yml`: ──► [Source: ToDo/CICD_ToDo.md #CI-4.3] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
  ```yaml
  - name: Documentation Coverage Audit Gate
    run: python -m ude audit --mode reject-undocumented --threshold 0.80
    if: github.ref == 'refs/heads/main'
  ```
- [ ] **[AD-QA-02]** 🟡 Adjust coverage gate threshold: ensure coverage ≥ 90% (default 0.80, then increase) ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-QA-02] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

---

## Section 4 — Phase 3 / Track F: QA and Testing

> **Parallel with Track D:** GAP-31 is completely independent of GAP-03 — can run in parallel. GAP-32 (tests using `EnumModel`, `VariableModel`, etc.) requires GAP-03; neutral infrastructure for GAP-32 (XML fixtures, base classes) allows parallel start.

### 4.1 GAP-31 — Validation of External Integration Scripts [REQ-V2-09]

**Testing and Verifying Existing Scripts:**

- [ ] **[TST-6.1]** 🔴 **[Python]** Run existing `python Tests/run_regression_tests.py` and verify all L1/L2/L3 tests pass for all 12 projects ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.2]** 🔴 **[Python]** Write test `test_run_regression_all_tiers_pass` — smoke test of running `run_regression_tests.py` via `subprocess` (exit code 0) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.3]** 🟡 **[Python]** Ensure `Tests/baseline/xml/` contains golden master Doxygen XML files for `facetmodeler` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-6.4]** 🟡 **[Python]** Write test `test_prepare_baseline_mock_suite` — running `prepare_baseline.py --suite mock` creates files in `baseline/ir/` and `baseline/html/` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.5]** 🔴 **[Python]** Write test `test_verify_pages_local_all_pages_found` — all MD files from `user-docs/docs/` are found in compiled dist → exit 0 ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.6]** 🔴 **[Python]** Write test `test_verify_pages_detects_missing_compiled_page` — one MD file is not compiled → exit 1 with error on stderr ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.7]** 🟡 **[Python]** Write test `test_verify_pages_remote_mode` — remote mode of `verify_pages.py` with mock HTTP (exit 0 on 200, exit 1 on 404) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.8]** 🟢 **[Python]** Clarify necessity of a separate script `verify_ude_links.py` to check internal UDE HTML links (discrepancy with REQ-V2-09) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.9]** 🔴 **[Python]** Write test `test_check_links_clean_site` — checking compiled directory with no broken links → exit 0 ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.10]** 🔴 **[Python]** Write test `test_check_links_detects_broken_internal_link` — broken internal link → exit 1 with filename ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.11]** 🟡 **[Python]** Write test `test_check_links_detects_broken_external_link` — broken external link (mock requests 404) → exit 1 ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.12]** 🟡 **[Python]** Write test `test_check_links_ude_prefix_strip` — correct link resolving with prefix `/ude-user-docs/api/` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Aggregator Script Development (with AW-05 protection):**

- [ ] **[TST-6.13]** 🔴 **[VB]** Create `Tests/run_all_integration_tests.bat` (Windows aggregator) using safe batch code checking %ERRORLEVEL% ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.14]** 🔴 **[VB]** Use `pushd`/`popd` to isolate directory traversal, preventing mutation of CWD on errors ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.15]** 🔴 **[VB]** Accept output directory path as argument `%1` with validation of existence (no hardcoding) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.16]** 🔴 **[VB]** Validate existence of all 3 child scripts before running, abort if missing ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-6.17]** 🟡 **[Python]** Create shell aggregator `Tests/run_all_integration_tests.sh` for CI (Linux) using `trap` for CWD and `$1` for paths ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-31] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

---

### 4.2 GAP-31 — Script Integration in CI

- [ ] **[AD-QA-04]** 🟡 Add step in `integration_tests.yml`: `Tests/check_links.py --site-dir ./user-docs/.vitepress/dist` ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-QA-04] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[AD-V2-04]** 🟡 Add step `python Tests/run_regression_tests.py` in `integration_tests.yml` as a separate stage after page verification ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-V2-04] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[AD-QA-05]** 🟢 Add `actions/upload-artifact@v4` for pytest coverage HTML report and `verify_pages.py` output — retention 7 days ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-QA-05] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

---

### 4.3 GAP-32 — Per-Language Integration Test Suites [REQ-V2-10]

> **Prerequisite (partial):** Tests using typed Pydantic models (`EnumModel`, `VariableModel`, `ConstantModel`) require GAP-03 completion. Without it, these tests are unimplemented — not just RED, but blocked API-wise. Infrastructure tasks (XML fixtures, `LanguageIntegrationBase`) allow parallel start with GAP-03.

**Basic Infrastructure Development:**

- [ ] **[TST-5.1]** 🔴 **[Python]** Add `LanguageIntegrationBase` mixin in `engine/tests/utils.py` with `LANGUAGE`, `XML_FIXTURE`, `RENDERER_CLASS` and `_run_pipeline()` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**C++ Specifics (GAP-32-A):**

- [ ] **[TST-5.2]** 🔴 **[Python]** Write test `test_cpp_category_landing_pages_exist` — existence of `Classes/index.html` with class table ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.3]** 🔴 **[Python]** Write test `test_cpp_overload_dispatcher_page` — dispatcher page creation for overloads (strict assert AW-04, no flat any) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.4]** 🔴 **[Python]** Write test `test_cpp_member_type_index_page` — existence of `Fields, Structures and Enums/index.html` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.5]** 🔴 **[Python]** Write test `test_cpp_template_class_rendering` — escaping angle brackets in templates like `MyClass<T, U>` in HTML ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.6]** 🔴 **[Python]** Write test `test_cpp_namespace_separator_double_colon` — double colon `::` separator in breadcrumbs and prototypes ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-5.7]** 🟡 **[C++]** Create XML fixture `engine/tests/assets/cpp_templates.xml` with templates, destructor, and overloaded constructors ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-5.8]** 🟡 **[Python]** Write test `test_cpp_destructor_rendering` — destructor rendering `~MyClass()` in output ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.9]** 🟡 **[Python]** Write test `test_cpp_global_functions_flat_rendered` — global functions rendered at sidebar root ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**C# Specifics (GAP-32-B):**

- [ ] **[TST-5.10]** 🔴 **[Python]** Write test `test_cs_interface_entity_rendering` — keyword `interface` displayed in prototype ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.11]** 🔴 **[Python]** Write test `test_cs_delegate_entity_rendering` — page creation for delegates ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.12]** 🔴 **[Python]** Write test `test_cs_event_member_rendering` — events (`event`) rendered in memberlist section ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.13]** 🔴 **[Python]** Write test `test_cs_namespace_index_page` — creation of `<Namespace>/index.html` with class table ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.14]** 🔴 **[Python]** Write test `test_cs_dot_separator_in_fqn` — `.` instead of `::` separator for C# ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-5.15]** 🟡 **[C#]** Create XML fixture `engine/tests/assets/cs_interface.xml` with interfaces and events ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-5.16]** 🟡 **[Python]** Write test `test_cs_property_getter_setter_rendering` — getter/setter accessor rendering for properties ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.17]** 🟡 **[Python]** Write test `test_cs_indexer_rendering` — indexers `this[int index]` displayed in members section ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Java Specifics (GAP-32-C):**

- [ ] **[TST-5.18]** 🔴 **[Python]** Write test `test_java_extends_implements_in_prototype` — base classes/interfaces displayed in prototype ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.19]** 🔴 **[Python]** Write test `test_java_package_index_page` — creation of package `index.html` with class table ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.20]** 🔴 **[Python]** Write test `test_java_interface_rendering` — correct Java interface rendering ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.21]** 🔴 **[Python]** Write test `test_java_annotation_type_rendering` — annotation (`@interface`) rendering in Java ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.22]** 🔴 **[Python]** Write test `test_java_dot_separator_in_fqn` — `.` separator for Java paths ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-5.23]** 🟡 **[Java]** Create XML fixture `engine/tests/assets/java_inheritance.xml` with inheritance and implementation links ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-5.24]** 🟡 **[Python]** Write test `test_java_enum_rendering` — rendering Java enum constants via EnumModel ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.25]** 🟢 **[Python]** Write test `test_java_nested_class_rendering` — nested classes (`OuterClass.InnerClass`) in sidebar ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Python Specifics (GAP-32-D):**

- [ ] **[TST-5.26]** 🔴 **[Python]** Write test `test_py_fget_fset_property_rendering` — displaying accessors `[get]`/`[set]` for Python properties ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.27]** 🔴 **[Python]** Write test `test_py_dunder_methods_present` — `__init__`, `__repr__`, `__eq__` methods not filtered out as private ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.28]** 🔴 **[Python]** Write test `test_py_swig_wrapper_fields_excluded` — SWIG fields (`swigCPtr`, `Dispose()`) filtered out ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.29]** 🔴 **[Python]** Write test `test_py_sphinx_rst_docstring_normalized` — Sphinx/RST parameters (`:param`, `:type`) converted to CommonMark ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.30]** 🔴 **[Python]** Write test `test_py_dot_separator_in_fqn` — `.` separator for Python paths ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-5.31]** 🟡 **[Python]** Create XML fixture `engine/tests/assets/py_swig.xml` with SWIG wrappers and properties ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-5.32]** 🟡 **[Python]** Write test `test_py_class_variable_vs_instance_variable` — separating class and instance variables in output ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-5.33]** 🟢 **[Python]** Write test `test_py_module_level_functions` — rendering module-level functions ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

---

### 4.4 Per-Language CI Matrix

- [ ] **[AD-LANG-01]** 🟡 After implementing GAP-32: add job `integration-tests-per-language` in `integration_tests.yml` with `matrix: language: [cpp, cs, java, py]` ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-LANG-01] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[AD-LANG-02]** 🟡 `continue-on-error: false` for the language matrix ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-LANG-02] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[AD-LANG-03]** 🟢 Artifact with per-language test reports ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-LANG-03] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

---

### 4.5 Entity Completeness and Page Structure Tests

**Doc-o-matic Alignment Check:**

- [ ] **[TST-4.1]** 🔴 **[Python]** Rerun `test_docomatic_alignment.py` and record `total_differences` for each language as the new baseline ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-4.2]** 🔴 **[Python]** Write test `test_total_differences_not_increased_cpp` — C++ differences do not exceed baseline after renderer changes ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.3]** 🔴 **[Python]** Write test `test_total_differences_not_increased_cs` — C# differences do not exceed baseline ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.4]** 🔴 **[Python]** Write test `test_total_differences_not_increased_java` — Java differences do not exceed baseline ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.5]** 🟡 **[Python]** Write test `test_no_silent_entity_loss_cpp` — number of classes in UDE ≥ number in Docomatic baseline for C++ ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-4.6]** 🟡 **[Python]** Write test `test_no_silent_entity_loss_cs` — similar verification for C# ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.7]** 🟡 **[Python]** Write test `test_no_silent_entity_loss_java` — similar verification for Java ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Quantitative Entity Completeness Verification:**

- [ ] **[TST-4.8]** 🔴 **[Python]** Write test `test_all_methods_present_after_aggregation_cpp` — number of methods in IR = number of methods on class HTML pages (lxml parsing of `<h3>`, `<section>`) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-4.9]** 🔴 **[Python]** Write test `test_all_methods_present_after_aggregation_cs` — similar check for C# ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.10]** 🔴 **[Python]** Write test `test_all_methods_present_after_aggregation_java` — similar check for Java ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.11]** 🔴 **[Python]** Write test `test_no_orphan_entities_cpp` — for every method in IR, an anchor link `<a id="...">` exists in class HTML file ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.12]** 🔴 **[Python]** Write test `test_no_orphan_entities_cs` — similar check for C# ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.13]** 🔴 **[Python]** Write test `test_no_orphan_entities_java` — similar check for Java ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.14]** 🟡 **[Python]** Write test `test_class_member_count_matches_toc_cpp` — number of class members in sidebar ToC matches number in IR ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.15]** 🟡 **[Python]** Write test `test_class_member_count_matches_toc_cs` — similar check for C# ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.16]** 🟡 **[Python]** Write test `test_class_member_count_matches_toc_java` — similar check for Java ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.17]** 🟡 **[Python]** Write test `test_overloaded_methods_all_present` — all overloads are presented on overload dispatcher page or inline ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.18]** 🟡 **[Python]** Write test `test_inherited_members_not_silently_dropped` — inherited class members are not lost in UDE output ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.19]** 🟢 **[Python]** Write test `test_static_vs_instance_segregation` — correctness of separating static and instance members ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Page Structural Integrity:**

- [ ] **[TST-4.20]** 🔴 **[Python]** Write test `test_class_page_has_method_section` — each class with methods contains an HTML methods section ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.21]** 🔴 **[Python]** Write test `test_class_page_has_fields_section_when_fields_exist` — presence of Fields section if fields exist in IR ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.22]** 🔴 **[Python]** Write test `test_namespace_index_lists_all_classes` — namespace index contains links to all its classes ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.23]** 🟡 **[Python]** Write test `test_sidebar_links_resolve_to_existing_files` — links in sidebar point to real generated files ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.24]** 🟡 **[Python]** Write test `test_breadcrumbs_contain_correct_namespace` — breadcrumbs show correct namespace path ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-4.25]** 🟡 **[Python]** Write test `test_entity_titles_follow_convention` — titles follow `<EntityID> <EntityType>` format ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

---

### 4.6 Performance, Load, and Regression Tests

**Performance Benchmarking:**

- [ ] **[TST-7.1]** 🟡 **[Python]** Ensure benchmark tests 1000 classes in time ≤ 5 s ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.2]** 🟡 **[Python]** Add load test separated by language (250 classes * 4 languages = 1000) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.3]** 🟡 **[Python]** Write test `test_benchmark_with_l2_cache_second_run` — second run with L2 cache is > 3x faster than the first ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.4]** 🟢 **[Python]** Write test `test_benchmark_large_class_many_methods` — correct handling of class with 200+ methods without truncation ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Golden Master Regression Test:**

- [ ] **[TST-7.5]** 🔴 **[Python]** After GAP-03, update baselines for Golden Master (accommodating both Linux and Windows PowerShell forms - AW-02) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Claude Code - Opus 3.8]
- [ ] **[TST-7.6]** 🔴 **[Python]** Verify successful execution of `test_golden_master.py` after regeneration ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-7.7]** 🔴 **[Python]** Ensure golden master covers all 16 configurations (4 languages * 2 outputs * 2 options) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.8]** 🟡 **[Python]** Add test `test_golden_master_html_legacy_cpp` (LegacyHtmlRenderer C++ vs baseline) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-7.9]** 🟡 **[Python]** Add test `test_golden_master_hugo_legacy_java` (LegacyHugoMarkdownRenderer Java vs baseline) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-7.10]** 🟡 **[Python]** Verify completeness of PIPELINE_COMPLEXES (contains all 16 combinations) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Reverse-Engineering Doc-o-matic:**

- [ ] **[TST-7.11]** 🟡 **[Python]** Verify existence of `Tests/docomatic_scraper.py` (or write according to SOP `skills/docomatic_semantics_analysis.md`) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-7.12]** 🟡 **[Python]** Write test `test_scraper_dry_run_output_valid_json` — JSON contains entity_types and filename_prefixes ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.13]** 🟡 **[Python]** Write test `test_scraper_detects_cpp_overload_patterns` — parsing of `!!OVERLOADED_` patterns ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.14]** 🟢 **[Python]** Write test `test_scraper_optionality_threshold` — marking entities as OPTIONAL when presence < 50% ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

**Language Edge Cases:**

- [ ] **[TST-7.15]** 🟡 **[Python]** Write test `test_cpp_nested_templates_parsing` — escaping of nested templates like `map<string, vector<...>>` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.16]** 🟡 **[Python]** Write test `test_cpp_anonymous_namespace_handling` — anonymous namespaces do not raise KeyError ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.17]** 🟡 **[Python]** Write test `test_cpp_export_macro_filtered` — export macros (`ODA_EXPORT`) stripped from signatures ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.18]** 🟡 **[Python]** Write test `test_cpp_constructor_destructor_ordering` — constructor and destructor ordered first in lists ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.19]** 🟡 **[C++]** Create XML fixture `engine/tests/assets/cpp_edge_cases.xml` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-7.20]** 🟡 **[Python]** Write test `test_cs_generic_type_rendering` — generic rendering `Dictionary<TKey, TValue>` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.21]** 🟡 **[Python]** Write test `test_cs_extension_method_rendering` — C# extension method detection ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.22]** 🟡 **[Python]** Write test `test_cs_nullable_type_rendering` — nullable types rendering `int?`, `string?` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.23]** 🟡 **[C#]** Create XML fixture `engine/tests/assets/cs_edge_cases.xml` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-7.24]** 🟡 **[Python]** Write test `test_java_generics_rendering` — wildcard generics rendering `Collection<? extends T>` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.25]** 🟡 **[Python]** Write test `test_java_varargs_rendering` — Java varargs rendering `String... args` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.26]** 🟡 **[Java]** Create XML fixture `engine/tests/assets/java_edge_cases.xml` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-7.27]** 🟡 **[Python]** Write test `test_legacy_html_output_matches_docomatic_naming` (names like `!!MEMBERTYPE_Methods_ClassName`) ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-7.28]** 🟡 **[Python]** Write test `test_legacy_hugo_sidebar_matches_html_sidebar` ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-7.29]** 🟡 **[Delphi]** Create utility `Tests/generate_docomatic_baseline.dpr` to reproduce Docomatic naming ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] **[TST-7.30]** 🟢 **[VB]** Write `Tests/generate_legacy_toc.vbs` to create contents.html tree ──► [Source: .antigravitycli/v2_execution_plan.md #GAP-32] ──► [Model: Antigravity - Gemini 3.1 Pro (High)]

---

## Section 5 — CI/CD and Deployment Infrastructure

> Parallel track with Phases 1–3. Does not block engine development, but must be completed before release v2.0.

### 5.1 Phase 1 CI/CD: Security and Credentials

- [ ] **[CI-1.1]** 🔴 Install and authenticate Wrangler CLI: `npm install -g wrangler && wrangler login` ──► [Source: ToDo/CICD_ToDo.md #CI-1.1] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[CI-1.2]** 🔴 Create 3 Cloudflare Pages projects: `ude-design-docs`, `ude-user-docs`, `ude-api-ref` ──► [Source: ToDo/CICD_ToDo.md #CI-1.2] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[CI-1.3]** 🔴 Configure Cloudflare Zero Trust Access for `ude-design-docs` — whitelist policy ──► [Source: ToDo/CICD_ToDo.md #CI-1.3] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-1.4]** 🔴 Create Cloudflare API Token with minimal rights (Pages: Edit, Zone: Read) ──► [Source: ToDo/CICD_ToDo.md #CI-1.4] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[CI-1.5]** 🔴 Register GitHub Secrets in all repositories: `CF_API_TOKEN`, `CF_ACCOUNT_ID` ──► [Source: ToDo/CICD_ToDo.md #CI-1.5] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[CI-1.6]** 🔴 Generate SSH Deploy Key for submodule engine; add to GitHub Secrets as `PIPELINE_DEPLOY_KEY` ──► [Source: ToDo/CICD_ToDo.md #CI-1.6] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[AD-SEC-04]** 🔴 Add `permissions:` block with least privilege to all workflows ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-SEC-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[AD-SEC-05]** 🟡 Enable Dependabot for GitHub Actions: `.github/dependabot.yml` ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-SEC-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-SEC-06]** 🟡 Enable GitHub Secret Scanning and Push Protection for all repositories ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-SEC-06] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-ISO-03]** 🔴 Remove step creating symlink `ln -s ../engine ./user-docs/engine` — replace with PYTHONPATH or sys.path in `ude_config_self.json` ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-ISO-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]

### 5.2 Phase 2 CI/CD: Basic GitHub Actions Workflows

- [ ] **[CI-2.1]** 🔴 Create `ude-design-docs/.github/workflows/deploy-design-docs.yml` — Docusaurus → Cloudflare Pages ──► [Source: ToDo/CICD_ToDo.md #CI-2.1] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[CI-2.2]** 🔴 Create `ude-user-docs/.github/workflows/deploy-user-docs.yml` — VitePress → Cloudflare Pages ──► [Source: ToDo/CICD_ToDo.md #CI-2.2] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[CI-2.3]** 🔴 Create `engine/.github/workflows/generate-api-ref.yml` — UDE compile → Cloudflare Pages ──► [Source: ToDo/CICD_ToDo.md #CI-2.3] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]

### 5.3 Phase 3 CI/CD: Caching and Performance

- [ ] **[CI-3.1]** 🟡 Cache npm (`actions/setup-node@v4` with `cache: 'npm'`) in Pipeline #1 and #2 ──► [Source: ToDo/CICD_ToDo.md #CI-3.1] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-3.2]** 🟡 Cache pip (`actions/cache@v4`) in Pipeline #3 ──► [Source: ToDo/CICD_ToDo.md #CI-3.2] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-3.3]** 🟢 Cache Docusaurus build cache (`.docusaurus`, `node_modules/.cache`) in Pipeline #1 ──► [Source: ToDo/CICD_ToDo.md #CI-3.3] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 5.4 Phase 4 CI/CD: Quality Gates

- [ ] **[CI-4.1]** 🔴 Add pytest + coverage gate to `generate-api-ref.yml`: `--cov-fail-under=98`; upload artifact with 14-day retention ──► [Source: ToDo/CICD_ToDo.md #CI-4.1] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[CI-4.2]** 🟡 Create `scripts/pydantic_guard.sh`; add Pydantic Migration Guard step to CI — blocks `dict` patterns in place of Pydantic models ──► [Source: ToDo/CICD_ToDo.md #CI-4.2] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[AD-QA-01]** 🟡 Add job `engine-tests` in `integration_tests.yml`: `pytest engine/tests/ --cov=ude --cov-report=term-missing`; TOTAL ≥ 98% ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-QA-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-QA-03]** 🟢 Add `markdownlint-cli2` step for `user-docs/docs/**/*.md` ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-QA-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-4.5]** 🟡 Add step executing integration tests: all 4 languages `test_integration_*.py` ──► [Source: ToDo/CICD_ToDo.md #CI-4.5] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 5.4.1 Test Automation in CI/CD (Quality Gates)

- [ ] **[TST-8.1]** 🔴 **[Python]** Add job `engine-tests` to `integration_tests.yml` (pass pytest with cover-fail-under=98) ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[TST-8.2]** 🟡 **[Python]** Add CI step for per-language integration: `pytest tests/test_integration_*.py` ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-8.3]** 🟡 **[Python]** Add CI step for Docomatic alignment: `pytest engine/tests/test_docomatic_alignment.py` ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-8.4]** 🟡 **[Python]** Add CI step for Entity Completeness: `pytest engine/tests/test_entity_completeness.py` ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-8.5]** 🟢 **[Python]** Configure upload of coverage HTML report artifact to GHA on failure (retention 7 days) ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-8.6]** 🟢 **[Python]** Configure upload of alignment suite JSON difference reports on failure ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TST-8.7]** 🔴 **[Python]** Create `scripts/pydantic_guard.ps1` to block key access to fields in renderers (for Windows) ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-8.8]** 🟡 **[Python]** Create `scripts/pydantic_guard.sh` — same script for Linux (CI runner) ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[TST-8.9]** 🟡 **[Python]** Add step executing `pydantic_guard.sh` in `generate-api-ref.yml` after GAP-03 ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[AD-RENDERER-01]** 🔴 Introduce CI requirement (Gate): `generate-api-ref.yml` MUST contain the Renderer Factory Guard (CB-04) step checking `__new__` signature ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-RENDERER-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[AD-RENDERER-02]** 🔴 Renderer Factory Guard (CB-04) step does NOT have `continue-on-error: true` — it is always blocking ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-RENDERER-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 5.5 Phase 5 CI/CD: Environment Isolation and Branch Protection

- [ ] **[CI-5.1]** 🟡 Add Preview Deployments for Pull Requests (branch deploy, PR comment with preview URL) ──► [Source: ToDo/CICD_ToDo.md #CI-5.1] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-5.2]** 🟡 Configure Branch Protection Rules for branch `main` in all repositories ──► [Source: ToDo/CICD_ToDo.md #CI-5.2] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-5.3]** 🟢 Create GitHub Environment `production` with required reviewers ──► [Source: ToDo/CICD_ToDo.md #CI-5.3] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 5.6 Phase 6 CI/CD: Monitoring and Documentation

- [ ] **[CI-6.1]** 🟢 Add build status badges to `README.md` of all repositories ──► [Source: ToDo/CICD_ToDo.md #CI-6.1] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-6.2]** 🟢 Add `$GITHUB_STEP_SUMMARY` step to each workflow ──► [Source: ToDo/CICD_ToDo.md #CI-6.2] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-6.3]** 🟢 Retention policy for artifacts — upload UDE output on failure, retention 3 days ──► [Source: ToDo/CICD_ToDo.md #CI-6.3] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CI-6.4]** 🟢 Create `RUNBOOK.md` in root umbrella: manual run, rollback, token rotation, troubleshooting ──► [Source: ToDo/CICD_ToDo.md #CI-6.4] ──► [Model: Antigravity - Gemini 3.5 Flash (High)]
- [ ] **[AD-MON-02]** 🟡 Add `timeout-minutes: 15` on job level ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-MON-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-MON-04]** 🟢 Step printing summary to `$GITHUB_STEP_SUMMARY`: pages, UDE time, verify_pages result ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-MON-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-MON-01]** 🟡 Configure GitHub Actions notification for failures on master branch: email notification via standard GitHub settings or Slack webhook ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-MON-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-MON-03]** 🟢 Add `if: always()` for final step (cleanup / report) — executes even on failure of previous steps ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-MON-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 5.7 New Workflows v2.0

- [ ] **[AD-V2-01]** 🟢 Create `.github/workflows/coverage-gate.yml` — `workflow_dispatch` + `ude audit --mode reject-undocumented` → GitHub Check ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-V2-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-V2-02]** 🟢 Create `.github/workflows/regression.yml` — cron `0 3 * * 0` (weekly), `LoadTest/run_load_test.py` ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-V2-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-V2-03]** 🟢 Create `CODEOWNERS` in `.github/`: `engine/**` and `.antigravitycli/**` → @pavel.sokolov ──► [Source: ToDo/ActivitiesReqs_ToDo.md #AD-V2-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

---

## Section 6 — User Documentation

> Executed in parallel with implementation phases. Priority tasks before release v2.0.

### 6.1 Structural Corrections of user-docs

- [ ] **[STRUCT-01]** 🔴 Create subdirectories in `user-docs/docs/`: `quickstart/`, `standards/`, `reference/`, `deployment/`, `case-study/` ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[STRUCT-02]** 🔴 Move `getting-started.md` and `first-config.md` → `docs/quickstart/` ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[STRUCT-03]** 🔴 Create `docs/quickstart/index.md` — Chapter 1 table of contents ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[STRUCT-04]** 🔴 Move `commenting-rules.md` and `exclusion-gates.md` → `docs/standards/` ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[STRUCT-05]** 🔴 Create `docs/standards/index.md` — Chapter 2 table of contents ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[STRUCT-06]** 🔴 Move `global-settings.md` and `target-settings.md` → `docs/reference/` ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-06] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[STRUCT-07]** 🔴 Create `docs/reference/index.md` — Chapter 3 table of contents ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-07] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[STRUCT-08]** 🔴 Create `docs/deployment/` and move `admin-deployment.md` there ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-08] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[STRUCT-09]** 🔴 Clarify status of `case-study.md` vs `chapter4-case-study.md` — delete duplicate or merge ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-09] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[STRUCT-10]** 🔴 Update VitePress sidebar (`docs/.vitepress/config.ts`) for new hierarchy ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-10] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[STRUCT-11]** 🔴 Check and update all relative links after moving files ──► [Source: ToDo/UserDocs_ToDo.md #STRUCT-11] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 6.2 Fixes in admin-deployment.md

- [ ] **[ADMIN-01]** 🔴 Remove link to non-existent `deploy.yml` in umbrella ──► [Source: ToDo/UserDocs_ToDo.md #ADMIN-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] **[ADMIN-02]** 🔴 Explain: deployment is executed by workflow of each submodule independently ──► [Source: ToDo/UserDocs_ToDo.md #ADMIN-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[ADMIN-03]** 🔴 Add current steps from `integration_tests.yml` ──► [Source: ToDo/UserDocs_ToDo.md #ADMIN-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[ADMIN-04]** 🔴 Secrets table: `PIPELINE_GITHUB_TOKEN` — purpose, minimal permissions ──► [Source: ToDo/UserDocs_ToDo.md #ADMIN-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[ADMIN-05]** 🟡 Describe symlink `user-docs/engine → ../engine` and why it is needed only in CI ──► [Source: ToDo/UserDocs_ToDo.md #ADMIN-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 6.3 CI/CD Documentation in user-docs

- [ ] **[CICD-01]** 🔴 Create `docs/deployment/cicd-pipelines.md` — overview of three pipelines ──► [Source: ToDo/UserDocs_ToDo.md #CICD-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CICD-05]** 🔴 Create `docs/deployment/repository-dispatch.md` — cross-repo events mechanism ──► [Source: ToDo/UserDocs_ToDo.md #CICD-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[CICD-07]** 🟡 Mermaid diagram: submodule push → repository_dispatch → umbrella CI → verify ──► [Source: ToDo/UserDocs_ToDo.md #CICD-07] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 6.4 New Sections v2.0

- [ ] **[MIG-01]** 🟡 Create `docs/reference/migration-v2.md` — Breaking Changes v1.0 → v2.0 ──► [Source: ToDo/UserDocs_ToDo.md #MIG-01] ──► [Model: Antigravity - Gemini 3.5 Flash (High)]
- [ ] **[MIG-02]** 🟡 Document: `ClassEntity` → 7 typed Pydantic models ──► [Source: ToDo/UserDocs_ToDo.md #MIG-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[MIG-03]** 🟡 Document: `ProjectCatalog` — new fields `project_name`, `version` ──► [Source: ToDo/UserDocs_ToDo.md #MIG-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[MIG-04]** 🟡 Document: CLI subcommands (backward compat preserved) ──► [Source: ToDo/UserDocs_ToDo.md #MIG-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[MIG-06]** 🟡 Document: `fields: List[str]` → `fields: List[VariableModel]` ──► [Source: ToDo/UserDocs_ToDo.md #MIG-06] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[MIG-07]** 🟡 Checklist for users migrating to v2.0 ──► [Source: ToDo/UserDocs_ToDo.md #MIG-07] ──► [Model: Antigravity - Gemini 3.5 Flash (High)]
- [ ] **[CLOG-01]** 🟡 Create `docs/changelog.md` — v1.0 and v2.0 logs ──► [Source: ToDo/UserDocs_ToDo.md #CLOG-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[TRB-01]** 🟢 Create `docs/quickstart/troubleshooting.md` — 7 typical errors with solutions ──► [Source: ToDo/UserDocs_ToDo.md #TRB-01] ──► [Model: Antigravity - Gemini 3.5 Flash (High)]
- [ ] **[AUDIT-01]** 🟡 Document `GlobalConfig.coverage_mode` and `coverage_threshold` ──► [Source: ToDo/UserDocs_ToDo.md #AUDIT-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AUDIT-02]** 🟡 Document `ude audit` coverage table format ──► [Source: ToDo/UserDocs_ToDo.md #AUDIT-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AUDIT-04]** 🟡 Example of integrating `ude audit` into a GitHub Actions step ──► [Source: ToDo/UserDocs_ToDo.md #AUDIT-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 6.5 Portfolio/Showcase Improvements

- [ ] **[PORT-01]** 🟢 Update landing `index.md`: key metrics (`<5s`, `98%`, `4 languages`, `12 projects`) ──► [Source: ToDo/UserDocs_ToDo.md #PORT-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[PORT-02]** 🟢 Add badges: GitHub Actions status, Python version, coverage ──► [Source: ToDo/UserDocs_ToDo.md #PORT-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[PORT-03]** 🟢 Mermaid diagram of architecture: Collector → Parser → Renderer ──► [Source: ToDo/UserDocs_ToDo.md #PORT-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

---

## Section 7 — Pipeline and CI/CD Documentation

### 7.1 Mandatory Documents (🔴 Urgent)

- [ ] **[AD-DOC-01]** 🔴 Create `docs/deployment/repository-dispatch.md` — cross-repo triggers mechanism ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-02]** 🔴 Create `docs/deployment/secrets.md` — `PIPELINE_GITHUB_TOKEN`: PAT type, permissions, 90-day rotation ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-03]** 🔴 Create `docs/deployment/cicd-pipelines.md` — matrix of 4 pipelines (design-docs, user-docs, engine, umbrella) ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-05]** 🔴 Document GitHub Checks: job `run-tests`, expected time ~3–5 min, failure playbook ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-06]** 🔴 Document `Tests/verify_pages.py`: arguments, what it checks, how to read errors ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-06] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 7.2 Important Documents (🟡 v2.0)

- [ ] **[AD-DOC-04]** 🟡 Document symlink `user-docs/engine`: why only in CI, why not needed on Windows ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-04] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-07]** 🟡 Mermaid diagram in `admin-deployment.md` — complete CI/CD flow ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-07] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-08]** 🟡 Create `.github/AGENTS.md` — description of each workflow, expected checks, failure playbook ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-08] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 7.3 Annotating Workflow Code

- [ ] **[AD-DOC-09]** 🟢 Add WHY-comments in `integration_tests.yml` — for non-trivial steps ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-09] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-10]** 🟢 Document `PYTHONPATH: engine` — why it is needed, when it requires updating ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-10] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-11]** 🟡 Document CI guard scripts in `admin-deployment.md` or dedicated section in `cicd-pipelines.md` ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-11] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[AD-DOC-12]** 🟡 Document CI step order in `generate-api-ref.yml` and rationale (WHY): Pydantic Guard → Renderer Factory Guard → Traceability Check → Compile ──► [Source: ToDo/ActivitiesDoc_ToDo.md #AD-DOC-12] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

---

## Section 8 — Documentation Quality Requirements

> ⚠️ Tasks marked 🔴 are active **from the start of work**. The most critical are duplicated in Section 0.3.

### 8.1 Markdown and Syntax Requirements

- [ ] **[DR-NEW-01]** 🔴 Establish requirement: all MD files must pass `markdownlint-cli2` in CI ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-01] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-02]** 🟡 markdownlint configuration: max 120 characters, `MD013` applied only to prose ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-02] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-03]** 🟡 Rule: in design-docs all files begin with YAML front-matter (`sidebar_position`, `title`) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-03] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-05]** 🟡 Rule: exactly one H1, first element, matching `title` in front-matter ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-05] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-06]** 🔴 Establish rule for Mermaid diagrams: each diagram contains a `%% Description` comment and a title node for accessibility ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-06] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 8.2 Automatic Link Checking

- [ ] **[DR-NEW-07]** 🔴 `Tests/check_links.py` (GAP-31) must be implemented before v2.0 release ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-07] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[DR-NEW-08]** 🟡 After GAP-31: `check_links.py` runs in `integration_tests.yml` as a separate step ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-08] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[DR-NEW-09]** 🟡 Check relative links in design-docs via `docusaurus-check-links` or similar ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-09] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-10]** 🔴 Establish rule: external links (HTTPS) are allowed only in `admin-deployment.md` and `getting-started.md`; in design-docs external links require a review comment with justification ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-10] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-11]** 🔴 Establish requirement: links to internal GitHub Pages (`Sir-Derryk.github.io`) in user-docs are verified by page-existence test (`verify_pages.py`) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-11] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 8.3 Versioning and Archiving

- [ ] **[DR-NEW-12]** 🟡 Before merging v2.0: create versioned snapshot in Docusaurus (`docusaurus docs:version 1.0`) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-12] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-13]** 🟡 Establish rule: in design-docs, `roadmap/future_v2.md` sections are moved to `roadmap/mvp_v2/` as they are implemented, not edited in place ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-13] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-14]** 🟡 Document versioning procedure in `CLAUDE.md` ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-14] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-15]** 🟡 After freezing v2.0: `requirements_v2_next.md` → `requirements_v3_next.md` ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-15] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 8.4 Traceability and Consistency

- [ ] **[DR-NEW-16]** 🟡 Each ⚠️-GAP in `integration_tests_specification.md` receives a `Resolution Target` field ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-16] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-17]** 🟡 Glossary of terms: `Collector`, `Orchestrator`, `Parser`, `Renderer`, `IR`, `Catalog` — uniform usage ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-17] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-18]** 🟢 Create Glossary page in design-docs (15+ terms) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-18] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-19]** 🟡 When removing a requirement — log in `quality_audit.md` with justification ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-19] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 8.5 Security and Docs Infrastructure Requirements

- [ ] **[DR-NEW-22]** 🔴 Document all used secrets in a separate file `docs/deployment/secrets.md` (user-docs) or `CLAUDE.md`: name, purpose, minimal permissions, rotation period ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-22] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-23]** 🔴 Establish requirement: `PIPELINE_GITHUB_TOKEN` secret must use a **Fine-grained Personal Access Token** (not classic), restricted by repository and permissions: `contents: read`, `actions: write` (for repository_dispatch) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-23] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-24]** 🔴 Establish rule: all environment variables in workflows are explicitly declared via `env:` at job or step level — not passed via undocumented inline shell substitution ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-24] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-25]** 🔴 Establish requirement: README or AGENTS.md in `.github/` describes the purpose of each workflow, its triggers, and expected Check statuses in the GitHub UI ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-25] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-26]** 🟡 Introduce formal deprecation procedure: files marked for deletion get frontmatter `deprecated: true` and section `> ⚠️ DEPRECATED:` specifying the replacement — not deleted immediately ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-26] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-27]** 🟡 Archive `brd/ude_portal_blueprint.md` — marked as obsolete legacy in design-docs; move to `design-docs/docs/_archive/` ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-27] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-28]** 🟢 Establish rule: on each major release, create a GitHub Release with release notes duplicating `changelog.md` from user-docs for portfolio visibility ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-28] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 8.6 Quality Gates for Documentation

- [ ] **[DR-NEW-29]** 🔴 Introduce CI step in `design-docs` workflow: Docusaurus build (`npm run build`) must terminate with exit 0 — warnings are treated as errors in the presence of broken links (flag `--fail-on-warning` for broken links) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-29] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-30]** 🟡 Introduce CI step: check that all files in `design-docs/docs/` have correct `sidebar_position` (numerical, unique in directory) — Python script or `remark-lint` ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-30] ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] **[DR-NEW-31]** 🟡 Establish rule: `v2_detailed_tasks.md` (2,364 lines) must be split into separate files in `tasks/` after freezing v2.0 — maximum size of documented file: 500 lines ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-31] ──► [Model: Antigravity - Gemini 3.5 Flash (High)]
- [ ] **[DR-NEW-32]** 🔴 Establish requirement: user-docs pages describing CLI commands are tested in CI by smoke test — command `python -m ude.cli --help` must return exit 0 and contain key flags from documentation ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-32] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 8.7 Documenting Architectural Decisions Requirements (Cross-Phase)

- [ ] **[DR-NEW-33]** 🟡 Establish requirement: TASK-A.1.1 (`GlobalConfig`) MUST contain a note that `coverage_mode` and `coverage_threshold` fields are **schema stubs for Phase 1** ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-33] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-34]** 🟡 Establish requirement: TASK-A.4.3 (`DoxygenXmlCollector` with 3-tier merge) must document **Doxyfile template resolution priority**: `GlobalConfig.global_templates_dir` → `templates` → `{}` ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-34] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-35]** 🟡 Establish requirement: tasks TASK-D.1.4 (C#), TASK-D.1.5 (Java), TASK-D.1.6 (Python) must contain **specific code examples** with language-specific XML kind mappings of Doxygen ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-35] ──► [Model: Antigravity - Gemini 3.5 Flash (High)]
- [ ] **[DR-NEW-36]** 🟡 Establish requirement: resolve ambiguity in TASK-F.2.5 (Python integration tests) regarding `is_property`, `fget`, `fset` fields in `VariableModel` / `MethodModel` ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-36] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-37]** 🟡 Establish requirement: each task file `TASK-*.md` in `.antigravitycli/tasks/` when specifying CLI verification commands MUST provide both forms — bash/sh and PowerShell (AW-02) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-37] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-38]** 🟡 Establish requirement: all verification commands in `TASK-*.md` using directory comparison MUST use `filecmp.dircmp` or Python script `scripts/compare_dirs.py`, not `diff -r` (AW-03) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-38] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-39]** 🟡 Establish requirement: `sidebar.toml` configuration is documented as a separate reference section (section structure, 3-way deep_merge cascade, `_load_sidebar_toml_graceful()` on missing) ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-39] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] **[DR-NEW-40]** 🟡 Establish requirement: `_load_static_file_from_path()` method on `BaseRenderer` is documented in the Renderer API reference ──► [Source: ToDo/DocReqs_ToDo.md #DR-NEW-40] ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

---

## Section 9 — Finalization and Release v2.0

### 9.1 Final Quality Checks

- [ ] 🔴 Full test suite run: `poetry run pytest engine/tests/ -v` — 0 failed ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🔴 Coverage gate: `poetry run pytest --cov=ude --cov-report=term-missing` — TOTAL ≥ 98% ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🔴 Performance benchmark: `poetry run pytest tests/test_performance_benchmark.py` — ≤ 5s ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🔴 v1.0 backward compat smoke test: `ude --doc-config path/to/ude_doc_config.json` works identically ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] 🔴 IR compatibility: `load_compressed_ir(v1_file)` does not raise exceptions ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]
- [ ] 🔴 Git hygiene: `git status --short` — no compiled `*.html`, `*.md` output files ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🟡 `ude parse | ude render` output byte-identical to `ude compile` ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]

### 9.2 Regression Tests

- [ ] 🔴 Run `Tests/run_all_integration_tests.sh` (GAP-31) — exit 0 ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] 🔴 Run golden master: `poetry run pytest tests/test_golden_master.py -v` — all PASSED ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] 🔴 Run Docomatic alignment: `poetry run pytest tests/test_docomatic_alignment.py -v` — `"total_differences"` not above pre-v2.0 baseline ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] 🟡 Run per-language integration: all 4 files `test_integration_*.py` — ≥ 20 tests PASSED ──► [Model: Antigravity - Gemini 3.1 Pro (Low)]

### 9.3 CI/CD Verification

- [ ] 🔴 Verify successful run of `integration_tests.yml` on master after all changes ──► [Model: Antigravity - Gemini 3.1 Pro (High)]
- [ ] 🔴 Verify pipeline #3 (`generate-api-ref.yml`) — coverage gate is active and passes ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🟡 Preview deployment in a PR — ensure preview URL is accessible ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]

### 9.4 Release Documentation

- [ ] 🔴 Complete `docs/changelog.md` with v2.0 entries (Breaking Changes + new features) ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] 🔴 Complete `docs/reference/migration-v2.md` — full user checklist ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🟡 Create versioned snapshot in Docusaurus: `docusaurus docs:version 1.0` ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🟡 Rename `requirements_v2_next.md` → `requirements_v3_next.md` in `.antigravitycli/` ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🟢 Create GitHub Release with release notes duplicating `changelog.md` ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]

### 9.5 Post-Finalization

- [ ] 🟢 Update `CLAUDE.md` — document `ude_` convention, audit gap analysis results ──► [Model: Antigravity - Gemini 3.5 Flash (Medium)]
- [ ] 🟢 Move `future_v2.md` sections to `roadmap/mvp_v2/` (intent history) ──► [Model: Antigravity - Gemini 3.5 Flash (Low)]
- [ ] 🟢 Split `v2_detailed_tasks.md` (2364 lines) into atomic files in `tasks/` — maximum 500 lines/file ──► [Model: Antigravity - Gemini 3.5 Flash (High)]

---

## Dependency Summary Table

```
Section 0 (Preparation)
        │
        ▼
Phase 1: GAP-09 ──► GAP-12 ──► GAP-07 ──► GAP-11
        │
        ▼
Phase 2: GAP-05 ──► GAP-01
        │
        ├──► Phase 3/D: GAP-03 ──► GAP-10
        │
        └──► Phase 3/F: GAP-31 ‖ GAP-32

In Parallel:
  Section 5 (CI/CD) — does not block engine, required before release
  Section 6 (UserDocs) — does not block engine, required before release
  Section 7 (Pipeline Docs) — parallel with implementation
  Section 8 (DocReqs) — applied from the start of work
```

---

## Final Summary by Sections

| # | Section | Critical 🔴 | Important 🟡 | Desirable 🟢 | Blocks |
|---|---------|------------|-------------|-------------|--------|
| 0 | Repository and Env Prep | 12 | 12 | 7 | — |
| 1 | Phase 1: Infrastructure | 59 | 11 | — | Phase 2 |
| 2 | Phase 2: API & CLI | 21 | 15 | 1 | Phase 3 |
| 3 | Phase 3/D: Typed IR | 45 | 14 | — | Release |
| 4 | Phase 3/F: QA | 47 | 55 | 9 | Release |
| 5 | CI/CD Deploy | 16 | 16 | 14 | Release |
| 6 | User Docs | 17 | 12 | 4 | Release |
| 7 | Pipeline Docs | 5 | 5 | 2 | Release |
| 8 | Doc Requirements | 11 | 24 | 2 | Release |
| 9 | Finalization | 13 | 5 | 4 | — |
| **∑** | **Total** | **246** | **169** | **43** | |

---

> **Status:** Document created 2026-06-29. All tasks awaiting execution.  
> **Next Step:** Section 0 (preparation, zero risk) → Phase 1 (GAP-09).  
> **Phase 3/D Constraint:** GAP-10 is activated after completing GAP-03 and GAP-01.  
> **CI/CD Phase 4 Constraint:** coverage gate via `ude audit` is activated after implementing GAP-10.
