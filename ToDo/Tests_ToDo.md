# UDE — Комплексный план разработки тестов
## Дорожная карта обеспечения качества при миграции Doc-o-matic → UDE

> **Документ:** `ToDo/Tests_ToDo.md`
> **Дата:** 2026-06-29
> **Автор анализа:** QA Architect / Migration Specialist
>
> **Источники:**
> - `.antigravitycli/v2_execution_plan.md` — технический план фаз v2.0
> - `.antigravitycli/v2_detailed_tasks.md` — атомарные задачи с кодовыми артефактами
> - `.antigravitycli/requirements_v2_next.md` — требования v2.0 с критериями приёмки
> - `.antigravitycli/active_plan.md` — хронология выполненных и плановых задач v1.0/v2.0
> - `.antigravitycli/contents_analysis_report.md` — количественный аудит ToC Doc-o-matic
> - `.antigravitycli/skills/docomatic_semantics_analysis.md` — SOP анализа семантики Docomatic
> - `.antigravitycli/skills/difference_minimization_iterator.md` — SOP минимизации расхождений
> - `ToDo/v20_todo.md` — сводный план задач v2.0

---

## Структурный и исторический контекст миграции

### Ключевая архитектурная разница: Doc-o-matic vs. UDE

| Аспект | Doc-o-matic (legacy) | UDE (целевая система) |
|--------|---------------------|----------------------|
| **Модель страниц** | Одна отдельная HTML-страница **на каждую сущность** (метод, свойство, поле — каждое имеет свой файл) | Одна страница **на весь класс** — все члены класса агрегированы на единой странице |
| **Именование файлов** | Уникальные плоские имена с кодированием символов (`!!OVERLOADED_`, `!!MEMBERTYPE_`, `!!CLASSES_`) | Иерархические пути в директориях по пространствам имён |
| **Навигация** | `contents.html` с раскрываемым деревом ToC | Боковая панель на основе `sidebar.toml` / JSON-конфигов |
| **Масштаб** | BimNv Java: **17 514 ToC-узлов**, **706 классов**, **15 600 листовых страниц** | Соответствующее количество страниц класса с агрегированными членами |

**Критическая угроза качества:** при агрегации страниц сущности могут быть **молча потеряны** или **структурно искажены** — без явного падения теста, только через отсутствие в ToC или неправильный рендеринг. Именно поэтому 100% полнота охвата сущностей является **абсолютным, не подлежащим обсуждению критерием успеха**.

### Масштаб данных (из `contents_analysis_report.md`)

| Продукт / Язык | Классов | Листовых узлов (страниц) | Пространств имён | Виртуальных групп |
|----------------|---------|------------------------|-----------------|------------------|
| FacetModeler C++ | 36 | 615 | 1 | 52 |
| FacetModeler C# | 76 | 1 413 | 3 | 149 |
| FacetModeler Java | 105 | 2 371 | 0 | 112 |
| BimNv C++ | 213 | 2 176 | 87 | 296 |
| BimNv C# | 375 | 8 219 | 7 | н/д |
| BimNv Java | 706 | 15 600 | 0 | н/д |

### Текущее состояние тест-сюита (v1.0 baseline)

- **209 тестов** в `engine/tests/` (сабмодуль), **≥ 98% statement coverage**
- В `pipeline/tests/` и `pipeline/engine/tests/` — файлов **нет** (тесты живут только в сабмодуле `engine`)
- Ключевые существующие тест-файлы: `test_golden_master.py`, `test_docomatic_alignment.py`, `test_integration_pipeline.py`, `test_html_renderer.py`, `test_hugo_renderer.py`, `test_legacy_renderer.py`, `test_doxygen_parser.py`

---

## Условные обозначения

| Маркер | Значение |
|--------|----------|
| 🔴 | Критичный — блокирует следующий шаг |
| 🟡 | Важный — требуется до релиза v2.0 |
| 🟢 | Желательный / параллельный |
| ⚡ | Зависит от предыдущего шага |
| `[GAP-XX]` | Ссылка на GAP из `v2_execution_plan.md` |
| `**[Python]**` | Язык реализации теста |

---

## Фаза 0 — Подтверждение базового состояния v1.0 (TDD: Baseline)

> **Цель:** Зафиксировать измеримый baseline перед началом любых изменений. Без зафиксированного baseline невозможно удостовериться, что v2.0-изменения не вызвали регрессию.
> **Язык реализации:** Python (pytest)

### 0.1 Верификация существующей тест-инфраструктуры

- [ ] 🔴 **[Python]** Запустить полный сюит движка и убедиться в прохождении всех 209 тестов — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._:
  `poetry run pytest engine/tests/ -v`
- [ ] 🔴 **[Python]** Подтвердить покрытие ≥ 98% — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._:
  `poetry run pytest --cov=ude --cov-report=term-missing | Select-String "TOTAL"`
- [ ] 🔴 **[Python]** Зафиксировать baseline-метрики: количество тестов, % coverage, время прогона в `ToDo/Tests_ToDo.md` (раздел Метрики) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Запустить performance-бенчмарк: `poetry run pytest tests/test_performance_benchmark.py -v` — убедиться ≤ 5 s для 1000 классов — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 0.2 Аудит покрытия по модулям (Gap-анализ)

- [ ] 🟡 **[Python]** Сгенерировать HTML-отчёт покрытия — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._:
  `poetry run pytest --cov=ude --cov-report=html`
- [ ] 🟡 **[Python]** Выявить модули с покрытием < 98% — зафиксировать пробелы в данном файле — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Создать тест `test_coverage_gate.py` с CI-ready параметром `--cov-fail-under=98` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

---

## Фаза 1 — Рефакторинг и стабилизация существующих тестов (TDD: Refactor)

> **Цель:** Привести существующую тест-базу в соответствие с v2.0-схемами именования и новой конфигурационной моделью.

### 1.1 Переименование конфигураций в тестах

> Переименование `ude_global.json` → `ude_global_config.json` и `ude_config.json` → `ude_doc_config.json` затрагивает все тест-файлы.

- [ ] 🔴 **[Python]** В `engine/tests/test_orchestrator.py`: заменить все вхождения `"ude_global.json"` → `"ude_global_config.json"`, `"ude_config.json"` → `"ude_doc_config.json"` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** В `engine/tests/test_integration_pipeline.py`: аналогичная замена — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** В `engine/tests/test_doxygen_collector.py`: аналогичная замена — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Обновить docstring-комментарии в `engine/ude/interfaces.py` и `engine/ude/collectors/doxygen.py` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Запустить `poetry run pytest engine/tests/ -v` после замен — убедиться в 0 failed — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 1.2 Исправление некорректного имени логгера (HC-05)

- [ ] 🔴 **[Python]** В `engine/tests/` найти все `caplog`-ассерты с `"ude.renderers"` из `interfaces.py` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._:
  `Select-String -Path engine\tests\*.py -Pattern '"ude.renderers"' -Recurse`
- [ ] 🔴 **[Python]** Обновить найденные ассерты: `"ude.renderers"` → `"ude.interfaces"` (соответствует исправлению HC-05 в `interfaces.py`) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Убедиться в прохождении тестов после исправления — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 1.3 Рефакторинг тест-утилит под v2.0 контракты

- [ ] 🟡 **[Python]** В `engine/tests/utils.py`: добавить `LanguageIntegrationBase` mixin (класс-основу для per-language integration tests) с полями `LANGUAGE`, `XML_FIXTURE`, `RENDERER_CLASS` и методом `_run_pipeline(tmp_path) -> Path` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить вспомогательную функцию `_write_test_config(tmp_path, **kwargs) -> Path` — создаёт временный `ude_doc_config.json` для интеграционных тестов — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Добавить фабрику `_make_mock_catalog(language, num_classes, num_methods)` — создаёт синтетический `ProjectCatalog` заданного размера для unit-тестов — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

---

## Фаза 2 — Новые юнит-тесты: Инфраструктурные улучшения v2.0

> **TDD-порядок:** RED (написать тест) → GREEN (реализация) → REFACTOR. Тесты пишутся ДО реализации.

### 2.1 `test_config.py` — GlobalConfig и logging_setup `[GAP-09, GAP-12]`

> **Файл:** `engine/tests/test_config.py` *(CREATE)*

- [ ] 🔴 **[Python]** Написать тест `test_global_config_defaults` — `GlobalConfig()` без аргументов даёт корректные дефолты (`log_level="WARNING"`, `error_policy="fail-fast"`, все Optional-поля `None`) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_global_config_full_round_trip` — все поля round-trip через `from_file()`: записать JSON → прочитать → сравнить — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_global_config_unknown_keys_ignored` — extra-ключи (`"future_field": 99`) не вызывают `ValidationError` (Pydantic `extra="ignore"`) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_global_config_missing_file_raises` — `from_file(non_existent_path)` → `FileNotFoundError` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_global_config_bad_json_raises` — `from_file(path_with_invalid_json)` → `ValueError` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_global_config_coverage_threshold_parses` — Phase 1 stub: `coverage_threshold=0.85` принимается без ошибок — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_global_config_coverage_threshold_bounds` — `coverage_threshold=1.5` → `ValidationError` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_apply_global_cfg_env_injects_path` — вызов `apply_global_cfg_env(cfg)` добавляет `doxygen_path` в `os.environ["PATH"]` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_apply_global_cfg_env_idempotent` — двойной вызов не дублирует запись в PATH — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_apply_global_cfg_env_noop_when_none` — `doxygen_path=None` → PATH не изменяется — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_logging_setup_stderr_only` — `log_file=None` → у логгера `"ude"` ровно 1 StreamHandler — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_logging_setup_with_log_file` — `log_file` → 2 хэндлера, файл создан на диске — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_logging_setup_level_debug` — `log_level="DEBUG"` → `logger.level == logging.DEBUG` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_logging_setup_invalid_level` — `log_level="VERBOSE"` (некорректный) → уровень падает к WARNING без исключения — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_logging_setup_idempotent` — два вызова `logging_setup()` → ровно 1 хэндлер (не накапливаются) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_orchestrator_stores_global_cfg_instance` — после инициализации `orchestrator._global_cfg` является экземпляром `GlobalConfig` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_orchestrator_sets_path_from_doxygen_path` — mock `subprocess.run`; `doxygen_path` из global config инжектируется в PATH до запуска Doxygen — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_orchestrator_cache_root_resolved_absolute` — `cache_root_dir` резолвится в абсолютный `Path` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

**Верификация фазы:**
```bash
poetry run pytest tests/test_config.py -v --tb=short
# Ожидается: ≥ 17 PASSED
```

### 2.2 `test_doxyfile.py` — 3-уровневый Doxyfile merge `[GAP-11]`

> **Файл:** `engine/tests/test_doxyfile.py` *(CREATE)*

- [ ] 🔴 **[Python]** Написать тест `test_parse_basic` — `"PROJECT_NAME = MyLib\nGENERATE_XML = YES\n"` → `{"PROJECT_NAME": "MyLib", "GENERATE_XML": "YES"}` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_parse_skip_comments_and_blanks` — строки с `#` и пустые строки не попадают в словарь — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_parse_continuation_lines` — backslash-continuation (`INPUT = src\\\n include\n`) → значение объединяется в одну строку — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_parse_value_with_equals` — `"PREDEFINED = FOO=1"` → `{"PREDEFINED": "FOO=1"}` (значение содержит `=`) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_serialize_round_trip` — parse → serialize → parse: все ключи сохраняются, порядок алфавитный — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_merge_t2_overrides_t1` — ключ в T1 и T2 → T2-значение побеждает — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_merge_t3_overrides_t2` — ключ в T1/T2/T3 → T3-значение побеждает — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_merge_debug_log_on_conflict` — конфликт T2 vs T1 → `caplog` фиксирует DEBUG-запись с именем ключа — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_merge_missing_tiers` — `merge_doxyfile_tiers({}, {}, t3)` → результат равен `t3` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_collector_uses_merged_doxyfile` — mock `subprocess.run`; записанный temp-Doxyfile содержит T3-ключи (`OUTPUT_DIRECTORY`, `GENERATE_XML`, `INPUT`) ровно по одному разу — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_collector_t3_overrides_t2_key` — target-Doxyfile задаёт `GENERATE_HTML = YES`; после merge в итоговом Doxyfile → `GENERATE_HTML = NO` (T3 побеждает) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

**Верификация фазы:**
```bash
poetry run pytest tests/test_doxyfile.py -v
# Ожидается: ≥ 11 PASSED
```

### 2.3 `test_caching.py` — L2 Render Cache `[GAP-07]`

> **Файл:** `engine/tests/test_caching.py` *(MODIFY — добавить новые тесты)*

- [ ] 🔴 **[Python]** Написать тест `test_compute_template_hash_stable` — одна директория → один и тот же хэш при двух последовательных вызовах — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_compute_template_hash_changes_on_content_change` — изменить один файл шаблона → хэш меняется — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_compute_template_hash_empty_dir` — пустая директория → `""` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_compute_template_hash_missing_dir` — несуществующая директория → `""` (без исключения) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_l2_html_cache_hit_skips_write` — рендер дважды (pytest-mock spy на `builtins.open`); второй прогон не вызывает файловую запись — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_l2_html_cache_miss_on_catalog_change` — мутировать один метод в catalog → файл пересоздаётся — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_l2_html_cache_miss_on_template_change` — изменить Jinja2-шаблон → файл пересоздаётся — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_l2_html_cache_disabled_when_no_manager` — `cache_manager=None` → поведение v1.0, файлы всегда пишутся — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_l2_hugo_cache_hit_skips_write` — аналог для Hugo markdown рендерера — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_l2_legacy_cache_hit_skips_write` — аналог для Legacy рендерера — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_sequential_build_l2_cache_hits` — интеграционный: два прогона `orchestrator.run()` → `mocker.spy` подтверждает, что на втором прогоне не происходит ни одной файловой записи — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

**Верификация фазы:**
```bash
poetry run pytest tests/test_caching.py -v
# Ожидается: все L2-тесты PASSED
```

### 2.4 Обязательная верификация передачи `cache_manager` через `__new__` (CB-04)

> **Источник:** `skills_compliance_report.md` CB-04 · `pydantic_migration_guard.md` Шаг 5  
> Разрыв `__new__` → `super().__init__()` для `cache_manager` в `hugo_markdown.py` или `legacy.py` **не вызывает исключений** — L2-кэш молча отключается для соответствующего формата вывода. Явная grep-верификация является обязательным acceptance criterion для TASK-A.3.2 и TASK-A.3.4.

- [ ] 🔴 **[Python]** После реализации TASK-A.3.2: выполнить обязательный grep-аудит ВСЕХ ТРЁХ семейств рендереров (bash) — _Python provides portable grep/audit scripting as a cross-platform pytest-compatible alternative._:
  ```bash
  for f in engine/ude/renderers/static_html.py \
            engine/ude/renderers/hugo_markdown.py \
            engine/ude/renderers/legacy.py; do
    echo "=== $f ==="; grep -n "def __new__\|def __init__\|cache_manager" "$f"
  done
  ```
- [ ] 🔴 **[Python]** Выполнить аналогичный аудит на Windows (локальный запуск) — _Python provides portable grep/audit automation replacing Windows-only PowerShell scripts._:
  ```powershell
  foreach ($f in @("engine/ude/renderers/static_html.py",
                   "engine/ude/renderers/hugo_markdown.py",
                   "engine/ude/renderers/legacy.py")) {
      Write-Host "=== $f ===" -ForegroundColor Cyan
      Select-String -Path $f -Pattern "def __new__|def __init__|cache_manager"
  }
  ```
- [ ] 🔴 **[Python]** Убедиться, что для каждого из трёх файлов: `cache_manager` присутствует как в сигнатуре `__new__` (или `**kwargs`), так и передаётся в `super().__init__(...)`. Отсутствие хотя бы в одном файле является блокирующим дефектом CB-04. — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cache_manager_forwarded_through_new_hugo` — `HugoMarkdownRenderer(language="cpp", cache_manager=mock_mgr)` сохраняет `_cache_mgr = mock_mgr` (не `None`) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cache_manager_forwarded_through_new_legacy` — аналог для `LegacyRenderer` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

**Верификация CB-04 (обязательно до закрытия TASK-A.3.4):**
```bash
# Ожидаемый вывод: cache_manager встречается в __new__ И __init__ каждого файла
grep -n "cache_manager" engine/ude/renderers/hugo_markdown.py
grep -n "cache_manager" engine/ude/renderers/legacy.py
# Если вывод пустой — TASK-A.3.4 не завершён (CB-04 нарушен)
```

---

## Фаза 3 — Новые тесты: Library API и CLI `[GAP-05, GAP-01]`

### 3.1 `test_orchestrator.py` — Public Library API `[GAP-05]`

> **Файл:** `engine/tests/test_orchestrator.py` *(MODIFY — добавить новые тесты)*

- [ ] 🔴 **[Python]** Написать тест `test_orchestrator_parse_returns_catalog` — `orchestrator.parse(config, config_dir)` с mock XML → возвращает экземпляр `ProjectCatalog` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_orchestrator_parse_skips_collector_when_xml_exists` — если `index.xml` уже существует → `DoxygenXmlCollector.collect` не вызывается (monkeypatch) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_orchestrator_render_produces_files` — `orchestrator.render(catalog, config, ...)` → файлы HTML/Markdown созданы в `out_dir` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_orchestrator_render_respects_format_config` — `config["renderer"]["type"] = "hugo_markdown"` → `.md`-файлы; `"html"` → `.html`-файлы — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_orchestrator_run_end_to_end` — `orchestrator.run(config_path)` возвращает `True`; output-файлы существуют — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_run_target_is_alias` — monkeypatch `UdeOrchestrator.run`; вызов `run_target()` делегирует в `run()` с тем же путём — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_orchestrator_run_returns_false_on_missing_config` — несуществующий путь → возвращает `False`, без исключения — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_resolve_config_returns_merged_dict` — передать global/sdk/doc configs → merged-словарь с корректным приоритетом override — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_resolve_config_graceful_sidebar_missing` — нет `sidebar.toml` → `sidebar_config = {}`, без исключения — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_resolve_config_sidebar_static_paths_absolute` — static `source_file` в `sidebar.toml` резолвируется в абсолютный путь — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_deep_merge_importable_from_both_modules` — `from ude.cli import deep_merge` и `from ude.orchestrator import deep_merge` оба работают без `ImportError` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 3.2 `test_cli.py` — CLI Subcommands `[GAP-01]`

> **Файл:** `engine/tests/test_cli.py` *(MODIFY — добавить новые тесты)*

- [ ] 🔴 **[Python]** Написать тест `test_compile_delegates_to_run_pipeline` — mock `run_pipeline`; `main(["compile", "--doc-config", "x.json"])` → `run_pipeline` вызывается с `doc_config_path=Path("x.json")` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_compile_missing_doc_config` — `main(["compile"])` → exit code `1` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_parse_subcommand_creates_ir_file` — `main(["parse", "--doc-config", "...", "--output-ir", "out.json.gz"])` → файл `.json.gz` создан — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_parse_subcommand_prints_json_summary` — `capsys.readouterr()` stdout → валидный JSON с ключом `"namespaces"` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_render_subcommand_from_ir` — сохранить IR, `main(["render", "--input-ir", "...", "--output", "..."])` → output-файлы существуют — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_parse_then_render_identical_to_compile` — `filecmp.dircmp(compile_out, render_out)` → нет различий (`diff_files`, `left_only`, `right_only` — все пустые) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_audit_stub_returns_2` — `main(["audit", "--doc-config", "x.json"])` → exit code `2` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_audit_stub_prints_to_stderr` — `capsys.readouterr()` stderr содержит `"not yet implemented"` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_flat_flags_still_work` — `main(["--doc-config", "..."])` → успешная работа (backward compat v1.0) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_all_subcommands_reachable` — `main([cmd, "--help"])` для каждой команды из `["compile", "parse", "render", "audit"]` → exit `0` (argparse help) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_cli_delegates_to_orchestrator` — mock `UdeOrchestrator.run`; `main(["--doc-config", "..."])` → orchestrator вызывается — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

**Верификация фаз 3.1–3.2:**
```bash
poetry run pytest tests/test_orchestrator.py tests/test_cli.py -v --tb=short
# Ожидается: все новые тесты PASSED, 0 регрессий
```

---

## Фаза 4 — Новые тесты: Типизированный IR и Coverage Gate `[GAP-03, GAP-10]`

### 4.1 `test_models.py` — 7-модельная типизированная схема `[GAP-03]`

> **Файл:** `engine/tests/test_models.py` *(FULL REWRITE)*

- [ ] 🔴 **[Python]** Написать тест `test_project_catalog_has_project_name_and_version` — `ProjectCatalog(project_name="SDK", version="2.0")` round-trip через JSON — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_class_model_fields_are_variable_models` — `ClassModel.fields[0]` является экземпляром `VariableModel` (не строкой) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_old_ir_json_deserializes_without_error` — загрузить v1.0-JSON без полей `free_functions`/`enums`/`constants` → без `ValidationError` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_variable_model_nonempty_round_trip` — `VariableModel(name="myField", type="int")` → serialize → deserialize → `fields[0].name == "myField"` и `fields[0].type == "int"` (Pydantic Guard Step 2b) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_class_model_extra_field_ignored` — `ClassModel.model_validate({"name": "X", "fully_qualified_name": "Y", "unknown_v3_field": 99})` → успех, `unknown_v3_field` не сохраняется (Guard Step 3) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_project_catalog_extra_field_ignored` — `ProjectCatalog.model_validate({"namespaces": [], "future_field": "x"})` → успех (Guard Step 3) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_backward_compat_alias` — `ClassEntity is ClassModel` → `True` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_7_model_round_trip` — создать `ProjectCatalog` со всеми 7 типами моделей; serialize → deserialize → все поля сохранены — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_method_model_overloads` — `MethodModel.overloads` является `List[OverloadModel]` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_enum_model_values` — `EnumModel.values` является `List[str]` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_constant_model_has_value` — `ConstantModel.value` nullable, сериализуется как `null` при `None` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_type_alias_model_round_trip` — `TypeAliasModel(name="MyAlias", aliased_type="int64_t")` round-trip — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 4.2 Рефакторинг тестов парсеров под v2.0 модели `[GAP-03]`

> **Файлы:** `test_doxygen_parser.py`, `test_html_renderer.py`, `test_hugo_renderer.py`, `test_legacy_renderer.py`

- [ ] 🔴 **[Python]** В `test_doxygen_parser.py`: обновить все ассерты — `entity.fields[i]` теперь `VariableModel`, использовать `entity.fields[i].name` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** В `test_doxygen_parser.py`: добавить тест `test_parser_populates_enum_model` — `<memberdef kind="enum">` в XML → `ClassModel.enums[0]` является `EnumModel` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** В `test_doxygen_parser.py`: добавить тест `test_parser_populates_constant_model` — `<memberdef kind="variable" mutable="no" static="yes">` → `ClassModel.constants` содержит `ConstantModel` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** В `test_html_renderer.py`: обновить fixtures под `ClassModel` с `fields: List[VariableModel]` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** В `test_hugo_renderer.py`: аналогичное обновление fixtures — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** В `test_legacy_renderer.py`: аналогичное обновление fixtures — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** После каждого файла: `poetry run pytest tests/<file> -v` — 0 failed перед переходом к следующему — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Проверить обязательный scan (Pydantic Guard Step 4): `Select-String -Path engine\ude\renderers\*.py -Pattern '\.fields\b' -Recurse` — все вхождения должны использовать `.name`/`.type`, а не строковый доступ — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 4.3 `test_coverage.py` — Documentation Coverage Gate `[GAP-10]`

> **Файл:** `engine/tests/test_coverage.py` *(CREATE)*

- [ ] 🔴 **[Python]** Написать тест `test_full_coverage_catalog` — все сущности имеют непустые docstrings → `overall.coverage == 1.0` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_zero_coverage_catalog` — все docstrings `None` → `overall.coverage == 0.0` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_mixed_coverage` — 3 из 4 методов задокументированы → `method.coverage == 0.75` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_reject_mode_exits_nonzero` — `main(["audit", "--mode", "reject-undocumented", "--threshold", "1.0", ...])` при 0% coverage → exit code `2` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_allow_mode_exits_zero` — та же ситуация, но `allow-undocumented` → exit code `0` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_audit_output_contains_table` — stdout содержит `| class |`, `| method |`, `| overall |` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_coverage_gate_runs_on_compile` — `orchestrator.run()` с `coverage_mode="reject-undocumented"` и 0% coverage → возвращает `False` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_coverage_gate_absent_on_parse` — `ude parse` не активирует gate (monkeypatch `compute_coverage` → assert not called) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_coverage_gate_absent_on_render` — `ude render` не активирует gate — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

**Верификация фазы 4:**
```powershell
poetry run pytest tests/test_models.py tests/test_coverage.py tests/test_doxygen_parser.py -v
# Ожидается: все PASSED
poetry run pytest --cov=ude --cov-report=term-missing | Select-String "TOTAL"
# Ожидается: ≥ 98%
```

### 4.5 Верификация трассировочных аннотаций docstring в Phase 3 (AW-08)

> **Источник:** `skills_compliance_report.md` AW-08 · `task_verification.md` Architectural Traceability criterion  
> Все публичные функции и классы в модулях фазы 3 (`coverage.py`, обновлённые парсеры, модели) обязаны содержать docstring с аннотацией `Implements TASK-D.X.X` или `Implements GAP-XX`. Без явной grep-проверки AI-агенты могут генерировать код без трассировочных маркеров.

- [ ] 🟡 **[Python]** После завершения TASK-D.2.7: выполнить grep-верификацию наличия аннотаций в Phase 3 модулях — _Python provides portable cross-platform scripting to replace CI-specific shell commands._:
  ```bash
  grep -rn "Implements TASK-D\|Implements GAP-" engine/ude/coverage.py
  grep -rn "Implements TASK-D\|Implements GAP-" engine/ude/models.py
  grep -rn "Implements TASK-D\|Implements GAP-" engine/ude/parsers/doxygen_csharp.py
  grep -rn "Implements TASK-D\|Implements GAP-" engine/ude/parsers/doxygen_java.py
  grep -rn "Implements TASK-D\|Implements GAP-" engine/ude/parsers/doxygen_python.py
  # Каждый файл должен вернуть ≥ 1 результат
  ```
- [ ] 🟡 **[Python]** Аналогичная проверка на Windows — _Python provides portable grep/audit automation replacing Windows-only PowerShell scripts._:
  ```powershell
  foreach ($f in @("engine/ude/coverage.py","engine/ude/models.py",
                   "engine/ude/parsers/doxygen_csharp.py",
                   "engine/ude/parsers/doxygen_java.py",
                   "engine/ude/parsers/doxygen_python.py")) {
      $hits = Select-String -Path $f -Pattern "Implements TASK-D|Implements GAP-"
      if (-not $hits) { Write-Error "AW-08 нарушен: $f не содержит Implements-аннотации" }
      else { Write-Host "OK: $f — $($hits.Count) аннотаций" }
  }
  ```
- [ ] 🟡 **[Python]** Написать тест `test_phase3_modules_have_traceability_docstrings` — для каждого Phase 3-модуля: `import inspect; assert "Implements" in inspect.getdoc(module.SomeClass)` или аналогичная проверка через `ast.parse` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

---

## Фаза 5 — Критические тесты полноты охвата сущностей (Entity Completeness)

> **Это ключевая фаза для миграции Doc-o-matic → UDE.** Обеспечивает 100% гарантию того, что ни одна сущность не потеряна при переходе от модели «страница-на-сущность» к модели «страница-на-класс».

### 5.1 Тесты Docomatic Alignment (существующие — расширить) `[GAP-03-H]`

> **Файл:** `engine/tests/test_docomatic_alignment.py` *(MODIFY)*

- [ ] 🔴 **[Python]** После GAP-03: перезапустить `test_docomatic_alignment.py` и зафиксировать `"total_differences"` для каждого языка как новый baseline — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Добавить тест `test_total_differences_not_increased_cpp` — после любого изменения в рендерере `total_differences` для C++ не выше pre-GAP-03 baseline — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Добавить тест `test_total_differences_not_increased_cs` — аналог для C# — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Добавить тест `test_total_differences_not_increased_java` — аналог для Java — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить тест `test_no_silent_entity_loss_cpp` — количество классов в UDE-output ≥ количество классов в Docomatic-baseline для C++ — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить тест `test_no_silent_entity_loss_cs` — аналог для C# — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить тест `test_no_silent_entity_loss_java` — аналог для Java — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 5.2 Количественные тесты полноты сущностей

> **Файл:** `engine/tests/test_entity_completeness.py` *(CREATE)*
> Эти тесты явно верифицируют, что объединение сущностей на страницах класса не приводит к потерям.

- [ ] 🔴 **[Python]** Написать тест `test_all_methods_present_after_aggregation_cpp` — для C++-каталога: количество методов в IR-модели = количеству методов в сгенерированных HTML-страницах (парсить `<h3>`, `<section>` в output) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_all_methods_present_after_aggregation_cs` — аналог для C# — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_all_methods_present_after_aggregation_java` — аналог для Java — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_no_orphan_entities_cpp` — для каждого метода в IR существует якорный элемент `<a id="...">` в соответствующем HTML-файле класса — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_no_orphan_entities_cs` — аналог для C# — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_no_orphan_entities_java` — аналог для Java — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_class_member_count_matches_toc_cpp` — количество членов класса в sidebar-ToC совпадает с количеством в IR — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_class_member_count_matches_toc_cs` — аналог для C# — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_class_member_count_matches_toc_java` — аналог для Java — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_overloaded_methods_all_present` — для каждого метода с перегрузками все перегрузки представлены в output (overload dispatcher страницы или inline секции) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_inherited_members_not_silently_dropped` — методы, унаследованные от базового класса, присутствуют (там, где это поддерживается Doxygen XML) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Написать тест `test_static_vs_instance_segregation` — static-члены и instance-члены правильно разделены в output — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 5.3 Тесты верификации структурной целостности страниц

> **Файл:** `engine/tests/test_page_structure.py` *(CREATE)*

- [ ] 🔴 **[Python]** Написать тест `test_class_page_has_method_section` — каждый класс с методами → страница содержит секцию методов (парсить lxml) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_class_page_has_fields_section_when_fields_exist` — классы с полями → секция Fields/Variables присутствует — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_namespace_index_lists_all_classes` — индексная страница пространства имён содержит ссылку на каждый класс из IR — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_sidebar_links_resolve_to_existing_files` — каждая ссылка в боковой панели резолвируется в существующий HTML-файл (без сетевого доступа) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_breadcrumbs_contain_correct_namespace` — хлебные крошки страницы класса содержат корректное пространство имён — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_entity_titles_follow_convention` — заголовки страниц следуют формату `<EntityID> <EntityType>` (регрессия TSK-RND-08) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

---

## Фаза 6 — Per-language Integration Test Suites `[GAP-32]`

> **Цель:** Полные `parse → render` интеграционные тесты для каждого из 4 поддерживаемых языков, покрывающие типы сущностей, не охваченные golden master regression suite.

### 6.1 `test_integration_cpp.py` — C++ специфика `[GAP-32-A]`

> **Файл:** `engine/tests/test_integration_cpp.py` *(CREATE)*
> **Fixture-данные:** C++ Doxygen XML (моделируются Python-утилитами MockAssetLoader)

- [ ] 🔴 **[Python]** Написать тест `test_cpp_category_landing_pages_exist` — `Classes/index.html` существует и содержит таблицу с описанием классов — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cpp_overload_dispatcher_page` — класс с `overloads` → создаётся страница overload dispatcher; **ВАЖНО (AW-04):** утверждение ОБЯЗАНО использовать специфичный assert — `overload_pages = [p for p in pages if "overload" in str(p).lower()]; assert len(overload_pages) > 0, "Страница overload dispatcher не найдена"`. Запрещено использовать `any(...or len(pages) > 0...)` — такое выражение всегда истинно и маскирует отсутствие dispatcher-страницы — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cpp_member_type_index_page` — `Fields, Structures and Enums/index.html` существует — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cpp_template_class_rendering` — шаблонный класс `MyClass<T, U>` рендерится с корректно экранированными угловыми скобками в HTML — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cpp_namespace_separator_double_colon` — fully qualified name использует `::` в prototypes и breadcrumbs — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[C++]** Создать XML-fixture для C++ с шаблонным классом, деструктором и перегруженными конструкторами (файл `engine/tests/assets/cpp_templates.xml` — источник данных в формате Doxygen XML) — _C++ native XML fixture embeds template/destructor syntax that cannot be represented in other host languages._
- [ ] 🟡 **[Python]** Написать тест `test_cpp_destructor_rendering` — деструктор `~MyClass()` присутствует в output — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_cpp_global_functions_flat_rendered` — глобальные функции (не в пространстве имён) рендерятся у корня сайдбара — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 6.2 `test_integration_cs.py` — C# специфика `[GAP-32-B]`

> **Файл:** `engine/tests/test_integration_cs.py` *(CREATE)*

- [ ] 🔴 **[Python]** Написать тест `test_cs_interface_entity_rendering` — `entity_type == "interface"` → ключевое слово `interface` в prototype HTML — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cs_delegate_entity_rendering` — `entity_type` содержит delegate → страница создаётся — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cs_event_member_rendering` — event-члены присутствуют в секции memberlist — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cs_namespace_index_page` — `<Namespace>/index.html` существует с таблицей классов — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_cs_dot_separator_in_fqn` — fully qualified name использует `.` (не `::`) в prototypes и breadcrumbs — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[C#]** Создать XML-fixture для C# с `<compounddef kind="interface">` и `<memberdef kind="event">` (файл `engine/tests/assets/cs_interface.xml`) — _C# native XML fixture provides interface/delegate/event nodes for language-specific parser validation._
- [ ] 🟡 **[Python]** Написать тест `test_cs_property_getter_setter_rendering` — свойства с `get`/`set` корректно помечены в output — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_cs_indexer_rendering` — индексаторы (`this[int index]`) представлены в members-секции — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 6.3 `test_integration_java.py` — Java специфика `[GAP-32-C]`

> **Файл:** `engine/tests/test_integration_java.py` *(CREATE)*

- [ ] 🔴 **[Python]** Написать тест `test_java_extends_implements_in_prototype` — `base_class` рендерится в секции prototype класса — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_java_package_index_page` — package root `index.html` содержит таблицу классов пакета — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_java_interface_rendering` — Java interface корректно рендерится с ключевым словом `interface` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_java_annotation_type_rendering` — аннотации (`@interface`) присутствуют в output — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_java_dot_separator_in_fqn` — fully qualified name использует `.` для Java — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Java]** Создать XML-fixture для Java с `<basecompoundref>` и implements-связями (файл `engine/tests/assets/java_inheritance.xml`) — _Java native XML fixture includes inheritance and annotation nodes required for complete parser coverage._
- [ ] 🟡 **[Python]** Написать тест `test_java_enum_rendering` — Java enum с константами → EnumModel корректно отображается — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Написать тест `test_java_nested_class_rendering` — вложенные классы (`OuterClass.InnerClass`) корректно вложены в sidebar — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 6.4 `test_integration_py.py` — Python специфика `[GAP-32-D]`

> **Файл:** `engine/tests/test_integration_py.py` *(CREATE)*

- [ ] 🔴 **[Python]** Написать тест `test_py_fget_fset_property_rendering` — property-члены отображают `[get]`/`[set]` accessors в memberlist — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_py_dunder_methods_present` — `__init__`, `__repr__`, `__eq__` присутствуют в method-list (не отфильтрованы как приватные) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_py_swig_wrapper_fields_excluded` — SWIG-поля (`swigCPtr`, `Dispose()`) отсутствуют в output — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_py_sphinx_rst_docstring_normalized` — Sphinx/RST-style параметры (`:param`, `:type`, `:return:`) конвертируются в CommonMark Markdown — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_py_dot_separator_in_fqn` — Python fully qualified name использует `.` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Создать XML-fixture для Python с SWIG-враппером и `<memberdef kind="property">` (файл `engine/tests/assets/py_swig.xml`) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_py_class_variable_vs_instance_variable` — class-level и instance-level атрибуты разделены в output — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Написать тест `test_py_module_level_functions` — module-level функции (не методы класса) рендерятся корректно — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

**Верификация фазы 6:**
```powershell
poetry run pytest tests/test_integration_cpp.py tests/test_integration_cs.py tests/test_integration_java.py tests/test_integration_py.py -v --tb=short
# Ожидается: ≥ 20 новых тестов, все PASSED
poetry run pytest --cov=ude --cov-report=term-missing | Select-String "TOTAL"
# Ожидается: ≥ 98%
```

---

## Фаза 7 — Внешние интеграционные скрипты `[GAP-31]`

> **Статус аудита (2026-06-29):** Четыре скрипта уже реализованы и закоммичены в `Tests/`. Требуется только создание корневого агрегатора и написание тестов для существующих скриптов с корректными CLI-интерфейсами.

### 7.0 Существующие скрипты — подтверждение и тестирование

#### `Tests/run_regression_tests.py` ✅ СУЩЕСТВУЕТ

Трёхуровневый golden master regression runner; покрывает 12 проектов:

| Сюита | Проекты |
|-------|---------|
| FacetModeler | `facetmodeler_api_cpp`, `_cs`, `_java`, `_py` |
| BimNv | `bimnv_api_cpp`, `_cs`, `_java`, `_py` |
| Mock | `mock_api_cpp`, `_cs`, `_java`, `_py` |

- **L1:** XML baseline → parse → сравнение IR JSON моделей
- **L2:** IR baseline → render HTML → `filecmp.dircmp` vs html baseline (CRLF-нормализация)
- **L3:** IR baseline → render Hugo MD → сравнение с hugo_md baseline
- Флаг `UPDATE_BASELINES=1` для регенерации baseline
- Читает из: `Tests/baseline/xml/{id}/`, `Tests/baseline/ir/{id}.json.gz`, `Tests/baseline/html/{id}/`, `Tests/baseline/hugo_md/{id}/`

- [ ] 🔴 **[Python]** Запустить `python Tests/run_regression_tests.py` — убедиться что все L1/L2/L3 проходят для всех 12 проектов — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_run_regression_all_tiers_pass` — smoke: `subprocess.run(["python", "Tests/run_regression_tests.py"])` → exit code `0` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

#### `Tests/prepare_baseline.py` ✅ СУЩЕСТВУЕТ

Baseline preparation утилита; CLI: `python Tests/prepare_baseline.py --suite [facetmodeler|both|mock|all]`

- Патчит `DoxygenXmlCollector.cleanup` → сохраняет Doxygen XML в `Tests/baseline/xml/{id}/`
- Патчит `DoxygenXmlParser.parse` → сохраняет `.json.gz` IR и рендерит HTML и Hugo MD baselines
- Поддерживает сюиты: `facetmodeler` (4 lang), `both` (8 lang), `mock` (4 lang), `all` (12 lang)

- [ ] 🟡 **[Python]** Убедиться: `Tests/baseline/xml/facetmodeler_api_cpp/` содержит Doxygen XML-файлы (существующий baseline зафиксирован) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_prepare_baseline_mock_suite` — `--suite mock` создаёт `Tests/baseline/ir/mock_api_cpp.json.gz` и директорию `Tests/baseline/html/mock_api_cpp/` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 7.1 Аудит `verify_pages.py` — корректировка и тестирование

> **Файл:** `Tests/verify_pages.py` ✅ **УЖЕ СУЩЕСТВУЕТ**
>
> **ВАЖНО:** Этот скрипт верифицирует страницы **портала документации** (VitePress/Hugo user docs), а **НЕ** API-документацию, сгенерированную UDE. Его назначение и интерфейс отличаются от acceptance criteria в REQ-V2-09.

**Фактический интерфейс:**
```bash
python Tests/verify_pages.py \
  --local-dir <compiled_dist_dir>   # скомпилированный выходной каталог (VitePress dist/ или Hugo public/)
  --remote-url <base_url>           # ИЛИ базовый URL для проверки удалённого сайта
  --user-docs <sources_dir>         # директория с исходными MD-файлами (default: ./user-docs)
```

**Логика работы:**
- Сканирует `user-docs/docs/` (VitePress) и `hugo-site/content/` (Hugo) для поиска MD-подписей страниц
- Для каждой MD-страницы проверяет, что соответствующая скомпилированная HTML-страница существует и содержит ожидаемый контент
- Поддерживает как локальную проверку файловой системы, так и удалённую HTTP-проверку

**Расхождение с REQ-V2-09:** Acceptance criteria требуют `--output-dir` для проверки внутренних ссылок UDE-output — это другой инструмент. Для полного выполнения GAP-31 требуется уточнение: либо обновить требование под фактический интерфейс, либо реализовать отдельный `Tests/verify_ude_links.py`.

- [ ] 🔴 **[Python]** Написать тест `test_verify_pages_local_all_pages_found` — все MD-сигнатуры из `user-docs/docs/` найдены в скомпилированном каталоге → exit 0 — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_verify_pages_detects_missing_compiled_page` — один MD-файл не скомпилирован → exit 1 с именем файла в stderr — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_verify_pages_remote_mode` — mock HTTP GET; проверяет `--remote-url` + путь страницы → exit 0 на HTTP 200, exit 1 на HTTP 404 — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Уточнить с командой: нужен ли отдельный `Tests/verify_ude_links.py` с интерфейсом `--output-dir` для проверки внутренних ссылок UDE-generated HTML (расхождение с REQ-V2-09) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 7.2 Аудит `check_links.py` — корректировка и тестирование

> **Файл:** `Tests/check_links.py` ✅ **УЖЕ СУЩЕСТВУЕТ**
>
> **ВАЖНО:** Проверяет **скомпилированные HTML-файлы** на сломанные ссылки (и внутренние, и внешние HTTP). Расхождение с REQ-V2-09: требование указывает `--site-dir`, фактический CLI использует `--local-dir`.

**Фактический интерфейс:**
```bash
python Tests/check_links.py --local-dir <compiled_dist_dir>
```

**Логика работы:**
- Рекурсивно сканирует HTML-файлы в `--local-dir`
- **Внутренние ссылки** (`href="/path"`, `href="./relative"`): проверяет существование файла в файловой системе
- **Внешние ссылки** (`http://`, `https://`): HTTP HEAD/GET запрос (требует сети)
- Обрабатывает маршрутный префикс `ude-user-docs/api` (strip-логика для корректного резолвинга)

**Расхождение с REQ-V2-09:** `--site-dir` → фактически `--local-dir`. Необходимо обновить `integration_tests_specification.md`.

- [ ] 🔴 **[Python]** Написать тест `test_check_links_clean_site` — HTML-директория без broken links → exit 0 — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Написать тест `test_check_links_detects_broken_internal_link` — внутренняя ссылка ведёт в несуществующий файл → exit 1 с именем файла — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_check_links_detects_broken_external_link` — mock `requests`/`urllib`; ссылка возвращает 404 → exit 1 — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_check_links_ude_prefix_strip` — ссылка с `/ude-user-docs/api/...` prefix корректно резолвируется после strip — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 7.3 Корневой агрегатор интеграционных тестов

> **Файлы:** `Tests/run_all_integration_tests.sh` / `.bat` *(CREATE — единственные скрипты GAP-31, ещё не существующие)*

- [ ] 🔴 **[VB]** Создать `Tests/run_all_integration_tests.bat` — агрегирует exit codes (основной скрипт для Windows) — _VBScript replaces batch file logic with structured Windows automation and correct error propagation._:
  1. `python Tests/run_regression_tests.py` — 3-tier regression (12 проектов)
  2. `pytest engine/tests/test_docomatic_alignment.py -v`
  3. `python Tests/verify_pages.py --local-dir user-docs/.vitepress/dist --user-docs user-docs/`
  4. `python Tests/check_links.py --local-dir user-docs/.vitepress/dist`
  5. Exit 0 только если все предыдущие вернули 0; проверка через `%ERRORLEVEL%`
- [ ] 🟡 **[Python]** Создать `Tests/run_all_integration_tests.sh` — аналог для CI (Linux) / Git Bash — _Python provides portable cross-platform scripting to replace CI-specific shell commands._
- [ ] 🟡 **[Python]** Обновить `design-docs/docs/srs/integration_tests_specification.md` — указать корректные CLI: `verify_pages.py --local-dir` (не `--output-dir`), `check_links.py --local-dir` (не `--site-dir`) — _Python provides portable cross-platform scripting to replace CI-specific shell commands._

#### Обязательные требования безопасности скрипта-агрегатора (AW-05)

> **Источник:** `skills_compliance_report.md` AW-05 · `task_verification.md` Safety & Guard Rails criterion  
> Скрипт `run_all_integration_tests.bat` требует специальной реализации для предотвращения мутации CWD и молчаливого пропуска шагов при ошибках.

- [ ] 🔴 **[VB]** Использовать `pushd engine` / `popd` вместо `cd engine &&` — обеспечивает восстановление CWD даже при сбое дочернего шага — _VBScript replaces batch file logic with structured Windows automation and correct error propagation._:
  ```bat
  pushd engine
  if errorlevel 1 (echo ОШИБКА: не удалось перейти в engine & exit /b 1)
  poetry run pytest tests/ --cov=ude --cov-fail-under=98 --tb=short
  set STEP_EXIT=%ERRORLEVEL%
  popd
  if %STEP_EXIT% neq 0 exit /b %STEP_EXIT%
  ```
- [ ] 🔴 **[VB]** Принимать путь выходной директории как параметр `%1` вместо хардкода `ude_output\bimnv_api_cpp` — хардкод привязывает скрипт к конкретному проекту и ломается при изменении имён — _VBScript replaces batch file logic with structured Windows automation and correct error propagation._:
  ```bat
  set OUTPUT_DIR=%~1
  if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=ude_output
  if not exist "%OUTPUT_DIR%" (
      echo ОШИБКА AW-05: директория "%OUTPUT_DIR%" не существует
      exit /b 1
  )
  ```
- [ ] 🔴 **[VB]** Валидировать существование скриптов `Tests/run_regression_tests.py`, `Tests/verify_pages.py`, `Tests/check_links.py` ДО начала выполнения — не допускать молчаливого пропуска при GAP-31 незавершённом — _VBScript replaces batch file logic with structured Windows automation and correct error propagation._:
  ```bat
  for %%F in (Tests\run_regression_tests.py Tests\verify_pages.py Tests\check_links.py) do (
      if not exist "%%F" (echo ОШИБКА AW-05: %%F не найден — GAP-31 не завершён & exit /b 1)
  )
  ```
- [ ] 🟡 **[Python]** Применить аналогичные защиты в `.sh`-версии: использовать `cd engine && trap 'cd ..' EXIT` для гарантированного возврата CWD, принимать пути как `$1` аргумент — _Python provides portable cross-platform scripting to replace CI-specific shell commands._

**Верификация фазы 7:**
```powershell
# Regression suite (уже работает)
python Tests/run_regression_tests.py
# Ожидается: exit 0, все L1/L2/L3 PASSED для 12 проектов

# Portal page verification (фактический интерфейс)
python Tests/verify_pages.py --local-dir user-docs/.vitepress/dist --user-docs user-docs/
# Ожидается: exit 0

# Link checking (фактический интерфейс)
python Tests/check_links.py --local-dir user-docs/.vitepress/dist
# Ожидается: exit 0

# Full integration suite
.\Tests\run_all_integration_tests.bat
# Ожидается: exit 0
```

---

## Фаза 8 — Производительность, нагрузка и регрессионные тесты

### 8.1 Performance Benchmark

> **Файл:** `engine/tests/test_performance_benchmark.py` *(MODIFY)*

- [ ] 🟡 **[Python]** Убедиться: существующий benchmark тестирует 1000 API-классов за < 5 s (качественный показатель из BRD) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить параметризованный тест производительности по языкам: C++, C#, Java, Python — каждый с 250 классами × 4 языка = 1000 общих — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить тест `test_benchmark_with_l2_cache_second_run` — второй прогон с L2 cache > 3× быстрее первого — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Добавить тест `test_benchmark_large_class_many_methods` — класс с 200+ методами рендерится корректно (без truncation) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 8.2 Golden Master Regression Suite `[TSK-TST-01]`

> **Файл:** `engine/tests/test_golden_master.py` *(MODIFY)*

- [ ] 🔴 **[Python]** После GAP-03 (typed IR): регенерировать baseline — **ВАЖНО (AW-02): использовать обе формы команды в зависимости от ОС** — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._:
  ```bash
  # Linux / macOS / CI (GitHub Actions ubuntu-latest):
  UPDATE_GOLDEN=1 poetry run pytest tests/test_golden_master.py -v
  ```
  ```powershell
  # Windows PowerShell (основная рабочая среда проекта):
  $env:UPDATE_GOLDEN = "1"; poetry run pytest tests/test_golden_master.py -v
  ```
  Запускать только после подтверждения `git diff --stat` — убедиться что изменения baseline осмысленны
- [ ] 🔴 **[Python]** После регенерации: verify clean run `poetry run pytest tests/test_golden_master.py -v` → все PASSED — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🔴 **[Python]** Убедиться: golden master покрывает все 16 конкретных рендереров (4 языка × 2 вывода × 2 варианта = 16) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить тест `test_golden_master_html_legacy_cpp` — LegacyHtmlRenderer C++ vs baseline — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить тест `test_golden_master_hugo_legacy_java` — LegacyHugoMarkdownRenderer Java vs baseline — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Проверить: `PIPELINE_COMPLEXES` registry содержит все 16 renderer/parser complexes — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 8.3 Doc-o-matic Scraper и TOC Recovery Tests

> Инструменты для reverse-engineering Docomatic semantics. Язык: Python.

- [ ] 🟡 **[Python]** Проверить наличие `Tests/docomatic_scraper.py` — если отсутствует, реализовать согласно SOP `skills/docomatic_semantics_analysis.md` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._:
  - CLI флаги: `--language`, `--folders`, `--output-dir`, `--dry-run`
  - Сканирует `!!` prefix-файлы; выводит `entity_types`, `filename_prefixes`, `member_types`, `total_files_scanned`
- [ ] 🟡 **[Python]** Написать тест `test_scraper_dry_run_output_valid_json` — `--dry-run` → stdout валидный JSON с ключами `entity_types`, `filename_prefixes` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_scraper_detects_cpp_overload_patterns` — C++ папки → `!!OVERLOADED_` паттерны детектируются — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Написать тест `test_scraper_optionality_threshold` — тип сущности, отсутствующий в ≥ 50% папок, помечается как OPTIONAL — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

---

## Фаза 9 — Тесты специфичных граничных случаев миграции

> **Цель:** Покрытие edge cases, уникальных для перехода от Doc-o-matic к UDE, включая языковые особенности которые могут привести к silent data loss.

### 9.1 Граничные случаи C++ парсинга

> **Файл:** `engine/tests/test_edge_cases_cpp.py` *(CREATE)*

- [ ] 🟡 **[Python]** Написать тест `test_cpp_nested_templates_parsing` — `map<string, vector<pair<int, double>>>` корректно экранируется в HTML — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_cpp_anonymous_namespace_handling` — анонимные пространства имён не вызывают KeyError — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_cpp_export_macro_filtered` — `NWDBEXPORT`/`ODA_EXPORT` макросы отфильтровываются из сигнатур — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_cpp_constructor_destructor_ordering` — конструктор и деструктор располагаются первыми в member list — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[C++]** Создать XML-fixture `engine/tests/assets/cpp_edge_cases.xml` с шаблонными вложениями, анонимными namespace и export-макросами — _C++ native XML fixture embeds template/destructor syntax that cannot be represented in other host languages._

### 9.2 Граничные случаи C# парсинга

> **Файл:** `engine/tests/test_edge_cases_cs.py` *(CREATE)*

- [ ] 🟡 **[Python]** Написать тест `test_cs_generic_type_rendering` — `List<T>`, `Dictionary<TKey, TValue>` корректно рендерятся — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_cs_extension_method_rendering` — extension methods корректно идентифицируются — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_cs_nullable_type_rendering` — `string?`, `int?` корректно в HTML — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[C#]** Создать XML-fixture `engine/tests/assets/cs_edge_cases.xml` с дженериками и nullable типами — _C# native XML fixture provides interface/delegate/event nodes for language-specific parser validation._

### 9.3 Граничные случаи Java парсинга

> **Файл:** `engine/tests/test_edge_cases_java.py` *(CREATE)*

- [ ] 🟡 **[Python]** Написать тест `test_java_generics_rendering` — `Collection<? extends T>` wildcard generics корректно рендерятся — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_java_varargs_rendering` — varargs (`String... args`) корректно в сигнатурах — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Java]** Создать XML-fixture `engine/tests/assets/java_edge_cases.xml` с generics и varargs — _Java native XML fixture includes inheritance and annotation nodes required for complete parser coverage._

### 9.4 Тесты обратной совместимости Legacy рендереров

> **Файл:** `engine/tests/test_legacy_compatibility.py` *(CREATE)*

- [ ] 🟡 **[Python]** Написать тест `test_legacy_html_output_matches_docomatic_naming` — legacy HTML файлы именуются по Docomatic-конвенции (`!!MEMBERTYPE_Methods_ClassName`) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Написать тест `test_legacy_hugo_sidebar_matches_html_sidebar` — legacy Hugo и legacy HTML sidebar имеют идентичную структуру (те же узлы) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Delphi]** Создать baseline-генератор `Tests/generate_docomatic_baseline.dpr` (Delphi-утилита для воспроизведения Doc-o-matic naming conventions при создании reference data — актуально, если оригинальные Doc-o-matic HTML недоступны) — _Delphi reproduces Doc-o-matic naming conventions to generate authoritative legacy reference baselines._
- [ ] 🟢 **[VB]** Написать `Tests/generate_legacy_toc.vbs` — VBScript-генератор legacy `contents.html` структуры на основе списка классов (для создания тестовых baseline данных без запуска Doc-o-matic) — _VBScript generates legacy contents.html tree structures matching Doc-o-matic output format exactly._

---

## Фаза 10 — CI/CD тест-инфраструктура

### 10.1 Автоматизация тест-запусков в GitHub Actions

- [ ] 🔴 **[Python]** Добавить job `engine-tests` в `integration_tests.yml` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._:
  ```yaml
  - name: Run Engine Tests
    run: poetry run pytest engine/tests/ --cov=ude --cov-fail-under=98 --tb=short
  ```
- [ ] 🟡 **[Python]** Добавить CI-step для per-language integration tests: `pytest tests/test_integration_*.py -v` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить CI-step для Docomatic alignment: `pytest engine/tests/test_docomatic_alignment.py -v` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟡 **[Python]** Добавить CI-step для Entity Completeness: `pytest engine/tests/test_entity_completeness.py -v` — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Артефакт: upload coverage HTML report при failure (retention 7 дней) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._
- [ ] 🟢 **[Python]** Артефакт: upload `difference_mock_sdk_*.json` из alignment suite при failure — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._

### 10.2 Pydantic Migration Guard

- [ ] 🔴 **[Python]** Создать `scripts/pydantic_guard.ps1` — скрипт для блокировки dict-паттернов (`entity["fields"]`) вместо Pydantic-доступа (`entity.fields`) в рендерерах (локальный запуск на Windows) — _Python provides portable grep/audit automation replacing Windows-only PowerShell scripts._
- [ ] 🟡 **[Python]** Создать `scripts/pydantic_guard.sh` — аналог для CI (GitHub Actions / Linux) — _Python provides portable cross-platform scripting to replace CI-specific shell commands._
- [ ] 🟡 **[Python]** Добавить step в `generate-api-ref.yml` после GAP-03 (CI runner — Linux) — _pytest fixtures enable isolated, parametric testing of UDE pipeline components._:
  ```yaml
  - name: Pydantic Migration Guard
    run: bash scripts/pydantic_guard.sh
  ```

---

## Сводная матрица пробелов в тестировании

| Категория | Существующих тестов v1.0 | Новых тестов (план) | Языки реализации |
|-----------|-------------------------|---------------------|-----------------|
| GlobalConfig & Logging | 0 | 17 | Python |
| Doxyfile 3-tier merge | 0 | 11 | Python |
| L2 Render Cache | 4 (L1 only) | 11 | Python |
| Orchestrator Public API | 0 | 11 | Python |
| CLI Subcommands | 0 | 11 | Python |
| Typed IR (7 models) | 8 (v1.0 schema) | 12 | Python |
| Coverage Gate | 0 | 9 | Python |
| Entity Completeness | 0 | 13 (критично!) | Python |
| Page Structure Integrity | 0 | 6 | Python |
| C++ Integration Tests | 5 (golden master) | 8 | Python + C++ fixtures |
| C# Integration Tests | 5 (golden master) | 8 | Python + C# fixtures |
| Java Integration Tests | 5 (golden master) | 7 | Python + Java fixtures |
| Python Integration Tests | 5 (golden master) | 7 | Python |
| run_regression_tests.py (✅ существует) | 0 | 2 | Python |
| prepare_baseline.py (✅ существует) | 0 | 2 | Python |
| verify_pages.py (✅ существует, иной интерфейс) | 0 | 4 | Python |
| check_links.py (✅ существует, иной интерфейс) | 0 | 4 | Python |
| Docomatic Scraper | 0 | 3 | Python |
| Edge Cases C++ | 0 | 5 | Python + C++ fixtures |
| Edge Cases C# | 0 | 3 | Python + C# fixtures |
| Edge Cases Java | 0 | 3 | Python + Java fixtures |
| Legacy Compatibility | 0 | 2 | Python + Delphi/VB |
| Performance & Benchmark | 1 | 3 | Python |
| **ИТОГО новых тестов** | — | **≥ 162** | **Преимущественно Python** |

---

## Хронологический порядок выполнения

```
Фаза 0: Baseline (≤1 день)
    │
Фаза 1: Рефакторинг существующих тестов (≤1 день)
    │
Фаза 2: Инфраструктурные тесты v2.0 (параллельно с GAP-09→GAP-11)
    │
Фаза 3: CLI & Orchestrator тесты (параллельно с GAP-05→GAP-01)
    │
Фаза 4: Typed IR & Coverage Gate тесты (параллельно с GAP-03→GAP-10)
    │
    ├──► Фаза 5: Entity Completeness (КРИТИЧНО — параллельно с Фазой 4)
    │
    ├──► Фаза 6: Per-language Integration (параллельно с GAP-32)
    │
    ├──► Фаза 7: Внешние скрипты (параллельно с GAP-31)
    │
Фаза 8: Performance & Golden Master регенерация
    │
Фаза 9: Edge Cases (после завершения парсеров)
    │
Фаза 10: CI/CD интеграция (финальный gate)
```

---

## Критерии приёмки всего тест-плана (Definition of Done)

| Критерий | Проверка |
|----------|----------|
| ≥ 98% statement coverage | `poetry run pytest --cov=ude --cov-report=term-missing \| Select-String "TOTAL"` |
| 0 failed тестов | `poetry run pytest engine/tests/ -v \| Select-String "PASSED\|FAILED\|ERROR"` |
| Entity completeness 100% | `pytest tests/test_entity_completeness.py -v` — все PASSED |
| Golden Master stable | `pytest tests/test_golden_master.py -v` — все PASSED |
| Docomatic alignment stable | `total_differences` не выше pre-v2.0 baseline для C++, C#, Java |
| Performance gate | `pytest tests/test_performance_benchmark.py` — ≤ 5s для 1000 классов |
| Backward compat | `ude --doc-config X` byte-identical vs `ude compile --doc-config X` |
| IR compatibility | `load_compressed_ir(v1_file)` не бросает исключений |
| Git hygiene | `git status --short` — нет `*.html`/`*.md` output-файлов |

---

> **Статус:** Документ создан 2026-06-29. Фаза 7 исправлена 2026-06-29 по результатам аудита `Tests/`.
> **Аудит фазы 7:** Обнаружено, что `verify_pages.py`, `check_links.py`, `run_regression_tests.py`, `prepare_baseline.py` уже существуют и полностью реализованы. Описания и CLI-интерфейсы в плане исправлены.
> **Следующий шаг:** Фаза 0 (верификация baseline) → Фазы 1–2 (параллельно с началом реализации GAP-09).
> **Приоритет:** Фаза 5 (Entity Completeness) — наивысший риск для качества миграции.
> **Ответственный:** pavel.sokolov@opendesign.com