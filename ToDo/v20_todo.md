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
> - `ToDo/Tests_ToDo.md` — план тестирования и обеспечения качества  
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

### 0.2 Подтверждение базового состояния v1.0 (TDD: Baseline)

- [ ] **[TST-0.1]** 🔴 **[Python]** Убедиться в прохождении всех 209 тестов движка: `poetry run pytest engine/tests/ -v`
- [ ] **[TST-0.2]** 🔴 **[Python]** Подтвердить покрытие ≥ 98%: `poetry run pytest --cov=ude --cov-report=term-missing` (или `grep TOTAL`)
- [ ] **[TST-0.3]** 🔴 **[Python]** Зафиксировать baseline-метрики (количество тестов, % coverage, время прогона) в `ToDo/Tests_ToDo.md`
- [ ] **[TST-0.4]** 🟡 **[Python]** Запустить performance-бенчмарк: `poetry run pytest tests/test_performance_benchmark.py -v` — убедиться в выполнении ≤ 5 с для 1000 классов
- [ ] **[TST-0.5]** 🟡 **[Python]** Сгенерировать HTML-отчет покрытия: `poetry run pytest --cov=ude --cov-report=html`
- [ ] **[TST-0.6]** 🟡 **[Python]** Выявить модули с покрытием < 98% и зафиксировать пробелы в файле `Tests_ToDo.md`
- [ ] **[TST-0.7]** 🟢 **[Python]** Создать тест `test_coverage_gate.py` с CI-ready параметром `--cov-fail-under=98`

### 0.3 Требования к документированию кода (применяются с этого момента)

- [ ] **[DR-NEW-04]** 🟡 Зафиксировать в `CLAUDE.md` правило именования файлов: kebab-case для `user-docs/`, snake_case для `.antigravitycli/`
- [ ] **[DR-NEW-21]** 🟡 Установить правило: каждый новый GitHub Actions workflow начинается с блока комментариев (назначение, триггеры, secrets, время выполнения)
- [ ] **[DR-NEW-20]** 🟡 Ввести правило: каждый новый `TASK-*.md` содержит поле `Related Docs` — файлы user-docs/design-docs, требующие обновления

### 0.4 Рефакторинг и аудит существующей тест-базы (TDD: Refactor)

- [ ] **[TST-0.8]** 🔴 **[Python]** В `engine/tests/test_orchestrator.py`: заменить все вхождения `"ude_global.json"` → `"ude_global_config.json"`, `"ude_config.json"` → `"ude_doc_config.json"`
- [ ] **[TST-0.9]** 🔴 **[Python]** В `engine/tests/test_integration_pipeline.py`: аналогичная замена
- [ ] **[TST-0.10]** 🔴 **[Python]** В `engine/tests/test_doxygen_collector.py`: аналогичная замена
- [ ] **[TST-0.11]** 🟡 **[Python]** Обновить docstring-комментарии в `engine/ude/interfaces.py` и `engine/ude/collectors/doxygen.py`
- [ ] **[TST-0.12]** 🟡 **[Python]** Запустить `poetry run pytest engine/tests/ -v` после замен — убедиться в 0 failed
- [ ] **[TST-0.13]** 🔴 **[Python]** В `engine/tests/` найти все `caplog`-ассерты с `"ude.renderers"` из `interfaces.py`
- [ ] **[TST-0.14]** 🔴 **[Python]** Обновить найденные ассерты: `"ude.renderers"` → `"ude.interfaces"` (исправление логгера HC-05)
- [ ] **[TST-0.15]** 🔴 **[Python]** Убедиться в прохождении тестов после исправления
- [ ] **[TST-0.16]** 🟡 **[Python]** В `engine/tests/utils.py`: добавить `LanguageIntegrationBase` mixin с `LANGUAGE`, `XML_FIXTURE`, `RENDERER_CLASS` и `_run_pipeline()`
- [ ] **[TST-0.17]** 🟡 **[Python]** Добавить вспомогательную функцию `_write_test_config(tmp_path, **kwargs) -> Path` для временных конфигураций
- [ ] **[TST-0.18]** 🟢 **[Python]** Добавить фабрику `_make_mock_catalog` для создания синтетического `ProjectCatalog`

---

## Раздел 1 — Фаза 1: Инфраструктура движка

> **Стратегический порядок:** GAP-09 → GAP-12 → GAP-07 → GAP-11  
> Каждый GAP разблокирует следующий. Всё разделение полностью последовательно.

### 1.1 GAP-09 — Активация полей GlobalConfig `[REQ-V2-01]`

> **Цель:** Сделать все поля `ude_global_config.json` оперативно активными через Pydantic-модель.

**Тесты (RED — написать первыми):**

- [ ] **[TST-1.1]** 🔴 **[Python]** Написать тест `test_global_config_defaults` — пустой JSON дает все дефолты
- [ ] **[TST-1.2]** 🔴 **[Python]** Написать тест `test_global_config_full_round_trip` — все поля round-trip через `from_file()`
- [ ] **[TST-1.3]** 🔴 **[Python]** Написать тест `test_global_config_unknown_keys_ignored` — extra keys не вызывают ValidationError
- [ ] **[TST-1.4]** 🔴 **[Python]** Написать тест `test_global_config_missing_file_raises` — FileNotFoundError при отсутствии файла
- [ ] **[TST-1.5]** 🔴 **[Python]** Написать тест `test_global_config_bad_json_raises` — ValueError при некорректном JSON
- [ ] **[TST-1.6]** 🔴 **[Python]** Написать тест `test_global_config_coverage_threshold_parses` — threshold 0.85 принимается без ошибок
- [ ] **[TST-1.7]** 🔴 **[Python]** Написать тест `test_global_config_coverage_threshold_bounds` — threshold 1.5 → ValidationError
- [ ] **[TST-1.8]** 🔴 **[Python]** Написать тест `test_apply_global_cfg_env_injects_path` — doxygen_path добавляется в PATH
- [ ] **[TST-1.9]** 🔴 **[Python]** Написать тест `test_apply_global_cfg_env_idempotent` — двойной вызов не дублирует путь в PATH
- [ ] **[TST-1.10]** 🔴 **[Python]** Написать тест `test_apply_global_cfg_env_noop_when_none` — doxygen_path=None не изменяет PATH
- [ ] **[TST-1.11]** 🟡 **[Python]** Написать тест `test_orchestrator_stores_global_cfg_instance` — orchestrator._global_cfg содержит экземпляр GlobalConfig
- [ ] **[TST-1.12]** 🟡 **[Python]** Написать тест `test_orchestrator_sets_path_from_doxygen_path` — mock subprocess.run; doxygen_path инжектируется до запуска doxygen
- [ ] **[TST-1.13]** 🟡 **[Python]** Написать тест `test_orchestrator_cache_root_resolved_absolute` — cache_root_dir резолвится в абсолютный путь

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

- [ ] **[TST-1.14]** 🔴 **[Python]** Написать тест `test_logging_setup_stderr_only` — log_file=None → ровно 1 StreamHandler
- [ ] **[TST-1.15]** 🔴 **[Python]** Написать тест `test_logging_setup_with_log_file` — log_file → 2 хэндлера, файл создан на диске
- [ ] **[TST-1.16]** 🔴 **[Python]** Написать тест `test_logging_setup_level_debug` — log_level="DEBUG" → logger.level == DEBUG
- [ ] **[TST-1.17]** 🔴 **[Python]** Написать тест `test_logging_setup_invalid_level` — VERBOSE (неверный) уровень падает к WARNING без краша
- [ ] **[TST-1.18]** 🔴 **[Python]** Написать тест `test_logging_setup_idempotent` — двойной вызов не накопливает StreamHandler-ы

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

- [ ] **[TST-1.19]** 🔴 **[Python]** Написать тест `test_compute_template_hash_stable` — хэш стабилен при повторных вызовах
- [ ] **[TST-1.20]** 🔴 **[Python]** Написать тест `test_compute_template_hash_changes_on_content_change` — изменение шаблона меняет хэш
- [ ] **[TST-1.21]** 🔴 **[Python]** Написать тест `test_compute_template_hash_empty_dir` — пустая директория → ""
- [ ] **[TST-1.22]** 🔴 **[Python]** Написать тест `test_compute_template_hash_missing_dir` — несуществующая директория → ""
- [ ] **[TST-1.23]** 🔴 **[Python]** Написать тест `test_l2_html_cache_hit_skips_write` — повторный рендер не перезаписывает файл (spy на open)
- [ ] **[TST-1.24]** 🔴 **[Python]** Написать тест `test_l2_html_cache_miss_on_catalog_change` — мутация метода в каталоге сбрасывает кэш
- [ ] **[TST-1.25]** 🔴 **[Python]** Написать тест `test_l2_html_cache_miss_on_template_change` — изменение Jinja2-шаблона сбрасывает кэш
- [ ] **[TST-1.26]** 🔴 **[Python]** Написать тест `test_l2_html_cache_disabled_when_no_manager` — cache_manager=None → файлы пишутся всегда (v1.0)
- [ ] **[TST-1.27]** 🔴 **[Python]** Написать тест `test_l2_hugo_cache_hit_skips_write` — аналог L2 кэш для Hugo рендерера
- [ ] **[TST-1.28]** 🔴 **[Python]** Написать тест `test_l2_legacy_cache_hit_skips_write` — аналог L2 кэш для Legacy рендерера
- [ ] **[TST-1.29]** 🟡 **[Python]** Написать тест `test_sequential_build_l2_cache_hits` — интеграционный: при втором orchestrator.run() записи отсутствуют
- [ ] **[TST-1.30]** 🔴 **[Python]** Выполнить grep-аудит (CB-04): убедиться, что `cache_manager` объявлен в `__new__` и прокидывается в `super().__init__()` рендереров
- [ ] **[TST-1.31]** 🔴 **[Python]** Написать тест `test_cache_manager_forwarded_through_new_hugo` — HugoMarkdownRenderer сохраняет `_cache_mgr`
- [ ] **[TST-1.32]** 🔴 **[Python]** Написать тест `test_cache_manager_forwarded_through_new_legacy` — LegacyRenderer сохраняет `_cache_mgr`

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

- [ ] **[TST-1.33]** 🔴 **[Python]** Написать тест `test_parse_basic` — парсинг простых пар Ключ = Значение в Doxyfile
- [ ] **[TST-1.34]** 🔴 **[Python]** Написать тест `test_parse_skip_comments_and_blanks` — комментарии `#` и пустые строки игнорируются
- [ ] **[TST-1.35]** 🔴 **[Python]** Написать тест `test_parse_continuation_lines` — переносы строк через backslash `\` сворачиваются в одну строку
- [ ] **[TST-1.36]** 🔴 **[Python]** Написать тест `test_parse_value_with_equals` — значения с символом `=` (например, PREDEFINED) парсятся верно
- [ ] **[TST-1.37]** 🔴 **[Python]** Написать тест `test_serialize_round_trip` — parse -> serialize -> parse сохраняет ключи в алфавитном порядке
- [ ] **[TST-1.38]** 🔴 **[Python]** Написать тест `test_merge_t2_overrides_t1` — переопределение T1 ключей значениями из T2
- [ ] **[TST-1.39]** 🔴 **[Python]** Написать тест `test_merge_t3_overrides_t2` — переопределение T2 ключей значениями из T3
- [ ] **[TST-1.40]** 🔴 **[Python]** Написать тест `test_merge_debug_log_on_conflict` — конфликт T2 vs T1 логирует DEBUG-сообщение
- [ ] **[TST-1.41]** 🔴 **[Python]** Написать тест `test_merge_missing_tiers` — корректная деградация мёрджа при отсутствии T1/T2
- [ ] **[TST-1.42]** 🟡 **[Python]** Написать тест `test_collector_uses_merged_doxyfile` — mock subprocess.run; результирующий Doxyfile содержит T3 ключи по одному разу
- [ ] **[TST-1.43]** 🟡 **[Python]** Написать тест `test_collector_t3_overrides_t2_key` — target-Doxyfile задает GENERATE_HTML=YES, мёрдж перебивает в NO

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

- [ ] **[TST-2.1]** 🔴 **[Python]** Написать тест `test_orchestrator_parse_returns_catalog` — `orchestrator.parse()` возвращает ProjectCatalog
- [ ] **[TST-2.2]** 🔴 **[Python]** Написать тест `test_orchestrator_parse_skips_collector_when_xml_exists` — повторный запуск не вызывает DoxygenXmlCollector.collect
- [ ] **[TST-2.3]** 🔴 **[Python]** Написать тест `test_orchestrator_render_produces_files` — `orchestrator.render()` создает файлы HTML/Markdown в out_dir
- [ ] **[TST-2.4]** 🔴 **[Python]** Написать тест `test_orchestrator_render_respects_format_config` — выбор формата рендерера (static_html / hugo_markdown)
- [ ] **[TST-2.5]** 🔴 **[Python]** Написать тест `test_orchestrator_run_end_to_end` — `orchestrator.run()` возвращает True при успехе, генерирует файлы
- [ ] **[TST-2.6]** 🔴 **[Python]** Написать тест `test_run_target_is_alias` — run_target() вызывает run() для обратной совместимости
- [ ] **[TST-2.7]** 🔴 **[Python]** Написать тест `test_orchestrator_run_returns_false_on_missing_config` — отсутствующий конфиг возвращает False
- [ ] **[TST-2.8]** 🟡 **[Python]** Написать тест `test_resolve_config_returns_merged_dict` — корректные приоритеты при слиянии global/sdk/doc configs
- [ ] **[TST-2.9]** 🟡 **[Python]** Написать тест `test_resolve_config_graceful_sidebar_missing` — отсутствие `sidebar.toml` не падает с ошибкой
- [ ] **[TST-2.10]** 🟡 **[Python]** Написать тест `test_resolve_config_sidebar_static_paths_absolute` — статические пути из sidebar.toml преобразуются в абсолютные
- [ ] **[TST-2.11]** 🟡 **[Python]** Написать тест `test_deep_merge_importable_from_both_modules` — импорт `deep_merge` работает и из `cli.py`, и из `orchestrator.py`

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

- [ ] **[TST-3.1]** 🔴 **[Python]** Написать тест `test_project_catalog_has_project_name_and_version` — имя и версия проекта round-trip через JSON
- [ ] **[TST-3.2]** 🔴 **[Python]** Написать тест `test_class_model_fields_are_variable_models` — поля класса содержат экземпляры VariableModel, не строки
- [ ] **[TST-3.3]** 🔴 **[Python]** Написать тест `test_old_ir_json_deserializes_without_error` — десериализация v1.0 IR без новых полей проходит успешно
- [ ] **[TST-3.4]** 🔴 **[Python]** Написать тест `test_variable_model_nonempty_round_trip` — непустые поля VariableModel корректно кодируются/декодируются
- [ ] **[TST-3.5]** 🔴 **[Python]** Написать тест `test_class_model_extra_field_ignored` — extra-поля при валидации ClassModel отсекаются
- [ ] **[TST-3.6]** 🔴 **[Python]** Написать тест `test_project_catalog_extra_field_ignored` — extra-поля при валидации ProjectCatalog отсекаются
- [ ] **[TST-3.7]** 🔴 **[Python]** Написать тест `test_backward_compat_alias` — алиас `ClassEntity is ClassModel` возвращает True
- [ ] **[TST-3.8]** 🔴 **[Python]** Написать тест `test_7_model_round_trip` — round-trip каталога, содержащего все 7 новых моделей
- [ ] **[TST-3.9]** 🟡 **[Python]** Написать тест `test_method_model_overloads` — `MethodModel.overloads` содержит список `OverloadModel`
- [ ] **[TST-3.10]** 🟡 **[Python]** Написать тест `test_enum_model_values` — `EnumModel.values` содержит список значений `List[str]`
- [ ] **[TST-3.11]** 🟡 **[Python]** Написать тест `test_constant_model_has_value` — `ConstantModel.value` сериализуется как `null` при значении `None`
- [ ] **[TST-3.12]** 🟡 **[Python]** Написать тест `test_type_alias_model_round_trip` — корректность сериализации/десериализации `TypeAliasModel`

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

**Рефакторинг существующих тестов под v2.0 модели:**

- [ ] **[TST-3.13]** 🔴 **[Python]** В `test_doxygen_parser.py`: обновить ассерты для `entity.fields` (доступ по `.name`, а не по индексам строк)
- [ ] **[TST-3.14]** 🔴 **[Python]** В `test_doxygen_parser.py`: добавить тест `test_parser_populates_enum_model` (Kind="enum" в XML парсится в `EnumModel`)
- [ ] **[TST-3.15]** 🔴 **[Python]** В `test_doxygen_parser.py`: добавить тест `test_parser_populates_constant_model` (Kind="variable" static=yes -> `ConstantModel`)
- [ ] **[TST-3.16]** 🔴 **[Python]** В `test_html_renderer.py`: обновить тестовые фикстуры под ClassModel с VariableModel
- [ ] **[TST-3.17]** 🔴 **[Python]** В `test_hugo_renderer.py`: обновить тестовые фикстуры аналогично
- [ ] **[TST-3.18]** 🔴 **[Python]** В `test_legacy_renderer.py`: обновить тестовые фикстуры аналогично
- [ ] **[TST-3.19]** 🔴 **[Python]** Выполнить проверку (Guard Step 4) на отсутствие `.fields` прямого обращения в рендерерах через grep
- [ ] **[TST-3.20]** 🔴 **[Python]** Запустить `test_doxygen_parser.py` и все интеграционные тесты для верификации правок

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

- [ ] **[TST-3.21]** 🔴 **[Python]** Написать тест `test_full_coverage_catalog` — 100% задокументированных сущностей дает coverage == 1.0
- [ ] **[TST-3.22]** 🔴 **[Python]** Написать тест `test_zero_coverage_catalog` — 0% задокументированных сущностей (docstrings = None) → coverage == 0.0
- [ ] **[TST-3.23]** 🔴 **[Python]** Написать тест `test_mixed_coverage` — частичное документирование (например, 3 из 4 методов → coverage == 0.75)
- [ ] **[TST-3.24]** 🔴 **[Python]** Написать тест `test_reject_mode_exits_nonzero` — `ude audit` в режиме `reject-undocumented` завершается с кодом 2 при покрытии ниже threshold
- [ ] **[TST-3.25]** 🔴 **[Python]** Написать тест `test_allow_mode_exits_zero` — `ude audit` в режиме `allow-undocumented` завершается с кодом 0 даже при 0% покрытии
- [ ] **[TST-3.26]** 🔴 **[Python]** Написать тест `test_audit_output_contains_table` — вывод аудита содержит форматированную markdown-таблицу покрытия
- [ ] **[TST-3.27]** 🟡 **[Python]** Написать тест `test_coverage_gate_runs_on_compile` — coverage gate запускается внутри `ude compile`
- [ ] **[TST-3.28]** 🟡 **[Python]** Написать тест `test_coverage_gate_absent_on_parse` — `ude parse` не выполняет аудит покрытия
- [ ] **[TST-3.29]** 🟡 **[Python]** Написать тест `test_coverage_gate_absent_on_render` — `ude render` не выполняет аудит покрытия
- [ ] **[TST-3.30]** 🟡 **[Python]** Выполнить проверку наличия трассировочных docstring-аннотаций `Implements TASK-D` / `Implements GAP-` во всех новых модулях Phase 3 через grep
- [ ] **[TST-3.31]** 🟡 **[Python]** Выполнить ту же проверку на Windows PowerShell (проверка AW-08)
- [ ] **[TST-3.32]** 🟡 **[Python]** Написать тест `test_phase3_modules_have_traceability_docstrings` — программный анализ AST модулей на наличие Implements-аннотаций

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

### 4.1 GAP-31 — Подтверждение внешних интеграционных скриптов [REQ-V2-09]

**Тесты и проверки существующих скриптов:**

- [ ] **[TST-6.1]** 🔴 **[Python]** Запустить существующий `python Tests/run_regression_tests.py` и проверить прохождение всех тестов L1/L2/L3 для всех 12 проектов
- [ ] **[TST-6.2]** 🔴 **[Python]** Написать тест `test_run_regression_all_tiers_pass` — smoke-тест запуска `run_regression_tests.py` через `subprocess` (exit code 0)
- [ ] **[TST-6.3]** 🟡 **[Python]** Убедиться, что `Tests/baseline/xml/` содержит эталонные Doxygen XML-файлы для `facetmodeler`
- [ ] **[TST-6.4]** 🟡 **[Python]** Написать тест `test_prepare_baseline_mock_suite` — запуск `prepare_baseline.py --suite mock` создает файлы в `baseline/ir/` и `baseline/html/`
- [ ] **[TST-6.5]** 🔴 **[Python]** Написать тест `test_verify_pages_local_all_pages_found` — все MD-файлы из `user-docs/docs/` найдены в скомпилированном dist → exit 0
- [ ] **[TST-6.6]** 🔴 **[Python]** Написать тест `test_verify_pages_detects_missing_compiled_page` — один MD-файл не скомпилирован → exit 1 с выводом ошибки в stderr
- [ ] **[TST-6.7]** 🟡 **[Python]** Написать тест `test_verify_pages_remote_mode` — удаленный режим работы `verify_pages.py` с mock HTTP (exit 0 на 200, exit 1 на 404)
- [ ] **[TST-6.8]** 🟢 **[Python]** Уточнить необходимость разработки отдельного скрипта `verify_ude_links.py` для проверки внутренних ссылок UDE HTML (расхождение с REQ-V2-09)
- [ ] **[TST-6.9]** 🔴 **[Python]** Написать тест `test_check_links_clean_site` — проверка скомпилированной директории без сломанных ссылок → exit 0
- [ ] **[TST-6.10]** 🔴 **[Python]** Написать тест `test_check_links_detects_broken_internal_link` — битая внутренняя ссылка → exit 1 с именем файла
- [ ] **[TST-6.11]** 🟡 **[Python]** Написать тест `test_check_links_detects_broken_external_link` — битая внешняя ссылка (mock requests 404) → exit 1
- [ ] **[TST-6.12]** 🟡 **[Python]** Написать тест `test_check_links_ude_prefix_strip` — корректность резолвинга ссылок с префиксом `/ude-user-docs/api/`

**Разработка скрипта-агрегатора (с защитой AW-05):**

- [ ] **[TST-6.13]** 🔴 **[VB]** Создать `Tests/run_all_integration_tests.bat` (агрегатор для Windows) на базе безопасного batch-кода с проверкой %ERRORLEVEL%
- [ ] **[TST-6.14]** 🔴 **[VB]** Использовать `pushd`/`popd` для изоляции перехода по каталогам, предотвращая мутацию CWD при ошибках
- [ ] **[TST-6.15]** 🔴 **[VB]** Принимать путь к выходной директории в качестве аргумента `%1` с валидацией его существования (без хардкода)
- [ ] **[TST-6.16]** 🔴 **[VB]** Валидировать наличие всех 3 дочерних скриптов до запуска, прерывать выполнение при их отсутствии
- [ ] **[TST-6.17]** 🟡 **[Python]** Создать shell-агрегатор `Tests/run_all_integration_tests.sh` для CI (Linux) с использованием `trap` для CWD и `$1` для путей

### 4.2 GAP-31 — Интеграция скриптов в CI

- [ ] **[AD-QA-04]** 🟡 Добавить step в `integration_tests.yml`: `Tests/check_links.py --site-dir ./user-docs/.vitepress/dist`
- [ ] **[AD-V2-04]** 🟡 Добавить step `python Tests/run_regression_tests.py` in `integration_tests.yml` как отдельный stage после page verification
- [ ] **[AD-QA-05]** 🟢 Добавить `actions/upload-artifact@v4` для pytest coverage HTML report и `verify_pages.py` output — retention 7 дней

### 4.3 GAP-32 — Per-language интеграционные тест-сюиты [REQ-V2-10]

**Разработка базовой инфраструктуры:**

- [ ] **[TST-5.1]** 🔴 **[Python]** Добавить `LanguageIntegrationBase` mixin в `engine/tests/utils.py` с `LANGUAGE`, `XML_FIXTURE`, `RENDERER_CLASS` и `_run_pipeline()`

**C++ специфика (GAP-32-A):**

- [ ] **[TST-5.2]** 🔴 **[Python]** Написать тест `test_cpp_category_landing_pages_exist` — существование `Classes/index.html` с таблицей классов
- [ ] **[TST-5.3]** 🔴 **[Python]** Написать тест `test_cpp_overload_dispatcher_page` — создание dispatcher-страницы для перегрузок (строгий assert AW-04, без flat any)
- [ ] **[TST-5.4]** 🔴 **[Python]** Написать тест `test_cpp_member_type_index_page` — существование `Fields, Structures and Enums/index.html`
- [ ] **[TST-5.5]** 🔴 **[Python]** Написать тест `test_cpp_template_class_rendering` — экранирование угловых скобок у шаблонов вида `MyClass<T, U>` в HTML
- [ ] **[TST-5.6]** 🔴 **[Python]** Написать тест `test_cpp_namespace_separator_double_colon` — использование разделителя `::` в breadcrumbs и prototype
- [ ] **[TST-5.7]** 🟡 **[C++]** Создать XML-fixture `engine/tests/assets/cpp_templates.xml` с шаблонами, деструктором и перегруженными конструкторами
- [ ] **[TST-5.8]** 🟡 **[Python]** Написать тест `test_cpp_destructor_rendering` — рендеринг деструктора `~MyClass()` в выводе
- [ ] **[TST-5.9]** 🟡 **[Python]** Написать тест `test_cpp_global_functions_flat_rendered` — глобальные функции рендерятся у корня сайдбара

**C# специфика (GAP-32-B):**

- [ ] **[TST-5.10]** 🔴 **[Python]** Написать тест `test_cs_interface_entity_rendering` — ключевое слово `interface` отображается в prototype
- [ ] **[TST-5.11]** 🔴 **[Python]** Написать тест `test_cs_delegate_entity_rendering` — создание страниц для делегатов
- [ ] **[TST-5.12]** 🔴 **[Python]** Написать тест `test_cs_event_member_rendering` — рендеринг событий (`event`) в секции memberlist
- [ ] **[TST-5.13]** 🔴 **[Python]** Написать тест `test_cs_namespace_index_page` — создание `<Namespace>/index.html` с таблицей классов
- [ ] **[TST-5.14]** 🔴 **[Python]** Написать тест `test_cs_dot_separator_in_fqn` — использование `.` вместо `::` для C#
- [ ] **[TST-5.15]** 🟡 **[C#]** Создать XML-fixture `engine/tests/assets/cs_interface.xml` с интерфейсами и событиями
- [ ] **[TST-5.16]** 🟡 **[Python]** Написать тест `test_cs_property_getter_setter_rendering` — отображение get/set аксессоров свойств
- [ ] **[TST-5.17]** 🟡 **[Python]** Написать тест `test_cs_indexer_rendering` — индексаторы `this[int index]` отображаются в секции members

**Java специфика (GAP-32-C):**

- [ ] **[TST-5.18]** 🔴 **[Python]** Написать тест `test_java_extends_implements_in_prototype` — базовые классы/интерфейсы отображаются в prototype
- [ ] **[TST-5.19]** 🔴 **[Python]** Написать тест `test_java_package_index_page` — создание `index.html` пакета с таблицей классов
- [ ] **[TST-5.20]** 🔴 **[Python]** Написать тест `test_java_interface_rendering` — корректный рендеринг Java interface
- [ ] **[TST-5.21]** 🔴 **[Python]** Написать тест `test_java_annotation_type_rendering` — рендеринг аннотаций (`@interface`) в Java
- [ ] **[TST-5.22]** 🔴 **[Python]** Написать тест `test_java_dot_separator_in_fqn` — использование `.` для Java-путей
- [ ] **[TST-5.23]** 🟡 **[Java]** Создать XML-fixture `engine/tests/assets/java_inheritance.xml` со связями наследования и имплементации
- [ ] **[TST-5.24]** 🟡 **[Python]** Написать тест `test_java_enum_rendering` — рендеринг констант Java enum через EnumModel
- [ ] **[TST-5.25]** 🟢 **[Python]** Написать тест `test_java_nested_class_rendering` — вложенные классы (`OuterClass.InnerClass`) в sidebar

**Python специфика (GAP-32-D):**

- [ ] **[TST-5.26]** 🔴 **[Python]** Написать тест `test_py_fget_fset_property_rendering` — отображение аксессоров `[get]`/`[set]` для свойств Python
- [ ] **[TST-5.27]** 🔴 **[Python]** Написать тест `test_py_dunder_methods_present` — методы `__init__`, `__repr__`, `__eq__` не отфильтрованы как приватные
- [ ] **[TST-5.28]** 🔴 **[Python]** Написать тест `test_py_swig_wrapper_fields_excluded` — SWIG-поля (`swigCPtr`, `Dispose()`) отфильтрованы
- [ ] **[TST-5.29]** 🔴 **[Python]** Написать тест `test_py_sphinx_rst_docstring_normalized` — Sphinx/RST-параметры (`:param`, `:type`) конвертируются в CommonMark
- [ ] **[TST-5.30]** 🔴 **[Python]** Написать тест `test_py_dot_separator_in_fqn` — использование `.` для Python-путей
- [ ] **[TST-5.31]** 🟡 **[Python]** Создать XML-fixture `engine/tests/assets/py_swig.xml` с SWIG-врапперами и свойствами
- [ ] **[TST-5.32]** 🟡 **[Python]** Написать тест `test_py_class_variable_vs_instance_variable` — разделение классовых и инстанс-переменных в выводе
- [ ] **[TST-5.33]** 🟢 **[Python]** Написать тест `test_py_module_level_functions` — рендеринг функций уровня модуля

### 4.4 Per-language CI matrix

- [ ] **[AD-LANG-01]** 🟡 После реализации GAP-32: добавить job `integration-tests-per-language` in `integration_tests.yml` с `matrix: language: [cpp, cs, java, py]`
- [ ] **[AD-LANG-02]** 🟡 `continue-on-error: false` для матрицы языков
- [ ] **[AD-LANG-03]** 🟢 Артефакт с per-language test reports

### 4.5 Тесты полноты охвата сущностей (Entity Completeness) и структуры страниц

**Проверка соответствия Doc-o-matic (Alignment):**

- [ ] **[TST-4.1]** 🔴 **[Python]** Перезапустить `test_docomatic_alignment.py` и зафиксировать `total_differences` для каждого языка как новый baseline
- [ ] **[TST-4.2]** 🔴 **[Python]** Написать тест `test_total_differences_not_increased_cpp` — расхождения для C++ не превышают baseline после правок рендерера
- [ ] **[TST-4.3]** 🔴 **[Python]** Написать тест `test_total_differences_not_increased_cs` — расхождения для C# не превышают baseline
- [ ] **[TST-4.4]** 🔴 **[Python]** Написать тест `test_total_differences_not_increased_java` — расхождения для Java не превышают baseline
- [ ] **[TST-4.5]** 🟡 **[Python]** Написать тест `test_no_silent_entity_loss_cpp` — количество классов в UDE >= количеству в Docomatic-baseline для C++
- [ ] **[TST-4.6]** 🟡 **[Python]** Написать тест `test_no_silent_entity_loss_cs` — аналогичная проверка для C#
- [ ] **[TST-4.7]** 🟡 **[Python]** Написать тест `test_no_silent_entity_loss_java` — аналогичная проверка для Java

**Количественная верификация полноты сущностей:**

- [ ] **[TST-4.8]** 🔴 **[Python]** Написать тест `test_all_methods_present_after_aggregation_cpp` — число методов в IR = числу методов на HTML-страницах классов (lxml парсинг `<h3>`, `<section>`)
- [ ] **[TST-4.9]** 🔴 **[Python]** Написать тест `test_all_methods_present_after_aggregation_cs` — аналогичная проверка для C#
- [ ] **[TST-4.10]** 🔴 **[Python]** Написать тест `test_all_methods_present_after_aggregation_java` — аналогичная проверка для Java
- [ ] **[TST-4.11]** 🔴 **[Python]** Написать тест `test_no_orphan_entities_cpp` — для каждого метода в IR существует якорная ссылка `<a id="...">` в HTML-файле
- [ ] **[TST-4.12]** 🔴 **[Python]** Написать тест `test_no_orphan_entities_cs` — аналогичная проверка для C#
- [ ] **[TST-4.13]** 🔴 **[Python]** Написать тест `test_no_orphan_entities_java` — аналогичная проверка для Java
- [ ] **[TST-4.14]** 🟡 **[Python]** Написать тест `test_class_member_count_matches_toc_cpp` — количество членов класса в sidebar ToC совпадает с числом в IR
- [ ] **[TST-4.15]** 🟡 **[Python]** Написать тест `test_class_member_count_matches_toc_cs` — аналогичная проверка для C#
- [ ] **[TST-4.16]** 🟡 **[Python]** Написать тест `test_class_member_count_matches_toc_java` — аналогичная проверка для Java
- [ ] **[TST-4.17]** 🟡 **[Python]** Написать тест `test_overloaded_methods_all_present` — все перегрузки представлены на overload dispatcher странице или inline
- [ ] **[TST-4.18]** 🟡 **[Python]** Написать тест `test_inherited_members_not_silently_dropped` — унаследованные члены класса не теряются в выводе UDE
- [ ] **[TST-4.19]** 🟢 **[Python]** Написать тест `test_static_vs_instance_segregation` — корректность разделения статических и инстанс-членов

**Структурная целостность страниц:**

- [ ] **[TST-4.20]** 🔴 **[Python]** Написать тест `test_class_page_has_method_section` — каждый класс с методами содержит HTML-секцию методов
- [ ] **[TST-4.21]** 🔴 **[Python]** Написать тест `test_class_page_has_fields_section_when_fields_exist` — наличие секции Fields при наличии полей в IR
- [ ] **[TST-4.22]** 🔴 **[Python]** Написать тест `test_namespace_index_lists_all_classes` — индекс namespace содержит ссылки на все его классы
- [ ] **[TST-4.23]** 🟡 **[Python]** Написать тест `test_sidebar_links_resolve_to_existing_files` — ссылки в sidebar ведут на реальные сгенерированные файлы
- [ ] **[TST-4.24]** 🟡 **[Python]** Написать тест `test_breadcrumbs_contain_correct_namespace` — хлебные крошки отображают верный путь пространства имен
- [ ] **[TST-4.25]** 🟡 **[Python]** Написать тест `test_entity_titles_follow_convention` — заголовки следуют формату `<EntityID> <EntityType>`

### 4.6 Производительность, нагрузка и регрессионные тесты

**Бенчмаркинг производительности:**

- [ ] **[TST-7.1]** 🟡 **[Python]** Убедиться, что benchmark тестирует 1000 классов за время ≤ 5 с
- [ ] **[TST-7.2]** 🟡 **[Python]** Добавить нагрузочный тест с разделением по языкам (250 классов * 4 языка = 1000)
- [ ] **[TST-7.3]** 🟡 **[Python]** Написать тест `test_benchmark_with_l2_cache_second_run` — второй запуск с L2 кэшем > 3x быстрее первого
- [ ] **[TST-7.4]** 🟢 **[Python]** Написать тест `test_benchmark_large_class_many_methods` — корректная обработка класса с 200+ методами без truncation

**Регрессионный тест Golden Master:**

- [ ] **[TST-7.5]** 🔴 **[Python]** После GAP-03 обновить baselines для Golden Master (учесть обе формы для Linux и Windows PowerShell - AW-02)
- [ ] **[TST-7.6]** 🔴 **[Python]** Проверить успешное выполнение `test_golden_master.py` после регенерации
- [ ] **[TST-7.7]** 🔴 **[Python]** Убедиться, что golden master покрывает все 16 конфигураций (4 языка * 2 вывода * 2 варианта)
- [ ] **[TST-7.8]** 🟡 **[Python]** Добавить тест `test_golden_master_html_legacy_cpp` (LegacyHtmlRenderer C++ vs baseline)
- [ ] **[TST-7.9]** 🟡 **[Python]** Добавить тест `test_golden_master_hugo_legacy_java` (LegacyHugoMarkdownRenderer Java vs baseline)
- [ ] **[TST-7.10]** 🟡 **[Python]** Проверить полноту PIPELINE_COMPLEXES (содержит все 16 комбинаций)

**Reverse-Engineering Doc-o-matic:**

- [ ] **[TST-7.11]** 🟡 **[Python]** Проверить наличие `Tests/docomatic_scraper.py` (или написать согласно SOP `skills/docomatic_semantics_analysis.md`)
- [ ] **[TST-7.12]** 🟡 **[Python]** Написать тест `test_scraper_dry_run_output_valid_json` — JSON содержит entity_types и filename_prefixes
- [ ] **[TST-7.13]** 🟡 **[Python]** Написать тест `test_scraper_detects_cpp_overload_patterns` — парсинг паттернов `!!OVERLOADED_`
- [ ] **[TST-7.14]** 🟢 **[Python]** Написать тест `test_scraper_optionality_threshold` — пометка сущностей как OPTIONAL при < 50% присутствия

**Граничные случаи по языкам:**

- [ ] **[TST-7.15]** 🟡 **[Python]** Написать тест `test_cpp_nested_templates_parsing` — экранирование вложенных шаблонов `map<string, vector<...>>`
- [ ] **[TST-7.16]** 🟡 **[Python]** Написать тест `test_cpp_anonymous_namespace_handling` — анонимные пространства имен не бросают KeyError
- [ ] **[TST-7.17]** 🟡 **[Python]** Написать тест `test_cpp_export_macro_filtered` — макросы экспорта (`ODA_EXPORT`) вырезаются из сигнатур
- [ ] **[TST-7.18]** 🟡 **[Python]** Написать тест `test_cpp_constructor_destructor_ordering` — конструктор и деструктор идут первыми в списке
- [ ] **[TST-7.19]** 🟡 **[C++]** Создать XML-fixture `engine/tests/assets/cpp_edge_cases.xml`
- [ ] **[TST-7.20]** 🟡 **[Python]** Написать тест `test_cs_generic_type_rendering` — рендеринг дженериков `Dictionary<TKey, TValue>`
- [ ] **[TST-7.21]** 🟡 **[Python]** Написать тест `test_cs_extension_method_rendering` — детекция C# extension методов
- [ ] **[TST-7.22]** 🟡 **[Python]** Написать тест `test_cs_nullable_type_rendering` — рендеринг nullable-типов `int?`, `string?`
- [ ] **[TST-7.23]** 🟡 **[C#]** Создать XML-fixture `engine/tests/assets/cs_edge_cases.xml`
- [ ] **[TST-7.24]** 🟡 **[Python]** Написать тест `test_java_generics_rendering` — рендеринг wildcard дженериков `Collection<? extends T>`
- [ ] **[TST-7.25]** 🟡 **[Python]** Написать тест `test_java_varargs_rendering` — рендеринг Java varargs `String... args`
- [ ] **[TST-7.26]** 🟡 **[Java]** Создать XML-fixture `engine/tests/assets/java_edge_cases.xml`
- [ ] **[TST-7.27]** 🟡 **[Python]** Написать тест `test_legacy_html_output_matches_docomatic_naming` (имена вида `!!MEMBERTYPE_Methods_ClassName`)
- [ ] **[TST-7.28]** 🟡 **[Python]** Написать тест `test_legacy_hugo_sidebar_matches_html_sidebar`
- [ ] **[TST-7.29]** 🟡 **[Delphi]** Создать утилиту `Tests/generate_docomatic_baseline.dpr` для воспроизведения Docomatic naming
- [ ] **[TST-7.30]** 🟢 **[VB]** Написать `Tests/generate_legacy_toc.vbs` для создания contents.html дерева

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
- [ ] **[AD-ISO-03]** 🔴 Удалить step создания симлинка `ln -s ../engine ./user-docs/engine` — заменить PYTHONPATH или sys.path в `ude_config_self.json`

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

### 5.4.1 Автоматизация тестов в CI/CD (Quality Gates)

- [ ] **[TST-8.1]** 🔴 **[Python]** Добавить job `engine-tests` в `integration_tests.yml` (прогон pytest с cover-fail-under=98)
- [ ] **[TST-8.2]** 🟡 **[Python]** Добавить CI-step для per-language integration: `pytest tests/test_integration_*.py`
- [ ] **[TST-8.3]** 🟡 **[Python]** Добавить CI-step для Docomatic alignment: `pytest engine/tests/test_docomatic_alignment.py`
- [ ] **[TST-8.4]** 🟡 **[Python]** Добавить CI-step для Entity Completeness: `pytest engine/tests/test_entity_completeness.py`
- [ ] **[TST-8.5]** 🟢 **[Python]** Настроить upload артефакта coverage HTML report в GHA при сбоях (retention 7 дней)
- [ ] **[TST-8.6]** 🟢 **[Python]** Настроить upload JSON-отчетов расхождений alignment suite при сбоях
- [ ] **[TST-8.7]** 🔴 **[Python]** Создать `scripts/pydantic_guard.ps1` для блокировки обращений по ключу к полям в рендерерах (для Windows)
- [ ] **[TST-8.8]** 🟡 **[Python]** Создать `scripts/pydantic_guard.sh` — аналогичный скрипт для Linux (CI runner)
- [ ] **[TST-8.9]** 🟡 **[Python]** Добавить step запуска `pydantic_guard.sh` в `generate-api-ref.yml` после GAP-03
- [ ] **[AD-RENDERER-01]** 🔴 Ввести CI-требование (Gate): в `generate-api-ref.yml` ОБЯЗАН присутствовать шаг Renderer Factory Guard (CB-04), проверяющий сигнатуру `__new__`
- [ ] **[AD-RENDERER-02]** 🔴 Шаг Renderer Factory Guard (CB-04) НЕ имеет `continue-on-error: true` — он всегда блокирующий

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
- [ ] **[AD-MON-01]** 🟡 Настроить GitHub Actions notification для failures на ветке master: email-уведомление через стандартные настройки GitHub или Slack webhook
- [ ] **[AD-MON-03]** 🟢 Добавить `if: always()` для финального step (cleanup / report) — выполняется даже при failure предыдущих steps

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
- [ ] **[AD-DOC-11]** 🟡 Задокументировать CI guard-скрипты в `admin-deployment.md` или выделенном разделе `cicd-pipelines.md`
- [ ] **[AD-DOC-12]** 🟡 Задокументировать порядок CI steps в `generate-api-ref.yml` и обоснование (WHY): Pydantic Guard → Renderer Factory Guard → Traceability Check → Compile

---

## Раздел 8 — Требования к качеству документации

### 8.1 Markdown и синтаксические требования

- [ ] **[DR-NEW-01]** 🔴 Ввести требование: все MD-файлы проходят `markdownlint-cli2` в CI
- [ ] **[DR-NEW-02]** 🟡 Конфигурация markdownlint: max 120 символов, `MD013` только к prose
- [ ] **[DR-NEW-03]** 🟡 Правило: в design-docs все файлы начинаются с YAML front-matter (`sidebar_position`, `title`)
- [ ] **[DR-NEW-05]** 🟡 Правило: H1 ровно один, первый, совпадает с `title` в front-matter
- [ ] **[DR-NEW-06]** 🔴 Установить правило для Mermaid-диаграмм: каждая диаграмма содержит `%% Description` комментарий и title-ноду для accessibility

### 8.2 Автоматическая проверка ссылок

- [ ] **[DR-NEW-07]** 🔴 `Tests/check_links.py` (GAP-31) должен быть реализован до релиза v2.0
- [ ] **[DR-NEW-08]** 🟡 После GAP-31: `check_links.py` запускается в `integration_tests.yml` как отдельный step
- [ ] **[DR-NEW-09]** 🟡 Проверка relative links в design-docs через `docusaurus-check-links` или аналог
- [ ] **[DR-NEW-10]** 🔴 Установить правило: внешние ссылки (HTTPS) допустимы только в `admin-deployment.md` и `getting-started.md`; в design-docs внешние ссылки требуют review-комментария с обоснованием
- [ ] **[DR-NEW-11]** 🔴 Ввести требование: ссылки на internal GitHub Pages (`Sir-Derryk.github.io`) в user-docs проверяются тестом page-existence (`verify_pages.py`)

### 8.3 Версионирование и архивирование

- [ ] **[DR-NEW-12]** 🟡 Перед слиянием v2.0: создать versioned snapshot в Docusaurus (`docusaurus docs:version 1.0`)
- [ ] **[DR-NEW-13]** 🟡 Ввести правило: в design-docs `roadmap/future_v2.md` разделы по мере реализации переносятся в `roadmap/mvp_v2/`, а не редактируются на месте
- [ ] **[DR-NEW-14]** 🟡 Документировать процедуру версионирования в `CLAUDE.md`
- [ ] **[DR-NEW-15]** 🟡 После freeze v2.0: `requirements_v2_next.md` → `requirements_v3_next.md`

### 8.4 Трассировка и согласованность

- [ ] **[DR-NEW-16]** 🟡 Каждый ⚠️-GAP в `integration_tests_specification.md` получает поле `Resolution Target`
- [ ] **[DR-NEW-17]** 🟡 Глоссарий терминов: `Collector`, `Orchestrator`, `Parser`, `Renderer`, `IR`, `Catalog` — единообразное использование
- [ ] **[DR-NEW-18]** 🟢 Создать Glossary-страницу в design-docs (15+ терминов)
- [ ] **[DR-NEW-19]** 🟡 При удалении требования — запись в `quality_audit.md` с обоснованием

### 8.5 Требования к безопасности и инфраструктуре доки

- [ ] **[DR-NEW-22]** 🔴 Документировать все используемые secrets в отдельном файле `docs/deployment/secrets.md` (user-docs) или `CLAUDE.md`: имя, назначение, минимальные права, срок ротации
- [ ] **[DR-NEW-23]** 🔴 Ввести требование: `PIPELINE_GITHUB_TOKEN` secret должен использовать **Fine-grained Personal Access Token** (не classic), с ограничением по репозиториям и permissions: `contents: read`, `actions: write` (для repository_dispatch)
- [ ] **[DR-NEW-24]** 🔴 Ввести правило: все environment variables в workflow явно декларируются через `env:` на уровне job или step — не передаются через inline shell substitution без документирования
- [ ] **[DR-NEW-25]** 🔴 Ввести требование: README или AGENTS.md в `.github/` описывает назначение каждого workflow, его триггеры и ожидаемые Check-статусы в GitHub UI
- [ ] **[DR-NEW-26]** 🟡 Ввести формальную процедуру deprecation: файлы, помеченные для удаления, получают frontmatter `deprecated: true` и раздел `> ⚠️ DEPRECATED:` с указанием замены — не удаляются сразу
- [ ] **[DR-NEW-27]** 🟡 Архивировать `brd/ude_portal_blueprint.md` — по статусу в design-docs он помечен как устаревший legacy; переместить в `design-docs/docs/_archive/`
- [ ] **[DR-NEW-28]** 🟢 Ввести правило: при каждом major-релизе создавать GitHub Release с release notes, дублирующими `changelog.md` из user-docs, для portfolio-видимости

### 8.6 Quality Gates для документации

- [ ] **[DR-NEW-29]** 🔴 Ввести CI-step в `design-docs` workflow: Docusaurus build (`npm run build`) должен завершаться с exit 0 — warnings считаются ошибками при наличии broken links (флаг `--fail-on-warning` для broken links)
- [ ] **[DR-NEW-30]** 🟡 Ввести CI-step: проверка, что все файлы в `design-docs/docs/` имеют корректный `sidebar_position` (числовой, уникальный в директории) — Python-скрипт или `remark-lint`
- [ ] **[DR-NEW-31]** 🟡 Ввести правило: `v2_detailed_tasks.md` (2 364 строки) должен быть разбит на отдельные файлы в `tasks/` после freeze v2.0 — максимальный размер задокументированного файла: 500 строк
- [ ] **[DR-NEW-32]** 🔴 Ввести требование: страницы user-docs, описывающие CLI-команды, тестируются в CI smoke-тестом — команда `python -m ude.cli --help` должна возвращать exit 0 и содержать ключевые флаги из документации

### 8.7 Требования к документированию архитектурных решений (Cross-Phase)

- [ ] **[DR-NEW-33]** 🟡 Ввести требование: TASK-A.1.1 (`GlobalConfig`) ОБЯЗАН содержать примечание о том, что поля `coverage_mode` и `coverage_threshold` являются **схемными заглушками фазы 1**
- [ ] **[DR-NEW-34]** 🟡 Ввести требование: TASK-A.4.3 (`DoxygenXmlCollector` с 3-уровневым merge) обязан документировать **приоритет разрешения T1-шаблона Doxyfile**: `GlobalConfig.global_templates_dir` → `templates` → `{}`
- [ ] **[DR-NEW-35]** 🟡 Ввести требование: задачи TASK-D.1.4 (C#), TASK-D.1.5 (Java), TASK-D.1.6 (Python) обязаны содержать **конкретные примеры кода** с языко-специфичными XML kind-маппингами Doxygen
- [ ] **[DR-NEW-36]** 🟡 Ввести требование: разрешить неоднозначность в TASK-F.2.5 (Python integration tests) относительно полей `is_property`, `fget`, `fset` в `VariableModel` / `MethodModel`
- [ ] **[DR-NEW-37]** 🟡 Ввести требование: каждый файл задачи `TASK-*.md` в `.antigravitycli/tasks/` при указании CLI-команд верификации ОБЯЗАН предоставлять обе формы — bash/sh и PowerShell (AW-02)
- [ ] **[DR-NEW-38]** 🟡 Ввести требование: все проверочные команды в `TASK-*.md`, использующие сравнение директорий, ОБЯЗАНЫ использовать `filecmp.dircmp` или Python-скрипт `scripts/compare_dirs.py`, а не `diff -r` (AW-03)
- [ ] **[DR-NEW-39]** 🟡 Ввести требование: конфигурация `sidebar.toml` документируется как отдельный справочный раздел (структура секций, 3-way deep_merge cascade, `_load_sidebar_toml_graceful()` при отсутствии)
- [ ] **[DR-NEW-40]** 🟡 Ввести требование: метод `_load_static_file_from_path()` на `BaseRenderer` документируется в справочнике API рендереров

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
| 0 | Подготовка репозитория и окружения | 12 | 12 | 7 | — |
| 1 | Фаза 1: Инфраструктура | 59 | 11 | — | Фазу 2 |
| 2 | Фаза 2: API & CLI | 21 | 15 | 1 | Фазу 3 |
| 3 | Фаза 3/D: Typed IR | 45 | 14 | — | Релиз |
| 4 | Фаза 3/F: QA | 47 | 55 | 9 | Релиз |
| 5 | CI/CD деплой | 16 | 16 | 14 | Релиз |
| 6 | User Docs | 17 | 12 | 4 | Релиз |
| 7 | Pipeline Docs | 5 | 5 | 2 | Релиз |
| 8 | Doc Requirements | 11 | 24 | 2 | Релиз |
| 9 | Финализация | 13 | 5 | 4 | — |
| **∑** | **Всего** | **246** | **169** | **43** | |

---

> **Статус:** Документ создан 2026-06-29. Все задачи ожидают исполнения.  
> **Следующий шаг:** Раздел 0 (подготовка, нулевой риск) → Фаза 1 (GAP-09).  
> **Ограничение Phase 3/D:** GAP-10 активируется после завершения GAP-03 и GAP-01.  
> **Ограничение CI/CD Фаза 4:** coverage gate через `ude audit` активируется после реализации GAP-10.
