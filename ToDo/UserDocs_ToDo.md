# UserDocs — Backlog улучшений пользовательской документации

> **Роль:** Principal DevOps Architect · Lead Technical Writer · Developer Portfolio Consultant  
> **Дата аудита:** 2026-06-28  
> **Источники:** `user-docs/docs/` (12 файлов), `index.md`, `admin-deployment.md`, v2.0 roadmap

---

## 1. Анализ текущей структуры

### 1.1 Текущий состав (VitePress portal, `user-docs/docs/`)

```
user-docs/
├── index.md                    # Лендинг (hero + 3 features)
└── docs/                       # Плоская структура — 12 файлов
    ├── chapter1-quick-start.md     # Индексная страница Ch.1
    ├── getting-started.md          # Установка, pipeline-концепт, Hello World
    ├── first-config.md             # ude_config.json
    ├── chapter2-coding-standards.md # Индексная страница Ch.2
    ├── commenting-rules.md         # Комментирование кода
    ├── exclusion-gates.md          # Фильтры исключений
    ├── chapter3-config-reference.md # Индексная страница Ch.3
    ├── global-settings.md          # ude_global_config.json
    ├── target-settings.md          # ude_doc_config.json
    ├── chapter4-case-study.md      # Индексная страница Ch.4
    ├── case-study.md               # ? Дублирует chapter4 или standalone?
    └── admin-deployment.md         # CI/CD деплой
```

### 1.2 Выявленные проблемы

| # | Проблема | Приоритет |
|---|---|---|
| P1 | Плоская структура — все 12 файлов в одной папке, без субдиректорий | 🔴 |
| P2 | `case-study.md` и `chapter4-case-study.md` — возможный дубликат | 🔴 |
| P3 | `admin-deployment.md` ссылается на несуществующий `deploy.yml` (в umbrella его нет, он в сабмодулях) | 🔴 |
| P4 | Нет документации по архитектуре трёх CI/CD пайплайнов (Pipeline #1/#2/#3) | 🔴 |
| P5 | Нет CLI-справочника (v2.0 вводит 4 сабкоманды: `compile`, `parse`, `render`, `audit`) | 🟡 |
| P6 | Нет руководства по миграции v1.0 → v2.0 (Breaking Changes) | 🟡 |
| P7 | Нет Changelog / Release Notes | 🟡 |
| P8 | Нет Troubleshooting-раздела | 🟡 |
| P9 | Нет раздела «Для контрибуторов» — важно для портфолио | 🟢 |
| P10 | Лендинговая страница не раскрывает ключевые метрики (98% coverage, <5s, 4 языка) | 🟢 |
| P11 | Нет документации по `ude audit` и Documentation Coverage Gate (v2.0) | 🟡 |
| P12 | Нет описания repository_dispatch механизма (как сабмодули триггерят umbrella CI) | 🔴 |

---

## 2. Целевая структура (v2.0-ready)

```
user-docs/
├── index.md                        # Лендинг (обновить — добавить метрики)
└── docs/
    ├── quickstart/
    │   ├── index.md                # "Глава 1: Быстрый старт" (оглавление)
    │   ├── getting-started.md      # Установка, pipeline, Hello World
    │   ├── first-config.md         # ude_doc_config.json — первый таргет
    │   └── troubleshooting.md      # NEW: типичные ошибки и решения
    ├── standards/
    │   ├── index.md                # "Глава 2: Стандарты комментирования"
    │   ├── commenting-rules.md     # Форматы: Doxygen, Javadoc, Google, Sphinx
    │   └── exclusion-gates.md      # DOM-IGNORE, cond, internal
    ├── reference/
    │   ├── index.md                # "Глава 3: Справочник конфигурации"
    │   ├── global-settings.md      # ude_global_config.json (все поля)
    │   ├── target-settings.md      # ude_doc_config.json (все поля)
    │   └── cli-reference.md        # NEW: ude compile/parse/render/audit
    ├── deployment/
    │   ├── index.md                # "Глава 4: Деплой и CI/CD"
    │   ├── admin-deployment.md     # Установка в enterprise CI (исправить)
    │   ├── cicd-pipelines.md       # NEW: архитектура трёх пайплайнов
    │   └── repository-dispatch.md  # NEW: механизм кросс-репо триггеров
    ├── case-study/
    │   ├── index.md                # "Глава 5: Case Study"
    │   └── oda-integration.md      # Реальный пример: ODA SDK + UDE
    └── changelog.md                # NEW: Release Notes v1.0 / v2.0
```

---

## 3. Backlog (атомарные задачи с чекбоксами)

### 3.1 Структурные исправления (P1–P3)

- [ ] **[STRUCT-01]** Создать субдиректории `quickstart/`, `standards/`, `reference/`, `deployment/`, `case-study/` в `user-docs/docs/`
- [ ] **[STRUCT-02]** Переместить `getting-started.md` и `first-config.md` в `docs/quickstart/`
- [ ] **[STRUCT-03]** Создать `docs/quickstart/index.md` как оглавление главы 1
- [ ] **[STRUCT-04]** Переместить `commenting-rules.md` и `exclusion-gates.md` в `docs/standards/`
- [ ] **[STRUCT-05]** Создать `docs/standards/index.md` как оглавление главы 2
- [ ] **[STRUCT-06]** Переместить `global-settings.md` и `target-settings.md` в `docs/reference/`
- [ ] **[STRUCT-07]** Создать `docs/reference/index.md` как оглавление главы 3
- [ ] **[STRUCT-08]** Создать `docs/deployment/` и переместить туда `admin-deployment.md`
- [ ] **[STRUCT-09]** Выяснить статус `case-study.md` vs `chapter4-case-study.md` — удалить дубликат или объединить
- [ ] **[STRUCT-10]** Обновить сайдбар VitePress (`docs/.vitepress/config.ts`) под новую иерархию
- [ ] **[STRUCT-11]** Проверить и обновить все относительные ссылки после перемещения файлов

### 3.2 Исправление `admin-deployment.md` (P3)

- [ ] **[ADMIN-01]** Убрать ссылку на `deploy.yml` в umbrella-репозитории — он не существует в `Pipeline/.github/`
- [ ] **[ADMIN-02]** Добавить пояснение: деплой выполняется воркфлоу в каждом сабмодуле (`design-docs`, `engine`, `user-docs`) независимо
- [ ] **[ADMIN-03]** Добавить актуальные шаги воркфлоу из `integration_tests.yml` (checkout с сабмодулями, Python 3.11, doxygen, Hugo, VitePress npm build, UDE compile, Hugo compile)
- [ ] **[ADMIN-04]** Добавить таблицу используемых секретов: `PIPELINE_GITHUB_TOKEN` — назначение, минимальные права (`repo`, `workflow`)
- [ ] **[ADMIN-05]** Описать симлинк `user-docs/engine → ../engine`, создаваемый в CI для совместимости путей на Linux

### 3.3 Новые разделы: CI/CD и пайплайны (P4, P12)

- [ ] **[CICD-01]** Создать `docs/deployment/cicd-pipelines.md` — обзор трёх пайплайнов
- [ ] **[CICD-02]** Документировать Pipeline #1 (design-docs → Docusaurus): триггер, артефакт, Cloudflare Pages
- [ ] **[CICD-03]** Документировать Pipeline #2 (user-docs → VitePress + Hugo): триггер, артефакт, деплой
- [ ] **[CICD-04]** Документировать Pipeline #3 (engine → UDE API reference): триггер — коммит в engine; артефакт — Hugo Markdown → встраивается в VitePress dist
- [ ] **[CICD-05]** Создать `docs/deployment/repository-dispatch.md` — как сабмодули отправляют `trigger-integration-tests` в umbrella-репо
- [ ] **[CICD-06]** Документировать шаг `verify_pages.py` в CI: что проверяет, как интерпретировать ошибки, GAP-31 статус
- [ ] **[CICD-07]** Добавить диаграмму (Mermaid) потока кросс-репо событий: submodule push → repository_dispatch → umbrella CI → verify

### 3.4 CLI-справочник для v2.0 (P5)

- [ ] **[CLI-01]** Создать `docs/reference/cli-reference.md`
- [ ] **[CLI-02]** Задокументировать плоский v1.0 интерфейс: `ude --global-config --sdk-config --doc-config` (backward compat)
- [ ] **[CLI-03]** Задокументировать сабкоманду `ude compile` — аргументы, примеры, exit-коды
- [ ] **[CLI-04]** Задокументировать сабкоманду `ude parse --output-ir` — формат JSON summary на stdout, формат IR-файла
- [ ] **[CLI-05]** Задокументировать сабкоманду `ude render --input-ir` — разделённый pipeline (parse + render = compile)
- [ ] **[CLI-06]** Задокументировать сабкоманду `ude audit` — режимы `reject-undocumented` / `allow-undocumented`, формат coverage-таблицы
- [ ] **[CLI-07]** Добавить таблицу exit-кодов: 0 (success), 1 (error), 2 (audit stub / not implemented)
- [ ] **[CLI-08]** Добавить примеры использования `ude parse` + `ude render` как конвейер

### 3.5 Руководство по миграции v1.0 → v2.0 (P6)

- [ ] **[MIG-01]** Создать `docs/reference/migration-v2.md` или раздел внутри changelog
- [ ] **[MIG-02]** Задокументировать Breaking Change: IR-схема `ClassEntity` → 7 typed Pydantic models
- [ ] **[MIG-03]** Задокументировать Breaking Change: `ProjectCatalog` — новые поля `project_name`, `version`
- [ ] **[MIG-04]** Задокументировать Breaking Change: CLI subcommands (backward compat сохраняется)
- [ ] **[MIG-05]** Задокументировать Breaking Change: `GlobalConfig` — активация всех полей, новая схема
- [ ] **[MIG-06]** Задокументировать: `fields: List[str]` → `fields: List[VariableModel]` — что нужно обновить в кастомных шаблонах
- [ ] **[MIG-07]** Добавить чеклист для пользователей: что нужно проверить при переходе на v2.0

### 3.6 Changelog / Release Notes (P7)

- [ ] **[CLOG-01]** Создать `docs/changelog.md` с записями v1.0 и v2.0
- [ ] **[CLOG-02]** Задокументировать v1.0 MVP: что реализовано (4 языка, 16 рендереров, CLI, кэш, Hugo + HTML вывод)
- [ ] **[CLOG-03]** Задокументировать v2.0: Breaking Changes + новые фичи (subcommands, typed IR, coverage gate, logging)
- [ ] **[CLOG-04]** Добавить раздел «Запланировано в v3.0+» со ссылкой на roadmap

### 3.7 Troubleshooting (P8)

- [ ] **[TRB-01]** Создать `docs/quickstart/troubleshooting.md`
- [ ] **[TRB-02]** Описать ошибку: Doxygen не найден в PATH — диагностика и решение
- [ ] **[TRB-03]** Описать ошибку: `FileNotFoundError` для `ude_global_config.json` — что проверить
- [ ] **[TRB-04]** Описать ошибку: `ValidationError` при загрузке конфига — как читать Pydantic-ошибки
- [ ] **[TRB-05]** Описать ошибку: `RendererError` — отсутствие шаблонов (strict mode с v2.0)
- [ ] **[TRB-06]** Описать проблему с симлинком в CI (Linux): `user-docs/engine` — как и когда создаётся
- [ ] **[TRB-07]** Добавить раздел «Проверка сред перед запуском»: Python 3.11+, Doxygen, Hugo version

### 3.8 Portfolio & Showcase улучшения (P10)

- [ ] **[PORT-01]** Обновить лендинг `index.md`: добавить ключевые метрики в блоке features — `<5s для 1000 entities`, `98% покрытие тестами`, `4 языка`, `12 интеграционных тестов`
- [ ] **[PORT-02]** Добавить на лендинг badges: GitHub Actions status, Python version, coverage
- [ ] **[PORT-03]** Добавить раздел «Architecture» с Mermaid-диаграммой трёхуровневого pipeline (Collector → Parser → Renderer)
- [ ] **[PORT-04]** Добавить страницу «Об авторе / Контрибуторство» — для portfolio visibility
- [ ] **[PORT-05]** В `getting-started.md` обновить «Expected Output» — убрать `[INFO]`-логи в старом формате, заменить реальным форматом v2.0 (`%(levelname)s [%(name)s] %(message)s`)
- [ ] **[PORT-06]** Добавить раздел «Production Use Case» — реальный пример: ODA SDK (C++/C#/Java/Python), 13 продуктов, `ude_projects/`

### 3.9 Документация Documentation Coverage Gate (P11)

- [ ] **[AUDIT-01]** Задокументировать `GlobalConfig.coverage_mode`: `reject-undocumented` vs `allow-undocumented`
- [ ] **[AUDIT-02]** Задокументировать `GlobalConfig.coverage_threshold`: диапазон 0.0–1.0, дефолт 1.0
- [ ] **[AUDIT-03]** Описать формат coverage-таблицы: `| class | method | overall |` — как читать
- [ ] **[AUDIT-04]** Показать пример интеграции `ude audit` в CI/CD: step в GitHub Actions
- [ ] **[AUDIT-05]** Описать exit-коды `ude audit`: 0 (pass/allow-mode), 2 (fail/reject-mode)

---

### 3.10 Документация конфигурации `sidebar.toml` (v2.0 Breaking Change)

> **Источник:** memory `project_sidebar_toml.md` · `CICD_ToDo.md` §4.2  
> **Контекст:** В v2.0 управление боковой панелью переведено с per-language JSON template-конфигов на `sidebar.toml`; `BaseRenderer` получил новый метод `_load_static_file_from_path()`. Это Breaking Change, требующий документации для пользователей, кастомизирующих UDE-порталы.

- [ ] **[TOML-01]** Создать `docs/reference/sidebar-config.md` — справочник формата `sidebar.toml`: структура секций `[[sidebar]]`, поддерживаемые поля, обязательные и опциональные ключи, примеры минимальной и расширенной конфигурации с использованием поля `source_file` для подключения статических страниц
- [ ] **[TOML-02]** Документировать 3-way deep_merge cascade в `sidebar.toml`: глобальный конфиг (global) → SDK-конфиг (sdk) → документ-конфиг (doc); объяснить, что doc-конфиг всегда имеет наивысший приоритет; привести пример слияния трёх уровней с показом итогового результата
- [ ] **[TOML-03]** Документировать оба режима поведения при отсутствии `sidebar.toml`: graceful fallback через `_load_sidebar_toml_graceful()` (возвращает `{}`, сайдбар формируется по умолчанию) и strict-режим (бросает `UdeException`); указать, как переключиться между режимами и когда каждый из них применяется
- [ ] **[TOML-04]** Добавить раздел «Миграция JSON → TOML» в `docs/reference/migration-v2.md` или в `sidebar-config.md`: пошаговый чеклист для пользователей, переходящих с per-language JSON template-конфигов на `sidebar.toml`; сравнительная таблица: старый JSON-формат vs новый TOML-формат

---

## 4. Итоговая таблица приоритетов

| # | Блок | Задач | Приоритет |
|---|---|---|---|
| 3.1 | Структурные исправления | 11 | 🔴 Срочно |
| 3.2 | Исправление admin-deployment | 5 | 🔴 Срочно |
| 3.3 | CI/CD и пайплайны | 7 | 🔴 Срочно |
| 3.4 | CLI-справочник v2.0 | 8 | 🟡 v2.0 |
| 3.5 | Миграция v1.0 → v2.0 | 7 | 🟡 v2.0 |
| 3.6 | Changelog | 4 | 🟡 v2.0 |
| 3.7 | Troubleshooting | 7 | 🟢 Желательно |
| 3.8 | Portfolio/Showcase | 6 | 🟢 Желательно |
| 3.9 | Coverage Gate | 5 | 🟡 v2.0 |
| 3.10 | sidebar.toml конфигурация (v2.0) | 4 | 🟡 v2.0 |
| **Итого** | | **64** | |
