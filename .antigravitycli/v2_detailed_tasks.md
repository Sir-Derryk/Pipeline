# UDE v2.0 — Low-Level Technical Task Backlog

**Derived from:** `.antigravitycli/v2_execution_plan.md`  
**Date:** 2026-06-28  
**Total atomic tasks:** 61 (Phase 1: 19 · Phase 2: 13 · Phase 3: 29)

All tasks follow TDD: write failing tests first (RED), implement minimally (GREEN), clean up (REFACTOR).  
Coverage gate: `≥ 98%` statement coverage must hold after every commit boundary.

---

## Phase 1 — Group A: Infrastructure

### GAP-09 — Global Config Field Activation (5 tasks)

---

#### TASK-A.1.1 — Define `GlobalConfig` Pydantic Model

**Targeted files:** `engine/ude/config.py` *(CREATE)*

**Code architecture:**
```python
# engine/ude/config.py
import sys
import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class GlobalConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    doxygen_path: Optional[str] = None
    log_level: str = Field(default="WARNING")
    log_file: Optional[str] = None
    cache_root_dir: Optional[str] = None
    global_templates_dir: Optional[str] = None
    error_policy: str = Field(default="fail-fast")
    translation_service: Optional[str] = None   # v3.0+ reserved
    coverage_mode: str = Field(default="allow-undocumented")   # GAP-10, added here
    coverage_threshold: float = Field(default=1.0, ge=0.0, le=1.0)  # GAP-10

    @classmethod
    def from_file(cls, path: Path) -> "GlobalConfig":
        """Load and validate from a JSON file. Raises FileNotFoundError or ValueError."""
        if not path.exists():
            raise FileNotFoundError(f"Global config not found: {path}")
        import json
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in global config {path}: {e}") from e
        return cls.model_validate(data)
```

**Technical gotchas:**
- `extra="ignore"` is mandatory — unknown keys in user JSON must not raise.
- `log_level` must survive as a raw string; validation/normalisation happens in `logging_setup()`, not here.
- `translation_service` must parse without error but is never acted upon in v2.0.
- `coverage_mode` and `coverage_threshold` are declared here as **Phase 1 schema stubs only** — the fields MUST parse without error, but they are NOT acted upon by any Phase 1 code path. The gate logic is implemented in Phase 3 (TASK-D.2.3). Tests in TASK-A.1.2 MUST verify parsing succeeds; they MUST NOT assert any behavioral effect (e.g., exit codes or log messages) from these fields.

**Test-driven acceptance criteria:**
- `GlobalConfig()` (no args) produces: `log_level="WARNING"`, `error_policy="fail-fast"`, all Optional fields `None`.
- `GlobalConfig.model_validate({"log_level": "DEBUG", "unknown_key": 42})` succeeds; `unknown_key` is silently dropped.
- `GlobalConfig.from_file(non_existent)` raises `FileNotFoundError`.
- `GlobalConfig.from_file(path_with_invalid_json)` raises `ValueError`.
- `GlobalConfig.from_file(path_with_valid_json)` returns a `GlobalConfig` with all fields populated.

**Commit boundary:**
```
feat(config): add GlobalConfig pydantic model with from_file() factory
```

---

#### TASK-A.1.2 — Unit Tests for `GlobalConfig`

**Targeted files:** `engine/tests/test_config.py` *(CREATE)*

**Code architecture:**
```python
import json, pytest
from pathlib import Path
from ude.config import GlobalConfig

def test_global_config_defaults():
    cfg = GlobalConfig()
    assert cfg.log_level == "WARNING"
    assert cfg.error_policy == "fail-fast"
    assert cfg.doxygen_path is None

def test_global_config_extra_keys_ignored():
    cfg = GlobalConfig.model_validate({"log_level": "DEBUG", "future_field": 99})
    assert cfg.log_level == "DEBUG"
    assert not hasattr(cfg, "future_field")

def test_global_config_from_file_success(tmp_path):
    p = tmp_path / "g.json"
    p.write_text(json.dumps({"log_level": "INFO", "error_policy": "continue-on-error"}))
    cfg = GlobalConfig.from_file(p)
    assert cfg.log_level == "INFO"
    assert cfg.error_policy == "continue-on-error"

def test_global_config_from_file_missing():
    with pytest.raises(FileNotFoundError):
        GlobalConfig.from_file(Path("/nonexistent/config.json"))

def test_global_config_from_file_bad_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json}")
    with pytest.raises(ValueError):
        GlobalConfig.from_file(p)

def test_global_config_coverage_threshold_parses():
    # Phase 1 stub: field must accept valid floats without error
    cfg = GlobalConfig.model_validate({"coverage_threshold": 0.85})
    assert cfg.coverage_threshold == 0.85

def test_global_config_coverage_threshold_bounds():
    # Must reject out-of-range values (ge=0.0, le=1.0 constraint)
    with pytest.raises(Exception):   # pydantic ValidationError
        GlobalConfig.model_validate({"coverage_threshold": 1.5})
```

**Technical gotchas:**
- Import must be `from ude.config import GlobalConfig` — the module does not exist yet, so this test file is the RED step that will fail until TASK-A.1.1 is done.
- `test_global_config_coverage_threshold_parses` verifies the field is a parseable Phase 1 stub — it MUST NOT assert any behavioral side effect (no exit code, no gate logic).

**Test-driven acceptance criteria:**
- `pytest tests/test_config.py` → 7 PASSED, 0 FAILED.

**Commit boundary:**  
*(Combined with TASK-A.1.1 into one commit — both the module and its tests are committed together.)*

---

#### TASK-A.1.3 — Wire `GlobalConfig` into `UdeOrchestrator`

**Targeted files:** `engine/ude/orchestrator.py` *(MODIFY)*

**Code architecture:**
- In `UdeOrchestrator.__init__()`, replace the raw `json.load` block with:
  ```python
  from ude.config import GlobalConfig
  self._global_cfg = GlobalConfig()          # safe default
  if self.global_config_path and self.global_config_path.exists():
      try:
          self._global_cfg = GlobalConfig.from_file(self.global_config_path)
      except Exception as e:
          logger.warning(f"Failed to load global config {self.global_config_path}: {e}")
  self.global_config = self._global_cfg.model_dump()  # keep legacy dict for downstream
  ```
- In `run_target()`, resolve and activate `doxygen_path`:
  ```python
  if self._global_cfg.doxygen_path:
      import os
      os.environ.setdefault("PATH",
          str(Path(self._global_cfg.doxygen_path).resolve()) +
          os.pathsep + os.environ.get("PATH", ""))
  ```
- Resolve `cache_root_dir` to an absolute `Path` and store as `self._cache_root: Optional[Path]`:
  ```python
  if self._global_cfg.cache_root_dir and self.global_config_path:
      self._cache_root = (
          self.global_config_path.parent / self._global_cfg.cache_root_dir
      ).resolve()
  else:
      self._cache_root = None
  ```
- Resolve `global_templates_dir` and store as `self._global_templates_dir: Optional[Path]`.

**Technical gotchas:**
- `os.environ.setdefault` must be used (not `os.environ[]=`), so an already-set PATH from the OS is never overwritten entirely.
- `self.global_config = self._global_cfg.model_dump()` preserves backward compatibility for any code that reads `self.global_config` as a raw dict.
- Do **not** call `logging_setup()` here yet — that is TASK-A.2.3.

**Test-driven acceptance criteria:**
- `test_orchestrator_stores_global_cfg_instance` — after init with a valid global config file, `orchestrator._global_cfg` is a `GlobalConfig` instance.
- `test_orchestrator_sets_path_from_doxygen_path` (mock `subprocess.run`) — when `doxygen_path="/opt/doxygen/bin"` is in global config, `os.environ["PATH"]` contains that path before Doxygen is invoked.
- `test_orchestrator_cache_root_resolved_absolute` — `orchestrator._cache_root` is an absolute `Path` when `cache_root_dir` is set.
- `test_orchestrator_global_cfg_default_on_missing_file` — init with a non-existent path sets `_global_cfg` to defaults (no exception raised).

**Commit boundary:**
```
feat(config): wire GlobalConfig into UdeOrchestrator init and run_target
```

---

#### TASK-A.1.4 — Wire `GlobalConfig` into `cli.py:run_pipeline()`

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
- At the top of `run_pipeline()`, after the file-existence checks, replace the raw `json.load` global-config block:
  ```python
  from ude.config import GlobalConfig
  global_cfg = GlobalConfig()
  if global_config_path is not None:
      try:
          global_cfg = GlobalConfig.from_file(global_config_path)
      except Exception as e:
          print(f"Error: Failed to parse global config: {e}", file=sys.stderr)
          return 1
  global_config: dict = global_cfg.model_dump(exclude_none=False)
  ```
- Apply `doxygen_path` → PATH injection (same logic as TASK-A.1.3, extracted to a shared helper `apply_global_cfg_env(cfg: GlobalConfig) -> None` in `config.py` to avoid duplication).

**Technical gotchas:**
- `global_config: dict = global_cfg.model_dump(...)` must retain the same variable name so the remainder of `run_pipeline()` (which uses `global_config` as a dict) works without further changes.
- `apply_global_cfg_env()` must live in `config.py`, not duplicated in both `orchestrator.py` and `cli.py`.

**Test-driven acceptance criteria:**
- `test_cli_run_pipeline_bad_global_json` — calling `run_pipeline()` with a malformed JSON global config returns exit code `1` and prints to stderr.
- `test_cli_run_pipeline_missing_global_file` (existing test) — must still pass unchanged.
- Full existing `test_cli.py` suite passes without regression.

**Commit boundary:**
```
feat(config): wire GlobalConfig into cli.py run_pipeline
```

---

#### TASK-A.1.5 — Add `apply_global_cfg_env()` Helper to `config.py`

**Targeted files:** `engine/ude/config.py` *(MODIFY)*

**Code architecture:**
```python
def apply_global_cfg_env(cfg: GlobalConfig) -> None:
    """Injects doxygen_path into PATH if set. Safe to call multiple times."""
    import os
    if cfg.doxygen_path:
        doxy_dir = str(Path(cfg.doxygen_path).resolve())
        current_path = os.environ.get("PATH", "")
        if doxy_dir not in current_path.split(os.pathsep):
            os.environ["PATH"] = doxy_dir + os.pathsep + current_path
```

**Technical gotchas:**
- The idempotency check (`if doxy_dir not in current_path.split(...)`) prevents PATH from growing unboundedly when the orchestrator is called multiple times in the same process (e.g., in tests).

**Test-driven acceptance criteria (added to `test_config.py`):**
- `test_apply_global_cfg_env_injects_path` — after calling `apply_global_cfg_env`, the directory appears in `os.environ["PATH"]`.
- `test_apply_global_cfg_env_idempotent` — calling it twice does not duplicate the entry.
- `test_apply_global_cfg_env_noop_when_none` — `doxygen_path=None` leaves PATH unchanged.

**Commit boundary:**
```
feat(config): add apply_global_cfg_env helper; wire into orchestrator and cli
```

---

### GAP-12 — Unified Logging (4 tasks)

---

#### TASK-A.2.1 — Fix HC-05: Incorrect Logger Label in `interfaces.py`

**Targeted files:** `engine/ude/interfaces.py` *(MODIFY)*

**Code architecture:**
- Line 8: change `logging.getLogger("ude.renderers")` → `logging.getLogger("ude.interfaces")`

**Technical gotchas:**
- Search all test files for assertions against `"ude.renderers"` that originate from `interfaces.py`. Any `caplog` fixture that asserts `record.name == "ude.renderers"` for a log emitted by `_interpolate_content()` or `_load_static_file()` must be updated to `"ude.interfaces"`.
- The renderer modules (`static_html.py`, `hugo_markdown.py`) each define their own logger (`"ude.renderers.static_html"`, etc.) — these are unaffected.

**Test-driven acceptance criteria:**
- After the rename, `logging.getLogger("ude.interfaces")` is the logger used for warnings in `_interpolate_content()` and `_load_static_file()`.
- `pytest tests/ -v` → zero failures (regression gate).
- `grep -rn '"ude.renderers"' engine/ude/interfaces.py` → no results.

**Commit boundary:**
```
fix(interfaces): correct logger name from ude.renderers to ude.interfaces (HC-05)
```

---

#### TASK-A.2.2 — Implement `logging_setup()` in `config.py`

**Targeted files:** `engine/ude/config.py` *(MODIFY)*

**Code architecture:**
```python
import logging, sys

_UDE_FORMATTER = logging.Formatter("%(levelname)s [%(name)s] %(message)s")
_UDE_FILE_FORMATTER = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")

def logging_setup(cfg: GlobalConfig) -> None:
    """Configure the root UDE logger. Safe to call multiple times (clears handlers)."""
    root = logging.getLogger("ude")
    root.handlers.clear()
    try:
        root.setLevel(cfg.log_level.upper())
    except (ValueError, AttributeError):
        root.setLevel(logging.WARNING)

    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(_UDE_FORMATTER)
    root.addHandler(sh)

    if cfg.log_file:
        try:
            fh = logging.FileHandler(cfg.log_file, encoding="utf-8")
            fh.setFormatter(_UDE_FILE_FORMATTER)
            root.addHandler(fh)
        except OSError as e:
            root.warning(f"Could not open log file {cfg.log_file!r}: {e}")
```

**Technical gotchas:**
- `root.handlers.clear()` prevents handler accumulation across test runs. Without this, pytest test isolation fails because each `UdeOrchestrator()` instantiation adds another handler.
- The `try/except` around `setLevel` guards against a user providing an invalid string like `"VERBOSE"` — fall back to WARNING silently.
- `OSError` on `FileHandler` must not crash the engine — log the warning and continue with stderr only.
- The `root` logger is `"ude"`, not the Python root `""`. This scopes all UDE output without hijacking third-party library logging.

**Test-driven acceptance criteria (added to `test_config.py`):**
- `test_logging_setup_stderr_only` — after `logging_setup(GlobalConfig())`, `logging.getLogger("ude")` has exactly 1 handler, which is a `StreamHandler`.
- `test_logging_setup_with_log_file(tmp_path)` — after `logging_setup(GlobalConfig(log_file=str(tmp_path/"ude.log")))`, logger has 2 handlers; the file is created.
- `test_logging_setup_level_debug` — `GlobalConfig(log_level="DEBUG")` → `logging.getLogger("ude").level == logging.DEBUG`.
- `test_logging_setup_invalid_level` — `GlobalConfig(log_level="VERBOSE")` → level falls back to `WARNING`, no exception.
- `test_logging_setup_idempotent` — calling `logging_setup` twice results in exactly 1 handler (not 2).
- `test_logging_setup_bad_log_file` — invalid file path does not raise; stderr handler still present.

**Commit boundary:**
```
feat(config): implement logging_setup() with StreamHandler and optional FileHandler
```

---

#### TASK-A.2.3 — Wire `logging_setup()` into Startup Points

**Targeted files:** `engine/ude/orchestrator.py` *(MODIFY)*, `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
- In `UdeOrchestrator.__init__()`, immediately after `self._global_cfg` is set (end of TASK-A.1.3 block):
  ```python
  from ude.config import logging_setup
  logging_setup(self._global_cfg)
  ```
- In `cli.py:run_pipeline()`, immediately after `global_cfg` is assigned (end of TASK-A.1.4 block):
  ```python
  from ude.config import logging_setup
  logging_setup(global_cfg)
  ```
- Remove the ad-hoc partial logging setup in `orchestrator.py:run_target()` (lines ~160–163):
  ```python
  # REMOVE THIS BLOCK (replaced by logging_setup in __init__):
  log_cfg = resolved_global_config.get("logging", {})
  if "level" in log_cfg:
      logging.getLogger().setLevel(log_cfg["level"].upper())
  ```

**Technical gotchas:**
- The removed ad-hoc block set the **root Python logger** (`logging.getLogger()`) instead of the scoped `"ude"` logger. Removing it fixes scope bleed but is a behavioral change — verify no tests relied on root logger level being changed.
- After removal, run `grep -n 'logging.getLogger()' engine/ude/orchestrator.py` → must return no results (the root logger must never be touched by UDE code).

**Test-driven acceptance criteria:**
- `test_orchestrator_calls_logging_setup(monkeypatch)` — monkeypatch `ude.config.logging_setup`; assert it is called once during `UdeOrchestrator()` init.
- `test_cli_calls_logging_setup(monkeypatch)` — monkeypatch `ude.config.logging_setup`; assert it is called once during `run_pipeline()`.
- Full test suite passes without regression.

**Commit boundary:**
```
feat(logging): wire logging_setup into UdeOrchestrator and cli startup
```

---

#### TASK-A.2.4 — Remove Orphan Logging Config Key from Orchestrator

**Targeted files:** `engine/ude/orchestrator.py` *(MODIFY)*

**Code architecture:**
- Search and remove any remaining reference to `resolved_global_config.get("logging", {})`.
- Confirm the orchestrator no longer contains `logging.getLogger()` (the root) — only named `logging.getLogger("ude.orchestrator")`.

**Technical gotchas:**
- If any existing test explicitly sets `{"logging": {"level": "DEBUG"}}` in a test fixture's global config dict, that test must be updated to use the top-level `"log_level"` key instead (the new `GlobalConfig` schema).

**Test-driven acceptance criteria:**
- `grep -n 'get("logging"' engine/ude/orchestrator.py` → 0 results.
- `pytest tests/test_orchestrator.py -v` → all PASSED.

**Commit boundary:**
*(Included in TASK-A.2.3 commit — one atomic change.)*

---

### GAP-07 — L2 Render Cache Activation (6 tasks)

---

#### TASK-A.3.1 — Add `compute_template_hash()` to `storage.py`

**Targeted files:** `engine/ude/storage.py` *(MODIFY)*

**Code architecture:**
```python
def compute_template_hash(template_dir: Path) -> str:
    """SHA-256 of all files in template_dir sorted alphabetically by relative path.

    Returns empty string if directory is absent or empty (cache effectively disabled).
    """
    if not template_dir.exists() or not template_dir.is_dir():
        return ""
    files = sorted(template_dir.rglob("*"))
    files = [f for f in files if f.is_file()]
    if not files:
        return ""
    combined = b"".join(f.read_bytes() for f in files)
    return calculate_sha256(combined)
```

**Technical gotchas:**
- Sorting must use `str(f.relative_to(template_dir))` not `f.name` — otherwise files in different subdirectories with the same name can produce identical hashes for distinct template sets.
- `rglob("*")` on a very large template dir is acceptable; UDE templates are small (< 50 files).
- Returns `""` (empty string) when directory is absent — callers treat `""` as "always stale" (no cache hit possible), which is the safe fallback.

**Test-driven acceptance criteria (added to `test_storage.py`):**
- `test_compute_template_hash_stable` — same directory contents → same hash on two calls.
- `test_compute_template_hash_changes_on_content_change` — modify one file → different hash.
- `test_compute_template_hash_empty_dir` → returns `""`.
- `test_compute_template_hash_missing_dir` → returns `""` (no exception).

**Commit boundary:**
```
feat(storage): add compute_template_hash() for L2 cache invalidation
```

---

#### TASK-A.3.2 — Add `cache_manager` Parameter to Renderer Constructors

**Targeted files:** `engine/ude/renderers/static_html.py` *(MODIFY)*, `engine/ude/renderers/hugo_markdown.py` *(MODIFY)*, `engine/ude/renderers/legacy.py` *(MODIFY)*

**Code architecture:**
- Each concrete renderer `__init__` must accept `cache_manager: Optional["BuildCacheManager"] = None`:
  ```python
  from ude.storage import BuildCacheManager   # TYPE_CHECKING import acceptable

  class CppHtmlDefaultRenderer(HtmlRenderer):
      def __init__(self, ..., cache_manager: Optional[BuildCacheManager] = None):
          super().__init__(..., cache_manager=cache_manager)
  ```
- `HtmlRenderer.__init__()` stores it: `self._cache_mgr = cache_manager`.
- Same pattern for `HugoMarkdownRenderer` base and all 8 Hugo concrete subclasses.
- Same for `legacy.py` base and 8 legacy concrete subclasses.

**Technical gotchas:**
- `HtmlRenderer` uses `__new__` as a factory — the `cache_manager` kwarg must be forwarded through `__new__` into the subclass `__init__`. Verify the `__new__` signature includes `**kwargs` or explicitly lists `cache_manager`.
- `cache_manager=None` is the default — zero behavior change for all existing code paths that do not pass it.
- Do **not** import `BuildCacheManager` at module top level in renderer files (circular import risk). Use `TYPE_CHECKING` guard:
  ```python
  from typing import TYPE_CHECKING
  if TYPE_CHECKING:
      from ude.storage import BuildCacheManager
  ```

**Test-driven acceptance criteria:**
- `HtmlRenderer(language="cpp", cache_manager=None)` instantiates without error.
- `HtmlRenderer(language="cpp", cache_manager=mock_cache_mgr)` stores `_cache_mgr = mock_cache_mgr`.
- All existing renderer tests pass without modification.
- **Mandatory factory kwarg verification (Pydantic Guard Step 5) — run for ALL THREE renderer families:**
  ```bash
  # bash / Git Bash / WSL / CI
  for f in engine/ude/renderers/static_html.py \
            engine/ude/renderers/hugo_markdown.py \
            engine/ude/renderers/legacy.py; do
    echo "=== $f ==="
    grep -n "def __new__\|def __init__\|cache_manager" "$f"
  done
  ```
  ```powershell
  # Windows PowerShell
  foreach ($f in @("engine/ude/renderers/static_html.py",
                   "engine/ude/renderers/hugo_markdown.py",
                   "engine/ude/renderers/legacy.py")) {
      Write-Host "=== $f ===" -ForegroundColor Cyan
      Select-String -Path $f -Pattern "def __new__|def __init__|cache_manager"
  }
  ```
  For each file: `cache_manager` MUST appear in both the `__new__` method signature (or `**kwargs`) AND be forwarded through `super().__init__(...)`. A gap in `hugo_markdown.py` or `legacy.py` is as fatal as a gap in `static_html.py`.

**Commit boundary:**
```
feat(renderers): add optional cache_manager parameter to all renderer constructors
```

---

#### TASK-A.3.3 — Wire `write_if_changed()` in `HtmlRenderer`

**Targeted files:** `engine/ude/renderers/static_html.py` *(MODIFY)*

**Code architecture:**
- Identify every `open(path, "w").write(content)` call in the renderer's `render()` method and its private helpers (e.g., `_write_entity_page()`, `_write_index_page()`).
- Replace each with a wrapper:
  ```python
  def _write_output(self, path: Path, content: str, entity_signature: str) -> bool:
      """Write file using L2 cache if available; return True if write executed."""
      template_hash = getattr(self, "_template_hash", "")
      if self._cache_mgr is not None:
          return self._cache_mgr.write_if_changed(path, content, entity_signature, template_hash)
      path.parent.mkdir(parents=True, exist_ok=True)
      with open(path, "w", encoding="utf-8") as f:
          f.write(content)
      return True
  ```
- Compute `_template_hash` once at the start of `render()`:
  ```python
  from ude.storage import compute_template_hash
  self._template_hash = compute_template_hash(self._template_dir)
  ```
- Replace every direct file write with `self._write_output(path, content, entity_sig)`.
- `entity_signature` = `calculate_sha256(entity.fully_qualified_name + entity.model_dump_json())`.

**Technical gotchas:**
- The `entity_signature` must change whenever the entity's IR data changes — use the full `model_dump_json()` not just the name.
- Static asset copies (`shutil.copy`) are **not** managed by the L2 cache — only generated HTML content files.
- After all writes in `render()`, call `self._cache_mgr.save()` once if `self._cache_mgr` is not None.

**Test-driven acceptance criteria (added to `test_caching.py`):**
- `test_l2_html_cache_hit_skips_write(tmp_path)` — render once; delete one output HTML file; render again with same catalog and templates; assert the deleted file is NOT recreated (cache hit).
- `test_l2_html_cache_miss_on_catalog_change(tmp_path)` — render once; mutate one method's docstring in the catalog; render again; assert output file IS recreated.
- `test_l2_html_cache_disabled_when_no_manager(tmp_path)` — `cache_manager=None`; render twice; assert files written both times (no skip).

**Commit boundary:**
```
feat(renderers): wire BuildCacheManager.write_if_changed into HtmlRenderer output
```

---

#### TASK-A.3.4 — Wire `write_if_changed()` in `HugoMarkdownRenderer` and `LegacyRenderer`

**Targeted files:** `engine/ude/renderers/hugo_markdown.py` *(MODIFY)*, `engine/ude/renderers/legacy.py` *(MODIFY)*

**Code architecture:**
- Identical pattern to TASK-A.3.3 — add `_write_output()` helper to `HugoMarkdownRenderer` base class; replace all `open(path, "w").write(...)` calls.
- Same for legacy renderer base.

**Technical gotchas:**
- Hugo output is Markdown (`.md` files); `entity_signature` for Hugo is `calculate_sha256(entity.fully_qualified_name + "hugo" + entity.model_dump_json())` — include `"hugo"` to prevent L2 hash collisions between HTML and Hugo outputs for the same entity when they share a `cache_dir`.

**Test-driven acceptance criteria:**
- `test_l2_hugo_cache_hit_skips_write(tmp_path)` — same pattern as HTML test.
- `test_l2_legacy_cache_hit_skips_write(tmp_path)`.
- Full test suite: `pytest tests/ -v` → 0 failures.
- **Mandatory `__new__` factory kwarg forwarding verification** for `hugo_markdown.py` and `legacy.py` (identical commands as TASK-A.3.2 acceptance criteria — run both bash and PowerShell forms). `cache_manager` must appear in `__new__` signature AND be forwarded via `super().__init__(...)` in both files before this task is considered complete.

**Commit boundary:**
```
feat(renderers): wire BuildCacheManager.write_if_changed into Hugo and Legacy renderers
```

---

#### TASK-A.3.5 — Thread `cache_dir` from `UdeOrchestrator` to Renderer Factory

**Targeted files:** `engine/ude/orchestrator.py` *(MODIFY)*

**Code architecture:**
- In `run_target()`, compute `cache_dir` before renderer instantiation:
  ```python
  from ude.storage import BuildCacheManager
  cache_mgr = None
  if self._cache_root is not None:
      target_slug = config_file_path.stem   # e.g. "ude_doc_config"
      cache_dir = self._cache_root / target_slug
      cache_dir.mkdir(parents=True, exist_ok=True)
      cache_mgr = BuildCacheManager(product_dir=cache_dir)
  ```
- Pass `cache_manager=cache_mgr` to the renderer constructor call.
- After `renderer.render(catalog, str(out_dir))`, call `cache_mgr.save()` if not None.

**Technical gotchas:**
- `target_slug` must be derived from the config file path, not the CWD, to keep cache dirs isolated per target when multiple targets share a global cache root.
- The same `BuildCacheManager` instance must be shared for a single `run_target()` call — do not instantiate it twice.
- In `cli.py:run_pipeline()`, the same threading must be added (using `global_cfg.cache_root_dir`).

**Test-driven acceptance criteria:**
- `test_orchestrator_passes_cache_mgr_to_renderer(monkeypatch, tmp_path)` — monkeypatch the renderer class; assert the `cache_manager` kwarg is a `BuildCacheManager` instance when `cache_root_dir` is set in global config.
- `test_orchestrator_no_cache_mgr_when_no_root(monkeypatch, tmp_path)` — `cache_root_dir` absent in global config; `cache_manager` kwarg is `None`.

**Commit boundary:**
```
feat(orchestrator): thread BuildCacheManager through orchestrator to renderer factory
```

---

#### TASK-A.3.6 — Integration Test: Sequential Build Cache Verification

**Targeted files:** `engine/tests/test_caching.py` *(MODIFY)*

**Code architecture:**
```python
def test_sequential_build_l2_cache_hits(tmp_path):
    """Second identical run must not write any HTML files."""
    cfg_file = _write_test_config(tmp_path, cache_root_dir=str(tmp_path / "cache"))
    orchestrator = UdeOrchestrator(global_config_path=cfg_file)
    orchestrator.run(doc_config_path=...)   # first run: writes files

    written_files_run1 = list((tmp_path / "output").rglob("*.html"))
    mtimes_run1 = {f: f.stat().st_mtime for f in written_files_run1}

    orchestrator.run(doc_config_path=...)   # second run: cache hits

    mtimes_run2 = {f: f.stat().st_mtime for f in written_files_run1}
    # All mtimes must be IDENTICAL — no files were rewritten
    assert mtimes_run1 == mtimes_run2
```

**Technical gotchas:**
- `st_mtime` precision varies by OS (FAT32 is 2-second granular; NTFS is 100ns). The `mtimes_run1 == mtimes_run2` assertion is unreliable on Windows if the two runs complete within the precision window.
- **Primary strategy (mandatory):** Use `pytest-mock` / `monkeypatch` to patch the file-write call and assert it was never invoked on the second run. Example:
  ```python
  def test_sequential_build_l2_cache_hits(tmp_path, mocker):
      write_spy = mocker.patch("builtins.open", wraps=open)
      orchestrator.run(...)   # first run
      write_spy.reset_mock()
      orchestrator.run(...)   # second run — cache hit
      write_calls = [c for c in write_spy.call_args_list if "w" in str(c)]
      assert len(write_calls) == 0, f"Unexpected writes on second run: {write_calls}"
  ```
- The `st_mtime` approach MAY be used as a secondary assertion in addition to the mock check, but never as the sole verification.

**Test-driven acceptance criteria:**
- `pytest tests/test_caching.py::test_sequential_build_l2_cache_hits -v` → PASSED.

**Commit boundary:**
*(Included in TASK-A.3.5 commit.)*

---

### GAP-11 — Doxyfile Key-Level 3-Tier Merge (4 tasks)

---

#### TASK-A.4.1 — Create `doxyfile.py` with Parser and Serializer

**Targeted files:** `engine/ude/collectors/doxyfile.py` *(CREATE)*

**Code architecture:**
```python
# engine/ude/collectors/doxyfile.py
import logging
from typing import Optional

logger = logging.getLogger("ude.collector.doxyfile")

def parse_doxyfile(content: str) -> dict[str, str]:
    """Parse Doxyfile text into {KEY: VALUE} dict.

    Rules:
    - Lines starting with '#' or blank are skipped.
    - Continuation lines ending with '\\' are joined.
    - Each 'KEY = VALUE' splits on the first '='.
    - Multiple values for the same key are space-joined (last overrides only for
      single-value keys; for multi-value keys like INPUT, values accumulate).
    """
    joined_lines = []
    buffer = ""
    for line in content.splitlines():
        stripped = line.rstrip()
        if stripped.endswith("\\"):
            buffer += stripped[:-1] + " "
        else:
            buffer += stripped
            joined_lines.append(buffer.strip())
            buffer = ""
    if buffer.strip():
        joined_lines.append(buffer.strip())

    result: dict[str, str] = {}
    for line in joined_lines:
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        if key in result:
            result[key] = result[key] + " " + val if val else result[key]
        else:
            result[key] = val
    return result


def serialize_doxyfile(kvs: dict[str, str]) -> str:
    """Serialize a key-value dict back to Doxyfile text (keys sorted alphabetically)."""
    lines = [f"{k} = {v}" for k, v in sorted(kvs.items())]
    return "\n".join(lines) + "\n"


def merge_doxyfile_tiers(
    t1: dict[str, str],
    t2: dict[str, str],
    t3: dict[str, str],
) -> dict[str, str]:
    """Merge three Doxyfile dicts: T1 = base, T2 overrides T1, T3 overrides T2."""
    result = dict(t1)
    for key, val in t2.items():
        if key in result and result[key] != val:
            logger.debug("Doxyfile T2 overrides T1 for key '%s': '%s' -> '%s'", key, result[key], val)
        result[key] = val
    for key, val in t3.items():
        if key in result and result[key] != val:
            logger.debug("Doxyfile T3 overrides T2 for key '%s': '%s' -> '%s'", key, result[key], val)
        result[key] = val
    return result
```

**Technical gotchas:**
- `partition("=")` (not `split("=", 1)`) cleanly separates key from value including values that contain `=` (e.g. `PREDEFINED = FOO=1`).
- The accumulation strategy for duplicate keys (space-join) mirrors Doxygen's own last-value-wins for single-value keys, while allowing multi-value keys like `INPUT` to be built up across tiers.

**Test-driven acceptance criteria (new `test_doxyfile.py`):**
- `test_parse_basic` — `"PROJECT_NAME = MyLib\nGENERATE_XML = YES\n"` → `{"PROJECT_NAME": "MyLib", "GENERATE_XML": "YES"}`.
- `test_parse_skip_comments_and_blanks` — comments and blank lines produce no entries.
- `test_parse_continuation_lines` — `"INPUT = src\\\n    include\n"` → `{"INPUT": "src  include"}` (joined).
- `test_parse_value_with_equals` — `"PREDEFINED = FOO=1"` → `{"PREDEFINED": "FOO=1"}`.
- `test_serialize_round_trip` — parse then serialize; all keys present, alphabetically ordered.
- `test_merge_t2_overrides_t1` — key in T1 and T2 → T2 value wins.
- `test_merge_t3_overrides_t2` — key in T1, T2, T3 → T3 value wins.
- `test_merge_debug_log(caplog)` — conflict in T2 vs T1 triggers a `DEBUG` log entry containing the key name.
- `test_merge_missing_tiers` — `merge_doxyfile_tiers({}, {}, t3)` → result equals `t3`.

**Commit boundary:**
```
feat(collector): add doxyfile.py with key-level parser, serializer and 3-tier merge
```

---

#### TASK-A.4.2 — Unit Tests for `doxyfile.py`

**Targeted files:** `engine/tests/test_doxyfile.py` *(CREATE)*

*(Tests listed in TASK-A.4.1 acceptance criteria above — this is the dedicated test file commit.)*

**Commit boundary:**
*(Combined with TASK-A.4.1 — ship module and tests together.)*

---

#### TASK-A.4.3 — Refactor `DoxygenXmlCollector.collect()` to Use Key-Level Merge

**Targeted files:** `engine/ude/collectors/doxygen.py` *(MODIFY)*

**Code architecture:**
- Replace lines 99–138 (the string concatenation block) with:
  ```python
  from ude.collectors.doxyfile import parse_doxyfile, serialize_doxyfile, merge_doxyfile_tiers

  # T1: global engine Doxyfile template
  # Priority: GlobalConfig.global_templates_dir (user-configured), then source-relative fallback.
  t1: dict[str, str] = {}
  _configured_dir = (
      Path(global_cfg.global_templates_dir) if global_cfg.global_templates_dir else None
  )
  _fallback_dir = Path(__file__).resolve().parent.parent / "templates"
  _t1_dir = _configured_dir if (_configured_dir and _configured_dir.is_dir()) else _fallback_dir
  global_template = _t1_dir / "Doxyfile"
  if global_template.exists():
      t1 = parse_doxyfile(global_template.read_text(encoding="utf-8"))

  # T2: target-specific Doxyfile template
  t2: dict[str, str] = {}
  if doxy_template.exists():
      t2 = parse_doxyfile(doxy_template.read_text(encoding="utf-8"))
  else:
      raise CollectorError(f"Doxyfile template {doxy_template} does not exist")

  # T3: runtime parameters (always win)
  t3: dict[str, str] = {
      "OUTPUT_DIRECTORY": f'"{temp_xml_path}"',
      "GENERATE_XML": "YES",
      "XML_OUTPUT": "xml",
      "INPUT": f'"{src_dir}"',
      "RECURSIVE": "YES",
      "GENERATE_HTML": "NO",
      "GENERATE_LATEX": "NO",
  }
  language = collector_cfg.get("language", "").lower()
  if language in ("java", "python"):
      t3["OPTIMIZE_OUTPUT_JAVA"] = "YES"

  merged = merge_doxyfile_tiers(t1, t2, t3)
  doxy_content = serialize_doxyfile(merged)
  ```
- Write `doxy_content` to `temp_doxyfile` (unchanged from current code).

**Technical gotchas:**
- **T1 path resolution:** T1 first tries `GlobalConfig.global_templates_dir / "Doxyfile"` (user-configured). If that directory does not exist or is not set, it falls back to `Path(__file__).resolve().parent.parent / "templates" / "Doxyfile"` (source-relative). Both paths are resolved before `parse_doxyfile()` is called — never hardcode the source-relative path as the only option.
- The old code appended `"\n"` between tiers; the new serializer handles formatting. Ensure the temp Doxyfile content does not start with a blank line that confuses Doxygen.
- `"OUTPUT_DIRECTORY"` value is quoted in the old code (`f'"{temp_xml_path}"'`) — preserve this quoting in T3.
- The `validate_environment()` method still reads the raw Doxyfile template; it must not be changed to use `parse_doxyfile()` — it only checks file existence.

**Test-driven acceptance criteria (added to `test_doxygen_collector.py`):**
- `test_collector_uses_merged_doxyfile(monkeypatch, tmp_path)` — mock `subprocess.run`; capture the written temp Doxyfile path; read it and call `parse_doxyfile()`; assert T3 keys (`OUTPUT_DIRECTORY`, `GENERATE_XML`, `INPUT`) are present exactly once.
- `test_collector_t3_overrides_t2_key(monkeypatch, tmp_path)` — write a target Doxyfile template that sets `GENERATE_HTML = YES`; after merge, assert the written Doxyfile has `GENERATE_HTML = NO` (T3 wins).
- `test_collector_no_global_template(monkeypatch, tmp_path)` — remove the global Doxyfile template file; collector still succeeds with T2+T3 only.

**Commit boundary:**
```
feat(collector): replace Doxyfile string concatenation with 3-tier key-level merge
```

---

#### TASK-A.4.4 — Validate Phase 1 Coverage Gate

**Targeted files:** `engine/tests/` *(RUN ONLY — no file changes)*

**Code architecture:**
```bash
cd engine
poetry run pytest --cov=ude --cov-report=term-missing -q
```

**Technical gotchas:**
- If coverage drops below 98%, identify the uncovered lines (usually exception branches in `doxyfile.py` or new `config.py` helpers) and add targeted tests before the Phase 1 merge.

**Test-driven acceptance criteria:**
- `pytest` exits with code `0` (all tests pass).
- Coverage report `TOTAL` line shows `>= 98%`.
- `pytest tests/test_config.py tests/test_doxyfile.py tests/test_caching.py -v` → all PASSED.

**Commit boundary:**
```
test(phase1): confirm ≥98% coverage gate after infrastructure changes
```

---

## Phase 2 — Group B: Library API & CLI Unification

### GAP-05 — UdeOrchestrator Library API (7 tasks)

---

#### TASK-B.1.1 — Relocate `deep_merge()` and `find_product_json()` from `cli.py` to `orchestrator.py`

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*, `engine/ude/orchestrator.py` *(MODIFY — verify already present)*

**Code architecture:**
- `orchestrator.py` already contains both functions. Confirm their signatures are identical to the copies in `cli.py`.
- Delete `deep_merge()` and `find_product_json()` from `cli.py`.
- At the top of `cli.py`, add:
  ```python
  from ude.orchestrator import deep_merge, find_product_json
  ```
- Update `engine/tests/test_cli.py` line 10:
  ```python
  # BEFORE:
  from ude.cli import main, find_product_json, run_pipeline, deep_merge
  # AFTER:
  from ude.cli import main, run_pipeline
  from ude.orchestrator import deep_merge, find_product_json
  ```

**Technical gotchas:**
- The two existing implementations are functionally identical but may have minor docstring differences. Keep the `orchestrator.py` version verbatim — do not merge/combine docstrings.
- After this change, running `python -c "from ude.cli import deep_merge"` must still work (the re-export via `from ude.orchestrator import deep_merge` in `cli.py` makes `deep_merge` importable from `ude.cli` as well).

**Test-driven acceptance criteria:**
- `from ude.cli import deep_merge` → still importable (no `ImportError`).
- `from ude.orchestrator import deep_merge, find_product_json` → importable.
- `pytest tests/test_cli.py tests/test_orchestrator.py -v` → all PASSED.
- `grep -n "^def deep_merge" engine/ude/cli.py` → 0 results (function removed from cli.py).

**Commit boundary:**
```
refactor(cli): consolidate deep_merge and find_product_json into orchestrator module
```

---

#### TASK-B.1.2 — Extract `resolve_config()` Helper in `orchestrator.py`

**Targeted files:** `engine/ude/orchestrator.py` *(MODIFY)*

**Code architecture:**
```python
def resolve_config(
    config_file_path: Path,
    global_cfg: "GlobalConfig",
    global_config_path: Optional[Path] = None,
) -> tuple[dict, Path, dict]:
    """Load, merge (global→sdk→doc), and return (merged_config, config_dir, sidebar_config).

    Raises:
        UdeException: If config file cannot be read.
    """
    # 1. Resolve global config dict
    resolved_global = global_cfg.model_dump(exclude_none=False)
    # 2. Load SDK config by ascending tree
    config_dir = config_file_path.parent
    product_json_path = find_product_json(config_dir)
    sdk_config = {}
    if product_json_path:
        with product_json_path.open("r", encoding="utf-8") as pf:
            sdk_config = json.load(pf)
    # 3. Load doc config
    with config_file_path.open("r", encoding="utf-8") as f:
        doc_config = json.load(f)
    # 4. 3-way merge
    config = deep_merge(deep_merge(resolved_global, sdk_config), doc_config)
    # 5. Load sidebar.toml (graceful — returns {} if absent)
    sidebar_config = _load_sidebar_toml_graceful(config_dir)
    # 6. Pre-resolve static source_file paths
    for item in sidebar_config.get("sidebar", []):
        if item.get("type") == "static" and item.get("source_file"):
            item["source_file"] = str((config_dir / item["source_file"]).resolve())
    return config, config_dir, sidebar_config
```

- Add `_load_sidebar_toml_graceful(doc_dir: Path) -> dict` that returns `{}` if `sidebar.toml` is absent (v1.0 graceful fallback; the strict `load_sidebar_toml` that raises remains available for explicit use).

**Technical gotchas:**
- The current `run_target()` calls `load_sidebar_toml(config_dir)` which **raises** if `sidebar.toml` is absent. `cli.py:run_pipeline()` has its own graceful fallback. `resolve_config()` must use the graceful version to unify both paths.
- This does **not** change `load_sidebar_toml()` itself — that function is preserved for future strict-mode use (v3.0+ `sidebar.toml` required).

**Test-driven acceptance criteria:**
- `test_resolve_config_returns_merged_dict(tmp_path)` — provide global, sdk, doc configs; assert merged dict has correct override priority.
- `test_resolve_config_graceful_sidebar_missing(tmp_path)` — no `sidebar.toml` in dir; `resolve_config` returns `{}` for `sidebar_config`, no exception.
- `test_resolve_config_sidebar_static_paths_absolute(tmp_path)` — static `source_file` in `sidebar.toml` is resolved to absolute path in returned `sidebar_config`.

**Commit boundary:**
```
refactor(orchestrator): extract resolve_config() and graceful sidebar loading helper
```

---

#### TASK-B.1.3 — Implement `UdeOrchestrator.parse()` Public Method

**Targeted files:** `engine/ude/orchestrator.py` *(MODIFY)*

**Code architecture:**
```python
def parse(self, config: dict, config_dir: Path) -> ProjectCatalog:
    """Collection + parsing stage. Returns populated ProjectCatalog.

    Skips collection if config_dir / src_dir already contains index.xml.
    """
    # ... (extracted from run_target collection + parsing block)
    return catalog
```

**Technical gotchas:**
- Extract the collection/parsing logic verbatim from `run_target()`. Do not change logic — only move it.
- The method signature `parse(self, config: dict, config_dir: Path)` is the stable v2.0 library API contract. Do not make it more complex.

**Test-driven acceptance criteria:**
- `test_orchestrator_parse_returns_catalog(tmp_path)` — call `orchestrator.parse(config, config_dir)` with a mock XML dir containing `index.xml`; assert result is `ProjectCatalog`.
- `test_orchestrator_parse_skips_collector_when_xml_exists(monkeypatch, tmp_path)` — assert `DoxygenXmlCollector.collect` is never called when `index.xml` already present.

**Commit boundary:**
```
feat(orchestrator): expose parse() as public library API method
```

---

#### TASK-B.1.4 — Implement `UdeOrchestrator.render()` Public Method

**Targeted files:** `engine/ude/orchestrator.py` *(MODIFY)*

**Code architecture:**
```python
def render(
    self,
    catalog: ProjectCatalog,
    config: dict,
    config_dir: Path,
    out_dir: Path,
    sidebar_config: Optional[dict] = None,
) -> None:
    """Rendering stage. Writes output files to out_dir."""
    # ... (extracted from run_target rendering block)
```

**Technical gotchas:**
- `cache_mgr` is computed from `self._cache_root` and passed internally — caller does not provide it.
- `sidebar_config` defaults to `{}` if None.

**Test-driven acceptance criteria:**
- `test_orchestrator_render_produces_files(tmp_path)` — call with a pre-built `ProjectCatalog`; assert HTML or Markdown files exist in `out_dir`.
- `test_orchestrator_render_respects_format_config(tmp_path)` — `config["renderer"]["type"] = "hugo_markdown"` → `.md` files produced; `"html"` → `.html` files produced.

**Commit boundary:**
```
feat(orchestrator): expose render() as public library API method
```

---

#### TASK-B.1.5 — Implement `UdeOrchestrator.run()` and Make `run_target()` a Thin Alias

**Targeted files:** `engine/ude/orchestrator.py` *(MODIFY)*

**Code architecture:**
```python
def run(self, doc_config_path: Path) -> bool:
    """Full pipeline: resolve_config → parse → render."""
    config_file_path = Path(doc_config_path).resolve()
    if not config_file_path.exists():
        logger.error(f"Config file {config_file_path} does not exist.")
        return False
    try:
        config, config_dir, sidebar_config = resolve_config(
            config_file_path, self._global_cfg, self.global_config_path
        )
        out_dir = _resolve_output_dir(config, config_dir, self.global_config_path)
        catalog = self.parse(config, config_dir)
        self.render(catalog, config, config_dir, out_dir, sidebar_config)
        return True
    except Exception as e:
        logger.error(f"Pipeline failed for {config_file_path}: {e}")
        return False

def run_target(self, config_path: Union[str, Path]) -> bool:
    """Backward-compatible alias for run()."""
    return self.run(Path(config_path))
```

- Extract `_resolve_output_dir(config, config_dir, global_config_path) -> Path` as a module-level helper.

**Technical gotchas:**
- `run_target()` body becomes a one-liner. All existing callers of `run_target()` continue to work unchanged.
- Error handling in `run()` must respect `self._global_cfg.error_policy` — if `"continue-on-error"`, `run()` should log and return `False` rather than re-raising. If `"fail-fast"`, re-raise.

**Test-driven acceptance criteria:**
- `test_orchestrator_run_end_to_end(tmp_path)` — `orchestrator.run(config_path)` returns `True`; output files exist.
- `test_run_target_is_alias(tmp_path, monkeypatch)` — monkeypatch `UdeOrchestrator.run`; call `run_target`; assert `run` was called with the same path.
- `test_orchestrator_run_returns_false_on_missing_config` — non-existent path → returns `False`, no exception.

**Commit boundary:**
```
feat(orchestrator): implement run() pipeline entry point; run_target becomes alias
```

---

#### TASK-B.1.6 — Slim `cli.py:run_pipeline()` to a Thin Wrapper

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
- `run_pipeline()` becomes:
  ```python
  def run_pipeline(global_config_path, sdk_config_path, doc_config_path,
                   input_override=None, output_override=None, format_override=None) -> int:
      from ude.config import GlobalConfig, logging_setup
      from ude.orchestrator import UdeOrchestrator
      global_cfg = GlobalConfig()
      if global_config_path:
          try:
              global_cfg = GlobalConfig.from_file(global_config_path)
          except Exception as e:
              print(f"Error: {e}", file=sys.stderr)
              return 1
      logging_setup(global_cfg)
      orchestrator = UdeOrchestrator(global_config_path=global_config_path)
      # Override injection for --input / --output / --format still supported
      # via a thin config mutation before calling orchestrator.run()
      ...
      return 0 if orchestrator.run(doc_config_path) else 1
  ```
- Keep `--input`, `--output`, `--format` overrides by mutating the doc config dict before `orchestrator.run()` (or via a new `run_with_overrides()` method on `UdeOrchestrator` added in this task).

**Technical gotchas:**
- The flat v1.0 invocation `ude --doc-config X` must produce **byte-identical output** before and after this refactor. Run the golden master suite to verify.

**Test-driven acceptance criteria:**
- `test_cli_flat_flags_still_work(tmp_path)` — existing flat-flag test passes unchanged.
- `test_cli_delegates_to_orchestrator_run(monkeypatch)` — monkeypatch `UdeOrchestrator.run`; call `main(["--doc-config", "..."])`; assert `run` was called.
- Golden master suite: `pytest tests/test_golden_master.py -v` → all PASSED.

**Commit boundary:**
```
refactor(cli): slim run_pipeline to thin orchestrator wrapper; preserve flat-flag interface
```

---

#### TASK-B.1.7 — Update Tests for GAP-05

**Targeted files:** `engine/tests/test_cli.py` *(MODIFY)*, `engine/tests/test_orchestrator.py` *(MODIFY)*

**Code architecture:**
- Move `test_deep_merge` and `test_find_product_json_*` to `test_orchestrator.py` (or keep in `test_cli.py` with updated import).
- Add all tests listed in TASK-B.1.3–B.1.6 acceptance criteria.

**Commit boundary:**
*(Spread across individual TASK-B.1.x commits as each method is added.)*

---

### GAP-01 — CLI Subcommands (6 tasks)

---

#### TASK-B.2.1 — Restructure `main()` with Argparse Subparsers

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
```python
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="ude",
        description="Universal Documentation Engine (UDE)",
    )
    # Preserve top-level flags for v1.0 backward compat
    parser.add_argument("--global-config", "-g", default=None)
    parser.add_argument("--sdk-config", "-s", default=None)
    parser.add_argument("--doc-config", "-d", default=None)
    parser.add_argument("--config", "-c", default=None)  # legacy alias
    parser.add_argument("--input", "-i", default=None)
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--format", "-f", choices=["hugo_markdown", "html"], default=None)

    subparsers = parser.add_subparsers(dest="command")

    _add_compile_subparser(subparsers)
    _add_parse_subparser(subparsers)
    _add_render_subparser(subparsers)
    _add_audit_subparser(subparsers)

    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if args.command is None:
        # v1.0 fallback: flat-flag dispatch
        return _handle_flat_flags(args)
    return _COMMAND_HANDLERS[args.command](args)
```

**Technical gotchas:**
- Putting all subparser definitions in private `_add_*_subparser()` helpers keeps `main()` readable.
- The `dest="command"` attribute resolves to `None` when no subcommand is given — this is the key for backward compat dispatch.
- `_COMMAND_HANDLERS` is a `dict[str, Callable[[Namespace], int]]`.

**Test-driven acceptance criteria:**
- `main([])` → invokes flat-flag handler, returns `1` (no `--doc-config` provided).
- `main(["compile", "--help"])` → argparse help exits `0`.
- `main(["unknown-command"])` → argparse error, exits `2`.

**Commit boundary:**
```
feat(cli): restructure main() with argparse subparsers; add backward-compat flat-flag dispatch
```

---

#### TASK-B.2.2 — Implement `ude compile` Subcommand

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
```python
def _handle_compile(args) -> int:
    doc_config = args.doc_config or getattr(args, "config", None)
    if not doc_config:
        print("Error: --doc-config is required for compile.", file=sys.stderr)
        return 1
    return run_pipeline(
        global_config_path=Path(args.global_config) if args.global_config else None,
        sdk_config_path=Path(args.sdk_config) if getattr(args, "sdk_config", None) else None,
        doc_config_path=Path(doc_config),
        input_override=getattr(args, "input", None),
        output_override=getattr(args, "output", None),
        format_override=getattr(args, "format", None),
    )
```

**Test-driven acceptance criteria:**
- `test_compile_delegates_to_run_pipeline(monkeypatch)` — monkeypatch `run_pipeline`; call `main(["compile", "--doc-config", "x.json"])`; assert `run_pipeline` called with `doc_config_path=Path("x.json")`.
- `test_compile_missing_doc_config` — `main(["compile"])` → returns `1`.

**Commit boundary:**
```
feat(cli): implement ude compile subcommand
```

---

#### TASK-B.2.3 — Implement `ude parse` Subcommand

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
```python
def _handle_parse(args) -> int:
    """Parse only: write IR to --output-ir path."""
    from ude.config import GlobalConfig, logging_setup
    from ude.orchestrator import UdeOrchestrator, resolve_config
    from ude.storage import save_compressed_ir
    import json

    doc_config_path = Path(args.doc_config).resolve()
    global_config_path = Path(args.global_config).resolve() if args.global_config else None
    output_ir = Path(args.output_ir)

    global_cfg = GlobalConfig.from_file(global_config_path) if global_config_path else GlobalConfig()
    logging_setup(global_cfg)

    orchestrator = UdeOrchestrator(global_config_path=global_config_path)
    try:
        config, config_dir, _ = resolve_config(doc_config_path, global_cfg, global_config_path)
        catalog = orchestrator.parse(config, config_dir)
        save_compressed_ir(catalog, output_ir)
        summary = {
            "namespaces": len(catalog.namespaces),
            "classes": sum(len(ns.classes) for ns in catalog.namespaces),
        }
        print(json.dumps(summary))
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
```

**Technical gotchas:**
- `--output-ir` argument must be registered on the `parse` subparser as **required**.
- JSON summary is printed to **stdout**; all other messages go to **stderr**.

**Test-driven acceptance criteria:**
- `test_parse_subcommand_creates_ir_file(tmp_path)` — run against mock XML dir; assert `.json.gz` file created at `--output-ir` path.
- `test_parse_subcommand_prints_json_summary(tmp_path, capsys)` — captured stdout is valid JSON with `"namespaces"` key.
- `test_parse_subcommand_missing_doc_config` — exits `1`.

**Commit boundary:**
```
feat(cli): implement ude parse subcommand with --output-ir flag
```

---

#### TASK-B.2.4 — Implement `ude render` Subcommand

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
```python
def _handle_render(args) -> int:
    """Render a pre-built IR file to --output directory."""
    from ude.config import GlobalConfig, logging_setup
    from ude.orchestrator import UdeOrchestrator, resolve_config
    from ude.storage import load_compressed_ir

    input_ir = Path(args.input_ir)
    output_dir = Path(args.output).resolve()
    doc_config_path = Path(args.doc_config).resolve() if args.doc_config else None
    global_config_path = Path(args.global_config).resolve() if args.global_config else None

    global_cfg = GlobalConfig.from_file(global_config_path) if global_config_path else GlobalConfig()
    logging_setup(global_cfg)

    try:
        catalog = load_compressed_ir(input_ir)
        orchestrator = UdeOrchestrator(global_config_path=global_config_path)
        config, config_dir, sidebar_config = resolve_config(
            doc_config_path, global_cfg, global_config_path
        ) if doc_config_path else ({}, Path.cwd(), {})
        orchestrator.render(catalog, config, config_dir, output_dir, sidebar_config)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
```

**Technical gotchas:**
- `ude parse` + `ude render` pipeline must produce byte-identical file content to `ude compile`. Add a golden master style diff assertion test using Python `filecmp.dircmp` (portable; no `diff -r` which is Linux-only):
  ```python
  import filecmp
  cmp = filecmp.dircmp(str(compile_out), str(render_out))
  assert not cmp.left_only and not cmp.right_only and not cmp.diff_files
  ```
- `--output` is required for `ude render`; `--doc-config` is optional (provides format/template context).
- Avoid `/tmp/` paths in verification commands — use `tmp_path` pytest fixture for portability across Windows and Linux.

**Test-driven acceptance criteria:**
- `test_render_subcommand_from_ir(tmp_path)` — save an IR, call `main(["render", ...])`, assert output files exist.
- `test_parse_then_render_identical_to_compile(tmp_path)` — file-tree diff of parse+render vs compile → no differences.

**Commit boundary:**
```
feat(cli): implement ude render subcommand consuming --input-ir flag
```

---

#### TASK-B.2.5 — Implement `ude audit` Stub

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
```python
def _handle_audit(args) -> int:
    print(
        "Error: 'ude audit' is not yet implemented. "
        "It will be available after GAP-10 (coverage gate) is merged.",
        file=sys.stderr,
    )
    return 2   # distinct exit code from general errors (1)
```

**Technical gotchas:**
- Exit code `2` is intentional — distinguishes "not implemented" from "error" (1) and "success" (0). This stub will be replaced by the full implementation in TASK-D.2.6.

**Test-driven acceptance criteria:**
- `test_audit_stub_returns_2` — `main(["audit", "--doc-config", "x.json"])` → exit code `2`.
- `test_audit_stub_prints_to_stderr(capsys)` — captured stderr contains `"not yet implemented"`.

**Commit boundary:**
```
feat(cli): add ude audit subcommand stub (full impl in GAP-10)
```

---

#### TASK-B.2.6 — Integration Tests for CLI Subcommands

**Targeted files:** `engine/tests/test_cli.py` *(MODIFY)*

**Code architecture:**
- Consolidate all subcommand tests added in TASK-B.2.2–B.2.5 into `test_cli.py`.
- Add `test_all_subcommands_reachable` — iterate `["compile", "parse", "render", "audit"]`; assert `main([cmd, "--help"])` exits `0` (argparse `--help` always exits 0).

**Test-driven acceptance criteria:**
- `pytest tests/test_cli.py -v` → all PASSED.
- `pytest --cov=ude --cov-report=term-missing` → TOTAL ≥ 98%.

**Commit boundary:**
```
test(cli): add integration tests for all four subcommands
```

---

## Phase 3 — Group D: Typed IR (11 tasks) ‖ Group F: QA (6 tasks)

### GAP-03 — Typed Entity Models (11 tasks)

---

#### TASK-D.1.1 — Rewrite `models.py` with 7 Typed Pydantic Models

**Targeted files:** `engine/ude/models.py` *(FULL REWRITE)*

**Code architecture:**
```python
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class ParameterModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    type: str
    description: Optional[str] = None

class OverloadModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    index: int
    description: Optional[str] = None
    parameters: List[ParameterModel] = Field(default_factory=list)
    return_type: Optional[str] = None
    signature: Optional[str] = None

class MethodModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    fully_qualified_name: str = ""
    signature: str = ""
    parameters: List[ParameterModel] = Field(default_factory=list)
    return_type: str = ""
    docstring: Optional[str] = None
    is_static: bool = False
    is_virtual: bool = False
    overloads: List[OverloadModel] = Field(default_factory=list)

class EnumModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    fully_qualified_name: str = ""
    docstring: Optional[str] = None
    values: List[str] = Field(default_factory=list)

class VariableModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    fully_qualified_name: str = ""
    type: str = ""
    docstring: Optional[str] = None
    is_static: bool = False

class ConstantModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    fully_qualified_name: str = ""
    type: str = ""
    value: Optional[str] = None
    docstring: Optional[str] = None

class TypeAliasModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    fully_qualified_name: str = ""
    aliased_type: str = ""
    docstring: Optional[str] = None

class ClassModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    fully_qualified_name: str
    entity_type: str = "class"   # not Literal — preserve v1.0 string variety
    docstring: Optional[str] = None
    base_class: Optional[str] = None
    methods: List[MethodModel] = Field(default_factory=list)
    fields: List[VariableModel] = Field(default_factory=list)
    enums: List[EnumModel] = Field(default_factory=list)
    constants: List[ConstantModel] = Field(default_factory=list)
    type_aliases: List[TypeAliasModel] = Field(default_factory=list)

class NamespaceModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    classes: List[ClassModel] = Field(default_factory=list)
    free_functions: List[MethodModel] = Field(default_factory=list)
    free_variables: List[VariableModel] = Field(default_factory=list)
    enums: List[EnumModel] = Field(default_factory=list)
    constants: List[ConstantModel] = Field(default_factory=list)
    type_aliases: List[TypeAliasModel] = Field(default_factory=list)

class ProjectCatalog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    project_name: str = ""
    version: str = ""
    namespaces: List[NamespaceModel] = Field(default_factory=list)
    metadata: Optional[dict] = Field(default_factory=dict)

# Backward-compatibility aliases
ClassEntity = ClassModel
NamespaceEntity = NamespaceModel
MethodEntity = MethodModel
ParameterField = ParameterModel
```

**Technical gotchas:**
- The backward-compat aliases (`ClassEntity = ClassModel`, etc.) allow existing code that still references the old names to continue working without changes during the transition period. Remove these aliases only after all callers are updated.
- `model_config = ConfigDict(extra="ignore")` is mandatory on EVERY model — unknown keys in v3.0+ IR files must not raise `ValidationError`. Forward-compatibility break if omitted.
- `ConfigDict` must be imported from `pydantic` alongside `BaseModel` and `Field`.
- `entity_type: str` (not `Literal[...]`) preserves the v1.0 wide-string convention — parsers set it to `"class"`, `"struct"`, `"interface"`, etc.
- All new fields default to `""` or `[]` — no `Optional` without a default. This ensures old `.json.gz` files from v1.0 (which lack `free_functions`, `enums`, `constants`, `type_aliases`) deserialize without error via Pydantic defaults.
- `fields: List[VariableModel]` replaces `fields: List[str]` — this is the primary breaking change. Any code that accesses `entity.fields[i]` as a string must be updated to `entity.fields[i].name`.

**Test-driven acceptance criteria (in `test_models.py` rewrite):**
- `test_project_catalog_has_project_name_and_version` — `ProjectCatalog(project_name="SDK", version="2.0")` round-trips.
- `test_class_model_fields_are_variable_models` — `ClassModel.fields[0]` is a `VariableModel`.
- `test_old_ir_json_deserializes_without_error` — load a v1.0 format JSON string lacking `free_functions`; no exception.
- `test_variable_model_nonempty_round_trip` — serialize `ProjectCatalog` containing `ClassModel(fields=[VariableModel(name="myField", fully_qualified_name="NS::C::myField", type="int")])` to JSON and back; assert `fields[0].name == "myField"` and `fields[0].type == "int"`. *(Pydantic Guard Step 2b)*
- `test_class_model_extra_field_ignored` — `ClassModel.model_validate({"name":"X","fully_qualified_name":"Y","unknown_v3_field":99})` succeeds; `unknown_v3_field` is not stored. *(Pydantic Guard Step 3)*
- `test_project_catalog_extra_field_ignored` — `ProjectCatalog.model_validate({"namespaces":[],"future_field":"x"})` succeeds. *(Pydantic Guard Step 3)*
- `test_backward_compat_alias` — `ClassEntity is ClassModel` → `True`.
- `test_7_model_round_trip` — build a `ProjectCatalog` with all 7 model types; serialize to JSON and back; all fields preserved.

**Commit boundary:**
```
feat(models): replace ClassEntity discriminated union with 7 typed Pydantic models
```

---

#### TASK-D.1.2 — Rewrite `test_models.py`

**Targeted files:** `engine/tests/test_models.py` *(REWRITE)*

*(Full test rewrite per TASK-D.1.1 acceptance criteria. This is the RED step that drives TASK-D.1.1.)*

**Commit boundary:**
*(Combined with TASK-D.1.1.)*

---

#### TASK-D.1.3 — Refactor `parsers/doxygen_base.py` and `doxygen.py`

**Targeted files:** `engine/ude/parsers/doxygen_base.py` *(MODIFY)*, `engine/ude/parsers/doxygen.py` *(MODIFY)*

**Code architecture:**
- Replace all `ClassEntity(...)` construction with `ClassModel(...)`.
- Replace `NamespaceEntity(...)` with `NamespaceModel(...)`.
- Where the parser currently sets `fields=["field_name"]` (a list of strings), change to:
  ```python
  fields=[VariableModel(name=f_name, fully_qualified_name=fqn, type=f_type)]
  ```
- For enum members detected by `kind="enum"` in Doxygen XML, populate `ClassModel.enums` (or `NamespaceModel.enums` for free enums) with `EnumModel` instances.

**Technical gotchas:**
- The transition from `fields: List[str]` to `fields: List[VariableModel]` is the highest-risk change. After this commit, all renderer code that accesses `entity.fields` as strings will break. This is intentional — the renderer refactors (TASK-D.1.7–D.1.9) follow immediately.
- Use the backward-compat alias (`ClassEntity = ClassModel`) — no import changes in parsers needed initially.
- Run `pytest tests/test_doxygen_parser.py -v` after this task; expect some failures in renderer tests (acceptable — they are fixed in TASK-D.1.7).

**Commit boundary:**
```
feat(parsers): update entity construction to use typed ClassModel and NamespaceModel
```

---

#### TASK-D.1.4–D.1.6 — Refactor Language-Specific Parsers

**Targeted files:** `engine/ude/parsers/doxygen_csharp.py`, `doxygen_java.py`, `doxygen_python.py` *(MODIFY each)*

**Code architecture (C# — TASK-D.1.4):**
```python
# doxygen_csharp.py
from ude.models import ClassModel, NamespaceModel, VariableModel

# BEFORE (v1.0):
entity = ClassEntity(name=name, fully_qualified_name=fqn, fields=["fieldA", "fieldB"])
# AFTER (v2.0):
entity = ClassModel(
    name=name,
    fully_qualified_name=fqn,
    fields=[VariableModel(name=f_name, type=f_type) for f_name, f_type in raw_fields],
)
```

**Code architecture (Java — TASK-D.1.5):**
```python
# doxygen_java.py
from ude.models import ClassModel, NamespaceModel, VariableModel

entity = ClassModel(
    name=name,
    fully_qualified_name=fqn,
    fields=[VariableModel(name=f_name, type=f_type) for f_name, f_type in raw_fields],
)
```

**Code architecture (Python — TASK-D.1.6):**
```python
# doxygen_python.py
from ude.models import ClassModel, NamespaceModel, VariableModel

entity = ClassModel(
    name=name,
    fully_qualified_name=fqn,
    fields=[VariableModel(name=f_name, type=f_type) for f_name, f_type in raw_fields],
)
```

**TDD RED step (run BEFORE modifying each parser):**
```bash
# Confirm the test currently fails due to type mismatch:
poetry run pytest tests/test_doxygen_parser.py -v -k "csharp and field"   # or java/python
# Expected: FAILED — fields elements are str, not VariableModel
```

**Code architecture (general pattern for each file):**
- Replace `ClassEntity` → `ClassModel`.
- Replace `NamespaceEntity` → `NamespaceModel`.
- Update `fields` population: `[VariableModel(name=..., type=...)]` instead of `["name"]`.
- Run `pytest tests/test_doxygen_parser.py -v -k "csharp"` (or java/python) after each file — must be GREEN.

**Commit boundary (one per language file):**
```
feat(parsers): update CSharp/Java/Python parser entity construction to typed models
```

---

#### TASK-D.1.7 — Refactor `renderers/static_html.py` for Typed Models

**Targeted files:** `engine/ude/renderers/static_html.py` *(MODIFY)*

**Code architecture:**
- Replace `from ude.models import ProjectCatalog, ClassEntity` → `from ude.models import ProjectCatalog, ClassModel, VariableModel`.
- Change all `for field in entity.fields:` loops: previously `field` was a `str`; now it is a `VariableModel`. Update templates/render calls to use `field.name`, `field.type`, `field.docstring`.
- Add rendering for `entity.enums`, `entity.constants`, `entity.type_aliases` in existing section containers.

**Technical gotchas:**
- Do not add new page types or change navigation structure — v2.0 render parity is frozen. New typed fields render inside existing sections only.
- Jinja2 templates may reference `{{ field }}` as a string; update template references to `{{ field.name }}`.

**Test-driven acceptance criteria:**
- `pytest tests/test_html_renderer.py -v` → all PASSED.
- Golden master suite: `pytest tests/test_golden_master.py -v -k "html"` — may need baseline regeneration (TASK-D.1.11).
- **Mandatory renderer string-access scan (Pydantic Guard Step 4):**
  ```bash
  # bash / Git Bash / WSL / CI
  grep -rn "\.fields\b" engine/ude/renderers/static_html.py
  grep -rn "\.methods\b" engine/ude/renderers/static_html.py
  grep -rn "\.enums\b" engine/ude/renderers/static_html.py
  grep -rn "\.constants\b" engine/ude/renderers/static_html.py
  grep -rn "\.type_aliases\b" engine/ude/renderers/static_html.py
  ```
  ```powershell
  # Windows PowerShell
  foreach ($pattern in @("\.fields\b","\.methods\b","\.enums\b","\.constants\b","\.type_aliases\b")) {
      Select-String -Path engine/ude/renderers/static_html.py -Pattern $pattern |
          Select-Object LineNumber, Line
  }
  ```
  Every match MUST be verified to use attribute access (`.name`, `.type`, `.docstring`) — NOT bare string usage in f-strings, concatenation, or Jinja2 `{{ field }}` without `.name`.
- **Traceability docstring check:** `grep -n "Implements TASK-D.1.7\|Implements GAP-03" engine/ude/renderers/static_html.py` → at least 1 result.

**Commit boundary:**
```
feat(renderers): update HtmlRenderer field access for VariableModel typed fields
```

---

#### TASK-D.1.8 — Refactor `renderers/hugo_markdown.py` for Typed Models

**Targeted files:** `engine/ude/renderers/hugo_markdown.py` *(MODIFY)*

*(Same pattern as TASK-D.1.7 for Hugo Markdown renderer.)*

**Test-driven acceptance criteria:**
- `pytest tests/test_hugo_renderer.py -v` → all PASSED.
- **Mandatory renderer string-access scan (Pydantic Guard Step 4) — same 5 grep patterns as TASK-D.1.7, targeting `hugo_markdown.py`.** Every match must use attribute access, not bare string.
- **Traceability docstring check:** `grep -n "Implements TASK-D.1.8\|Implements GAP-03" engine/ude/renderers/hugo_markdown.py` → at least 1 result.

**Commit boundary:**
```
feat(renderers): update HugoMarkdownRenderer for typed entity models
```

---

#### TASK-D.1.9 — Refactor `renderers/legacy.py` for Typed Models

**Targeted files:** `engine/ude/renderers/legacy.py` *(MODIFY)*

*(Same pattern as TASK-D.1.7 for legacy renderers.)*

**Test-driven acceptance criteria:**
- `pytest tests/test_legacy_renderer.py -v` → all PASSED.
- **Mandatory renderer string-access scan (Pydantic Guard Step 4) — same 5 grep patterns as TASK-D.1.7, targeting `legacy.py`.** Every match must use attribute access, not bare string.
- **Traceability docstring check:** `grep -n "Implements TASK-D.1.9\|Implements GAP-03" engine/ude/renderers/legacy.py` → at least 1 result.

**Commit boundary:**
```
feat(renderers): update LegacyRenderers for typed entity models
```

---

#### TASK-D.1.10 — Update All Affected Test Files

**Targeted files:** `engine/tests/test_doxygen_parser.py`, `test_html_renderer.py`, `test_hugo_renderer.py`, `test_legacy_renderer.py`, `test_integration_pipeline.py` *(MODIFY each)*

**Code architecture:**
- Update fixture catalog construction: replace `ClassEntity(...)` with `ClassModel(...)`, `fields=["x"]` with `fields=[VariableModel(name="x", type="int")]`.
- Run tests after each file is updated.

**Technical gotchas:**
- `test_integration_pipeline.py` is the most important — it runs the full E2E pipeline. If it passes, the model migration is coherent across all layers.

**Commit boundary (one per test file):**
```
test(models): update <file> fixtures to use typed ClassModel/VariableModel
```

---

#### TASK-D.1.11 — Regenerate Golden Master Baselines

**Targeted files:** `engine/tests/` *(RUN ONLY)*

**Code architecture:**
```bash
# Linux / macOS / CI
cd engine
UPDATE_GOLDEN=1 poetry run pytest tests/test_golden_master.py -v
poetry run pytest tests/test_golden_master.py -v   # must pass on re-run
```
```powershell
# Windows PowerShell (primary project shell)
cd engine
$env:UPDATE_GOLDEN="1"; poetry run pytest tests/test_golden_master.py -v
poetry run pytest tests/test_golden_master.py -v   # must pass on re-run
```

**Technical gotchas:**
- Run with `UPDATE_GOLDEN=1` **only** after all render-layer changes (TASK-D.1.7–D.1.9) are confirmed correct.
- Inspect the diff before committing the new baselines: `git diff --stat` should show only content changes in baseline files, not file additions or deletions.
- Run the Docomatic alignment suite to confirm no cross-language regression was introduced (see TASK-D.1.12).

**Commit boundary:**
```
chore(baselines): regenerate golden master baselines after typed IR migration
```

---

#### TASK-D.1.12 — Re-baseline Docomatic Alignment Suite Post-Typed-IR

**Targeted files:** `engine/tests/test_docomatic_alignment.py` *(RUN + verify)*

**Code architecture:**
```powershell
# Windows PowerShell
poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short
```
```bash
# Linux / macOS / CI
poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short
```

After running, open each language's discrepancy report (`difference_mock_sdk_{lang}.json`) and
check the `"total_differences"` key. Compare against the baseline value recorded before
TASK-D.1.7–D.1.9 were applied.

**Technical gotchas:**
- GAP-03 renderer changes add new typed entity sections (`constants`, `type_aliases`, `enums`)
  to rendered output. The alignment suite baselines will be stale — the new sections will
  appear as differences. This is EXPECTED behavior, not a regression.
- Do NOT update alignment baselines automatically. Follow the `difference_minimization_iterator.md`
  workflow: present each new difference to the user, get explicit confirmation that it is an
  allowance, then update with `$env:UPDATE_ALLOWANCES="1"` / `UPDATE_ALLOWANCES=1`.
- If `"total_differences"` DECREASES for any language: good — the typed models resolved
  previously mismatched output.
- If `"total_differences"` INCREASES unexpectedly for a language NOT being worked on: a
  cross-language regression was introduced. Revert TASK-D.1.7–D.1.9 changes touching shared
  base classes or Jinja2 templates and re-investigate.

**Test-driven acceptance criteria:**
- `pytest engine/tests/test_docomatic_alignment.py` exits without unexpected NEW failures
  (failures caused by new typed sections are acceptable and handled via the allowances flow).
- After allowances are registered for new typed sections: `total_differences` ≤ pre-GAP-03 baseline.

**Commit boundary:**
```
chore(alignment): re-baseline docomatic alignment suite post-typed-IR migration (GAP-03)
```

---

### GAP-10 — Documentation Coverage Gate (7 tasks)

---

#### TASK-D.2.1 — Create `coverage.py` Pydantic Response Models

**Targeted files:** `engine/ude/coverage.py` *(CREATE)*

**Code architecture:**
```python
from pydantic import BaseModel

class EntityCoverage(BaseModel):
    total: int
    documented: int
    coverage: float   # 0.0–1.0

class CoverageReport(BaseModel):
    per_type: dict[str, EntityCoverage]
    overall: EntityCoverage
```

**Test-driven acceptance criteria:**
- `from ude.coverage import EntityCoverage, CoverageReport` succeeds without error.
- `EntityCoverage(total=10, documented=7, coverage=0.7)` validates and returns correct field values.
- `CoverageReport(per_type={"class": EntityCoverage(...)}, overall=EntityCoverage(...))` validates.
- **Traceability docstring check:**
  ```bash
  grep -n "Implements TASK-D.2.1\|Implements GAP-10" engine/ude/coverage.py
  ```
  → at least 1 result. Each public class (`EntityCoverage`, `CoverageReport`) MUST carry a one-line docstring with `Implements GAP-10` or `Implements TASK-D.2.x`.

**Commit boundary:**
```
feat(coverage): add CoverageReport and EntityCoverage pydantic models
```

---

#### TASK-D.2.2 — Implement `compute_coverage()`

**Targeted files:** `engine/ude/coverage.py` *(MODIFY)*

**Code architecture:**
```python
from ude.models import ProjectCatalog

def _is_documented(docstring) -> bool:
    return docstring is not None and str(docstring).strip() != ""

def compute_coverage(catalog: ProjectCatalog) -> CoverageReport:
    counts: dict[str, list[bool]] = {
        "class": [], "method": [], "enum": [],
        "variable": [], "constant": [], "type_alias": [],
    }
    for ns in catalog.namespaces:
        for cls in ns.classes:
            counts["class"].append(_is_documented(cls.docstring))
            for m in cls.methods:
                counts["method"].append(_is_documented(m.docstring))
            for e in cls.enums:
                counts["enum"].append(_is_documented(e.docstring))
            for v in cls.fields:
                counts["variable"].append(_is_documented(v.docstring))
            for c in cls.constants:
                counts["constant"].append(_is_documented(c.docstring))
            for t in cls.type_aliases:
                counts["type_alias"].append(_is_documented(t.docstring))
        for fn in ns.free_functions:
            counts["method"].append(_is_documented(fn.docstring))
        for e in ns.enums:
            counts["enum"].append(_is_documented(e.docstring))

    per_type = {}
    all_results = []
    for key, results in counts.items():
        total = len(results)
        doc = sum(results)
        per_type[key] = EntityCoverage(
            total=total,
            documented=doc,
            coverage=doc / total if total > 0 else 1.0,
        )
        all_results.extend(results)

    total_all = len(all_results)
    doc_all = sum(all_results)
    overall = EntityCoverage(
        total=total_all,
        documented=doc_all,
        coverage=doc_all / total_all if total_all > 0 else 1.0,
    )
    return CoverageReport(per_type=per_type, overall=overall)
```

**Technical gotchas:**
- Empty catalog (zero entities) → `coverage=1.0` (not division-by-zero; fully covered by definition).
- `_is_documented` must handle `None`, `""`, and whitespace-only strings as undocumented.

**Commit boundary:**
```
feat(coverage): implement compute_coverage() for per-entity-type analysis
```

---

#### TASK-D.2.3 — Implement `apply_coverage_gate()` and Wire into `UdeOrchestrator.run()`

**Targeted files:** `engine/ude/coverage.py` *(MODIFY)*, `engine/ude/orchestrator.py` *(MODIFY)*

**Code architecture:**
```python
# In coverage.py
import logging
logger = logging.getLogger("ude.coverage")

def apply_coverage_gate(catalog: ProjectCatalog, cfg: "GlobalConfig") -> int:
    """Returns exit code: 0 = pass, 2 = reject-undocumented threshold failed."""
    report = compute_coverage(catalog)
    if report.overall.coverage < cfg.coverage_threshold:
        msg = (
            f"Coverage {report.overall.coverage:.1%} is below threshold "
            f"{cfg.coverage_threshold:.1%}."
        )
        if cfg.coverage_mode == "reject-undocumented":
            logger.error(msg + " Blocking build (reject-undocumented mode).")
            return 2
        else:
            logger.warning(msg + " Continuing (allow-undocumented mode).")
    return 0
```

- In `UdeOrchestrator.run()`, after `self.render(...)`:
  ```python
  from ude.coverage import apply_coverage_gate
  gate_code = apply_coverage_gate(catalog, self._global_cfg)
  if gate_code != 0:
      return False   # run() returning False propagates to cli exit code 1
  ```

**Technical gotchas:**
- `apply_coverage_gate` returns an int (0 or 2) for use in CLI exit code mapping; `run()` maps `gate_code != 0` to `return False` (which maps to exit code 1 in the CLI). The `2` exit code is only visible directly from `ude audit` (TASK-D.2.6).

**Commit boundary:**
```
feat(coverage): implement coverage gate and wire into UdeOrchestrator.run
```

---

#### TASK-D.2.4–D.2.5 — Unit Tests for `coverage.py`

**Targeted files:** `engine/tests/test_coverage.py` *(CREATE)*

**Code architecture (test cases):**
- `test_full_coverage` — all docstrings set → `overall.coverage == 1.0`, exit code `0`.
- `test_zero_coverage_allow_mode` — all None docstrings, `allow-undocumented` → exit code `0`.
- `test_zero_coverage_reject_mode` — all None docstrings, `reject-undocumented`, threshold `1.0` → exit code `2`.
- `test_mixed_coverage` — 3/4 methods documented → `method.coverage == 0.75`.
- `test_empty_catalog_is_fully_covered` — empty `ProjectCatalog()` → `overall.coverage == 1.0`.
- `test_coverage_threshold_boundary` — `coverage=0.85`, `threshold=0.80` → gate passes; `threshold=0.90` → gate fails in reject mode.

**Commit boundary:**
```
test(coverage): add unit tests for compute_coverage and apply_coverage_gate
```

---

#### TASK-D.2.6 — Implement Full `ude audit` Subcommand (Replaces Stub)

**Targeted files:** `engine/ude/cli.py` *(MODIFY)*

**Code architecture:**
```python
def _handle_audit(args) -> int:
    from ude.config import GlobalConfig, logging_setup
    from ude.orchestrator import UdeOrchestrator, resolve_config
    from ude.coverage import compute_coverage, apply_coverage_gate

    doc_config_path = Path(args.doc_config).resolve()
    global_config_path = Path(args.global_config).resolve() if args.global_config else None

    global_cfg = GlobalConfig.from_file(global_config_path) if global_config_path else GlobalConfig()
    # Allow --mode and --threshold to override global config
    if hasattr(args, "mode") and args.mode:
        global_cfg = global_cfg.model_copy(update={"coverage_mode": args.mode})
    if hasattr(args, "threshold") and args.threshold is not None:
        global_cfg = global_cfg.model_copy(update={"coverage_threshold": float(args.threshold)})
    logging_setup(global_cfg)

    orchestrator = UdeOrchestrator(global_config_path=global_config_path)
    config, config_dir, _ = resolve_config(doc_config_path, global_cfg, global_config_path)
    catalog = orchestrator.parse(config, config_dir)
    report = compute_coverage(catalog)

    # Print Markdown table to stdout
    print("| Entity Type | Total | Documented | Coverage |")
    print("|---|---|---|---|")
    for entity_type, ec in sorted(report.per_type.items()):
        print(f"| {entity_type} | {ec.total} | {ec.documented} | {ec.coverage:.1%} |")
    print(f"| **overall** | {report.overall.total} | {report.overall.documented} | {report.overall.coverage:.1%} |")

    return apply_coverage_gate(catalog, global_cfg)
```

**Technical gotchas:**
- `model_copy(update={...})` is the Pydantic v2 idiom for immutable field override.
- The stub from TASK-B.2.5 is replaced entirely — this is the complete implementation.

**Commit boundary:**
```
feat(cli): implement full ude audit subcommand with coverage report output
```

---

#### TASK-D.2.7 — Integration Test: `ude audit` End-to-End

**Targeted files:** `engine/tests/test_coverage.py` *(MODIFY)*

**Code architecture:**
```python
def test_audit_prints_markdown_table(tmp_path, capsys):
    # Set up a minimal doc config pointing at a mock XML dir
    ...
    result = main(["audit", "--doc-config", str(cfg_path)])
    captured = capsys.readouterr()
    assert "| Entity Type |" in captured.out
    assert "| overall |" in captured.out
    assert result in (0, 2)   # either pass or reject

def test_audit_reject_mode_returns_2(tmp_path):
    # Catalog with 0% coverage, reject-undocumented mode
    ...
    result = main(["audit", "--doc-config", str(cfg_path),
                   "--mode", "reject-undocumented", "--threshold", "1.0"])
    assert result == 2
```

**Commit boundary:**
*(Combined with TASK-D.2.6.)*

---

### GAP-31 — External Script Confirmation (5 tasks)

---

#### TASK-F.1.1 — Audit Test Infrastructure

**Targeted files:** `design-docs/docs/srs/integration_tests_specification.md` *(MODIFY — annotations only)*

**Code architecture:**
- Run: `Get-ChildItem -Recurse -Filter "*.py" "D:\My repositories\Pipeline\Tests" 2>$null`
- Confirmed: `Tests/` directory does not exist at root `Pipeline/` level.
- Confirmed present: `engine/tests/test_golden_master.py` (TEST-INT-01), `engine/tests/test_docomatic_alignment.py`.
- Confirmed absent: `verify_pages.py`, `check_links.py`, `run_regression_tests.py`.
- Add a note block in `integration_tests_specification.md` for each test:  
  `> **2026-06-28 audit**: [Confirmed Present at <path> | Implemented in TASK-F.1.x]`

**Commit boundary:**
```
docs(srs): annotate integration_tests_specification with 2026-06-28 audit findings
```

---

#### TASK-F.1.2 — Implement `Tests/verify_pages.py`

**Targeted files:** `Tests/verify_pages.py` *(CREATE — root repository level)*

**Code architecture:**
```python
#!/usr/bin/env python3
"""TEST-INT-03: Verify all internal href links in an HTML output directory resolve locally."""
import argparse, sys
from pathlib import Path
from html.parser import HTMLParser

class LinkCollector(HTMLParser):
    def __init__(self): super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, val in attrs:
                if attr == "href" and val and not val.startswith(("http", "mailto", "#")):
                    self.links.append(val.split("#")[0])

def verify_pages(output_dir: Path) -> int:
    broken = []
    for html_file in output_dir.rglob("*.html"):
        collector = LinkCollector()
        collector.feed(html_file.read_text(encoding="utf-8", errors="replace"))
        for link in collector.links:
            target = (html_file.parent / link).resolve()
            if not target.exists():
                broken.append(f"{html_file.relative_to(output_dir)} -> {link}")
    if broken:
        print(f"BROKEN LINKS ({len(broken)}):", file=sys.stderr)
        for b in broken: print(f"  {b}", file=sys.stderr)
        return 1
    print(f"All links verified in {len(list(output_dir.rglob('*.html')))} HTML files.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    sys.exit(verify_pages(Path(args.output_dir)))
```

**Technical gotchas:**
- Fragment-only links (`#anchor`) are skipped — only file-path links are checked.
- No network access — purely local file resolution.
- `errors="replace"` in `read_text` prevents crash on non-UTF-8 HTML files.

**Test-driven acceptance criteria:**
- `python Tests/verify_pages.py --output-dir ude_output/bimnv_api_cpp/html` → exit 0.
- `python Tests/verify_pages.py --output-dir /tmp/broken_output` (dir with a broken link) → exit 1, broken link printed to stderr.

**Commit boundary:**
```
feat(tests): implement Tests/verify_pages.py for TEST-INT-03 link verification
```

---

#### TASK-F.1.3 — Implement `Tests/check_links.py`

**Targeted files:** `Tests/check_links.py` *(CREATE — root repository level)*

**Code architecture:**
- Identical pattern to `verify_pages.py` but targets a Hugo-built site (`public/` directory).
- Also checks `href` values in Markdown-rendered `<a>` tags in `.html` files within `public/`.
- Additional check: cross-reference `*.html` page `href` values against the Hugo `public/` file tree.

**Test-driven acceptance criteria:**
- `python Tests/check_links.py --site-dir hugo-site/public` → exit 0 on clean site.

**Commit boundary:**
```
feat(tests): implement Tests/check_links.py for TEST-INT-04/06 Hugo link checking
```

---

#### TASK-F.1.4 — Implement Root Integration Test Runner

**Targeted files:** `Tests/run_all_integration_tests.sh` *(CREATE)*, `Tests/run_all_integration_tests.bat` *(CREATE)*

**Code architecture (`.sh` — Linux/macOS/CI):**
```bash
#!/usr/bin/env bash
set -euo pipefail
ERRORS=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
HTML_OUTPUT_DIR="${1:-$REPO_ROOT/ude_output}"
SITE_DIR="${2:-$REPO_ROOT/hugo-site/public}"

echo "[1/3] Running golden master regression tests..."
(cd "$REPO_ROOT/engine" && poetry run pytest tests/test_golden_master.py -v) || ERRORS=$((ERRORS+1))

echo "[2/3] Verifying HTML output links..."
python "$SCRIPT_DIR/verify_pages.py" --output-dir "$HTML_OUTPUT_DIR" || ERRORS=$((ERRORS+1))

echo "[3/3] Checking Hugo site links..."
python "$SCRIPT_DIR/check_links.py" --site-dir "$SITE_DIR" || ERRORS=$((ERRORS+1))

[ $ERRORS -gt 0 ] && { echo "FAILED: $ERRORS test step(s) failed."; exit 1; }
echo "ALL INTEGRATION TESTS PASSED."
```

**Code architecture (`.bat` — Windows):**
```bat
@echo off
setlocal enabledelayedexpansion
set ERRORS=0
set SCRIPT_DIR=%~dp0
set REPO_ROOT=%SCRIPT_DIR%..
set HTML_OUTPUT_DIR=%~1
set SITE_DIR=%~2
if "%HTML_OUTPUT_DIR%"=="" set HTML_OUTPUT_DIR=%REPO_ROOT%\ude_output
if "%SITE_DIR%"=="" set SITE_DIR=%REPO_ROOT%\hugo-site\public

echo [1/3] Running golden master regression tests...
pushd "%REPO_ROOT%\engine"
poetry run pytest tests/test_golden_master.py -v
if errorlevel 1 set /a ERRORS+=1
popd

echo [2/3] Verifying HTML output links...
python "%SCRIPT_DIR%verify_pages.py" --output-dir "%HTML_OUTPUT_DIR%"
if errorlevel 1 set /a ERRORS+=1

echo [3/3] Checking Hugo site links...
python "%SCRIPT_DIR%check_links.py" --site-dir "%SITE_DIR%"
if errorlevel 1 set /a ERRORS+=1

if %ERRORS% gtr 0 (echo FAILED: %ERRORS% test step(s) failed. & exit /b 1)
echo ALL INTEGRATION TESTS PASSED.
```

**Technical gotchas:**
- Both scripts accept optional positional arguments for `--output-dir` and `--site-dir` — no hardcoded project-specific paths.
- The `.bat` uses `pushd`/`popd` for safe CWD management — `cd engine` alone would leave the shell in the wrong directory if the test fails.
- The `.sh` uses `set -euo pipefail` but catches each step individually with `|| ERRORS+=1` to aggregate failures rather than exiting early.

**Commit boundary:**
```
feat(tests): add root-level integration test runner scripts (sh + bat)
```

---

#### TASK-F.1.5 — Update `integration_tests_specification.md` with Final Paths

**Targeted files:** `design-docs/docs/srs/integration_tests_specification.md` *(MODIFY)*

- Update each test entry with the canonical file path confirmed or created by TASK-F.1.1–F.1.4.
- Update status badges from `[Unconfirmed]` to `[Confirmed]` or `[Implemented]`.

**Commit boundary:**
```
docs(srs): update integration_tests_specification with confirmed/implemented paths
```

---

### GAP-32 — Per-Language Integration Suites (6 tasks)

---

#### TASK-F.2.1 — Add `LanguageIntegrationBase` to `tests/utils.py`

**Targeted files:** `engine/tests/utils.py` *(MODIFY)*

**Code architecture:**
```python
class LanguageIntegrationBase:
    """Mixin providing shared parse-render pipeline for per-language integration tests."""
    LANGUAGE: str = "cpp"
    XML_ASSET_KEY: str = "main"   # key into MockAssetLoader

    def _build_catalog(self):
        from tests.utils import MockAssetLoader
        from ude.parsers.doxygen import DoxygenXmlParser
        loader = MockAssetLoader()
        xml_dir = loader.get_asset_dir(self.XML_ASSET_KEY)
        return DoxygenXmlParser(language=self.LANGUAGE).parse(str(xml_dir))

    def _render_html(self, catalog, tmp_path):
        from ude.renderers.static_html import HtmlRenderer
        renderer = HtmlRenderer(language=self.LANGUAGE)
        renderer.render(catalog, str(tmp_path / "html_out"))
        return tmp_path / "html_out"

    def _render_hugo(self, catalog, tmp_path):
        from ude.renderers.hugo_markdown import HugoMarkdownRenderer
        renderer = HugoMarkdownRenderer(language=self.LANGUAGE)
        renderer.render(catalog, str(tmp_path / "hugo_out"))
        return tmp_path / "hugo_out"
```

**Commit boundary:**
```
test(utils): add LanguageIntegrationBase mixin for per-language integration suites
```

---

#### TASK-F.2.2 — Create `test_integration_cpp.py`

**Targeted files:** `engine/tests/test_integration_cpp.py` *(CREATE)*

**Code architecture:**
```python
class TestCppIntegration(LanguageIntegrationBase):
    LANGUAGE = "cpp"

    def test_category_landing_page_exists(self, tmp_path):
        catalog = self._build_catalog()
        out = self._render_html(catalog, tmp_path)
        # At least one category index page must exist
        indices = list(out.rglob("index.html"))
        assert len(indices) > 0

    def test_member_type_index_exists(self, tmp_path):
        catalog = self._build_catalog()
        out = self._render_html(catalog, tmp_path)
        # "Fields, Structures and Enums" or "Classes" index must exist
        content = " ".join(f.read_text() for f in out.rglob("*.html"))
        assert "Classes" in content or "Fields" in content

    def test_overload_dispatcher_rendered(self, tmp_path):
        # Requires a fixture entity with overloads list
        catalog = self._build_catalog_with_overloads()
        out = self._render_html(catalog, tmp_path)
        # The overloaded method's page must exist — deterministic assertion
        pages = list(out.rglob("*.html"))
        overload_pages = [p for p in pages if "overload" in str(p).lower()]
        assert len(overload_pages) > 0, (
            f"No overload dispatcher page found in output. Pages found: {[str(p.name) for p in pages]}"
        )
```

**Technical gotchas:**
- `_build_catalog_with_overloads()` composes a `ProjectCatalog` with a `MethodModel` that has a non-empty `overloads` list, using `MockAssetLoader` or direct Pydantic construction.

**Commit boundary:**
```
test(integration): add per-language integration suite for C++ (GAP-32)
```

---

#### TASK-F.2.3 — Create `test_integration_cs.py`

**Targeted files:** `engine/tests/test_integration_cs.py` *(CREATE)*

**Code architecture — key test cases:**
- `test_interface_entity_renders_interface_keyword` — `ClassModel(entity_type="interface")` → rendered HTML contains `interface` keyword in prototype.
- `test_delegate_entity_renders_member_list` — `ClassModel(entity_type="delegate")` → rendered page exists.
- `test_namespace_index_page_exists` — `NamespaceModel` with classes → `<namespace>/index.html` exists.

**Commit boundary:**
```
test(integration): add per-language integration suite for C# (GAP-32)
```

---

#### TASK-F.2.4 — Create `test_integration_java.py`

**Targeted files:** `engine/tests/test_integration_java.py` *(CREATE)*

**Code architecture — key test cases:**
- `test_base_class_rendered_in_prototype` — `ClassModel(base_class="AbstractBase")` → rendered HTML prototype contains `AbstractBase`.
- `test_package_index_page_exists` — `NamespaceModel` with classes → `<package>/index.html` exists with class table.

**Commit boundary:**
```
test(integration): add per-language integration suite for Java (GAP-32)
```

---

#### TASK-F.2.5 — Create `test_integration_py.py`

**Targeted files:** `engine/tests/test_integration_py.py` *(CREATE)*

**Code architecture — key test cases:**
- `test_property_method_rendered` — `MethodModel(name="get_value")` with `is_property=True` (if the v2.0 schema includes this flag) OR a bare `MethodModel(name="get_value")` → appears in the rendered method list. **Note:** `fget`/`fset` markers are NOT part of the v2.0 `VariableModel`/`MethodModel` schema. Do NOT assert `[get]`/`[set]` labels — that is a v3.0+ renderer feature. Limit the test to "property-like method is rendered at all."
- `test_dunder_methods_not_filtered` — `MethodModel(name="__init__")` → appears in rendered method list.
- `test_dunder_repr_visible` — `MethodModel(name="__repr__")` → page includes the method.
- `test_dunder_eq_visible` — `MethodModel(name="__eq__")` → page includes the method (verifies no dunder filter beyond `__init__` is silently applied).

**Commit boundary:**
```
test(integration): add per-language integration suite for Python (GAP-32)
```

---

#### TASK-F.2.6 — Full Suite Coverage Gate for Phase 3

**Targeted files:** `engine/tests/` *(RUN ONLY)*

**Code architecture:**
```bash
cd engine
poetry run pytest tests/ -v --tb=short 2>&1 | tail -30
poetry run pytest --cov=ude --cov-report=term-missing | grep "TOTAL"
```

**Technical gotchas:**
- New integration tests may add uncovered branches in renderer code (e.g. `entity_type == "delegate"` branch). Add targeted unit tests in the renderer test files to cover these before declaring the coverage gate met.

**Test-driven acceptance criteria:**
- `pytest` exits `0` (all tests pass).
- `TOTAL` coverage ≥ 98%.
- Per-language test count: ≥ 5 tests per language file (20 new tests minimum across all four `test_integration_*.py` files).

**Commit boundary:**
```
test(phase3): confirm ≥98% coverage gate after typed IR migration and QA suites
```

---

## Summary

| Phase | Group | GAP | Tasks | New Files | Modified Files |
|---|---|---|---|---|---|
| 1 | A | GAP-09 | 5 | `config.py`, `test_config.py` | `orchestrator.py`, `cli.py` |
| 1 | A | GAP-12 | 4 | — | `config.py`, `interfaces.py`, `orchestrator.py`, `cli.py` |
| 1 | A | GAP-07 | 6 | — | `storage.py`, `static_html.py`, `hugo_markdown.py`, `legacy.py`, `orchestrator.py` |
| 1 | A | GAP-11 | 4 | `doxyfile.py`, `test_doxyfile.py` | `doxygen.py` |
| 2 | B | GAP-05 | 7 | — | `orchestrator.py`, `cli.py`, `test_cli.py`, `test_orchestrator.py` |
| 2 | B | GAP-01 | 6 | — | `cli.py`, `test_cli.py` |
| 3 | D | GAP-03 | 11 | — | `models.py`, `test_models.py`, all parsers, all renderers |
| 3 | D | GAP-10 | 7 | `coverage.py`, `test_coverage.py` | `orchestrator.py`, `cli.py` |
| 3 | F | GAP-31 | 5 | `Tests/verify_pages.py`, `Tests/check_links.py`, `Tests/run_all_integration_tests.*` | `integration_tests_specification.md` |
| 3 | F | GAP-32 | 6 | `test_integration_cpp/cs/java/py.py` | `tests/utils.py` |
| **Total** | | **10 GAPs** | **61 tasks** | **14 new files** | **25 modified files** |

---

*Status: BACKLOG. Awaiting implementation signal for Phase 1 / TASK-A.1.1.*
