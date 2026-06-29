# DocReqs — Backlog требований к технической документации

> **Роль:** Principal DevOps Architect · Lead Technical Writer  
> **Дата аудита:** 2026-06-28  
> **Источники:** `design-docs/docs/srs/`, `.antigravitycli/styles/`, `requirements_v2_next.md`, `user-docs/docs/`

---

## 1. Действующие требования к документации (статус: применяются сейчас)

### 1.1 Технические требования к коду (из `.antigravitycli/styles/`)

| ID | Требование | Источник |
|---|---|---|
| DR-CUR-01 | Все комментарии и docstrings в коде — строго на **английском языке** | `code_style.md` |
| DR-CUR-02 | Coverage gate: ≥ **98%** statement coverage после каждого commit boundary | `testing_style.md` |
| DR-CUR-03 | TDD: Red → Green → Refactor для каждой атомарной задачи | `testing_style.md` |
| DR-CUR-04 | Двунаправленная трассировка: `GAP-XX` → `TASK-<Phase>.<Group>.<Seq>` | `requirements_audit.md` |
| DR-CUR-05 | Commit messages строго в формате `feat/fix/refactor/test/docs(scope): description` | `git_style.md` |
| DR-CUR-06 | Каждый `TASK-*.md` содержит: Code Architecture, Technical Gotchas, Acceptance Criteria, Commit Boundary | `tasks/*.md` |

### 1.2 Требования к проектной документации (BRD/SRS/SDD)

| ID | Требование | Источник |
|---|---|---|
| DR-CUR-07 | Трёхуровневая иерархия: BRD → SRS → SDD (каждый уровень ссылается на предыдущий) | `architecture_style.md` |
| DR-CUR-08 | Каждое требование имеет `Traces to:` ссылку на бизнес-требование | `requirements_style.md` |
| DR-CUR-09 | `quality_audit.md` использует 10-балльную scorecard для проверки качества требований | `quality_audit.md` |
| DR-CUR-10 | `task_compliance.md` отслеживает соответствие задач требованиям | `task_compliance.md` |
| DR-CUR-11 | NFR: исполнение ≤ 5 сек для 1 000 сущностей на GitHub Actions runner | `REQ-NFN-01` |
| DR-CUR-12 | NFR: модульность — обязательны абстрактные базовые классы `BaseParser`, `BaseRenderer` | `REQ-NFN-02` |

### 1.3 Требования к пользовательской документации (user-docs)

| ID | Требование | Источник |
|---|---|---|
| DR-CUR-13 | Каждая страница user-docs содержит Traceability Trace на SRS-требование | `getting-started.md` |
| DR-CUR-14 | VitePress build должен компилироваться без ошибок (`npm run docs:build`) | `integration_tests.yml` |
| DR-CUR-15 | Hugo API reference должен компилироваться (`hugo --destination`) | `integration_tests.yml` |
| DR-CUR-16 | Страницы проходят `verify_pages.py --local-dir ./user-docs/.vitepress/dist` | `integration_tests.yml` |

---

## 2. Выявленные пробелы (Gap Analysis)

| ID | Пробел | Критичность |
|---|---|---|
| DR-GAP-01 | Нет требования к **Markdown-линтингу** — стиль заголовков, пробелы, trailing spaces не контролируются | 🔴 |
| DR-GAP-02 | Нет автоматической **проверки битых ссылок** ни в design-docs (Docusaurus), ни в user-docs (VitePress) — `check_links.py` GAP-31 | 🔴 |
| DR-GAP-03 | Нет требования к валидации **front-matter / sidebar_position** в design-docs MD-файлах | 🔴 |
| DR-GAP-04 | Нет требования к **версионированию design-docs** в Docusaurus при переходе v1.0 → v2.0 | 🟡 |
| DR-GAP-05 | Нет стандарта на **именование файлов** — смешиваются kebab-case (`cli-reference.md`), snake_case (`requirements_v2_next.md`) и CamelCase в путях | 🟡 |
| DR-GAP-06 | `admin-deployment.md` ссылается на `deploy.yml`, которого нет в umbrella — нет процедуры **синхронизации doc-кода с реальным workflow** | 🔴 |
| DR-GAP-07 | Нет требования к **максимальному размеру** документа — некоторые файлы (`v2_detailed_tasks.md` — 2364 строки) плохо навигируются | 🟡 |
| DR-GAP-08 | Нет **формальной процедуры устаревания** (deprecation) для требований, перенесённых в следующую версию | 🟡 |
| DR-GAP-09 | `integration_tests_specification.md` содержит ⚠️-метки о GAP-31 (скрипты `verify_pages.py`, `check_links.py`, `run_regression_tests.py` — location unconfirmed), но нет timeline для их резолюции | 🔴 |
| DR-GAP-10 | Нет стандарта для документирования **GitHub Actions secrets** — `PIPELINE_GITHUB_TOKEN` не имеет документации о минимально необходимых правах | 🔴 |
| DR-GAP-11 | Нет требования к **Accessibility** документации (WCAG) — важно для портфолио-позиционирования | 🟢 |
| DR-GAP-12 | Нет требования к **cross-doc consistency** — одни и те же термины (например, `collector`, `orchestrator`) могут определяться по-разному в BRD и SDD | 🟡 |

---

## 3. Новые требования к документации (Backlog)

### 3.1 Markdown и синтаксические требования

- [ ] **[DR-NEW-01]** Ввести обязательное требование: все Markdown-файлы в `design-docs/docs/` и `user-docs/docs/` проходят **markdownlint** (`markdownlint-cli2`) без ошибок в CI
- [ ] **[DR-NEW-02]** Утвердить конфигурацию markdownlint: допускается максимальная длина строки 120 символов; `MD013` (line-length) применяется только к prose, не к code-блокам
- [ ] **[DR-NEW-03]** Установить правило: в design-docs **все** файлы должны начинаться с YAML front-matter блока с обязательными полями `sidebar_position` и `title`
- [ ] **[DR-NEW-04]** Установить правило именования файлов: **kebab-case** для user-docs; **snake_case** для внутренних `.antigravitycli/` документов; никакого смешивания в пределах одной директории
- [ ] **[DR-NEW-05]** Ввести требование: в каждом Markdown-файле заголовок `H1` — ровно один, первый, совпадает с `title` в front-matter (если есть)
- [ ] **[DR-NEW-06]** Установить правило для Mermaid-диаграмм: каждая диаграмма содержит `%% Description` комментарий и title-ноду для accessibility

### 3.2 Автоматическая проверка ссылок

- [ ] **[DR-NEW-07]** Ввести строгое требование: `Tests/check_links.py` (GAP-31) должен быть локализован, закоммичен или переимплементирован до релиза v2.0; без этого CI-пайплайн считается неполным
- [ ] **[DR-NEW-08]** После резолюции GAP-31: `check_links.py` запускается в `integration_tests.yml` как отдельный step после Hugo compilation, проверяет все внутренние ссылки в `user-docs/.vitepress/dist`
- [ ] **[DR-NEW-09]** Ввести требование: проверка **relative links** в design-docs (Docusaurus) запускается в CI-воркфлоу `design-docs` репозитория через `docusaurus-check-links` или аналогичный инструмент
- [ ] **[DR-NEW-10]** Установить правило: внешние ссылки (HTTPS) допустимы только в `admin-deployment.md` и `getting-started.md`; в design-docs внешние ссылки требуют review-комментария с обоснованием
- [ ] **[DR-NEW-11]** Ввести требование: ссылки на internal GitHub Pages (`Sir-Derryk.github.io`) в user-docs проверяются тестом page-existence (уже существующий `verify_pages.py`)

### 3.3 Версионирование документации

- [ ] **[DR-NEW-12]** Ввести требование: при переходе v1.0 → v2.0 создать **versioned snapshot** в Docusaurus (`docusaurus docs:version 1.0`) перед слиянием v2.0 изменений в main
- [ ] **[DR-NEW-13]** Ввести правило: в design-docs `roadmap/future_v2.md` разделы по мере реализации переносятся в `roadmap/mvp_v2/`, а не редактируются на месте — сохраняется история намерений
- [ ] **[DR-NEW-14]** Документировать процедуру версионирования в `CLAUDE.md`: когда снапшот создавать, кто ответственен, как обновлять dropdown в Docusaurus
- [ ] **[DR-NEW-15]** Установить правило: `requirements_v2_next.md` становится `requirements_v3_next.md` после freeze v2.0 — не редактировать на месте

### 3.4 Трассировка и согласованность

- [ ] **[DR-NEW-16]** Ввести требование к **GAP-статусам** в `integration_tests_specification.md`: каждый ⚠️-GAP должен иметь поле `Resolution Target` (версия + ответственный), а не просто метку
- [ ] **[DR-NEW-17]** Ввести правило: термины `Collector`, `Orchestrator`, `Parser`, `Renderer`, `IR`, `Catalog` должны использоваться консистентно во всех документах — без синонимов типа `compiler` вместо `orchestrator` в user-docs (исключение: маркетинговые тексты в лендинге)
- [ ] **[DR-NEW-18]** Создать **Glossary-страницу** в design-docs, содержащую определения 15+ ключевых терминов с ссылками на SRS-требования, где они формально определены
- [ ] **[DR-NEW-19]** Ввести правило: при удалении требования (например, GAP переносится в defer) — добавить запись в `quality_audit.md` с обоснованием, не удалять безследно
- [ ] **[DR-NEW-20]** Ввести требование: каждый новый `TASK-*.md` в `.antigravitycli/tasks/` должен содержать поле `Related Docs` — список файлов user-docs или design-docs, требующих обновления после реализации

### 3.5 Документирование CI/CD инфраструктуры

- [ ] **[DR-NEW-21]** Ввести обязательное требование: каждый новый GitHub Actions workflow должен содержать блок комментариев в начале файла: назначение, триггеры, требуемые secrets, ожидаемое время исполнения
- [ ] **[DR-NEW-22]** Документировать все используемые secrets в отдельном файле `docs/deployment/secrets.md` (user-docs) или `CLAUDE.md`: имя, назначение, минимальные права, срок ротации
- [ ] **[DR-NEW-23]** Ввести требование: `PIPELINE_GITHUB_TOKEN` secret должен использовать **Fine-grained Personal Access Token** (не classic), с ограничением по репозиториям и permissions: `contents: read`, `actions: write` (для repository_dispatch)
- [ ] **[DR-NEW-24]** Ввести правило: все environment variables в workflow явно декларируются через `env:` на уровне job или step — не передаются через inline shell substitution без документирования
- [ ] **[DR-NEW-25]** Ввести требование: README или AGENTS.md в `.github/` описывает назначение каждого workflow, его триггеры и ожидаемые Check-статусы в GitHub UI

### 3.6 Устаревание и архивирование

- [ ] **[DR-NEW-26]** Ввести формальную процедуру deprecation: файлы, помеченные для удаления, получают frontmatter `deprecated: true` и раздел `> ⚠️ DEPRECATED:` с указанием замены — не удаляются сразу
- [ ] **[DR-NEW-27]** Архивировать `brd/ude_portal_blueprint.md` — по статусу в design-docs он помечен как устаревший legacy; переместить в `design-docs/docs/_archive/`
- [ ] **[DR-NEW-28]** Ввести правило: при каждом major-релизе создавать GitHub Release с release notes, дублирующими `changelog.md` из user-docs, для portfolio-видимости

### 3.7 Quality Gates для документации

- [ ] **[DR-NEW-29]** Ввести CI-step в `design-docs` workflow: Docusaurus build (`npm run build`) должен завершаться с exit 0 — warnings считаются ошибками при наличии broken links (флаг `--fail-on-warning` для broken links)
- [ ] **[DR-NEW-30]** Ввести CI-step: проверка, что все файлы в `design-docs/docs/` имеют корректный `sidebar_position` (числовой, уникальный в директории) — Python-скрипт или `remark-lint`
- [ ] **[DR-NEW-31]** Ввести правило: `v2_detailed_tasks.md` (2 364 строки) должен быть разбит на отдельные файлы в `tasks/` после freeze v2.0 — максимальный размер задокументированного файла: 500 строк
- [ ] **[DR-NEW-32]** Ввести требование: страницы user-docs, описывающие CLI-команды, тестируются в CI smoke-тестом — команда `python -m ude.cli --help` должна возвращать exit 0 и содержать ключевые флаги из документации

---

### 3.8 Требования к документированию архитектурных решений и cross-phase зависимостей

> Пробелы AW-06, AW-07, CO-01 из `skills_compliance_report.md` — отсутствие документирования нетривиальных архитектурных решений в атомарных задачах создаёт риск некорректной реализации при автономном выполнении.

- [ ] **[DR-NEW-33]** Ввести требование: TASK-A.1.1 (`GlobalConfig`) ОБЯЗАН содержать явное примечание о том, что поля `coverage_mode` и `coverage_threshold` являются **схемными заглушками фазы 1** (парсируются без ошибок, но не оказывают поведенческого эффекта до TASK-D.2.3). Тесты TASK-A.1.2 должны верифицировать только парсинг полей, но не логику порогов — в противном случае проверяющий Phase 1 инженер вынужден понимать семантику Phase 3 (нарушение изоляции фаз).
- [ ] **[DR-NEW-34]** Ввести требование: TASK-A.4.3 (`DoxygenXmlCollector` с 3-уровневым merge) обязан явно документировать **приоритет разрешения T1-шаблона Doxyfile**: `GlobalConfig.global_templates_dir` (пользовательский) → `Path(__file__).parent.parent / "templates"` (исходный fallback) → пустой словарь `{}` (при отсутствии обоих). Текущая реализация TASK-A.4.3 хардкодит только source-relative путь, что противоречит намерению GAP-09-C (`global_templates_dir` должен быть первичным источником).
- [ ] **[DR-NEW-35]** Ввести требование: задачи TASK-D.1.4 (C#), TASK-D.1.5 (Java), TASK-D.1.6 (Python) обязаны содержать **конкретные примеры кода** с языко-специфичными XML kind-маппингами Doxygen. Формулировка «идентично TASK-D.1.3» недостаточна: C# использует `<memberdef kind="property">`, Java — `<compounddef kind="interface">`, Python — отдельную обработку `__init__` и `__class__`. Без примеров AI-агент будет некорректно переносить C++ паттерны.
- [ ] **[DR-NEW-36]** Ввести требование: разрешить неоднозначность в TASK-F.2.5 (Python integration tests) относительно полей `is_property`, `fget`, `fset` в `VariableModel` / `MethodModel`. Два допустимых пути: (A) добавить `is_property: bool = False`, `has_getter: bool = False`, `has_setter: bool = False` в `MethodModel` с изменением TASK-D.1.1; (B) тестировать только по соглашению именования, документировать scope явно. Выбор одного пути является обязательным до начала выполнения TASK-F.2.5 — иначе реализации будут расходиться.
- [ ] **[DR-NEW-37]** Ввести требование: каждый файл задачи `TASK-*.md` в `.antigravitycli/tasks/` при указании CLI-команд верификации ОБЯЗАН предоставлять обе формы — bash/sh (для CI и Linux) и PowerShell (для Windows-разработчика). Единственная форма `UPDATE_GOLDEN=1 poetry run pytest` является нарушением переносимости (AW-02); единственная форма `$env:UPDATE_GOLDEN = '1'` непригодна в CI GitHub Actions с `ubuntu-latest`.
- [ ] **[DR-NEW-38]** Ввести требование: все проверочные команды в `TASK-*.md`, использующие сравнение директорий (например, верификация byte-identical output `ude compile` vs `ude parse + render`), ОБЯЗАНЫ использовать `filecmp.dircmp` или Python-скрипт `scripts/compare_dirs.py`, а не `diff -r` (AW-03). Команда `diff -r` не существует на Windows и не подходит для CI-матриц с Windows runner.
- [ ] **[DR-NEW-39]** Ввести требование: конфигурация `sidebar.toml` документируется как отдельный справочный раздел, поскольку в v2.0 TOML заменяет per-language JSON template-конфиги — описать структуру секций `[[sidebar]]`, поле `source_file` для статических страниц, 3-way deep_merge cascade (global → sdk → doc), поведение `UdeException` при отсутствии файла в strict-режиме и graceful fallback (`{}`) в стандартном режиме через `_load_sidebar_toml_graceful()`
- [ ] **[DR-NEW-40]** Ввести требование: метод `_load_static_file_from_path()` на `BaseRenderer` (v2.0 Breaking Change) документируется в справочнике API рендереров — описать сигнатуру, параметры, возвращаемый тип, поведение при отсутствии файла; без документации пользователи, создающие кастомные шаблоны, не смогут правильно подключить статические страницы через `sidebar.toml`

---

## 4. Итоговая таблица

| Блок | Задач | Приоритет |
|---|---|---|
| 3.1 Markdown требования | 6 | 🔴 Срочно |
| 3.2 Автоматическая проверка ссылок | 5 | 🔴 Срочно |
| 3.3 Версионирование | 4 | 🟡 v2.0 |
| 3.4 Трассировка и согласованность | 5 | 🟡 v2.0 |
| 3.5 CI/CD инфраструктура | 5 | 🔴 Срочно |
| 3.6 Устаревание и архивирование | 3 | 🟢 Желательно |
| 3.7 Quality Gates | 4 | 🟡 v2.0 |
| 3.8 Cross-phase архитектурные решения | 8 | 🟡 v2.0 |
| **Итого** | **40** | |
