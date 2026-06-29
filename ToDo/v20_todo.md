# UDE v2.0 — Сводный план задач

> **Документ:** `ToDo/v20_todo.md`  
> **Дата:** 2026-06-29  
> **Источники:**  
> - `.antigravitycli/v2_execution_plan.md` — технический план фаз (GAP-09 → GAP-12 → GAP-07 → GAP-11 → GAP-05 → GAP-01 → GAP-03 → GAP-10 → GAP-31 → GAP-32)  
> - `ToDo/RepoStruct_ToDo.md` — структура репозитория  
> - `ToDo/CICD_ToDo.md` — CI/CD миграция  
> - `ToDo/ActivitiesReqs_ToDo.md` — требования к пайплайнам  
> - `ToDo/ActivitiesDoc_ToDo.md` — документация пайплайнов  
> - `ToDo/DocReqs_ToDo.md` — требования к технической документации  
> - `ToDo/UserDocs_ToDo.md` — пользовательская документация  
>
> **TDD-инвариант (обязателен для каждого коммита):**  
> Red → Green → Refactor · Coverage gate ≥ 98% · Ни один шаг не снимается без пройденных тестов

---

## Условные обозначения

| Маркер | Значение |
|--------|----------|
| 🔴 | Блокирует следующий шаг / критичный |
| 🟡 | Важно для v2.0 / требуется до релиза |
| 🟢 | Желательно / можно параллелить |
| ⚡ | Зависит от завершения предыдущего шага |
| `[GAP-XX]` | Ссылка на GAP из `v2_execution_plan.md` |
| `[AD-XXX]` | Ссылка на задачу из `ActivitiesDoc_ToDo.md` |
| `[AR-XXX]` | Ссылка на задачу из `ActivitiesReqs_ToDo.md` |
| `[DR-XXX]` | Ссылка на задачу из `DocReqs_ToDo.md` |
| `[UD-XXX]` | Ссылка на задачу из `UserDocs_ToDo.md` |
| `[RS-TX]` | Ссылка на задачу из `RepoStruct_ToDo.md` |
| `[CI-X.Y]` | Ссылка на задачу из `CICD_ToDo.md` |

---

## Раздел 0 — Подготовка репозитория и окружения

> **Цель:** Привести репозиторий в порядок до начала реализации v2.0. Выполняется один раз. Не блокирует Phase 1 полностью, но снижает технический долг.

### 0.1 Структурные изменения репозитория (нулевой риск)

- [ ] **[RS-T1]** 🔴 Закоммитить незакоммиченные архитектурные документы: `CICD.md`, `RepoStruct.md`, `RepoStruct_ToDo.md`
- [ ] **[RS-T2]** 🔴 Удалить `FutureImprovements/` — 4 файла без ценности (`doxygen_cpp.py`, `cpp_signature_formatter.py`, `legacy_cpp_sidebar.json`, `cpp_class_layout.html`)
- [ ] **[RS-T3]** 🔴 Задокументировать конвенцию `ude_`-префикса для корневых директорий в `CLAUDE.md`
- [ ] **[RS-T4]** 🟡 Переименовать `/refs/` → `/sdk_refs/` в `.gitignore` (устраняет конфликт с git-терминологией)
- [ ] **[RS-T5]** 🟡 Переместить утилиты `compress_history.bat`, `compress_history.ps1`, `run_swig.bat` в `scripts/`
- [ ] **[RS-T6]** 🟢 Объединить `Tests/` + `LoadTest/` → `ude_tests/regression/` + `ude_tests/load/`; обновить пути в `.github/workflows/integration_tests.yml`
- [ ] **[RS-T7]** 🟢 Проверить избыточность правил `.gitignore` для `ude_projects/` — запустить генерацию, проверить `git status`
- [ ] **[RS-T8]** 🟢 Провести аудит `make_release.py` — понять логику ODA-совместимости (prerequisite для RS-T9)
- [ ] **[RS-T9]** 🟢 Переименовать `main/` → `sdk_sources/` после RS-T8
- [ ] **[RS-T10]** 🟢 Переименовать ветку umbrella `master` → `main` (требует координации с CI/CD)

### 0.2 Подтверждение базового состояния v1.0

- [ ] 🔴 Убедиться что 209 тестов движка проходят: `poetry run pytest engine/tests/ -v`
- [ ] 🔴 Подтвердить coverage ≥ 98%: `poetry run pytest --cov=ude --cov-report=term-missing`
- [ ] 🔴 Зафиксировать baseline метрики: количество тестов, % coverage, время прогона
- [ ] 🟡 Запустить performance benchmark: `poetry run pytest tests/test_performance_benchmark.py -v` — убедиться что ≤ 5s для 1000 классов

### 0.3 Требования к документированию кода (применяются с этого момента)

- [ ] **[DR-NEW-04]** 🟡 Зафиксировать в `CLAUDE.md` правило именования файлов: kebab-case для `user-docs/`, snake_case для `.antigravitycli/`
- [ ] **[DR-NEW-21]** 🟡 Установить правило: каждый новый GitHub Actions workflow начинается с блока комментариев (назначение, триггеры, secrets, время выполнения)
- [ ] **[DR-NEW-20]** 🟡 Ввести правило: каждый новый `TASK-*.md` содержит поле `Related Docs` — файлы user-docs/design-docs, требующие обновления

---

## Раздел 1 — Фаза 1: Инфраструктура движка

> **Стратегический порядок:** GAP-09 → GAP-12 → GAP-07 → GAP-11  
> Каждый GAP разблокирует следующий. Всё разделение полностью последовательно.

### 1.1 GAP-09 — Активация полей GlobalConfig `[REQ-V2-01]`

> **Цель:** Сделать все поля `ude_global_config.json` оперативно активными через Pydantic-модель.

**Тесты (RED — написать первыми):**

- [ ] 🔴 Создать `engine/tests/test_config.py` — 6 тест-кейсов:
  - `test_global_config_defaults` — пустой JSON даёт все дефолты
  - `test_global_config_full_round_trip` — все поля round-trip через `from_file()`
  - `test_global_config_unknown_keys_ignored` — extra keys не бросают исключений
  - `test_global_config_missing_file_raises` — `FileNotFoundError` при отсутствии файла
  - `test_orchestrator_respects_doxygen_path` — mock `DoxygenXmlCollector`, проверить env var
  - `test_orchestrator_respects_cache_root_dir` — `BuildCacheManager` получает абсолютный путь

**Реализация (GREEN):**

- [ ] ⚡ 🔴 Создать `engine/ude/config.py` — `GlobalConfig(BaseModel)` с полями `doxygen_path`, `log_level`, `log_file`, `cache_root_dir`, `global_templates_dir`, `error_policy`, `translation_service`, `coverage_mode`, `coverage_threshold`; фабрика `from_file()`; `ConfigDict(extra="ignore")`
- [ ] ⚡ 🔴 Заменить raw `json.load` в `UdeOrchestrator.__init__()` на `GlobalConfig.from_file()`, хранить как `self._global_cfg`
- [ ] ⚡ 🔴 В `run_target()`: инжектировать `doxygen_path` в env, резолвить `global_templates_dir` и `cache_root_dir`
- [ ] ⚡ 🔴 В `cli.py:run_pipeline()`: заменить raw `json.load` на `GlobalConfig.from_file()`
- [ ] ⚡ 🔴 Все пути в `GlobalConfig` резолвить относительно родительской директории config-файла, не CWD

**Верификация:**
```bash
poetry run pytest tests/test_config.py -v --tb=short
# Ожидается: 6/6 PASSED
poetry run pytest --cov=ude --cov-report=term-missing | grep TOTAL
# Ожидается: ≥ 98%
```

**Коммит:** `feat(config): add GlobalConfig pydantic model with from_file() factory`

---

### 1.2 GAP-12 — Унифицированное логирование `[REQ-V2-02]`

> **Prerequisite:** GAP-09 завершён и смёрджен.

**Тесты (RED):**

- [ ] ⚡ 🔴 Дополнить `engine/tests/test_config.py` — 4 новых тест-кейса:
  - `test_logging_setup_stderr_only` — `log_file=None` → ровно 1 StreamHandler
  - `test_logging_setup_with_file` — `log_file` установлен → 2 хэндлера, файл создан
  - `test_logging_setup_level_applied` — `log_level="DEBUG"` → `logger.level == DEBUG`
  - `test_hc05_logger_label_fixed` — `"ude.interfaces"` использован в `interfaces.py`

**Реализация (GREEN):**

- [ ] ⚡ 🔴 В `engine/ude/interfaces.py` строка 8: `"ude.renderers"` → `"ude.interfaces"` (HC-05)
- [ ] ⚡ 🔴 Добавить `logging_setup(cfg: GlobalConfig) -> None` в `engine/ude/config.py` с `root.handlers.clear()`
- [ ] ⚡ 🔴 Вызвать `logging_setup(self._global_cfg)` в `UdeOrchestrator.__init__()` после `from_file()`
- [ ] ⚡ 🔴 Вызвать `logging_setup(global_cfg)` в `cli.py:run_pipeline()` сразу после загрузки конфига
- [ ] ⚡ 🟡 Найти все тесты с assert `"ude.renderers"` из `interfaces.py` и обновить

**Верификация:**
```bash
poetry run pytest tests/test_config.py -v -k "logging"
# Ожидается: 4/4 PASSED
```

**Коммит:** `feat(config): add unified logging_setup(); fix HC-05 logger label`

---

### 1.3 GAP-07 — Активация L2 Render Cache `[REQ-V2-03]`

> **Prerequisite:** GAP-09 завершён (нужен `cache_root_dir` из `GlobalConfig`).

**Тесты (RED):**

- [ ] ⚡ 🔴 Дополнить `engine/tests/test_caching.py` — 4 новых тест-кейса:
  - `test_l2_cache_hit_skips_file_write` — рендер дважды, второй не перезаписывает файл
  - `test_l2_cache_miss_on_ir_change` — изменение в catalog → файл пересоздаётся
  - `test_l2_cache_miss_on_template_change` — изменение шаблона → файл пересоздаётся
  - `test_l2_cache_disabled_when_no_cache_dir` — `cache_dir=None` → поведение v1.0 без регрессии

**Реализация (GREEN):**

- [ ] ⚡ 🔴 Проверить/реализовать `BuildCacheManager` в `engine/ude/storage.py` — методы `is_render_stale()`, `update()`, `save()`
- [ ] ⚡ 🔴 Добавить `compute_template_hash(template_dir: Path) -> str` в `storage.py`
- [ ] ⚡ 🔴 Резолвить `cache_dir` в `UdeOrchestrator.run_target()` из `GlobalConfig.cache_root_dir`
- [ ] ⚡ 🔴 Передать `cache_dir` в конструктор рендерера; обновить `BaseRenderer.__init__()` — параметр `cache_dir: Optional[Path] = None`
- [ ] ⚡ 🔴 В `BaseRenderer.render()`: перед записью каждого файла — проверить L2 cache, при HIT — пропустить запись, логировать DEBUG `"[L2 cache HIT]"`
- [ ] ⚡ 🔴 Убедиться: `cache_manager` kwarg пробрасывается через `__new__` всех трёх семейств рендереров (`static_html`, `hugo_markdown`, `legacy`)

**Верификация:**
```bash
poetry run pytest tests/test_caching.py -v
# Ожидается: все L2-тесты PASSED
# Второй прогон должен логировать "[L2 cache HIT]" для неизменных сущностей
```

**Коммит:** `feat(cache): wire L2 render cache into BaseRenderer.render()`

---

### 1.4 GAP-11 — Doxyfile 3-уровневый ключевой мёрдж `[REQ-V2-04]`

> **Prerequisite:** Не имеет жёсткой зависимости от GAP-09/12/07, но выполняется после них.

**Тесты (RED — TDD):**

- [ ] ⚡ 🔴 Создать `engine/tests/test_doxyfile.py` — 8 тест-кейсов:
  - `test_parse_doxyfile_basic`
  - `test_parse_doxyfile_continuation_lines` — backslash-continuation сворачиваются
  - `test_parse_doxyfile_skip_comments`
  - `test_serialize_doxyfile_round_trip`
  - `test_merge_tiers_t2_overrides_t1`
  - `test_merge_tiers_t3_overrides_t2`
  - `test_merge_tiers_debug_log_on_conflict` (с `caplog`)
  - `test_collector_uses_merged_doxyfile` — mock `subprocess.run`, assert содержимое Doxyfile

**Реализация (GREEN):**

- [ ] ⚡ 🔴 Создать `engine/ude/collectors/doxyfile.py` — `parse_doxyfile()`, `serialize_doxyfile()`, `merge_doxyfile_tiers(t1, t2, t3) -> dict`
- [ ] ⚡ 🔴 В `engine/ude/collectors/doxygen.py`: заменить конкатенацию 3-х файлов на `parse_doxyfile` + `merge_doxyfile_tiers` + `serialize_doxyfile`
- [ ] ⚡ 🟡 Обеспечить: при отсутствии `global_templates_dir` → T1 = `{}` (мёрдж деградирует до T2+T3)
- [ ] ⚡ 🟡 Обратная совместимость: `doxyfile_template` в `ude_doc_config.json` продолжает работать

**Верификация:**
```bash
poetry run pytest tests/test_doxyfile.py -v
# Ожидается: 8/8 PASSED
poetry run pytest --cov=ude --cov-report=term-missing | grep TOTAL
# Ожидается: ≥ 98%
```

**Коммит:** `feat(collector): replace doxyfile concatenation with 3-tier key-level merge`

---

### 1.5 Обеспечение окружения Phase 1 (CI/CD security gate)

- [ ] **[AR-GAP-02]** 🔴 Добавить блок `permissions:` в `integration_tests.yml`: `contents: read`, `checks: write`, `actions: read`
- [ ] **[AD-SEC-01]** 🔴 Зафиксировать версию `actions/checkout` (pinned semver-tag)
- [ ] **[AD-SEC-02]** 🔴 Зафиксировать версию `actions/setup-python` (pinned semver-tag)
- [ ] **[AD-SEC-03]** 🔴 Зафиксировать версию `peaceiris/actions-hugo` (конкретная версия, не `latest`)
- [ ] **[AD-SEC-07]** 🔴 Убрать fallback `|| github.token` — workflow должен явно падать без PAT
- [ ] **[AD-ISO-01]** 🟡 Перевести `pip install` на virtual environment в CI runner
- [ ] **[AD-ISO-02]** 🟡 Перенести `PYTHONPATH: engine` в секцию `env:` на уровне job

---

## Раздел 2 — Фаза 2: Library API и CLI Unification

> **Стратегический порядок:** GAP-05 → GAP-01  
> **Prerequisite:** Phase 1 полностью завершена.

### 2.1 GAP-05 — UdeOrchestrator Public Library API `[REQ-V2-05]`

**Тесты (RED):**

- [ ] ⚡ 🔴 Дополнить `engine/tests/test_orchestrator.py` — 4 новых теста:
  - `test_orchestrator_parse_returns_catalog`
  - `test_orchestrator_render_produces_files`
  - `test_orchestrator_run_end_to_end`
  - `test_cli_delegates_to_orchestrator` (mock `UdeOrchestrator.run`)
- [ ] ⚡ 🔴 Обновить `engine/tests/test_cli.py`: переместить тесты `deep_merge`/`find_product_json` на импорт из `ude.orchestrator`

**Реализация (GREEN):**

- [ ] ⚡ 🔴 Переместить `deep_merge()` и `find_product_json()` из `cli.py` → `orchestrator.py`
- [ ] ⚡ 🔴 Обновить импорт в `cli.py`: `from ude.orchestrator import deep_merge, find_product_json`
- [ ] ⚡ 🔴 Добавить `resolve_config(doc_config_path, global_cfg) -> tuple[dict, Path]` в `orchestrator.py`
- [ ] ⚡ 🔴 Реализовать публичный метод `parse(config, config_dir) -> ProjectCatalog` на `UdeOrchestrator`
- [ ] ⚡ 🔴 Реализовать публичный метод `render(catalog, config, config_dir, out_dir) -> None`
- [ ] ⚡ 🔴 Реализовать публичный метод `run(doc_config_path) -> bool` — end-to-end shortcut
- [ ] ⚡ 🔴 Сделать `run_target()` тонким алиасом, вызывающим `run()` для обратной совместимости
- [ ] ⚡ 🔴 Упростить `cli.py:run_pipeline()` до: load GlobalConfig → instantiate orchestrator → call `run()`
- [ ] ⚡ 🟡 v1.0 flat CLI flags (`--global-config`, `--sdk-config`, `--doc-config`, `--input`, `--output`, `--format`) работают идентично

**Smoke test:**
```bash
python -c "from ude.orchestrator import UdeOrchestrator; o = UdeOrchestrator(); print(dir(o))"
# parse, render, run — в выводе
```

**Коммит:** `refactor(orchestrator): expose public parse/render/run API; slim cli.py`

---

### 2.2 GAP-01 — CLI Subcommands `[REQ-V2-06]`

> **Prerequisite:** GAP-05 завершён.

**Тесты (RED):**

- [ ] ⚡ 🔴 Дополнить `engine/tests/test_cli.py` — 6 новых тестов:
  - `test_compile_subcommand_delegates_to_run`
  - `test_parse_subcommand_creates_ir_file`
  - `test_render_subcommand_from_ir_file`
  - `test_flat_flags_still_work` — backward compat
  - `test_parse_then_render_output_identical_to_compile`
  - `test_audit_subcommand_reachable` — возвращает non-zero (stub), не крашит argparse

**Реализация (GREEN):**

- [ ] ⚡ 🔴 Реструктурировать `main()` в `cli.py` — `parser.add_subparsers(dest="command")`; при `args.command is None` — fallback к v1.0
- [ ] ⚡ 🔴 Реализовать субкоманду `ude compile` — поведение идентично v1.0 flat
- [ ] ⚡ 🔴 Реализовать субкоманду `ude parse` — аргумент `--output-ir`, печатает JSON summary на stdout
- [ ] ⚡ 🔴 Реализовать субкоманду `ude render` — аргумент `--input-ir`, загружает IR и рендерит
- [ ] ⚡ 🔴 Реализовать субкоманду `ude audit` — shell stub с `NotImplementedError` (полная реализация в GAP-10)
- [ ] ⚡ 🟡 `ude compile --doc-config X` и `ude --doc-config X` дают byte-identical output

**Верификация:**
```bash
poetry run pytest tests/test_cli.py -v
# Все тесты PASSED
```

**Коммит:** `feat(cli): add compile/parse/render/audit subcommands; keep v1.0 flat interface`

---

### 2.3 Документация CLI для User Docs

- [ ] **[UD-CLI-01]** 🟡 Создать `user-docs/docs/reference/cli-reference.md`
- [ ] **[UD-CLI-02]** 🟡 Задокументировать v1.0 flat-интерфейс (backward compat)
- [ ] **[UD-CLI-03]** 🟡 Задокументировать `ude compile` — аргументы, примеры, exit-коды
- [ ] **[UD-CLI-04]** 🟡 Задокументировать `ude parse` — `--output-ir`, формат JSON summary
- [ ] **[UD-CLI-05]** 🟡 Задокументировать `ude render` — `--input-ir`, разделённый pipeline
- [ ] **[UD-CLI-06]** 🟡 Задокументировать `ude audit` (stub в v2.0) — режимы, exit-коды
- [ ] **[UD-CLI-07]** 🟡 Добавить таблицу exit-кодов: 0 (success), 1 (error), 2 (audit fail)
- [ ] **[UD-CLI-08]** 🟢 Добавить примеры конвейера `ude parse` + `ude render`

### 2.4 CI Transition Gate для CLI

- [ ] **[CI-4.4]** 🟡 Добавить в `generate-api-ref.yml` CLI backward compatibility smoke test: `ude --help`, `ude compile --help`, `ude parse --help`, `ude render --help`, `ude audit --help`
- [ ] **[CI-4.4]** 🟡 После реализации GAP-01: обновить step компиляции в CI с flat CLI на `ude compile --all --output`; перед переключением верифицировать byte-identical output между v1.0 и v2.0

---

## Раздел 3 — Фаза 3 / Трек D: Типизированный IR

> **Prerequisite:** GAP-01 завершён (`ude audit` stub доступен).  
> **Внимание:** Самый объёмный пункт v2.0. Затрагивает все слои pipeline.  
> **Порядок:** GAP-03 → GAP-10

### 3.1 GAP-03 — Типизированные модели сущностей `[REQ-V2-07]`

**Тесты (RED — написать до изменения models.py):**

- [ ] ⚡ 🔴 Переписать `engine/tests/test_models.py` под 7 новых моделей — round-trip для каждой
- [ ] ⚡ 🔴 Добавить тесты: `ProjectCatalog` с `project_name` и `version`; старые IR-файлы без этих полей десериализуются

**Реализация `models.py` (GREEN):**

- [ ] ⚡ 🔴 Полностью заменить `engine/ude/models.py` — 7 моделей: `ParameterModel`, `OverloadModel`, `MethodModel`, `EnumModel`, `VariableModel`, `ConstantModel`, `TypeAliasModel`, `ClassModel`, `NamespaceModel`, `ProjectCatalog`
- [ ] ⚡ 🔴 `ProjectCatalog` добавить `project_name: str = ""` и `version: str = ""`
- [ ] ⚡ 🔴 Глобальный поиск-замена: `NamespaceEntity` → `NamespaceModel` по всей кодовой базе
- [ ] ⚡ 🔴 Закоммитить `models.py` в изоляции — до правки парсеров и рендереров

**Рефакторинг парсеров:**

- [ ] ⚡ 🔴 `engine/ude/parsers/doxygen.py` — `ClassEntity(...)` → `ClassModel(...)`; `NamespaceEntity(...)` → `NamespaceModel(...)`; `MethodEntity` → `MethodModel`; `ParameterField` → `ParameterModel`
- [ ] ⚡ 🔴 `doxygen_csharp.py`, `doxygen_java.py`, `doxygen_python.py`, `doxygen_base.py`, `doxygen_router.py` — аналогичный рефакторинг
- [ ] ⚡ 🔴 Заполнить новые типизированные списки (`VariableModel`, `ConstantModel`, `EnumModel`) данными из Doxygen XML; при недостатке метаданных — `None`, не удалять сущность
- [ ] ⚡ 🔴 После каждого файла — `poetry run pytest tests/test_doxygen_parser.py` (catch regressions early)

**Рефакторинг рендереров:**

- [ ] ⚡ 🔴 `engine/ude/renderers/static_html.py` — заменить атрибуты `ClassEntity` на новые модели; `entity.fields` (was `List[str]`) → iterate as `List[VariableModel]`
- [ ] ⚡ 🔴 `hugo_markdown.py` — аналогичный рефакторинг
- [ ] ⚡ 🔴 `legacy.py` — аналогичный рефакторинг
- [ ] ⚡ 🟡 Добавить рендеринг `entity.enums`, `entity.constants`, `entity.type_aliases` в существующих секциях страниц (без новых layout-изменений — v3.0+)

**Рефакторинг хранилища и тестов:**

- [ ] ⚡ 🔴 `engine/ude/storage.py` — добавить round-trip тест 7-модельной структуры через gzip
- [ ] ⚡ 🔴 Обновить `test_doxygen_parser.py`, `test_html_renderer.py`, `test_hugo_renderer.py`, `test_legacy_renderer.py`, `test_integration_pipeline.py` под новую схему
- [ ] ⚡ 🔴 Регенерировать golden master baselines (`UPDATE_GOLDEN=1 poetry run pytest tests/test_golden_master.py`) — только после подтверждения `git diff --stat`
- [ ] ⚡ 🔴 Перезапустить Docomatic alignment suite (`test_docomatic_alignment.py`); проверить что `"total_differences"` не вырос для незатронутых языков

**Верификация Pydantic-совместимости (CB-02, CB-03 из `skills_compliance_report.md`):**

- [ ] ⚡ 🔴 Проверить наличие `model_config = ConfigDict(extra="ignore")` на КАЖДОЙ из типизированных Pydantic-моделей в `engine/ude/models.py` (CB-02): `ParameterModel`, `OverloadModel`, `MethodModel`, `EnumModel`, `VariableModel`, `ConstantModel`, `TypeAliasModel`, `ClassModel`, `NamespaceModel`, `ProjectCatalog` — отсутствие хотя бы на одной делает загрузку v3.0+ IR-файлов несовместимой (`ValidationError` при неизвестных полях); выполнить: `grep -c "extra=\"ignore\"" engine/ude/models.py` — должно вернуть ≥ 10
- [ ] ⚡ 🔴 Написать тест `test_variable_model_nonempty_round_trip` (CB-03 — Pydantic Guard Step 2b): создать `ProjectCatalog` с `ClassModel(fields=[VariableModel(name="myField", fully_qualified_name="NS::C::myField", type="int")])`, сериализовать в JSON и обратно; проверить `fields[0].name == "myField"` и `fields[0].type == "int"` — тест верифицирует непустой VariableModel round-trip, не покрываемый тестом `test_old_ir_json_deserializes_without_error`, который проверяет только пустые дефолты
- [ ] ⚡ 🔴 **[TASK-D.1.12]** После завершения TASK-D.1.9 (рефакторинг `legacy.py`): выполнить Docomatic alignment re-baseline check — `poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short`; если `"total_differences"` вырос для любого из языков (C++, C#, Java) относительно pre-GAP-03 baseline — применить SOP `.antigravitycli/skills/difference_minimization_iterator.md` Шаг 5 до полного восстановления значений; GAP-03 не считается завершённым без явного подтверждения нулевого роста расхождений (CO-04)
- [ ] ⚡ 🟡 При регенерации golden master на Windows использовать PowerShell-форму команды (AW-02 — портируемость): `$env:UPDATE_GOLDEN = "1"; poetry run pytest engine/tests/test_golden_master.py -v` — Linux-форма `UPDATE_GOLDEN=1 poetry run pytest ...` не работает в PowerShell и не подходит для CI-матрицы с Windows runner

**Coverage checkpoint:**
```bash
poetry run pytest --cov=ude --cov-report=term-missing | grep TOTAL
# Ожидается: ≥ 98%
```

**Коммит:** `feat(models): replace ClassEntity with 7 typed Pydantic models (GAP-03)`

---

### 3.2 GAP-10 — Documentation Coverage Gate `[REQ-V2-08]`

> **Prerequisite:** GAP-03 (typed IR) и GAP-01 (ude audit stub) завершены.

**Тесты (RED):**

- [ ] ⚡ 🔴 Создать `engine/tests/test_coverage.py` — 6 тест-кейсов:
  - `test_full_coverage_catalog` — все docstrings → `overall.coverage == 1.0`
  - `test_zero_coverage_catalog` — все `None` → `overall.coverage == 0.0`
  - `test_mixed_coverage` — 3 из 4 методов → `method.coverage == 0.75`
  - `test_reject_mode_exits_nonzero` — 0% coverage + reject → exit code 2
  - `test_allow_mode_exits_zero` — 0% coverage + allow → exit code 0
  - `test_audit_output_contains_table` — stdout содержит `| class |`, `| method |`, `| overall |`

**Реализация (GREEN):**

- [ ] ⚡ 🔴 Создать `engine/ude/coverage.py` — модели `EntityCoverage`, `CoverageReport`; функция `compute_coverage(catalog: ProjectCatalog) -> CoverageReport`
- [ ] ⚡ 🔴 Расширить `GlobalConfig` в `config.py`: `coverage_mode` и `coverage_threshold` становятся активными (были stub в TASK-A.1.1)
- [ ] ⚡ 🔴 Реализовать `ude audit` handler в `cli.py` — вызов `orchestrator.parse()` + `compute_coverage()` + печать таблицы + apply mode policy
- [ ] ⚡ 🔴 В `UdeOrchestrator.run()`: после рендеринга вызвать `apply_coverage_gate(catalog, self._global_cfg)` — только для `ude compile` и `ude audit`, НЕ для `ude parse` и `ude render`
- [ ] ⚡ 🔴 Coverage gate активен только на ветке `main` в CI (conditional `if: github.ref == 'refs/heads/main'`)

**Верификация:**
```bash
poetry run pytest tests/test_coverage.py -v
# Все PASSED
ude audit --doc-config path/to/ude_doc_config.json --mode allow-undocumented
# Печатает coverage table; exit 0
ude audit --doc-config path/to/ude_doc_config.json --mode reject-undocumented --threshold 0.99
# Exit 2 если coverage < 99%
```

**Коммит:** `feat(coverage): implement ude audit coverage gate (GAP-10)`

### 3.3 CI gate для GAP-10

- [ ] **[CI-4.3]** 🟡 После реализации GAP-10: добавить step в `generate-api-ref.yml`:
  ```yaml
  - name: Documentation Coverage Audit Gate
    run: python -m ude audit --mode reject-undocumented --threshold 0.80
    if: github.ref == 'refs/heads/main'
  ```
- [ ] **[AD-QA-02]** 🟡 Настроить порог coverage gate: убедиться что coverage ≥ 90% (дефолт 0.80, затем повышать)

---

## Раздел 4 — Фаза 3 / Трек F: QA и тестирование

> **Параллельно с Треком D.** GAP-31 и GAP-32 независимы — можно чередовать спринты.

### 4.1 GAP-31 — Подтверждение внешних интеграционных скриптов `[REQ-V2-09]`

**Аудит (выполнить первым):**

- [ ] ⚡ 🔴 Поиск по всему `Pipeline/`: `run_regression_tests.py`, `verify_pages.py`, `check_links.py`
- [ ] ⚡ 🔴 Обновить `integration_tests_specification.md` — для каждого скрипта: Confirmed Present / Confirmed Absent / Replaced By
- [ ] ⚡ 🔴 Зафиксировать: `engine/tests/test_golden_master.py` является каноническим TEST-INT-01

**Реализация отсутствующих скриптов:**

- [ ] ⚡ 🔴 Проверить наличие `Tests/verify_pages.py`; если отсутствует — реализовать:
  - Интерфейс: `python Tests/verify_pages.py --output-dir path/to/ude_output`
  - Проверяет: все `<a href>` internal links резолвятся в локальные файлы
  - Exit 0 / 1 с перечнем broken links; без сетевого доступа
- [ ] ⚡ 🔴 Проверить наличие `Tests/check_links.py`; если отсутствует — реализовать:
  - Интерфейс: `python Tests/check_links.py --site-dir path/to/hugo_output`
  - Проверяет: cross-references markdown → HTML
- [ ] ⚡ 🟡 Создать `Tests/run_all_integration_tests.sh` / `.bat` — агрегирует exit codes всех скриптов
- [ ] ⚡ 🟡 Обновить `integration_tests_specification.md` с точными путями к файлам

**Верификация:**
```bash
python Tests/verify_pages.py --output-dir ude_output/
# Exit 0: "All X links verified."
python Tests/check_links.py --site-dir hugo-site/public/
# Exit 0 с количеством ссылок
```

**Коммит:** `feat(tests): confirm/implement verify_pages.py and check_links.py (GAP-31)`

### 4.2 GAP-31 — Интеграция скриптов в CI

- [ ] **[AD-QA-04]** 🟡 Добавить step в `integration_tests.yml`: `Tests/check_links.py --site-dir ./user-docs/.vitepress/dist`
- [ ] **[AD-V2-04]** 🟡 Добавить step `python Tests/run_regression_tests.py` в `integration_tests.yml` как отдельный stage после page verification
- [ ] **[AD-QA-05]** 🟢 Добавить `actions/upload-artifact@v4` для pytest coverage HTML report и `verify_pages.py` output — retention 7 дней

---

### 4.3 GAP-32 — Per-language интеграционные тест-сюиты `[REQ-V2-10]`

**Shared infrastructure (первым):**

- [ ] ⚡ 🔴 Добавить `LanguageIntegrationBase` mixin в `engine/tests/utils.py` с `LANGUAGE`, `XML_FIXTURE`, `RENDERER_CLASS`, `_run_pipeline(tmp_path) -> Path`

**C++ (GAP-32-A):**

- [ ] ⚡ 🔴 Создать `engine/tests/test_integration_cpp.py` (≥ 5 тестов):
  - Category landing pages: `Classes/index.html` существует и содержит таблицу
  - Overload dispatcher pages: сущность с `overloads` → dedicated page
  - Member-type index pages: `Fields, Structures and Enums/index.html` существует

**C# (GAP-32-B):**

- [ ] ⚡ 🔴 Создать `engine/tests/test_integration_cs.py` (≥ 5 тестов):
  - Interface entity: `entity_type == "interface"` → `interface` keyword в prototype
  - Delegate entity rendering
  - Event member rendering
  - Namespace index pages

**Java (GAP-32-C):**

- [ ] ⚡ 🔴 Создать `engine/tests/test_integration_java.py` (≥ 5 тестов):
  - `extends`/`implements`: `base_class` рендерится в prototype
  - Package-level index pages

**Python (GAP-32-D):**

- [ ] ⚡ 🔴 Создать `engine/tests/test_integration_py.py` (≥ 5 тестов):
  - `fget`/`fset` property: `[get]`/`[set]` accessors в member list
  - Dunder methods (`__init__`, `__repr__`, `__eq__`) — в method list, не отфильтрованы

**Финальная проверка:**
```bash
poetry run pytest tests/test_integration_cpp.py tests/test_integration_cs.py \
  tests/test_integration_java.py tests/test_integration_py.py -v --tb=short
# Ожидается: ≥ 20 новых тестов, все PASSED
poetry run pytest --cov=ude --cov-report=term-missing | grep TOTAL
# Ожидается: ≥ 98%
```

**Коммит:** `feat(tests): add per-language integration test suites cpp/cs/java/py (GAP-32)`

### 4.4 Per-language CI matrix

- [ ] **[AD-LANG-01]** 🟡 После реализации GAP-32: добавить job `integration-tests-per-language` в `integration_tests.yml` с `matrix: language: [cpp, cs, java, py]`
- [ ] **[AD-LANG-02]** 🟡 `continue-on-error: false` для матрицы языков
- [ ] **[AD-LANG-03]** 🟢 Артефакт с per-language test reports

---

## Раздел 5 — CI/CD и инфраструктура деплоя

> Параллельный трек с Фазами 1–3. Не блокирует разработку движка, но должен быть завершён до релиза v2.0.

### 5.1 Фаза 1 CI/CD: Безопасность и учётные данные

- [ ] **[CI-1.1]** 🔴 Установить и аутентифицировать Wrangler CLI: `npm install -g wrangler && wrangler login`
- [ ] **[CI-1.2]** 🔴 Создать 3 Cloudflare Pages проекта: `ude-design-docs`, `ude-user-docs`, `ude-api-ref`
- [ ] **[CI-1.3]** 🔴 Настроить Cloudflare Zero Trust Access для `ude-design-docs` — whitelist policy
- [ ] **[CI-1.4]** 🔴 Создать Cloudflare API Token с минимальными правами (Pages: Edit, Zone: Read)
- [ ] **[CI-1.5]** 🔴 Зарегистрировать GitHub Secrets во всех репозиториях: `CF_API_TOKEN`, `CF_ACCOUNT_ID`
- [ ] **[CI-1.6]** 🔴 Сгенерировать SSH Deploy Key для субмодуля engine; добавить в GitHub Secrets как `PIPELINE_DEPLOY_KEY`
- [ ] **[AD-SEC-04]** 🔴 Добавить блок `permissions:` с least-privilege во все workflows
- [ ] **[AD-SEC-05]** 🟡 Включить Dependabot для GitHub Actions: `.github/dependabot.yml`
- [ ] **[AD-SEC-06]** 🟡 Включить GitHub Secret Scanning и Push Protection для всех репозиториев

### 5.2 Фаза 2 CI/CD: Базовые GitHub Actions Workflows

- [ ] **[CI-2.1]** 🔴 Создать `ude-design-docs/.github/workflows/deploy-design-docs.yml` — Docusaurus → Cloudflare Pages
- [ ] **[CI-2.2]** 🔴 Создать `ude-user-docs/.github/workflows/deploy-user-docs.yml` — VitePress → Cloudflare Pages
- [ ] **[CI-2.3]** 🔴 Создать `engine/.github/workflows/generate-api-ref.yml` — UDE compile → Cloudflare Pages

### 5.3 Фаза 3 CI/CD: Кэширование и производительность

- [ ] **[CI-3.1]** 🟡 Кэширование npm (`actions/setup-node@v4` с `cache: 'npm'`) в Pipeline #1 и #2
- [ ] **[CI-3.2]** 🟡 Кэширование pip (`actions/cache@v4`) в Pipeline #3
- [ ] **[CI-3.3]** 🟢 Кэширование Docusaurus build cache (`.docusaurus`, `node_modules/.cache`) в Pipeline #1

### 5.4 Фаза 4 CI/CD: Quality Gates

- [ ] **[CI-4.1]** 🔴 Добавить pytest + coverage gate в `generate-api-ref.yml`: `--cov-fail-under=98`; upload артефакта retention 14 дней
- [ ] **[CI-4.2]** 🟡 Создать `scripts/pydantic_guard.sh`; добавить Pydantic Migration Guard step в CI — блокирует `dict`-паттерны вместо Pydantic-моделей
- [ ] **[AD-QA-01]** 🟡 Добавить job `engine-tests` в `integration_tests.yml`: `pytest engine/tests/ --cov=ude --cov-report=term-missing`; TOTAL ≥ 98%
- [ ] **[AD-QA-03]** 🟢 Добавить `markdownlint-cli2` step для `user-docs/docs/**/*.md`
- [ ] **[CI-4.5]** 🟡 Добавить step запуска integration tests: все 4 языка `test_integration_*.py`

### 5.5 Фаза 5 CI/CD: Изоляция сред и защита веток

- [ ] **[CI-5.1]** 🟡 Добавить Preview Deployments для Pull Requests (branch deploy, PR comment с preview URL)
- [ ] **[CI-5.2]** 🟡 Настроить Branch Protection Rules для ветки `main` во всех репозиториях
- [ ] **[CI-5.3]** 🟢 Создать GitHub Environment `production` с required reviewers

### 5.6 Фаза 6 CI/CD: Мониторинг и документация

- [ ] **[CI-6.1]** 🟢 Добавить build status badges в `README.md` всех репозиториев
- [ ] **[CI-6.2]** 🟢 Добавить `$GITHUB_STEP_SUMMARY` шаг в каждый workflow
- [ ] **[CI-6.3]** 🟢 Retention policy для артефактов — upload UDE output при failure, retention 3 дня
- [ ] **[CI-6.4]** 🟢 Создать `RUNBOOK.md` в корне umbrella: ручной запуск, rollback, ротация токенов, troubleshooting
- [ ] **[AD-MON-02]** 🟡 Добавить `timeout-minutes: 15` на уровне job
- [ ] **[AD-MON-04]** 🟢 Step вывода summary в `$GITHUB_STEP_SUMMARY`: страницы, время UDE, результат verify_pages

### 5.7 Новые workflows v2.0

- [ ] **[AD-V2-01]** 🟢 Создать `.github/workflows/coverage-gate.yml` — `workflow_dispatch` + `ude audit --mode reject-undocumented` → GitHub Check
- [ ] **[AD-V2-02]** 🟢 Создать `.github/workflows/regression.yml` — cron `0 3 * * 0` (еженедельно), `LoadTest/run_load_test.py`
- [ ] **[AD-V2-03]** 🟢 Создать `CODEOWNERS` в `.github/`: `engine/**` и `.antigravitycli/**` → @pavel.sokolov

---

## Раздел 6 — Пользовательская документация

> Выполняется параллельно с фазами реализации. Приоритетные задачи — до релиза v2.0.

### 6.1 Структурные исправления user-docs

- [ ] **[STRUCT-01]** 🔴 Создать субдиректории в `user-docs/docs/`: `quickstart/`, `standards/`, `reference/`, `deployment/`, `case-study/`
- [ ] **[STRUCT-02]** 🔴 Переместить `getting-started.md` и `first-config.md` → `docs/quickstart/`
- [ ] **[STRUCT-03]** 🔴 Создать `docs/quickstart/index.md` — оглавление главы 1
- [ ] **[STRUCT-04]** 🔴 Переместить `commenting-rules.md` и `exclusion-gates.md` → `docs/standards/`
- [ ] **[STRUCT-05]** 🔴 Создать `docs/standards/index.md` — оглавление главы 2
- [ ] **[STRUCT-06]** 🔴 Переместить `global-settings.md` и `target-settings.md` → `docs/reference/`
- [ ] **[STRUCT-07]** 🔴 Создать `docs/reference/index.md` — оглавление главы 3
- [ ] **[STRUCT-08]** 🔴 Создать `docs/deployment/` и переместить туда `admin-deployment.md`
- [ ] **[STRUCT-09]** 🔴 Выяснить статус `case-study.md` vs `chapter4-case-study.md` — удалить дубликат или объединить
- [ ] **[STRUCT-10]** 🔴 Обновить сайдбар VitePress (`docs/.vitepress/config.ts`) под новую иерархию
- [ ] **[STRUCT-11]** 🔴 Проверить и обновить все относительные ссылки после перемещения файлов

### 6.2 Исправление admin-deployment.md

- [ ] **[ADMIN-01]** 🔴 Убрать ссылку на несуществующий `deploy.yml` в umbrella
- [ ] **[ADMIN-02]** 🔴 Пояснить: деплой выполняется workflow каждого сабмодуля независимо
- [ ] **[ADMIN-03]** 🔴 Добавить актуальные шаги из `integration_tests.yml`
- [ ] **[ADMIN-04]** 🔴 Таблица secrets: `PIPELINE_GITHUB_TOKEN` — назначение, минимальные права
- [ ] **[ADMIN-05]** 🟡 Описать симлинк `user-docs/engine → ../engine` и почему он нужен только в CI

### 6.3 CI/CD документация в user-docs

- [ ] **[CICD-01]** 🔴 Создать `docs/deployment/cicd-pipelines.md` — обзор трёх пайплайнов
- [ ] **[CICD-05]** 🔴 Создать `docs/deployment/repository-dispatch.md` — механизм кросс-репо событий
- [ ] **[CICD-07]** 🟡 Mermaid-диаграмма: submodule push → repository_dispatch → umbrella CI → verify

### 6.4 Новые разделы v2.0

- [ ] **[MIG-01]** 🟡 Создать `docs/reference/migration-v2.md` — Breaking Changes v1.0 → v2.0
- [ ] **[MIG-02]** 🟡 Документировать: `ClassEntity` → 7 typed Pydantic models
- [ ] **[MIG-03]** 🟡 Документировать: `ProjectCatalog` — новые поля `project_name`, `version`
- [ ] **[MIG-04]** 🟡 Документировать: CLI subcommands (backward compat сохраняется)
- [ ] **[MIG-06]** 🟡 Документировать: `fields: List[str]` → `fields: List[VariableModel]`
- [ ] **[MIG-07]** 🟡 Чеклист для пользователей при переходе на v2.0
- [ ] **[CLOG-01]** 🟡 Создать `docs/changelog.md` — записи v1.0 и v2.0
- [ ] **[TRB-01]** 🟢 Создать `docs/quickstart/troubleshooting.md` — 7 типичных ошибок с решениями
- [ ] **[AUDIT-01]** 🟡 Задокументировать `GlobalConfig.coverage_mode` и `coverage_threshold`
- [ ] **[AUDIT-02]** 🟡 Задокументировать формат coverage-таблицы `ude audit`
- [ ] **[AUDIT-04]** 🟡 Пример интеграции `ude audit` в GitHub Actions step

### 6.5 Portfolio/Showcase улучшения

- [ ] **[PORT-01]** 🟢 Обновить лендинг `index.md`: ключевые метрики (`<5s`, `98%`, `4 языка`, `12 тестов`)
- [ ] **[PORT-02]** 🟢 Добавить badges: GitHub Actions status, Python version, coverage
- [ ] **[PORT-03]** 🟢 Mermaid-диаграмма архитектуры: Collector → Parser → Renderer

---

## Раздел 7 — Документация пайплайнов и CI/CD

### 7.1 Обязательные документы (🔴 Срочно)

- [ ] **[AD-DOC-01]** 🔴 Создать `docs/deployment/repository-dispatch.md` — механизм кросс-репо триггеров
- [ ] **[AD-DOC-02]** 🔴 Создать `docs/deployment/secrets.md` — `PIPELINE_GITHUB_TOKEN`: тип PAT, права, ротация 90 дней
- [ ] **[AD-DOC-03]** 🔴 Создать `docs/deployment/cicd-pipelines.md` — матрица 4 пайплайнов (design-docs, user-docs, engine, umbrella)
- [ ] **[AD-DOC-05]** 🔴 Задокументировать GitHub Checks: job `run-tests`, ожидаемое время ~3–5 мин, failure playbook
- [ ] **[AD-DOC-06]** 🔴 Задокументировать `Tests/verify_pages.py`: аргументы, что проверяет, как читать ошибки

### 7.2 Важные документы (🟡 v2.0)

- [ ] **[AD-DOC-04]** 🟡 Задокументировать симлинк `user-docs/engine`: почему только в CI, почему не нужен на Windows
- [ ] **[AD-DOC-07]** 🟡 Mermaid-диаграмма в `admin-deployment.md` — полный поток CI/CD
- [ ] **[AD-DOC-08]** 🟡 Создать `.github/AGENTS.md` — описание каждого workflow, expected checks, failure playbook

### 7.3 Аннотирование workflow кода

- [ ] **[AD-DOC-09]** 🟢 Добавить WHY-комментарии в `integration_tests.yml` — для нетривиальных steps
- [ ] **[AD-DOC-10]** 🟢 Задокументировать `PYTHONPATH: engine` — почему нужна, когда потребует обновления

---

## Раздел 8 — Требования к качеству документации

### 8.1 Markdown и синтаксические требования

- [ ] **[DR-NEW-01]** 🔴 Ввести требование: все MD-файлы проходят `markdownlint-cli2` в CI
- [ ] **[DR-NEW-02]** 🟡 Конфигурация markdownlint: max 120 символов, `MD013` только к prose
- [ ] **[DR-NEW-03]** 🟡 Правило: в design-docs все файлы начинаются с YAML front-matter (`sidebar_position`, `title`)
- [ ] **[DR-NEW-05]** 🟡 Правило: H1 ровно один, первый, совпадает с `title` в front-matter

### 8.2 Автоматическая проверка ссылок

- [ ] **[DR-NEW-07]** 🔴 `Tests/check_links.py` (GAP-31) должен быть реализован до релиза v2.0
- [ ] **[DR-NEW-08]** 🟡 После GAP-31: `check_links.py` запускается в `integration_tests.yml` как отдельный step
- [ ] **[DR-NEW-09]** 🟡 Проверка relative links в design-docs через `docusaurus-check-links` или аналог

### 8.3 Версионирование и архивирование

- [ ] **[DR-NEW-12]** 🟡 Перед слиянием v2.0: создать versioned snapshot в Docusaurus (`docusaurus docs:version 1.0`)
- [ ] **[DR-NEW-14]** 🟡 Документировать процедуру версионирования в `CLAUDE.md`
- [ ] **[DR-NEW-15]** 🟡 После freeze v2.0: `requirements_v2_next.md` → `requirements_v3_next.md`

### 8.4 Трассировка и согласованность

- [ ] **[DR-NEW-16]** 🟡 Каждый ⚠️-GAP в `integration_tests_specification.md` получает поле `Resolution Target`
- [ ] **[DR-NEW-17]** 🟡 Глоссарий терминов: `Collector`, `Orchestrator`, `Parser`, `Renderer`, `IR`, `Catalog` — единообразное использование
- [ ] **[DR-NEW-18]** 🟢 Создать Glossary-страницу в design-docs (15+ терминов)
- [ ] **[DR-NEW-19]** 🟡 При удалении требования — запись в `quality_audit.md` с обоснованием

---

## Раздел 9 — Финализация и релиз v2.0

### 9.1 Финальные проверки качества

- [ ] 🔴 Полный прогон тест-сюита: `poetry run pytest engine/tests/ -v` — 0 failed
- [ ] 🔴 Coverage gate: `poetry run pytest --cov=ude --cov-report=term-missing` — TOTAL ≥ 98%
- [ ] 🔴 Performance benchmark: `poetry run pytest tests/test_performance_benchmark.py` — ≤ 5s
- [ ] 🔴 v1.0 backward compat smoke test: `ude --doc-config path/to/ude_doc_config.json` работает идентично
- [ ] 🔴 IR compatibility: `load_compressed_ir(v1_file)` не бросает исключений
- [ ] 🔴 Git hygiene: `git status --short` — нет скомпилированных `*.html`, `*.md` output файлов
- [ ] 🟡 `ude parse | ude render` вывод byte-identical с `ude compile`

### 9.2 Регрессионные тесты

- [ ] 🔴 Запустить `Tests/run_all_integration_tests.sh` (GAP-31) — exit 0
- [ ] 🔴 Запустить golden master: `poetry run pytest tests/test_golden_master.py -v` — все PASSED
- [ ] 🔴 Запустить Docomatic alignment: `poetry run pytest tests/test_docomatic_alignment.py -v` — `"total_differences"` не выше pre-v2.0 baseline
- [ ] 🟡 Запустить per-language integration: все 4 файла `test_integration_*.py` — ≥ 20 тестов PASSED

### 9.3 CI/CD верификация

- [ ] 🔴 Проверить успешный прогон `integration_tests.yml` на master после всех изменений
- [ ] 🔴 Проверить pipeline #3 (`generate-api-ref.yml`) — coverage gate активен и проходит
- [ ] 🟡 Preview deployment в одном из PR — убедиться, что preview URL доступен

### 9.4 Документация релиза

- [ ] 🔴 Завершить `docs/changelog.md` с записями v2.0 (Breaking Changes + новые фичи)
- [ ] 🔴 Завершить `docs/reference/migration-v2.md` — полный чеклист для пользователей
- [ ] 🟡 Создать versioned snapshot в Docusaurus: `docusaurus docs:version 1.0`
- [ ] 🟡 Переименовать `requirements_v2_next.md` → `requirements_v3_next.md` в `.antigravitycli/`
- [ ] 🟢 Создать GitHub Release с release notes, дублирующими `changelog.md`

### 9.5 Постфинализация

- [ ] 🟢 Обновить `CLAUDE.md` — задокументировать `ude_`-конвенцию, результаты audit gap-анализа
- [ ] 🟢 Перенести разделы `future_v2.md` в `roadmap/mvp_v2/` (история намерений)
- [ ] 🟢 Разбить `v2_detailed_tasks.md` (2364 строки) на атомарные файлы в `tasks/` — максимум 500 строк/файл

---

## Сводная таблица зависимостей

```
Раздел 0 (Подготовка)
        │
        ▼
Фаза 1: GAP-09 ──► GAP-12 ──► GAP-07 ──► GAP-11
        │
        ▼
Фаза 2: GAP-05 ──► GAP-01
        │
        ├──► Фаза 3/D: GAP-03 ──► GAP-10
        │
        └──► Фаза 3/F: GAP-31 ‖ GAP-32

Параллельно:
  Раздел 5 (CI/CD) — не блокирует движок, требуется до релиза
  Раздел 6 (UserDocs) — не блокирует движок, требуется до релиза
  Раздел 7 (Pipeline Docs) — параллельно с реализацией
  Раздел 8 (DocReqs) — применяются с момента начала работ
```

---

## Итоговая сводка по разделам

| # | Раздел | Критичных 🔴 | Важных 🟡 | Желательных 🟢 | Блокирует |
|---|--------|-------------|----------|----------------|-----------|
| 0 | Подготовка репозитория | 3 | 3 | 4 | — |
| 1 | Фаза 1: Инфраструктура | 20 | 4 | — | Фазу 2 |
| 2 | Фаза 2: API & CLI | 14 | 6 | 2 | Фазу 3 |
| 3 | Фаза 3/D: Typed IR | 18 | 3 | — | Релиз |
| 4 | Фаза 3/F: QA | 12 | 5 | 2 | Релиз |
| 5 | CI/CD деплой | 11 | 16 | 10 | Релиз |
| 6 | User Docs | 16 | 15 | 6 | Релиз |
| 7 | Pipeline Docs | 5 | 5 | 2 | Релиз |
| 8 | Doc Requirements | 3 | 8 | 2 | Релиз |
| 9 | Финализация | 12 | 5 | 5 | — |
| **∑** | **Всего** | **114** | **70** | **33** | |

---

> **Статус:** Документ создан 2026-06-29. Все задачи ожидают исполнения.  
> **Следующий шаг:** Раздел 0 (подготовка, нулевой риск) → Фаза 1 (GAP-09).  
> **Ограничение Phase 3/D:** GAP-10 активируется после завершения GAP-03 и GAP-01.  
> **Ограничение CI/CD Фаза 4:** coverage gate через `ude audit` активируется после реализации GAP-10.
