---
name: pydantic-migration-guard
description: >-
  Pre-merge verification checklist for Pydantic model migrations. Detects silent
  deserialization failures, renderer string-access breakage, factory kwarg forwarding
  gaps, and cross-layer IR contract violations introduced by typed model changes.
---

# Skill: Pydantic Model Migration Guard

## 🎯 General Description
This skill is a mandatory pre-merge gate for any commit that modifies `engine/ude/models.py`, `engine/ude/interfaces.py`, or any file that imports from them. It exists because Pydantic v2 model migrations produce the most dangerous class of silent failure in the UDE engine: code that passes all pytest assertions yet produces broken output because a field type change cascades undetected through parsers, renderers, and IR serialization.

Invoke this skill **before** merging Phase 3 (GAP-03) tasks, or any future task that renames, adds, or changes the type of a field in any Pydantic model used in the IR pipeline.

---

## 🔔 Trigger Conditions

Invoke automatically when a task specification or code diff satisfies ANY of the following:
- Modifies `engine/ude/models.py`
- Adds or renames a class in `engine/ude/models.py`
- Changes a field type from `List[str]` to `List[SomeModel]` or vice versa
- Adds a new `BaseModel` subclass that participates in `ProjectCatalog`
- Modifies `engine/ude/interfaces.py` (logger name, abstract method signatures)
- Modifies any renderer that accesses `.fields`, `.methods`, `.enums`, `.constants`, or `.type_aliases` on an entity model

---

## ⚙️ Mandatory Verification Steps

Run these six steps **in sequence** before accepting any Pydantic migration task as complete. A failure at any step is a 🔴 blocker — do NOT proceed to the next step without resolving it.

---

### Step 1 — Backward-Compat Alias Verification

All renamed model classes must expose the original name as a module-level alias. Verify:

```bash
python -c "
from ude.models import ClassEntity, NamespaceEntity, MethodEntity
from ude.models import ClassModel, NamespaceModel, MethodModel
assert ClassEntity is ClassModel, 'ClassEntity alias broken'
assert NamespaceEntity is NamespaceModel, 'NamespaceEntity alias broken'
assert MethodEntity is MethodModel, 'MethodEntity alias broken'
print('Step 1 PASSED: all backward-compat aliases intact')
"
```

**Expected output**: `Step 1 PASSED: all backward-compat aliases intact`

**Failure action**: Add the missing alias to `models.py` (e.g., `ClassEntity = ClassModel`). Do NOT remove existing aliases even if no internal code references them — external consumers of the library depend on them.

---

### Step 2 — Old IR Deserialization Safety

v1.0 `.json.gz` IR files lack the following fields introduced in v2.0: `free_functions`, `enums`, `constants`, `type_aliases`, `project_name`, `version`. Pydantic must silently default these without raising `ValidationError`.

```bash
python -c "
from ude.models import ProjectCatalog
import json

# Minimal v1.0-format IR: no free_functions, no enums, fields as empty list
old_ir = json.dumps({
    'namespaces': [{
        'name': 'MyNS',
        'classes': [{
            'name': 'MyClass',
            'fully_qualified_name': 'MyNS::MyClass',
            'fields': []
        }]
    }]
})
catalog = ProjectCatalog.model_validate_json(old_ir)
assert catalog.namespaces[0].classes[0].fields == [], 'fields default broken'
assert catalog.namespaces[0].classes[0].enums == [], 'enums default broken'
assert catalog.project_name == '', 'project_name default broken'
print('Step 2 PASSED: old IR deserializes cleanly')
"
```

**Expected output**: `Step 2 PASSED: old IR deserializes cleanly`

Also verify the **v2.0 non-empty VariableModel round-trip** (tests the actual migrated field type, not just the empty-list case):

```bash
python -c "
from ude.models import ProjectCatalog
import json

v2_ir = json.dumps({
    'namespaces': [{
        'name': 'MyNS',
        'classes': [{
            'name': 'MyClass',
            'fully_qualified_name': 'MyNS::MyClass',
            'fields': [{'name': 'myField', 'fully_qualified_name': 'MyNS::MyClass::myField', 'type': 'int'}]
        }]
    }]
})
catalog2 = ProjectCatalog.model_validate_json(v2_ir)
assert catalog2.namespaces[0].classes[0].fields[0].name == 'myField', 'VariableModel round-trip broken'
assert catalog2.namespaces[0].classes[0].fields[0].type == 'int', 'VariableModel type broken'
print('Step 2b PASSED: v2.0 VariableModel non-empty round-trip clean')
"
```

**Expected output**: `Step 2b PASSED: v2.0 VariableModel non-empty round-trip clean`

**Failure action**: Add `Field(default_factory=list)` or `= ""` defaults to every new field. Never use a required field (no default) on a model that appears in persisted IR.

---

### Step 3 — Extra-Field Safety (ConfigDict Check)

All models that can appear in user-supplied JSON (GlobalConfig, ClassModel, ProjectCatalog) must silently discard unknown keys rather than raising `ValidationError`. This prevents forward-compatibility breaks when a v2.0 client reads a v3.0 IR file.

```bash
python -c "
from ude.models import ClassModel
from ude.config import GlobalConfig

# Unknown field must be silently ignored
cls = ClassModel.model_validate({
    'name': 'X',
    'fully_qualified_name': 'NS::X',
    'unknown_v3_field': 42
})
assert cls.name == 'X'

cfg = GlobalConfig.model_validate({'log_level': 'DEBUG', 'future_option': True})
assert cfg.log_level == 'DEBUG'

print('Step 3 PASSED: extra fields silently ignored')
"
```

**Expected output**: `Step 3 PASSED: extra fields silently ignored`

**Failure action**: Add `model_config = ConfigDict(extra=\"ignore\")` to any model that lacks it.

---

### Step 4 — Renderer String-Access Scan

After any `List[str]` → `List[SomeModel]` field change, every renderer that accesses that field must be updated to use attribute access (`.name`, `.type`) rather than treating the element as a bare string.

```bash
# bash / Git Bash / WSL / CI
grep -rn "\.fields\b" engine/ude/renderers/
grep -rn "\.methods\b" engine/ude/renderers/
grep -rn "\.enums\b" engine/ude/renderers/
grep -rn "\.constants\b" engine/ude/renderers/
grep -rn "\.type_aliases\b" engine/ude/renderers/
```

```powershell
# Windows (PowerShell) — equivalent scan
foreach ($pattern in @("\.fields\b","\.methods\b","\.enums\b","\.constants\b","\.type_aliases\b")) {
    Get-ChildItem -Recurse engine/ude/renderers/*.py |
        Select-String -Pattern $pattern |
        Select-Object Path, LineNumber, Line
}
```

> **Note**: On Windows without Git Bash or WSL, use the PowerShell block above. Both produce equivalent output — a list of file:line hits to inspect manually.

For every match, manually verify the line treats the element as a **model object** (accessing `.name`, `.type`, `.docstring`, etc.), NOT as a bare string passed to an f-string, `.format()`, string concatenation, or Jinja2 `{{ field }}` without attribute access.

**Red flags to look for**:
```python
# BROKEN — field is now a VariableModel, not a str
f"Field: {field}"
f"{field}"
str(field)
content += field + "\n"
```

**Correct patterns**:
```python
# CORRECT
f"Field: {field.name} ({field.type})"
f"{field.name}"
```

**Failure action**: Update every renderer line and every Jinja2 template variable that passes a typed field element directly as a string.

---

### Step 5 — Factory Kwarg Forwarding Verification

`HtmlRenderer` uses `__new__` as a factory that dispatches to language-specific subclasses. Any kwarg added to renderer constructors (e.g., `cache_manager`) must be explicitly forwarded through `__new__` into the concrete subclass `__init__`. Failure to do this silently drops the kwarg — the L2 cache is never wired, but no exception is raised and all unit tests pass.

```bash
# Check all three renderer families for factory kwarg forwarding (bash / Git Bash / WSL)
for f in engine/ude/renderers/static_html.py \
          engine/ude/renderers/hugo_markdown.py \
          engine/ude/renderers/legacy.py; do
  echo "=== $f ==="
  grep -n "def __new__\|def __init__\|cache_manager" "$f"
done
```

```powershell
# Windows (PowerShell)
foreach ($f in @("engine/ude/renderers/static_html.py",
                 "engine/ude/renderers/hugo_markdown.py",
                 "engine/ude/renderers/legacy.py")) {
    Write-Host "=== $f ===" -ForegroundColor Cyan
    Select-String -Path $f -Pattern "def __new__|def __init__|cache_manager"
}
```

**Required** (verified for ALL THREE renderer files): `cache_manager` must appear in:
1. The `__new__` method signature (or `**kwargs` that captures it), AND
2. The `super().__init__(...)` call that forwards kwargs to the concrete subclass.

A gap in `hugo_markdown.py` or `legacy.py` is just as fatal as a gap in `static_html.py` — the L2 cache will be silently disconnected for those output formats.

**Failure action**: Add `cache_manager` explicitly to `__new__`'s parameter list in each failing renderer and forward it through. Do not rely on `**kwargs` alone without verifying the concrete subclass `__init__` also declares the parameter.

---

### Step 6 — Full Test Suite + Coverage Gate

```bash
cd engine
poetry run pytest tests/ -v --tb=short 2>&1 | tail -40
poetry run pytest --cov=ude --cov-report=term-missing | grep "TOTAL"
```

**Requirements**:
- All tests PASSED (exit code 0).
- `TOTAL` coverage `>= 98%`.
- If golden master tests fail, run them separately and inspect the diff before updating baselines:

```bash
poetry run pytest tests/test_golden_master.py -v --tb=short
```

If output structure changed expectedly (new entity types now appear), ask the user:
> "The golden master diff shows new entity sections in the output (expected from GAP-03). Shall I regenerate the baselines?"

Only update baselines upon explicit confirmation:
```powershell
# Windows (PowerShell)
$env:UPDATE_BASELINES="1"; poetry run pytest tests/test_golden_master.py
```
```bash
# Linux / macOS / CI
UPDATE_BASELINES=1 poetry run pytest tests/test_golden_master.py
```

**Failure action**: Any failing test is a 🔴 blocker. Do NOT accept coverage < 98% — identify uncovered branches (usually new exception paths or new model fields) and add targeted tests.

---

## 📄 Output Template

Generate this report after completing all six steps:

```markdown
# Pydantic Migration Guard Report: [Commit / Task ID]

## 📊 Verification Matrix

| Check | Status | Detail |
| :--- | :---: | :--- |
| **Step 1** — Backward-compat aliases | 🟢/🔴 | [Aliases present / Missing: X, Y] |
| **Step 2** — Old IR deserialization | 🟢/🔴 | [Clean / ValidationError on field: X] |
| **Step 3** — Extra-field safety | 🟢/🔴 | [ConfigDict(extra="ignore") present / Missing on: X] |
| **Step 4** — Renderer string-access scan | 🟢/🟡/🔴 | [N hits requiring review / All clean] |
| **Step 5** — Factory kwarg forwarding | 🟢/🔴 | [cache_manager forwarded / Missing from __new__] |
| **Step 6** — Test suite + coverage | 🟢/🔴 | [X% coverage / N failures] |

*🟢 = Pass (no action required) · 🟡 = Warning (review recommended) · 🔴 = Blocker (must resolve before merge)*

## 🔍 Findings and Required Actions
* **[Step N]**: [Description of failure]. *Action*: [Exact fix required].

## 🧪 Test Evidence
- **pytest exit code**: `[0 = pass / 1 = fail]`
- **Coverage**: `[XX%]` — `[complies / does NOT comply]` with ≥ 98% gate
- **Golden master**: `[Passed / Failed — baselines updated with user approval / Failed — regression]`
```

---

## ⚠️ Common Migration Pitfalls

* **Silent default trap**: Adding a new required field (no default) to `ProjectCatalog` or `ClassModel` will cause all existing `.json.gz` IR files to fail deserialization. Always provide a default.
* **Alias drift**: Renaming a model class without adding the alias immediately breaks any external caller that imports the old name. Ship alias and rename in the same commit.
* **Factory blind spot**: The `HtmlRenderer.__new__` factory is the single most common place for new kwargs to be silently dropped. Always verify forwarding explicitly — do not trust that it "probably works."
* **Template string leakage**: Jinja2 templates that iterate `{% for field in entity.fields %}{{ field }}` will render a Pydantic model repr string (e.g., `name='x' type='int' ...`) instead of the field name after the `List[str]` → `List[VariableModel]` migration. Always update templates alongside model changes.
* **Cross-layer breakage**: A model change that passes parser tests AND renderer tests individually can still fail integration tests if the serialization format changed (e.g., `model_dump_json()` output used as an L2 cache signature key). Run the full pipeline integration test, not just unit tests per layer.
