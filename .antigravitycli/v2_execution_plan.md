# UDE v2.0 — Granular Execution Plan

**Version:** 2.0 ("AI-Accelerated Core & Quality Upgrade")  
**Prepared:** 2026-06-28  
**Source documents:** `design-docs/docs/roadmap/future_v2.md` · `design-docs/docs/roadmap/mvp_v1/requirements.md`  
**Prerequisite:** UDE v1.0 MVP fully delivered (209 tests passing, ≥98% coverage confirmed).

---

## Strategic Delivery Order

```
Phase 1 ──► Phase 2 ──► Phase 3 (D ‖ F)
  Group A      Group B      Group D  Group F
(Foundation) (Interfaces) (Typed IR) (QA)
```

Phases 1 and 2 are strictly sequential — each phase unlocks the next.  
Phase 3 splits into two independent tracks (Group D and Group F) that run in parallel.

---

## Phase 1 — Group A: Infrastructure (Foundation)

*Delivery order within the phase: GAP-09 → GAP-12 → GAP-07 → GAP-11*  
*Rationale: GAP-09 activates the config fields that GAP-12 (log file) and GAP-07 (cache_root_dir) depend on. GAP-11 is collector-only and has no dependency on the others, but benefits from the logging infrastructure established in GAP-12.*

---

### GAP-09 — Global Config Field Activation

**Goal:** Make all fields in `ude_global_config.json` operationally active. Currently only `error_policy` is read and respected; `doxygen_path`, `log_level`, `log_file`, `cache_root_dir`, and `global_templates_dir` are parsed but silently ignored.

#### Sub-tasks

**GAP-09-A · Audit current global-config consumption**

- Read `engine/ude/orchestrator.py:run_target()` and `engine/ude/cli.py:run_pipeline()` and list every key actually consumed from `resolved_global_config`.
- Confirm that only `error_policy` (via `orchestrator.py`) and a partial `logging.level` key (line ~162) are active.
- Document the audit result as an inline comment block at the top of `orchestrator.py`.
- *AI guideline:* Do not refactor during this step — read and annotate only.

**GAP-09-B · Define the global-config schema as a Pydantic model**

- Create `engine/ude/config.py` (new file).
- Define `GlobalConfig(BaseModel)` with fields:
  ```python
  doxygen_path: Optional[str] = None
  log_level: str = "WARNING"
  log_file: Optional[str] = None
  cache_root_dir: Optional[str] = None
  global_templates_dir: Optional[str] = None
  error_policy: str = "fail-fast"
  translation_service: Optional[str] = None  # reserved, v3.0+
  ```
- Add a factory `GlobalConfig.from_file(path: Path) -> "GlobalConfig"` that loads JSON and validates.
- *Technical constraint:* `translation_service` must parse without error but must not be acted upon in v2.0. Add a `# v3.0+ reserved` comment.
- *AI guideline:* Implement the Pydantic model first, before touching orchestrator, to ensure the schema is solid before wiring it.

**GAP-09-C · Wire GlobalConfig into UdeOrchestrator**

- Replace the raw `json.load` global-config dict in `UdeOrchestrator.__init__()` with `GlobalConfig.from_file()`.
- Store the parsed `GlobalConfig` instance as `self._global_cfg`.
- In `run_target()`:
  - Resolve `doxygen_path` and inject it into `DoxygenXmlCollector` env before `collect()`.
  - Resolve `global_templates_dir` and pass it as a fallback template search path to the renderer factory.
  - Resolve `cache_root_dir` into an absolute `Path` and store as `self._cache_root`; pass to `BuildCacheManager` (consumed by GAP-07).
- *Technical constraint:* All paths in `GlobalConfig` must be resolved relative to the global config file's parent directory, not the CWD.
- *Technical constraint:* Backward compatibility — if `ude_global_config.json` exists but lacks new fields, Pydantic defaults must silently apply; no exception may be raised.

**GAP-09-D · Wire GlobalConfig into cli.py run_pipeline()**

- In `cli.py:run_pipeline()`, replace the raw `json.load` global-config dict with `GlobalConfig.from_file()`.
- Apply the same `doxygen_path` → env and `global_templates_dir` → renderer logic.
- *AI guideline:* Keep `cli.py` thin — move any non-trivial resolution logic into `orchestrator.py` helper functions and call them from `cli.py`. This is a stepping stone toward GAP-05.

**GAP-09-E · Unit tests for GlobalConfig**

- File: `engine/tests/test_config.py` (new).
- Test cases:
  - `test_global_config_defaults` — empty JSON `{}` produces all defaults correctly.
  - `test_global_config_full_round_trip` — all fields round-trip through `from_file()`.
  - `test_global_config_unknown_keys_ignored` — extra keys do not raise (Pydantic `model_config = ConfigDict(extra="ignore")`).
  - `test_global_config_missing_file_raises` — `from_file(non_existent)` raises `FileNotFoundError`.
  - `test_orchestrator_respects_doxygen_path` — mock `DoxygenXmlCollector.collect` and assert env var `DOXYGEN_PATH` set before call.
  - `test_orchestrator_respects_cache_root_dir` — assert `BuildCacheManager` receives an absolute path derived from `cache_root_dir`.

**Verification:**
```bash
cd engine
poetry run pytest tests/test_config.py -v --tb=short
# Expected: 6/6 PASSED
poetry run pytest --co -q | grep "test_config"
# Expected: lists all 6 tests
```

---

### GAP-12 — Unified Logging

**Goal:** Introduce a single `logging_setup()` call that configures `StreamHandler` (stderr, always) and optional `FileHandler` (when `log_file` is set). Fix the incorrect logger label `ude.renderers` in `interfaces.py` (HC-05).

**Prerequisite confirmed:** GAP-09 must be merged — `log_level` and `log_file` are read from `GlobalConfig`.

#### Sub-tasks

**GAP-12-A · Fix the incorrect logger label in interfaces.py (HC-05)**

- File: `engine/ude/interfaces.py`, line 8.
- Change `logging.getLogger("ude.renderers")` → `logging.getLogger("ude.interfaces")`.
- *Technical constraint:* This is a pure rename — no logic changes. Any tests that assert the logger name `"ude.renderers"` coming from `interfaces.py` must be updated accordingly.
- *AI guideline:* Search all test files for `"ude.renderers"` to find assertions that need updating.

**GAP-12-B · Implement logging_setup() in config.py**

- File: `engine/ude/config.py` (extends GAP-09-B).
- Add function:
  ```python
  def logging_setup(cfg: GlobalConfig) -> None:
      """Configures root UDE logger. Call once at engine startup."""
      root = logging.getLogger("ude")
      root.setLevel(cfg.log_level.upper())
      root.handlers.clear()
      # StreamHandler always present
      sh = logging.StreamHandler(sys.stderr)
      sh.setFormatter(logging.Formatter("%(levelname)s [%(name)s] %(message)s"))
      root.addHandler(sh)
      # FileHandler only when log_file is set
      if cfg.log_file:
          fh = logging.FileHandler(cfg.log_file, encoding="utf-8")
          fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))
          root.addHandler(fh)
  ```
- *Technical constraint:* `root.handlers.clear()` prevents duplicate handler accumulation across unit test runs. All test files that capture log output must use `caplog` or `capfd` pytest fixtures.

**GAP-12-C · Call logging_setup() at engine startup**

- In `UdeOrchestrator.__init__()`: call `logging_setup(self._global_cfg)` after `GlobalConfig.from_file()`.
- In `cli.py:run_pipeline()`: call `logging_setup(global_cfg)` immediately after loading the global config.
- *Technical constraint:* `logging_setup()` must be idempotent across multiple `UdeOrchestrator` instantiations in the same process (guaranteed by `handlers.clear()`).

**GAP-12-D · Unit tests for logging_setup**

- File: `engine/tests/test_config.py` (extend GAP-09-E test file).
- Test cases:
  - `test_logging_setup_stderr_only` — when `log_file=None`, root `"ude"` logger has exactly 1 handler (StreamHandler).
  - `test_logging_setup_with_file` — when `log_file` set to a tmp path, logger has 2 handlers; file is created.
  - `test_logging_setup_level_applied` — `log_level="DEBUG"` → `logger.level == logging.DEBUG`.
  - `test_hc05_logger_label_fixed` — `logging.getLogger("ude.interfaces")` is the logger used in `interfaces.py`.

**Verification:**
```bash
poetry run pytest tests/test_config.py -v -k "logging"
# Expected: 4/4 PASSED
# Manual smoke: run `ude --global-config path/to/global.json --doc-config ...`
# with log_level="DEBUG" in global config; DEBUG lines must appear on stderr.
```

---

### GAP-07 — L2 Render Cache Activation

**Goal:** Wire the existing `BuildCacheManager` L2 render cache into all 16 concrete renderer `render()` calls. Cache invalidation is based on IR hash + Jinja2 template hashes. The orchestrator must pass `cache_dir` (derived from `GlobalConfig.cache_root_dir`) to the renderer factory.

**Prerequisite confirmed:** GAP-09 must be merged — `cache_root_dir` must be readable from `GlobalConfig`.

#### Sub-tasks

**GAP-07-A · Verify BuildCacheManager L2 API in storage.py**

- Read `engine/ude/storage.py` fully and confirm the `BuildCacheManager` class and its L2 methods exist.
- Identify the method signatures for `is_render_cached(entity_sig: str, template_hash: str) -> bool` and `mark_render_cached(entity_sig: str, template_hash: str) -> None` (or equivalent).
- If the `BuildCacheManager` class is absent from `storage.py`, implement it as sub-task GAP-07-A1:
  - Add `BuildCacheManager` to `storage.py` with constructor `__init__(cache_dir: Path)`.
  - L2 state stored as `{entity_sig: template_hash}` in `cache_dir / ".render_cache.json"`, lazily loaded on first use.
  - Methods: `is_render_stale(ir_hash: str, template_hash: str) -> bool`, `update(ir_hash: str, template_hash: str) -> None`, `save() -> None`.
- *AI guideline:* Implement and test `BuildCacheManager` in isolation before wiring to renderers.

**GAP-07-B · Compute IR hash and template hash at render time**

- The IR hash = `calculate_sha256(catalog.model_dump_json())` using the existing `calculate_sha256()` in `storage.py`.
- The template hash = SHA-256 of all Jinja2 template file contents concatenated in alphabetical order from the template directory in use.
- Add a helper `compute_template_hash(template_dir: Path) -> str` to `storage.py`.

**GAP-07-C · Thread cache_dir through the renderer factory**

- In `UdeOrchestrator.run_target()`, compute `cache_dir`:
  ```python
  if self._global_cfg.cache_root_dir:
      cache_dir = (global_cfg_parent / self._global_cfg.cache_root_dir / target_slug).resolve()
  else:
      cache_dir = config_dir / ".ude_cache"
  ```
- Pass `cache_dir` to the renderer constructor (both `HtmlRenderer` and `HugoMarkdownRenderer`).
- Update `BaseRenderer.__init__()` to accept `cache_dir: Optional[Path] = None` and store it.

**GAP-07-D · Wire L2 cache skip into BaseRenderer.render()**

- In `BaseRenderer.render()` (in `interfaces.py`), before writing each output file:
  1. Compute `ir_hash` and `template_hash`.
  2. If `self._cache_mgr` is not None and `not self._cache_mgr.is_render_stale(ir_hash, template_hash)` → skip writing and log at `DEBUG` level: `"[L2 cache HIT] Skipped render for <entity>"`.
  3. Otherwise, write output file and call `self._cache_mgr.update(ir_hash, template_hash)`.
  4. Call `self._cache_mgr.save()` after all entities are rendered.
- *Technical constraint:* `cache_dir=None` must produce identical behavior to v1.0 — the L2 cache is opt-in via `cache_root_dir` in global config. Zero behavior change when `cache_root_dir` is absent.

**GAP-07-E · Unit and integration tests**

- File: `engine/tests/test_caching.py` (extend existing).
- New test cases:
  - `test_l2_cache_hit_skips_file_write` — render once, delete output file, render again with same catalog and templates; assert output file is NOT re-created (cache hit).
  - `test_l2_cache_miss_on_ir_change` — render once, mutate one field in catalog, render again; assert output is re-created.
  - `test_l2_cache_miss_on_template_change` — render once, modify a template file's mtime/content, render again; assert output is re-created.
  - `test_l2_cache_disabled_when_no_cache_dir` — with `cache_dir=None`, all files are always written (no regression vs v1.0).

**Verification:**
```bash
poetry run pytest tests/test_caching.py -v
# Expected: all L2 tests PASSED
# Sequential pipeline run: second run must log "[L2 cache HIT]" for unchanged entities.
# `poetry run ude --global-config ... --doc-config ...` twice; second run faster.
```

---

### GAP-11 — Doxyfile Key-Level 3-Tier Merge

**Goal:** Replace the current source-concatenation Doxyfile assembly (Doxygen last-value-wins) with an explicit 3-tier key-level merge: T1 (global template) → T2 (target-specific template) → T3 (runtime parameters). Key conflicts logged at `DEBUG`.

#### Sub-tasks

**GAP-11-A · Implement Doxyfile parser/serializer**

- File: `engine/ude/collectors/doxyfile.py` (new module).
- `parse_doxyfile(content: str) -> dict[str, str]` — split lines on `=`, strip whitespace, skip comments (`#`) and blank lines. Multi-value keys (e.g. `INPUT`) accumulate as space-joined strings per Doxygen convention.
- `serialize_doxyfile(kvs: dict[str, str]) -> str` — format as `KEY = VALUE\n` pairs sorted alphabetically.
- *Technical constraint:* The parser must be tolerant of Doxygen's continuation lines (`\` at end of line) — join continuation lines before splitting.
- *AI guideline:* Write tests before the parser implementation (TDD red-green-refactor).

**GAP-11-B · Implement 3-tier merge function**

- In `doxyfile.py`, add:
  ```python
  def merge_doxyfile_tiers(t1: dict, t2: dict, t3: dict) -> dict:
      """T1 = base, T2 overrides T1, T3 overrides T2. Conflicts logged at DEBUG."""
  ```
- Log each T2 override over T1 and each T3 override over T2 at `DEBUG` using `logging.getLogger("ude.collector.doxyfile")`.

**GAP-11-C · Replace concatenation in DoxygenXmlCollector**

- File: `engine/ude/collectors/doxygen.py`.
- In the Doxyfile assembly section, replace the 3-file string concatenation with:
  1. Parse T1 (global template from `GlobalConfig.global_templates_dir / "Doxyfile"`).
  2. Parse T2 (target-specific template from `collector_cfg["doxyfile_template"]`).
  3. Build T3 as a dict of runtime keys (`INPUT`, `OUTPUT_DIRECTORY`, `NUM_PROC_THREADS`, etc.).
  4. Call `merge_doxyfile_tiers(t1, t2, t3)` and serialize to the temp Doxyfile path.
- *Technical constraint:* If the global template is absent (e.g., `global_templates_dir` not set), T1 defaults to `{}` (empty dict) — the merge degrades gracefully to T2+T3 only.
- *Technical constraint:* v1.0 backward compatibility — existing `ude_doc_config.json` files that specify a `doxyfile_template` path must continue to work identically; only the assembly mechanism changes internally.

**GAP-11-D · Unit tests**

- File: `engine/tests/test_doxygen_collector.py` (extend existing) or new `test_doxyfile.py`.
- Test cases:
  - `test_parse_doxyfile_basic` — well-formed Doxyfile content parses to correct dict.
  - `test_parse_doxyfile_continuation_lines` — multi-line values (backslash continuation) collapse correctly.
  - `test_parse_doxyfile_skip_comments` — `#` lines and blank lines are excluded.
  - `test_serialize_doxyfile_round_trip` — parse then serialize produces equivalent output (key order may differ).
  - `test_merge_tiers_t2_overrides_t1` — a key present in both T1 and T2 uses T2 value.
  - `test_merge_tiers_t3_overrides_t2` — a key present in T2 and T3 uses T3 value.
  - `test_merge_tiers_debug_log_on_conflict` (use `caplog`) — conflict triggers a DEBUG log entry.
  - `test_collector_uses_merged_doxyfile` — mock `subprocess.run` and assert the written Doxyfile content is the merged result, not a raw concatenation.

**Verification:**
```bash
poetry run pytest tests/test_doxyfile.py -v  # or test_doxygen_collector.py -v -k "doxyfile"
# Expected: 8/8 PASSED
# Run a real Doxygen collection and inspect the generated temp Doxyfile:
# Only one value per key; explicit T3 values (INPUT, OUTPUT_DIRECTORY) appear exactly once.
```

---

## Phase 2 — Group B: Library API & CLI Unification

*Delivery order: GAP-05 → GAP-01*  
*Rationale: GAP-01 (CLI subcommands) calls through to the public library methods introduced by GAP-05. The thin-wrapper invariant cannot be upheld until GAP-05 moves logic into `UdeOrchestrator`.*

---

### GAP-05 — UdeOrchestrator Library API

**Goal:** Expose `parse(config) -> ProjectCatalog`, `render(catalog, config) -> None`, and `run(config) -> None` as stable, importable public methods on `UdeOrchestrator`. Consolidate the duplicated `deep_merge()` and `find_product_json()` utilities (currently present in both `cli.py` and `orchestrator.py`) into `orchestrator.py`. Reduce `cli.py` to argument parsing and a thin call to the orchestrator.

#### Sub-tasks

**GAP-05-A · Move deep_merge() and find_product_json() to orchestrator.py**

- Delete `deep_merge()` and `find_product_json()` from `engine/ude/cli.py`.
- Update the import at the top of `cli.py` to: `from ude.orchestrator import deep_merge, find_product_json`.
- *Technical constraint:* Do not change function signatures or behavior — this is a pure relocation. Any test in `test_cli.py` that tests these functions must be updated to import from `ude.orchestrator`.
- Run the full test suite after this step; zero failures allowed before proceeding.

**GAP-05-B · Extract config resolution logic from run_target() into a reusable helper**

- In `orchestrator.py`, add:
  ```python
  def resolve_config(doc_config_path: Path, global_cfg: GlobalConfig) -> tuple[dict, Path]:
      """Loads, merges (global→sdk→doc), and returns the resolved config dict and config_dir."""
  ```
- Move the 3-way deep merge, `find_product_json()` tree walk, `sidebar.toml` loading, and language detection into `resolve_config()`.
- `run_target()` delegates entirely to `resolve_config()` + the new public methods introduced below.
- *AI guideline:* Extract, don't rewrite. Copy the exact logic from `run_target()` into `resolve_config()` first; then slim down `run_target()` to call it.

**GAP-05-C · Implement public parse() method on UdeOrchestrator**

```python
def parse(self, config: dict, config_dir: Path) -> ProjectCatalog:
    """Runs collection (if needed) + parsing. Returns the populated ProjectCatalog."""
```
- Internally: collector logic (detect if `xml_dir` already has `index.xml`; otherwise run `DoxygenXmlCollector`) + `DoxygenXmlParser.parse()`.
- Signature must be stable across v2.0; it is the boundary the `ude parse` subcommand calls.

**GAP-05-D · Implement public render() method on UdeOrchestrator**

```python
def render(self, catalog: ProjectCatalog, config: dict, config_dir: Path, out_dir: Path) -> None:
    """Renders a pre-built ProjectCatalog to the target output directory."""
```
- Internally: renderer factory selection (html vs hugo_markdown), `cache_dir` injection (GAP-07), `renderer.render(catalog, str(out_dir))`.

**GAP-05-E · Implement public run() method on UdeOrchestrator**

```python
def run(self, doc_config_path: Path) -> bool:
    """End-to-end pipeline shortcut: resolve_config → parse → render."""
```
- This replaces the body of `run_target()`. `run_target()` becomes a thin alias calling `run()` for backward compatibility.

**GAP-05-F · Slim down cli.py to a thin wrapper**

- `cli.py:run_pipeline()` must:
  1. Load `GlobalConfig` via `config.py`.
  2. Instantiate `UdeOrchestrator(global_config_path)`.
  3. Call `orchestrator.run(doc_config_path)` and convert result to exit code.
- All pipeline logic is removed from `cli.py`. The module retains only `argparse` setup and `main()`.
- *Technical constraint:* The v1.0 flat CLI flags (`--global-config`, `--sdk-config`, `--doc-config`, `--input`, `--output`, `--format`) must still work identically. No CLI interface breakage.

**GAP-05-G · Update test_cli.py and test_orchestrator.py**

- Move `deep_merge` / `find_product_json` import assertions from `test_cli.py` to `test_orchestrator.py`.
- Add new tests:
  - `test_orchestrator_parse_returns_catalog` — calls `orchestrator.parse()` directly; asserts result is `ProjectCatalog`.
  - `test_orchestrator_render_produces_files` — calls `orchestrator.render()` directly with a pre-built catalog; asserts output files exist.
  - `test_orchestrator_run_end_to_end` — calls `orchestrator.run()` with a mock XML dir; asserts output files exist.
  - `test_cli_delegates_to_orchestrator` (mock `UdeOrchestrator.run`) — confirms `cli.py` passes control to orchestrator without re-implementing logic.

**Verification:**
```bash
poetry run pytest tests/test_orchestrator.py tests/test_cli.py -v --tb=short
# Expected: all tests PASSED; zero import errors for deep_merge from ude.orchestrator.
# Smoke test: python -c "from ude.orchestrator import UdeOrchestrator; o = UdeOrchestrator(); print(dir(o))"
# Must show: parse, render, run in the output.
```

---

### GAP-01 — CLI Subcommands

**Goal:** Add `ude compile`, `ude parse`, `ude render`, and `ude audit` subcommands to `cli.py` using argparse subparsers. The flat v1.0 interface (`ude --global-config ... --doc-config ...`) must remain fully operational.

**Prerequisite confirmed:** GAP-05 must be merged — subcommands delegate to `UdeOrchestrator` public methods.

#### Sub-tasks

**GAP-01-A · Add argparse subparsers to cli.py**

- Restructure `main()` to use `parser.add_subparsers(dest="command")`.
- If `args.command is None`, fall back to the v1.0 flat-flag path in `run_pipeline()` (backward-compatible dispatch).
- Add four subparsers: `compile`, `parse`, `render`, `audit`.

**GAP-01-B · Implement ude compile subcommand**

- Arguments: `--global-config`, `--doc-config` (required), `--input` (optional), `--output` (optional), `--format` (optional).
- Behavior: identical to the v1.0 flat invocation. Calls `orchestrator.run(doc_config_path)`.
- `ude --doc-config X` and `ude compile --doc-config X` must produce byte-identical output.

**GAP-01-C · Implement ude parse subcommand**

- Arguments: `--global-config`, `--doc-config` (required), `--output-ir` (path for the `.json.gz` IR output, required).
- Behavior: calls `orchestrator.parse(config, config_dir)` then `save_compressed_ir(catalog, args.output_ir)`.
- Stdout: prints `{"namespaces": N, "classes": M}` summary JSON on success.
- Exit code: 0 on success, 1 on error.

**GAP-01-D · Implement ude render subcommand**

- Arguments: `--global-config`, `--doc-config`, `--input-ir` (path to `.json.gz` IR, required), `--output` (required), `--format` (optional).
- Behavior: calls `load_compressed_ir(args.input_ir)` then `orchestrator.render(catalog, config, config_dir, out_dir)`.
- `ude parse --output-ir /tmp/ir.json.gz && ude render --input-ir /tmp/ir.json.gz --output ./out` must produce identical output to `ude compile`.

**GAP-01-E · Implement ude audit subcommand (shell stub)**

- Arguments: `--global-config`, `--doc-config` (required), `--mode` choices `["reject-undocumented", "allow-undocumented"]` (default: `"allow-undocumented"`), `--threshold` (float 0.0–1.0, default 1.0).
- Behavior in v2.0 at GAP-01 stage: parse the IR, count total entities and undocumented entities, print coverage report, apply mode policy (non-zero exit if reject and coverage < threshold).
- *Technical constraint:* The full `ude audit` coverage logic is implemented in GAP-10. GAP-01-E only wires the subcommand plumbing; the handler may call a `raise NotImplementedError("ude audit: implemented in GAP-10")` stub that produces a clear error message, making the subcommand discoverable.

**GAP-01-F · Update test_cli.py**

- Test cases:
  - `test_compile_subcommand_delegates_to_run` — mock `UdeOrchestrator.run`; assert called.
  - `test_parse_subcommand_creates_ir_file` — run against mock XML dir; assert `.json.gz` created.
  - `test_render_subcommand_from_ir_file` — load pre-built `.json.gz`; assert output files match `ude compile` output.
  - `test_flat_flags_still_work` — `main(["--doc-config", "..."])` succeeds (backward compat).
  - `test_parse_then_render_output_identical_to_compile` — byte-level comparison of output trees.
  - `test_audit_subcommand_reachable` — `main(["audit", "--doc-config", "..."])` returns non-zero (NotImplementedError stub) without crashing argparse.

**Verification:**
```bash
# Linux / macOS / CI
poetry run pytest tests/test_cli.py -v
# All tests PASSED.
# Manual smoke:
ude compile --doc-config path/to/ude_doc_config.json --output /tmp/out_compile
ude parse   --doc-config path/to/ude_doc_config.json --output-ir /tmp/ir.json.gz
ude render  --doc-config path/to/ude_doc_config.json --input-ir /tmp/ir.json.gz --output /tmp/out_render
# Portable tree comparison (cross-platform — replaces Linux-only diff -r):
python -c "
import filecmp, sys
cmp = filecmp.dircmp('/tmp/out_compile', '/tmp/out_render')
diffs = cmp.diff_files + cmp.left_only + cmp.right_only
if diffs:
    print('DIFF:', diffs); sys.exit(1)
print('Trees are byte-identical.')
"
```

```powershell
# Windows PowerShell equivalent
poetry run pytest tests/test_cli.py -v
ude compile --doc-config path/to/ude_doc_config.json --output $env:TEMP\out_compile
ude parse   --doc-config path/to/ude_doc_config.json --output-ir $env:TEMP\ir.json.gz
ude render  --doc-config path/to/ude_doc_config.json --input-ir $env:TEMP\ir.json.gz --output $env:TEMP\out_render
python -c @"
import filecmp, sys
cmp = filecmp.dircmp(r'$env:TEMP\out_compile', r'$env:TEMP\out_render')
diffs = cmp.diff_files + cmp.left_only + cmp.right_only
if diffs:
    print('DIFF:', diffs); sys.exit(1)
print('Trees are byte-identical.')
"@
```

---

## Phase 3 — Group D + Group F (Parallel Tracks)

*Group D (GAP-03 → GAP-10) and Group F (GAP-31, GAP-32) are independent and can be assigned to separate workstreams or interleaved across sprints.*

---

## Phase 3 / Group D — Typed IR

*Delivery order within Group D: GAP-03 → GAP-10*  
*Rationale: GAP-10 (coverage gate) requires per-entity-type counting, which requires the typed models from GAP-03.*

---

### GAP-03 — Typed Entity Models

**Goal:** Replace the v1.0 `ClassEntity` discriminated union with seven explicit Pydantic models: `ClassModel`, `MethodModel`, `ParameterModel`, `EnumModel`, `VariableModel`, `ConstantModel`, `TypeAliasModel`. Extend `ProjectCatalog` with `project_name: str` and `version: str` fields. Refactor all parsers, renderers, and tests to use the new schema.

**WARNING — Highest-effort item:** This is the highest-effort item in v2.0 and a prerequisite for GAP-10. Its scope touches every layer of the pipeline. Treat it as a mini-project with its own internal sequencing.

#### Sub-tasks

**GAP-03-A · Design the 7-model schema (models.py)**

- Replace `models.py` entirely. New contents:

  ```python
  class ParameterModel(BaseModel):
      name: str
      type: str
      description: Optional[str] = None

  class MethodModel(BaseModel):
      name: str
      fully_qualified_name: str
      signature: str
      parameters: List[ParameterModel] = Field(default_factory=list)
      return_type: str
      docstring: Optional[str] = None
      is_static: bool = False
      is_virtual: bool = False
      overloads: List["OverloadModel"] = Field(default_factory=list)

  class OverloadModel(BaseModel):
      index: int
      description: Optional[str] = None
      parameters: List[ParameterModel] = Field(default_factory=list)
      return_type: Optional[str] = None
      signature: Optional[str] = None

  class EnumModel(BaseModel):
      name: str
      fully_qualified_name: str
      docstring: Optional[str] = None
      values: List[str] = Field(default_factory=list)

  class VariableModel(BaseModel):
      name: str
      fully_qualified_name: str
      type: str
      docstring: Optional[str] = None
      is_static: bool = False

  class ConstantModel(BaseModel):
      name: str
      fully_qualified_name: str
      type: str
      value: Optional[str] = None
      docstring: Optional[str] = None

  class TypeAliasModel(BaseModel):
      name: str
      fully_qualified_name: str
      aliased_type: str
      docstring: Optional[str] = None

  class ClassModel(BaseModel):
      name: str
      fully_qualified_name: str
      entity_type: Literal["class", "struct", "interface", "exception", "enum_class"]
      docstring: Optional[str] = None
      base_class: Optional[str] = None
      methods: List[MethodModel] = Field(default_factory=list)
      fields: List[VariableModel] = Field(default_factory=list)
      enums: List[EnumModel] = Field(default_factory=list)
      constants: List[ConstantModel] = Field(default_factory=list)
      type_aliases: List[TypeAliasModel] = Field(default_factory=list)

  class NamespaceModel(BaseModel):
      name: str
      classes: List[ClassModel] = Field(default_factory=list)
      free_functions: List[MethodModel] = Field(default_factory=list)
      free_variables: List[VariableModel] = Field(default_factory=list)
      enums: List[EnumModel] = Field(default_factory=list)
      constants: List[ConstantModel] = Field(default_factory=list)
      type_aliases: List[TypeAliasModel] = Field(default_factory=list)

  class ProjectCatalog(BaseModel):
      project_name: str = ""
      version: str = ""
      namespaces: List[NamespaceModel] = Field(default_factory=list)
      metadata: Optional[dict] = Field(default_factory=dict)
  ```

- *Technical constraint:* `project_name` and `version` default to `""` to preserve backward compatibility with existing IR files that lack these fields.
- *Technical constraint:* `NamespaceEntity` is renamed to `NamespaceModel`; all internal references must be updated via a global search-replace.
- *AI guideline:* Implement `models.py` in full and commit it in isolation before touching any parser or renderer. Then refactor layer by layer: parsers → renderers → tests. This avoids context pollution where a half-updated renderer confuses diagnostics.

**GAP-03-B · Update test_models.py**

- Rewrite `engine/tests/test_models.py` to exercise all 7 new model types.
- Verify: `ProjectCatalog` accepts `project_name` and `version`; old IR JSON files without these fields still deserialize (Pydantic defaults apply).
- Add round-trip serialization tests for each model.

**GAP-03-C · Refactor parsers**

- Files: `engine/ude/parsers/doxygen.py`, `doxygen_csharp.py`, `doxygen_java.py`, `doxygen_python.py`, `doxygen_base.py`, `doxygen_router.py`.
- Replace all construction of `ClassEntity(...)` with `ClassModel(...)`.
- Replace `NamespaceEntity(...)` with `NamespaceModel(...)`.
- Map `MethodEntity` → `MethodModel`, `ParameterField` → `ParameterModel`.
- Populate the new per-entity typed lists: any field currently stored as a raw string in `ClassEntity.fields` must be inspected and mapped to `VariableModel`, `ConstantModel`, or `EnumModel` where Doxygen XML provides the necessary metadata.
- *Technical constraint:* Where Doxygen XML lacks sufficient metadata to populate a new field (e.g., constant value), set to `None` — never silently drop the entity.
- Run `test_doxygen_parser.py` after each language-file refactor to catch regressions early.

**GAP-03-D · Refactor renderers**

- Files: `engine/ude/renderers/static_html.py`, `hugo_markdown.py`, `legacy.py`.
- Replace all attribute accesses on `ClassEntity` with the new model attributes.
- `entity.fields` (was `List[str]`) → iterate `entity.fields` as `List[VariableModel]`, use `.name` and `.type`.
- Add rendering for `entity.enums`, `entity.constants`, `entity.type_aliases` in entity detail pages.
- *Technical constraint:* No new pages or layout changes — render new entity types within existing section containers. Navigation architecture is frozen for v2.0. Visual layout changes are deferred to v3.0+.

**GAP-03-E · Refactor storage.py and update round-trip test**

- `save_compressed_ir` and `load_compressed_ir` already use `catalog.model_dump_json()` and `ProjectCatalog.model_validate_json()` — no functional change required.
- Add a round-trip test that serializes the new 7-model structure and deserializes it back; confirm all nested typed models survive the gzip cycle.

**GAP-03-F · Update all test files**

- `test_models.py` — complete rewrite (GAP-03-B above).
- `test_doxygen_parser.py` — update assertions to use `ClassModel`, `MethodModel`, etc.
- `test_html_renderer.py`, `test_hugo_renderer.py`, `test_legacy_renderer.py` — update fixture catalogs.
- `test_integration_pipeline.py` — end-to-end test must pass with new schema.
- `test_golden_master.py` — regenerate baselines after renderer is updated.
- Run full coverage after each test file update: `poetry run pytest --cov=ude --cov-report=term-missing`.

**GAP-03-G · Regenerate golden master baselines**

- After all parsers, renderers, and tests pass, regenerate the golden master baselines.
  Only run with explicit user confirmation — inspect `git diff --stat` on the regenerated files first.
  ```bash
  # Linux / macOS / CI
  cd engine
  UPDATE_GOLDEN=1 poetry run pytest tests/test_golden_master.py -v
  poetry run pytest tests/test_golden_master.py -v   # must pass on clean re-run
  ```
  ```powershell
  # Windows PowerShell (primary project shell)
  cd engine
  $env:UPDATE_GOLDEN="1"; poetry run pytest tests/test_golden_master.py -v
  poetry run pytest tests/test_golden_master.py -v   # must pass on clean re-run
  ```
- Commit the regenerated baselines after confirming `git diff --stat` shows only content changes
  in existing baseline files — no file additions or deletions expected.

**GAP-03-H · Re-baseline Docomatic alignment suite**

- Run the Docomatic alignment suite after all render-layer changes (TASK-D.1.7–D.1.9) and golden master regeneration:
  ```bash
  # Linux / macOS / CI
  poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short
  ```
  ```powershell
  # Windows PowerShell
  poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short
  ```
- Compare `"total_differences"` in each `difference_mock_sdk_{lang}.json` report against the pre-GAP-03 baseline.
- New typed entity sections (`constants`, `type_aliases`, `enums`) appearing as differences are EXPECTED — follow the `difference_minimization_iterator.md` allowances workflow before updating baselines:
  ```bash
  UPDATE_ALLOWANCES=1 poetry run pytest engine/tests/test_docomatic_alignment.py  # bash
  ```
  ```powershell
  $env:UPDATE_ALLOWANCES="1"; poetry run pytest engine/tests/test_docomatic_alignment.py  # PS
  ```
- If `"total_differences"` INCREASES for a language NOT being worked on: cross-language regression — do NOT update allowances; revert and investigate.

**Verification:**
```bash
# Linux / macOS / CI
poetry run pytest --cov=ude --cov-report=term-missing
# Coverage must remain ≥ 98%.
poetry run pytest tests/test_models.py tests/test_doxygen_parser.py tests/test_integration_pipeline.py -v
# All PASSED.
# Manual IR inspection:
ude parse --doc-config path/to/ude_doc_config.json --output-ir /tmp/ir_v2.json.gz
python -c "from ude.storage import load_compressed_ir; c = load_compressed_ir('/tmp/ir_v2.json.gz'); print(c.project_name, c.version, len(c.namespaces))"
# Must print project_name and version fields (empty string if not set in sdk config).
```

---

### GAP-10 — Documentation Coverage Gate

**Goal:** Add two read-only enforcement modes configurable via `GlobalConfig`: `reject-undocumented` (non-zero exit if coverage below threshold) and `allow-undocumented` (warnings only). Implement `ude audit` subcommand generating a coverage report per entity type. No LLM calls in v2.0.

**Prerequisite confirmed:** GAP-03 (typed IR) and GAP-01 (`ude audit` subcommand stub) must be merged.

#### Sub-tasks

**GAP-10-A · Define coverage metrics**

- Entities counted for coverage:
  - `ClassModel` → `docstring is not None and docstring.strip() != ""`
  - `MethodModel` → `docstring is not None and docstring.strip() != ""`
  - `EnumModel` → `docstring is not None and docstring.strip() != ""`
  - `VariableModel` / `ConstantModel` / `TypeAliasModel` → `docstring is not None and docstring.strip() != ""`
- Coverage = `documented_count / total_count` (float 0.0–1.0).
- Report groups: `class`, `method`, `enum`, `variable`, `constant`, `type_alias`, `overall`.

**GAP-10-B · Implement compute_coverage() in a new coverage.py module**

- File: `engine/ude/coverage.py` (new).
- `compute_coverage(catalog: ProjectCatalog) -> CoverageReport` where:
  ```python
  class EntityCoverage(BaseModel):
      total: int
      documented: int
      coverage: float  # 0.0–1.0

  class CoverageReport(BaseModel):
      per_type: dict[str, EntityCoverage]
      overall: EntityCoverage
  ```
- *AI guideline:* Write the Pydantic models and the `compute_coverage()` function before wiring to the CLI.

**GAP-10-C · Implement ude audit subcommand handler (replaces GAP-01-E stub)**

- In `cli.py`, implement the `audit` handler:
  1. Load `GlobalConfig`.
  2. Instantiate `UdeOrchestrator`.
  3. Call `orchestrator.parse(config, config_dir)` to get `catalog`.
  4. Call `compute_coverage(catalog)` to get `report`.
  5. Print report to stdout as formatted Markdown table.
  6. Apply mode policy:
     - `allow-undocumented`: always exit 0 (print warnings on stderr if any entity type below threshold).
     - `reject-undocumented`: exit 2 if `report.overall.coverage < threshold`.

**GAP-10-D · Add coverage_mode to GlobalConfig**

- Extend `GlobalConfig` in `config.py`:
  ```python
  coverage_mode: str = "allow-undocumented"   # or "reject-undocumented"
  coverage_threshold: float = 1.0              # fraction 0.0–1.0
  ```
- In `UdeOrchestrator.run()`, after rendering, call `apply_coverage_gate(catalog, self._global_cfg)` which internally calls `compute_coverage()` and applies the mode policy.
- *Technical constraint:* Coverage gate must run during `ude compile` and `ude audit`. It must NOT run during `ude parse` or `ude render` (those are intermediate pipeline steps).

**GAP-10-E · Unit tests for coverage.py**

- File: `engine/tests/test_coverage.py` (new).
- Test cases:
  - `test_full_coverage_catalog` — catalog where all entities have non-empty docstrings → `overall.coverage == 1.0`.
  - `test_zero_coverage_catalog` — all docstrings `None` → `overall.coverage == 0.0`.
  - `test_mixed_coverage` — 3 of 4 methods documented → `method.coverage == 0.75`.
  - `test_reject_mode_exits_nonzero` — run `main(["audit", "--mode", "reject-undocumented", "--threshold", "1.0", "--doc-config", "..."])` with 0% coverage → exit code 2.
  - `test_allow_mode_exits_zero` — same scenario but `allow-undocumented` → exit code 0.
  - `test_audit_output_contains_table` — stdout contains `| class |`, `| method |`, `| overall |`.

**Verification:**
```bash
poetry run pytest tests/test_coverage.py -v
# All PASSED.
ude audit --doc-config path/to/ude_doc_config.json --mode allow-undocumented
# Expected: prints coverage table per entity type; exits 0.
ude audit --doc-config path/to/ude_doc_config.json --mode reject-undocumented --threshold 0.99
# Expected: exits 2 if coverage below 99%; exits 0 if above.
echo $?
```

---

## Phase 3 / Group F — QA & Testing Completeness

*GAP-31 and GAP-32 are independent; they can proceed in parallel with each other and with Group D.*

---

### GAP-31 — External Integration Script Confirmation

**Goal:** Locate, commit, or re-implement three integration scripts referenced in `integration_tests_specification.md` whose repository location is currently unconfirmed: `Tests/run_regression_tests.py` (TEST-INT-01), `Tests/verify_pages.py` (TEST-INT-03), `Tests/check_links.py` (TEST-INT-04, TEST-INT-06).

#### Sub-tasks

**GAP-31-A · Audit current test infrastructure**

- Search the entire `Pipeline/` repository tree for:
  - `run_regression_tests.py` (known location: `Tests/` directory in root or engine submodule).
  - `verify_pages.py`
  - `check_links.py`
- Confirmed present in `engine/tests/`: `test_golden_master.py` (TEST-INT-01 equivalent) and `test_docomatic_alignment.py`.
- Confirmed missing: external `Tests/` directory does not exist at the root `Pipeline/` level.
- *Output of this sub-task:* a written audit result comment in `integration_tests_specification.md` for each script: Confirmed Present / Confirmed Absent / Replaced By.

**GAP-31-B · Resolve TEST-INT-01 (run_regression_tests.py)**

- Decision: `engine/tests/test_golden_master.py` is the authoritative implementation of TEST-INT-01.
- Action: Update `integration_tests_specification.md` to reference `engine/tests/test_golden_master.py` as the canonical file path. No new file needed.

**GAP-31-C · Resolve TEST-INT-03 (verify_pages.py)**

- Check if `verify_pages.py` exists anywhere. If absent, implement it:
  - File: `Tests/verify_pages.py` (root repository level).
  - Purpose: for each generated HTML output directory, assert that all `<a href>` internal links resolve to existing files within the output tree.
  - Interface: `python Tests/verify_pages.py --output-dir path/to/ude_output` → exits 0 if all links valid, 1 with a list of broken links.
  - *Technical constraint:* Must not require network access — local file resolution only.

**GAP-31-D · Resolve TEST-INT-04 / TEST-INT-06 (check_links.py)**

- Check if `check_links.py` exists anywhere. If absent, implement it:
  - File: `Tests/check_links.py` (root repository level).
  - Purpose: broader link check that includes Hugo-generated output (validates `href` across markdown → HTML cross-references).
  - Interface: `python Tests/check_links.py --site-dir path/to/hugo_output` → exits 0 on clean, 1 with broken reference list.

**GAP-31-E · Wire the external scripts into a root-level runner**

- File: `Tests/run_all_integration_tests.sh` (or `.bat` for Windows).
- Steps: run golden master, run verify_pages, run check_links; aggregate exit codes.
- Update `integration_tests_specification.md` with accurate file paths for each test.

**Verification:**
```bash
python Tests/verify_pages.py --output-dir ude_output/
# Expected: exit 0 with "All X links verified."
python Tests/check_links.py --site-dir hugo-site/public/
# Expected: exit 0 with link count.
# integration_tests_specification.md must reference all correct paths — manual review required.
```

---

### GAP-32 — Per-Language Integration Test Suites

**Goal:** Implement full `parse → render` integration test suites for each of the four supported languages, exercising Doxygen XML input through to output file structure verification. Current per-language coverage is golden master regression only.

#### Sub-tasks

**GAP-32-A · C++ integration test gaps**

- File: `engine/tests/test_integration_cpp.py` (new).
- Missing coverage per spec:
  - Category landing pages: assert `Classes/index.html` exists and contains class summary table.
  - Overload dispatcher pages: assert an entity with `overloads` list produces a dedicated overload dispatcher page.
  - Member-type index pages: assert `Fields, Structures and Enums/index.html` exists.
- Use existing `engine/tests/assets/main/` C++ XML fixtures; extend fixtures if needed.
- *AI guideline:* Do not create new Doxygen XML from scratch — use `MockAssetLoader` to compose XML strings that exercise the specific C++ features.

**GAP-32-B · C# integration test gaps**

- File: `engine/tests/test_integration_cs.py` (new).
- Missing coverage:
  - Interface entity rendering: assert `entity_type == "interface"` produces correct HTML with `interface` keyword in prototype.
  - Delegate entity rendering: assert `entity_type` containing delegate produces correct page.
  - Event entity rendering: assert event members appear in the member list section.
  - Namespace index pages: assert `<Namespace>/index.html` exists with class table.
- Compose C# XML fixtures to include `<compounddef kind="interface">` and `<memberdef kind="event">` entries.

**GAP-32-C · Java integration test gaps**

- File: `engine/tests/test_integration_java.py` (new).
- Missing coverage:
  - `extends`/`implements` relationships: assert `base_class` is rendered in the class prototype section.
  - Package-level index pages: assert package root `index.html` contains the package class table.
- Compose Java XML fixtures with `<basecompoundref>` elements.

**GAP-32-D · Python integration test gaps**

- File: `engine/tests/test_integration_py.py` (new).
- Missing coverage:
  - `fget`/`fset` property rendering: assert property members display `[get]`/`[set]` accessors in the member list.
  - Dunder method edge cases: assert `__init__`, `__repr__`, `__eq__` appear in the method list (not filtered as private).
- Compose Python XML fixtures with `<memberdef kind="property">` and dunder methods.

**GAP-32-E · Shared test infrastructure for per-language suites**

- Add a `LanguageIntegrationBase` test mixin in `engine/tests/utils.py`:
  ```python
  class LanguageIntegrationBase:
      LANGUAGE: str
      XML_FIXTURE: str  # path to XML fixture directory
      RENDERER_CLASS: type  # concrete renderer class

      def _run_pipeline(self, tmp_path) -> Path:
          """Parse XML → render → return output_dir."""
          ...
  ```
- Each `test_integration_<lang>.py` inherits from `LanguageIntegrationBase` and parameterizes `LANGUAGE`, `XML_FIXTURE`, `RENDERER_CLASS`.

**GAP-32-F · Run full suite and enforce coverage**

- After all 4 language integration test files are complete:
  ```bash
  poetry run pytest tests/test_integration_cpp.py tests/test_integration_cs.py \
    tests/test_integration_java.py tests/test_integration_py.py -v --tb=short
  # Expected: all PASSED.
  poetry run pytest --cov=ude --cov-report=term-missing
  # Coverage must remain ≥ 98%.
  ```

**Verification:**
```bash
poetry run pytest tests/ -v --tb=short 2>&1 | tail -20
# Must show: n passed, 0 failed, 0 errors
# Per-language test count expected: ≥ 5 tests per language (20 new tests minimum across GAP-32).
poetry run pytest --cov=ude --cov-report=term-missing | grep "TOTAL"
# Must show: ≥ 98%
```

---

## Quality Gates (Inherited from v1.0, Enforced Across All Phases)

| Gate | Criterion | How to Verify |
|---|---|---|
| Test Coverage | `≥ 98%` statement coverage | `poetry run pytest --cov=ude --cov-report=term-missing` |
| Performance | `< 5s` for 1,000 API classes (cold build) | `poetry run pytest tests/test_performance_benchmark.py -v` |
| Git Hygiene | Zero compiled output files committed | `git status --short` → no `*.html`, `*.md` output files staged |
| Breaking Change | v1.0 flat CLI (`ude --doc-config ...`) works identically | Full E2E smoke test post-GAP-05 and GAP-01 |
| IR Compatibility | Old `.json.gz` files from v1.0 deserialize into v2.0 `ProjectCatalog` | `load_compressed_ir(v1_file)` must not raise |

---

## Dependency Graph Summary

```
GAP-09 ──► GAP-12
GAP-09 ──► GAP-07
GAP-11  (independent within Phase 1)

GAP-05 ──► GAP-01

GAP-03 ──► GAP-10
GAP-01 ──► GAP-10  (ude audit subcommand stub)

GAP-31  (independent)
GAP-32  (independent; benefits from GAP-03 typed IR but not a hard prerequisite)
```

---

## New File Inventory

| File | Phase | Action |
|---|---|---|
| `engine/ude/config.py` | 1 (GAP-09, GAP-12) | CREATE |
| `engine/ude/collectors/doxyfile.py` | 1 (GAP-11) | CREATE |
| `engine/ude/coverage.py` | 3 (GAP-10) | CREATE |
| `engine/tests/test_config.py` | 1 (GAP-09, GAP-12) | CREATE |
| `engine/tests/test_doxyfile.py` | 1 (GAP-11) | CREATE |
| `engine/tests/test_coverage.py` | 3 (GAP-10) | CREATE |
| `engine/tests/test_integration_cpp.py` | 3 (GAP-32) | CREATE |
| `engine/tests/test_integration_cs.py` | 3 (GAP-32) | CREATE |
| `engine/tests/test_integration_java.py` | 3 (GAP-32) | CREATE |
| `engine/tests/test_integration_py.py` | 3 (GAP-32) | CREATE |
| `Tests/verify_pages.py` | 3 (GAP-31) | CREATE (if absent) |
| `Tests/check_links.py` | 3 (GAP-31) | CREATE (if absent) |
| `Tests/run_all_integration_tests.sh` | 3 (GAP-31) | CREATE |
| `engine/ude/models.py` | 3 (GAP-03) | FULL REWRITE |
| `engine/ude/cli.py` | 2 (GAP-05, GAP-01) | MODIFY |
| `engine/ude/orchestrator.py` | 2 (GAP-05) | MODIFY |
| `engine/ude/storage.py` | 1 (GAP-07), 3 (GAP-03) | MODIFY |
| `engine/ude/interfaces.py` | 1 (GAP-12) | MODIFY (1 line) |
| `engine/ude/collectors/doxygen.py` | 1 (GAP-11), 1 (GAP-09) | MODIFY |
| `engine/ude/renderers/static_html.py` | 1 (GAP-07), 3 (GAP-03) | MODIFY |
| `engine/ude/renderers/hugo_markdown.py` | 1 (GAP-07), 3 (GAP-03) | MODIFY |
| `engine/ude/renderers/legacy.py` | 3 (GAP-03) | MODIFY |
| `engine/tests/test_models.py` | 3 (GAP-03) | REWRITE |
| `engine/tests/test_cli.py` | 2 (GAP-05, GAP-01) | MODIFY |
| `engine/tests/test_orchestrator.py` | 2 (GAP-05) | MODIFY |
| `engine/tests/test_caching.py` | 1 (GAP-07) | MODIFY |
| `engine/tests/test_doxygen_collector.py` | 1 (GAP-11) | MODIFY |

---

*Status: PLAN. Awaiting instruction to begin Phase 1 implementation.*
