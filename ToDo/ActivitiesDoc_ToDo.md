# ActivitiesDoc — Backlog документирования GitHub Actions пайплайнов

> **Роль:** Principal DevOps Architect · Lead Technical Writer  
> **Дата аудита:** 2026-06-28  
> **Источники:** `.github/workflows/integration_tests.yml`, `user-docs/docs/admin-deployment.md`, `integration_tests_specification.md`, `requirements_v2_next.md`

---

## 1. Анализ текущей структуры

### 1.1 Текущий состав (GitHub Actions воркфлоу)

```
Pipeline (umbrella)/
└── .github/workflows/
    └── integration_tests.yml       # Portal Integration Tests — главный воркфлоу

Триггеры integration_tests.yml:
  push:               ветка master (изменения в umbrella-репо)
  repository_dispatch:
    types:            [trigger-integration-tests]   ← события от сабмодулей

Job: run-tests (runs-on: ubuntu-latest)
Steps:
  1. Checkout Code with Submodules   (actions/checkout@v4, submodules: recursive)
  2. Set up Python 3.11              (actions/setup-python@v5)
  3. Install System Dependencies     (apt-get install -y doxygen)
  4. Install Hugo                    (peaceiris/actions-hugo@v3, latest)
  5. Install Python Dependencies     (pydantic jinja2 lxml markdown)
  6. Compile Portal & Guides         (ln -s, npm build, ude compile, hugo)
  7. Run Page Verification           (Tests/verify_pages.py --local-dir)

Сабмодульные воркфлоу (не проверялись):
  design-docs/  → Docusaurus build + Cloudflare Pages deploy
  engine/       → Тесты движка + API reference generation
  user-docs/    → VitePress build + Hugo + Cloudflare Pages deploy
```

### 1.2 Выявленные проблемы

| # | Проблема | Приоритет |
|---|---|---|
| P1 | Нет документации механизма `repository_dispatch` — как сабмодули отправляют событие в umbrella | 🔴 |
| P2 | Нет документации `PIPELINE_GITHUB_TOKEN` — тип токена, минимальные permissions, инструкция выдачи | 🔴 |
| P3 | Нет описания трёх независимых пайплайнов (#1, #2, #3) — матрица триггеров и артефактов | 🔴 |
| P4 | Нет описания GitHub Checks в UI — что появляется после push, что означает ✅/❌ в статусах PR | 🔴 |
| P5 | Нет документации `Tests/verify_pages.py` — аргументы, поведение, интерпретация ошибок | 🔴 |
| P6 | Нет матрицы триггеров в user-docs в целевом состоянии после v2.0 | 🔴 |
| P7 | Нет объяснения симлинка `user-docs/engine → ../engine` — зачем, почему только в CI | 🟡 |
| P8 | Нет описания `ude_config_self.json` — конфиг UDE для self-documentation pipeline | 🟡 |
| P9 | Нет описания `ude_self_sdk_config.json` — что описывает, какой SDK документирует | 🟡 |
| P10 | Нет Mermaid-диаграммы полного потока CI/CD от коммита до задеплоенного портала | 🟡 |
| P11 | Нет `AGENTS.md` в `.github/` с описанием воркфлоу, expected checks и failure playbook | 🟡 |
| P12 | Нет комментариев WHY в `integration_tests.yml` для нетривиальных шагов | 🟢 |

---

## 2. Целевая структура документации пайплайнов

```
user-docs/docs/deployment/
├── index.md                      # "Глава 4: Деплой и CI/CD" (оглавление)
├── admin-deployment.md           # Обновить: Mermaid-диаграмма + WHY-аннотации
├── cicd-pipelines.md             # NEW: матрица трёх пайплайнов + матрица триггеров
├── repository-dispatch.md        # NEW: механизм кросс-репо событий
└── secrets.md                    # NEW: документация всех GitHub secrets

.github/
└── AGENTS.md                     # NEW: назначение воркфлоу, expected checks, failure playbook
```

---

## 3. Backlog (атомарные задачи с чекбоксами)

### 3.1 Документация архитектуры кросс-репо пайплайнов (P1, P3, P6)

- [ ] **[AD-DOC-01]** Создать `docs/deployment/repository-dispatch.md` — объяснение механизма кросс-репо триггеров
  - Как сабмодуль (design-docs / engine / user-docs) диспатчит событие `trigger-integration-tests` в umbrella
  - Пример GitHub Actions step для отправки `repository_dispatch`
  - Почему токен нужен (cross-repo write permissions)
  - Диаграмма: submodule push → workflow → dispatch → umbrella trigger → integration_tests.yml
- [ ] **[AD-DOC-03]** Создать таблицу «Матрица пайплайнов» в `docs/deployment/cicd-pipelines.md`:
  - Pipeline #1: триггер (commit в design-docs), воркфлоу (design-docs/.github/), артефакт (Docusaurus → Cloudflare Pages)
  - Pipeline #2: триггер (commit в user-docs), воркфлоу (user-docs/.github/), артефакт (VitePress+Hugo → Cloudflare Pages)
  - Pipeline #3: триггер (commit в engine), воркфлоу (engine/.github/), артефакт (UDE compile → API Reference, встраивается в VitePress dist)
  - Umbrella: триггер (push master + repository_dispatch), воркфлоу (integration_tests.yml), артефакт (Full portal build + page verification)

### 3.2 Документация secrets и токенов (P2)

- [ ] **[AD-DOC-02]** Создать `docs/deployment/secrets.md` — документация всех GitHub secrets
  - `PIPELINE_GITHUB_TOKEN`: назначение (cross-repo checkout + dispatch), тип (Fine-grained PAT), минимальные permissions: `Contents: Read`, `Actions: Write`, `Metadata: Read`
  - Инструкция: где создать в GitHub Settings, как добавить в репозиторий
  - Рекомендуемый срок ротации: 90 дней

### 3.3 Документация среды сборки (P7, P10)

- [ ] **[AD-DOC-04]** Задокументировать симлинк `user-docs/engine`: добавить отдельную секцию в `admin-deployment.md` — почему `ln -s ../engine ./user-docs/engine` выполняется только в CI (на Linux Ubuntu runner), и почему шаг не нужен при локальной разработке на Windows
- [ ] **[AD-DOC-07]** Добавить Mermaid-диаграмму в `admin-deployment.md` — полный поток CI/CD от коммита до задеплоенного портала, включая cross-repo события через `repository_dispatch`

### 3.4 GitHub Checks и видимость статусов (P4)

- [ ] **[AD-DOC-05]** Задокументировать GitHub Checks в user-docs:
  - `run-tests` — единственный job; что означает ✅/❌ в PR status checks
  - Ожидаемое время исполнения (~3–5 минут)
  - Что делать при failure: где смотреть логи, какие артефакты доступны, как retry

### 3.5 Документация скриптов верификации (P5)

- [ ] **[AD-DOC-06]** Задокументировать `Tests/verify_pages.py`:
  - Аргументы: `--local-dir <path>` — директория скомпилированного VitePress dist
  - Что проверяет: физическое существование HTML-файлов, heading signatures
  - Как интерпретировать ошибки (GAP-31: статус unconfirmed)
  - Добавить ссылку на `integration_tests_specification.md` §3 (TEST-INT-03)

### 3.6 Метадокументация воркфлоу (P11)

- [ ] **[AD-DOC-08]** Создать `AGENTS.md` в `.github/` (если отсутствует) или дополнить существующий: описание каждого workflow, expected checks, failure playbook

### 3.7 Аннотирование кода воркфлоу (P12)

- [ ] **[AD-DOC-09]** Добавить комментарии в `integration_tests.yml`: у каждого step — однострочный комментарий WHY (не WHAT), особенно для нетривиальных шагов (симлинк, fallback token, PYTHONPATH)
- [ ] **[AD-DOC-10]** Задокументировать переменную `PYTHONPATH: engine` в `integration_tests.yml` — почему она нужна и при каком рефакторинге модульной структуры потребует обновления

### 3.8 Документация CI guard-скриптов (CICD_ToDo.md §4.2, §4.6, §4.7)

> **Источник:** `skills_compliance_report.md` CB-04, AW-08 · `CICD_ToDo.md` §4.2, §4.6, §4.7  
> **Цель:** Guard-скрипты в `scripts/` добавляются как CI-ворота v2.0, но без документации разработчики не понимают их назначения, параметров и ожидаемого вывода.

- [ ] **[AD-DOC-11]** Задокументировать CI guard-скрипты в `admin-deployment.md` или выделенном разделе `cicd-pipelines.md`:
  - `scripts/pydantic_guard.sh` — назначение: блокировать dict-паттерны (`ClassEntity = dict`, `fields: List[str]`) в `engine/ude/`; ожидаемый вывод при нарушении; как добавлять исключения через комментарий `# pydantic-guard: ignore`
  - `scripts/renderer_factory_guard.sh` / `.ps1` — назначение: верификация CB-04 (`cache_manager` forwarding через `__new__` в трёх файлах рендереров); почему шаг НЕ имеет `continue-on-error: true`; вывод при успехе и при ошибке
  - `scripts/traceability_check.sh` — назначение: AW-08 (наличие `Implements TASK-D.*` аннотаций в Phase 3-модулях); почему на начальном этапе имеет `continue-on-error: true`; как переключить в блокирующий режим
- [ ] **[AD-DOC-12]** Задокументировать порядок CI steps в `generate-api-ref.yml` и обоснование (WHY): Pydantic Guard → Renderer Factory Guard → Traceability Check → Compile — каждый последующий шаг зависит от успеха предыдущего; перестановка шагов нарушает цепочку валидации и может маскировать реальную причину сбоя

---

## 4. Итоговая таблица приоритетов

| # | Блок | Задач | Приоритет |
|---|---|---|---|
| 3.1 | Документация архитектуры кросс-репо пайплайнов | 2 | 🔴 Срочно |
| 3.2 | Документация secrets и токенов | 1 | 🔴 Срочно |
| 3.3 | Документация среды сборки | 2 | 🟡 v2.0 |
| 3.4 | GitHub Checks и видимость статусов | 1 | 🔴 Срочно |
| 3.5 | Документация скриптов верификации | 1 | 🔴 Срочно |
| 3.6 | Метадокументация воркфлоу | 1 | 🟡 v2.0 |
| 3.7 | Аннотирование кода воркфлоу | 2 | 🟢 Желательно |
| 3.8 | Документация CI guard-скриптов | 2 | 🟡 v2.0 |
| **Итого** | | **12** | |
