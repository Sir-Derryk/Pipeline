# ActivitiesReqs — Backlog требований к CI/CD пайплайнам

> **Роль:** Principal DevOps Architect · Lead Technical Writer  
> **Дата аудита:** 2026-06-28  
> **Источники:** `.github/workflows/integration_tests.yml`, `integration_tests_specification.md`, `requirements_v2_next.md`, `.antigravitycli/styles/`

---

## 1. Действующие требования к пайплайнам (статус: применяются сейчас)

### 1.1 Технические требования к инфраструктуре сборки

| ID | Требование | Источник |
|---|---|---|
| AD-CUR-01 | Сабмодули подключаются рекурсивно (`submodules: recursive`) при checkout | `integration_tests.yml` |
| AD-CUR-02 | Doxygen устанавливается через системный пакетный менеджер (`apt-get install -y doxygen`) | `integration_tests.yml` |
| AD-CUR-03 | Hugo устанавливается через `peaceiris/actions-hugo@v3` с нефиксированной версией (`latest`) | `integration_tests.yml` |
| AD-CUR-04 | Python-зависимости: `pydantic jinja2 lxml markdown` — без version pinning | `integration_tests.yml` |

### 1.2 Требования к скриптам верификации

| ID | Требование | Источник |
|---|---|---|
| AD-CUR-05 | Скрипты не требуют сетевого доступа к внешним ресурсам | `REQ-V2-09` |
| AD-CUR-06 | `verify_pages.py` работает с флагом `--local-dir` — полностью офлайн, без HTTP-запросов | `integration_tests.yml` |

### 1.3 Требования к checkout и управлению окружением

| ID | Требование | Источник |
|---|---|---|
| AD-CUR-07 | Token для checkout: `secrets.PIPELINE_GITHUB_TOKEN \|\| github.token` (с fallback) | `integration_tests.yml` |
| AD-CUR-08 | `PYTHONPATH: engine` устанавливается для разрешения путей модуля UDE | `integration_tests.yml` |
| AD-CUR-09 | Симлинк `user-docs/engine → ../engine` создаётся в CI для Linux-совместимости путей | `integration_tests.yml` |

---

## 2. Выявленные пробелы (Gap Analysis)

| ID | Пробел | Критичность |
|---|---|---|
| AR-GAP-01 | Версии `actions/checkout`, `actions/setup-python`, `peaceiris/actions-hugo` не зафиксированы — используется `latest` или плавающий tag; нарушение supply-chain безопасности | 🔴 |
| AR-GAP-02 | Нет блока `permissions:` на уровне workflow — применяются дефолтные `read-all`, нарушается принцип least-privilege | 🔴 |
| AR-GAP-03 | Fallback `\|\| github.token` в token-параметре checkout маскирует недоступность PAT; workflow должен явно проваливаться при отсутствии секрета | 🔴 |
| AR-GAP-04 | `Tests/verify_pages.py` — GAP-31, местоположение не подтверждено; pipeline считается неполным до резолюции | 🔴 |
| AR-GAP-05 | Нет Dependabot для GitHub Actions зависимостей — обновления action-версий не отслеживаются | 🟡 |
| AR-GAP-06 | Нет кэширования зависимостей (pip, npm, Hugo binary) — каждый запуск cold-start ~5–7 мин | 🟡 |
| AR-GAP-07 | Python-зависимости установлены глобально без virtual environment — риск конфликтов системных пакетов на runner | 🟡 |
| AR-GAP-08 | `ude audit` не вызывается в CI (coverage gate реализован только в unit-тестах, не в integration pipeline) | 🟡 |
| AR-GAP-09 | Нет `actions/upload-artifact` для test reports — failure разбор требует просмотра потоков логов напрямую | 🟡 |
| AR-GAP-10 | Нет per-language matrix strategy — тестируется только Python 3.11; языковые интеграции не изолированы | 🟡 |
| AR-GAP-11 | Нет `timeout-minutes` на уровне job — зависание npm install или Hugo build блокирует runner неограниченно | 🟢 |
| AR-GAP-12 | Нет механизма уведомлений о failures на ветке master — сбои обнаруживаются только при ручной проверке | 🟢 |

---

## 3. Новые требования к пайплайнам (Backlog)

### 3.1 Требования к безопасности

- [ ] **[AD-SEC-01]** Зафиксировать версию `actions/checkout`: `v4` → `actions/checkout@v4.1.7` (pinned semver-tag с Dependabot auto-update)
- [ ] **[AD-SEC-02]** Зафиксировать версию `actions/setup-python`: аналогично pinned tag
- [ ] **[AD-SEC-03]** Зафиксировать версию `peaceiris/actions-hugo`: убрать `hugo-version: 'latest'` — заменить конкретной версией (пример: `0.134.0`) с weekly Dependabot update
- [ ] **[AD-SEC-04]** Добавить блок `permissions:` на уровне workflow с принципом least-privilege: `contents: read`, `checks: write`, `actions: read`; не использовать дефолтные `read-all`
- [ ] **[AD-SEC-05]** Включить **Dependabot** для GitHub Actions в `.github/dependabot.yml`: `package-ecosystem: "github-actions"`, расписание: weekly
- [ ] **[AD-SEC-06]** Включить **GitHub Secret Scanning** и **Push Protection** для всех трёх репозиториев (Settings → Security → Code security)
- [ ] **[AD-SEC-07]** Убрать fallback `|| github.token` в `token: ${{ secrets.PIPELINE_GITHUB_TOKEN || github.token }}` — если PAT недоступен, workflow должен явно провалиться, а не молча использовать `github.token` с ограниченными правами

### 3.2 Требования к кэшированию зависимостей

- [ ] **[AD-CACHE-01]** Добавить step кэширования npm-зависимостей (`actions/cache@v4`): `key: ${{ runner.os }}-node-${{ hashFiles('user-docs/package-lock.json') }}`; path: `~/.npm`
- [ ] **[AD-CACHE-02]** Добавить step кэширования pip-зависимостей (`actions/cache@v4`): `key: ${{ runner.os }}-pip-${{ hashFiles('engine/pyproject.toml', 'engine/requirements*.txt') }}`; path: `~/.cache/pip`
- [ ] **[AD-CACHE-03]** Проверить поддержку встроенного кэширования в `peaceiris/actions-hugo`; если не поддерживается — добавить явный cache step для Hugo binary
- [ ] **[AD-CACHE-04]** Задокументировать ожидаемое ускорение после применения кэшей: cold build ~5–7 мин → warm build ~2–3 мин (оценочно)

### 3.3 Требования к изоляции окружения

- [ ] **[AD-ISO-01]** Перевести `pip install` с прямой установки на **virtual environment**: `python -m venv .venv && .venv/bin/pip install ...` — исключить конфликты системных пакетов на runner
- [ ] **[AD-ISO-02]** Добавить `PYTHONPATH: engine` в секцию `env:` на уровне job (не только в одном step) — все steps используют единое окружение
- [ ] **[AD-ISO-03]** Удалить step создания симлинка `ln -s ../engine ./user-docs/engine` — заменить корректной настройкой `PYTHONPATH` или `sys.path` в `ude_config_self.json`; симлинк несовместим с Windows и является хрупким решением

### 3.4 Требования к coverage и quality gates

- [ ] **[AD-QA-01]** Добавить job `engine-tests` в `integration_tests.yml` (или в отдельный `ci.yml`): `pytest engine/tests/ --cov=ude --cov-report=term-missing`; проверять что TOTAL ≥ 98%
- [ ] **[AD-QA-02]** После реализации v2.0 (GAP-10): добавить step `ude audit --mode reject-undocumented --threshold 0.9` в CI — завершать с ошибкой если coverage < 90%
- [ ] **[AD-QA-03]** Добавить `markdownlint-cli2` step для `user-docs/docs/**/*.md` (после принятия DR-NEW-01)
- [ ] **[AD-QA-04]** Добавить step `Tests/check_links.py --site-dir ./user-docs/.vitepress/dist` после резолюции GAP-31
- [ ] **[AD-QA-05]** Добавить upload артефактов: `actions/upload-artifact@v4` для pytest coverage HTML report и `verify_pages.py` output — retention 7 дней
- [ ] **[AD-QA-06]** Ввести требование: Pipeline #3 (`generate-api-ref.yml`) обязан устанавливать `poetry` до запуска любых тестов движка — шаг `pip install poetry` предшествует шагу `poetry install --no-interaction`; прямой вызов `pip install -r requirements.txt` не воспроизводит Poetry-venv и не обнаруживает dev-зависимости (`pytest`, `pytest-cov`, `pytest-mock`); отсутствие poetry-шага приводит к тому, что coverage gate тестирует неправильное окружение
- [ ] **[AD-QA-07]** Ввести требование: `pytest-mock` зафиксирован в dev-зависимостях движка (`engine/pyproject.toml`, группа `test` или `dev`); обязателен для TASK-A.3.6 (верификация L2 cache hit через `mocker.patch`) и для изоляции mock-тестов на Windows CI-runners; отсутствие в `pyproject.toml` делает TASK-A.3.6 нереализуемым без изменения зависимостей
- [ ] **[AD-QA-08]** Ввести требование: команда coverage gate в CI использует корректный путь к тестам движка — `poetry run pytest engine/tests/ --cov=ude --cov-report=term-missing --cov-fail-under=98`; запрещено использовать `pytest tests/` (неверный путь — тесты находятся в `engine/tests/`) и запрещено запускать без `poetry run` (не находит зависимости, установленные в Poetry venv)

### 3.5 Требования к per-language интеграционным тестам (v2.0)

- [ ] **[AD-LANG-01]** После реализации REQ-V2-10 (GAP-32): добавить job `integration-tests-per-language` в `integration_tests.yml`
  ```yaml
  strategy:
    matrix:
      language: [cpp, cs, java, py]
  steps:
    - run: pytest engine/tests/test_integration_${{ matrix.language }}.py -v
  ```
- [ ] **[AD-LANG-02]** Установить `continue-on-error: false` для матриц языков — failure в любом языке проваливает весь build
- [ ] **[AD-LANG-03]** Добавить артефакт с per-language test reports для разбора failures в pull request

### 3.6 Требования к мониторингу и уведомлениям

- [ ] **[AD-MON-01]** Настроить **GitHub Actions notification** для failures на ветке master: email-уведомление через стандартные настройки GitHub или Slack webhook
- [ ] **[AD-MON-02]** Добавить `timeout-minutes: 15` на уровне job — предотвратить зависание runner при проблемах с npm install или Hugo build
- [ ] **[AD-MON-03]** Добавить `if: always()` для финального step (cleanup / report) — выполняется даже при failure предыдущих steps
- [ ] **[AD-MON-04]** Добавить step вывода summary в GitHub Job Summary (`$GITHUB_STEP_SUMMARY`): количество собранных страниц, время компиляции UDE, результат verify_pages

### 3.7 Требования к новым воркфлоу v2.0

- [ ] **[AD-V2-01]** Создать `.github/workflows/coverage-gate.yml` — запускается вручную (`workflow_dispatch`) или после merge в master; выполняет `ude audit --mode reject-undocumented` и публикует результат как GitHub Check
- [ ] **[AD-V2-02]** Создать `.github/workflows/regression.yml` — регрессионное тестирование; запускается по расписанию (`cron: '0 3 * * 0'` — раз в неделю); выполняет `LoadTest/run_load_test.py` с конфигурацией `LoadTest/sdks.json`
- [ ] **[AD-V2-03]** Создать `CODEOWNERS` в `.github/` (если не существует): `engine/**` → @pavel.sokolov, `.antigravitycli/**` → @pavel.sokolov — защита критических директорий от несанкционированных изменений
- [ ] **[AD-V2-04]** После резолюции GAP-31: добавить step `python Tests/run_regression_tests.py` в `integration_tests.yml` как отдельный stage после page verification

---

### 3.8 Требования к безопасности скриптов-агрегаторов и к воротам проверки рендерер-фабрик

> Пробелы AW-05 и CB-04 из `skills_compliance_report.md` — отсутствие формальных требований к безопасности `.bat/.sh` агрегаторов и к CI-верификации `__new__` kwarg forwarding создаёт операционные риски и молчаливые сбои.

- [ ] **[AD-BAT-01]** Ввести обязательное требование: скрипт `Tests/run_all_integration_tests.bat` (TASK-F.1.4) использует `pushd`/`popd` для управления рабочей директорией. Паттерн `cd engine && poetry run ...` НЕ ДОПУСКАЕТСЯ: при падении `poetry run` шаг `cd ..` не выполняется, что оставляет CWD в неправильном состоянии для следующих шагов и делает `%ERRORLEVEL%` ненадёжным.
- [ ] **[AD-BAT-02]** Ввести требование: все пути к выходным директориям (`--output-dir`, `--site-dir`) в `run_all_integration_tests.bat` и `.sh` принимаются как именованные аргументы командной строки — не хардкодятся. Хардкод проектно-специфичных путей (например, `ude_output\bimnv_api_cpp`) нарушает переносимость скрипта между проектами.
- [ ] **[AD-BAT-03]** Ввести требование: скрипт-агрегатор проверяет существование всех зависимых скриптов (`run_regression_tests.py`, `verify_pages.py`, `check_links.py`) ДО начала выполнения первого шага. Молчаливое продолжение при отсутствии зависимости создаёт ложное впечатление успеха при незавершённом GAP-31.
- [ ] **[AD-RENDERER-01]** Ввести CI-требование (Gate): в `generate-api-ref.yml` (Pipeline #3) ОБЯЗАН присутствовать шаг `Renderer Factory __new__ Guard` (CB-04), проверяющий через grep наличие `cache_manager` в сигнатуре `__new__` и её передачу в `super().__init__()` для всех трёх файлов: `static_html.py`, `hugo_markdown.py`, `legacy.py`. Этот шаг должен располагаться ДО шага компиляции и ПОСЛЕ Pydantic Migration Guard (§4.2). Отсутствие шага в workflow является нарушением требований безопасности CI.
- [ ] **[AD-RENDERER-02]** Ввести требование: шаг `Renderer Factory __new__ Guard` (CB-04) НЕ имеет `continue-on-error: true` — он всегда блокирующий. Молчаливый разрыв `cache_manager` forwarding в `hugo_markdown.py` или `legacy.py` отключает L2-кэш для соответствующего формата вывода без каких-либо runtime-исключений, что обнаруживается только при performance-сравнении двух прогонов.

---

## 4. Итоговая таблица

| Блок | Задач | Приоритет |
|---|---|---|
| 3.1 Требования к безопасности | 7 | 🔴 Срочно |
| 3.2 Требования к кэшированию зависимостей | 4 | 🟡 v2.0 |
| 3.3 Требования к изоляции окружения | 3 | 🟡 v2.0 |
| 3.4 Требования к coverage и quality gates | 8 | 🟡 v2.0 |
| 3.5 Требования к per-language тестам | 3 | 🟡 v2.0 |
| 3.6 Требования к мониторингу и уведомлениям | 4 | 🟢 Желательно |
| 3.7 Требования к новым воркфлоу v2.0 | 4 | 🟢 v3.0-ready |
| 3.8 Безопасность агрегаторов и ворота рендерер-фабрик | 5 | 🔴 Срочно |
| **Итого** | **38** | |
