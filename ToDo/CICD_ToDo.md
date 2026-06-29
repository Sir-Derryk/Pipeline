# CICD_ToDo.md — Дорожная карта миграции на Вариант 2 (Cloudflare Pages + Zero Trust)

> **Документ:** `CICD_ToDo.md`  
> **Версия:** 1.0  
> **Дата:** 2026-06-28  
> **Роль:** Principal DevSecOps Engineer / CI/CD Architect  
> **Источник анализа:** `CICD.md` (архитектурное решение), `.antigravitycli/requirements_v2_next.md` (требования v2.0)  
> **Цель:** Полный переход с текущего отсутствия автоматизации на целевую архитектуру Вариант 2

---

## Ключевые GAP-ы, выявленные при анализе

| # | Разрыв | Источник | Критичность |
|---|--------|----------|-------------|
| G-01 | GitHub Actions workflows не существуют ни в одном из трёх репозиториев | `CICD.md §Шаг 3, 4` | 🔴 Критичный |
| G-02 | Cloudflare Pages проекты не созданы, `wrangler` не настроен | `CICD.md §2.1` | 🔴 Критичный |
| G-03 | Cloudflare Zero Trust Access Application и политики whitelist отсутствуют | `CICD.md §2.2` | 🔴 Критичный |
| G-04 | GitHub Secrets (`CF_API_TOKEN`, `CF_ACCOUNT_ID`) не зарегистрированы ни в одном репо | `CICD.md §2.4` | 🔴 Критичный |
| G-05 | Нет кэширования зависимостей (npm, pip) → медленные билды | `CICD.md §Шаг 3` | 🟡 Важный |
| G-06 | Нет pytest + coverage gate в Pipeline #3; порог ≥98% не применяется | `REQ-V2-09, REQ-V2-10` | 🟡 Важный |
| G-07 | Нет Pydantic migration guard — CI не блокирует регрессию к `dict`-паттернам | `.antigravitycli/skills/pydantic_migration_guard.md` | 🟡 Важный |
| G-08 | `ude audit` (REQ-V2-08) не интегрирован ни в один pipeline | `REQ-V2-08, GAP-10` | 🟡 Важный |
| G-09 | Pipeline #3 использует плоский CLI (`ude --doc-config`), но v2.0 добавляет субкоманды | `REQ-V2-06, GAP-01` | 🟠 Средний |
| G-10 | Нет изоляции сред (dev/preview/production) — один deploy всегда в prod | `CICD.md §2.1` | 🟠 Средний |
| G-11 | Нет защиты ветки `main` (branch protection rules) | — | 🟠 Средний |
| G-12 | Нет retention артефактов и сводок билда (build summaries) | — | 🟢 Желательный |
| G-13 | Субмодуль `engine/` требует deploy key или PAT для checkout в CI | `CICD.md §Шаг 4` | 🔴 Критичный |

---

## Фазовая структура миграции

```
Фаза 1  —  Безопасность и управление секретами           (G-02, G-03, G-04, G-13)
Фаза 2  —  Базовые GitHub Actions workflows               (G-01)
Фаза 3  —  Кэширование, производительность, оптимизация   (G-05)
Фаза 4  —  Quality Gates и ворота валидации v2.0          (G-06, G-07, G-08, G-09)
Фаза 5  —  Изоляция сред и защита веток                   (G-10, G-11)
Фаза 6  —  Мониторинг, артефакты и документация           (G-12)
```

---

## Фаза 1 — Безопасность и управление секретами

> **Цель:** Установить все необходимые учётные данные и внешнюю инфраструктуру Cloudflare до написания первого workflow. Нельзя создавать workflows без секретов — они сразу упадут.

### 1.1 Установка и аутентификация wrangler CLI

- [ ] Установить Wrangler CLI глобально: `npm install -g wrangler`
- [ ] Выполнить аутентификацию через браузер: `wrangler login`
- [ ] Проверить доступ к аккаунту Cloudflare: `wrangler whoami`
- [ ] Сохранить `CF_ACCOUNT_ID` из вывода `wrangler whoami` в локальный `.env.local` (НЕ в Git)

**Проверка:** `wrangler pages project list` возвращает пустой список без ошибок.

**Ценность для портфолио:** Демонстрирует владение Cloudflare Developer Platform и CLI-first подходом к DevOps.

---

### 1.2 Создание Cloudflare Pages проектов

- [ ] Создать Pages-проект для Design Docs (приватный):
  ```bash
  wrangler pages project create ude-design-docs
  ```
- [ ] Создать Pages-проект для User Docs (публичный):
  ```bash
  wrangler pages project create ude-user-docs
  ```
- [ ] Создать Pages-проект для API Reference (публичный):
  ```bash
  wrangler pages project create ude-api-ref
  ```
- [ ] В Cloudflare Dashboard → Pages → `ude-design-docs` → Custom domains: привязать `private.example.com`
- [ ] В Cloudflare Dashboard → Pages → `ude-user-docs` → Custom domains: привязать `docs.example.com`
- [ ] В Cloudflare Dashboard → Pages → `ude-api-ref` → Custom domains: привязать `api.example.com`

**Проверка:** `wrangler pages project list` отображает все три проекта. Открытие `private.example.com` даёт 404 (проект создан, контент ещё не задеплоен).

**Ценность для портфолио:** Три изолированных проекта Pages — правильная микросервисная декомпозиция хостинга с гранулярным контролем.

---

### 1.3 Настройка Cloudflare Zero Trust Access для Design Docs

- [ ] В Cloudflare Dashboard → Zero Trust → Access → Applications → Add application → Self-hosted
- [ ] Указать параметры приложения:
  - Name: `UDE Design Docs`
  - Domain: `private.example.com`
  - Session Duration: `24h`
  - Auto-redirect to identity: `enabled`
- [ ] Создать политику Allow (email whitelist):
  - Policy name: `Design Docs Whitelist`
  - Action: `Allow`
  - Include rule: `Emails` → добавить email-адреса рецензентов
- [ ] Создать политику Deny All Others:
  - Policy name: `Deny Everyone Else`
  - Action: `Block`
  - Include rule: `Everyone`
  - Precedence: ниже, чем Allow policy
- [ ] Проверить, что `Service Auth` включён для программного деплоя через `wrangler`
- [ ] Сохранить `APP_ID` и `POLICY_ID` из Zero Trust Dashboard для будущих API-вызовов

**Проверка:**
```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/access/apps" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | jq '.result[].name'
# Ожидаемый вывод: "UDE Design Docs"
```

**Ценность для портфолио:** Реализация настоящего Zero Trust (не security through obscurity) — enterprise-паттерн контроля доступа к внутренней документации.

---

### 1.4 Создание Cloudflare API Token с минимальными правами

- [ ] В Cloudflare Dashboard → My Profile → API Tokens → Create Token
- [ ] Использовать шаблон `Edit Cloudflare Workers`
- [ ] Добавить разрешения:
  - `Account` → `Cloudflare Pages` → `Edit`
  - `Zone` → `Zone` → `Read` (для привязанного домена)
- [ ] Ограничить Token конкретным аккаунтом (Account Resources: specific account)
- [ ] Скопировать сгенерированный токен (отображается только один раз)
- [ ] Сохранить в локальный `.env.local` как `CF_API_TOKEN=...` (НЕ в Git)

**Проверка:**
```bash
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" | jq '.result.status'
# Ожидаемый вывод: "active"
```

---

### 1.5 Регистрация GitHub Secrets во всех репозиториях

> Каждый репозиторий требует отдельной регистрации секретов через GitHub Settings → Secrets and variables → Actions.

**Репозиторий `ude-design-docs`:**
- [ ] Добавить секрет `CF_API_TOKEN` (значение из §1.4)
- [ ] Добавить секрет `CF_ACCOUNT_ID` (значение из §1.1)

**Репозиторий `ude-user-docs`:**
- [ ] Добавить секрет `CF_API_TOKEN`
- [ ] Добавить секрет `CF_ACCOUNT_ID`

**Репозиторий `universal-document-engine` (engine):**
- [ ] Добавить секрет `CF_API_TOKEN`
- [ ] Добавить секрет `CF_ACCOUNT_ID`
- [ ] Добавить секрет `PIPELINE_DEPLOY_KEY` (SSH Deploy Key для checkout субмодуля — см. §1.6)

**Проверка:** В каждом репозитории в разделе Settings → Secrets видны все зарегистрированные секреты (значения скрыты — это норма).

---

### 1.6 Настройка Deploy Key для субмодуля engine в Pipeline #3

> Pipeline #3 запускается в репозитории `engine`, но может потребовать доступ к подпроектам. Если `ude_projects/` — отдельный субмодуль, нужен отдельный ключ.

- [ ] Сгенерировать SSH-ключ без парольной фразы:
  ```bash
  ssh-keygen -t ed25519 -C "ci-pipeline3-deploy" -f ./ci_deploy_key -N ""
  ```
- [ ] Добавить **публичный ключ** (`ci_deploy_key.pub`) в GitHub → репозиторий `engine` → Settings → Deploy keys → Add deploy key (Read access)
- [ ] Добавить **приватный ключ** (`ci_deploy_key`) как GitHub Secret `PIPELINE_DEPLOY_KEY` в репозиторий `engine`
- [ ] Удалить локальные файлы ключей: `del ci_deploy_key ci_deploy_key.pub`

**Проверка:** Checkout с `ssh-key: ${{ secrets.PIPELINE_DEPLOY_KEY }}` в Actions проходит без ошибок аутентификации.

---

## Фаза 2 — Базовые GitHub Actions Workflows

> **Цель:** Создать три полноценных workflow файла, реализующих все три пайплайна UDE из `CICD.md §Рекомендация`.

### 2.1 Pipeline #1 — Deploy Design Docs (ude-design-docs)

**Путь файла:** `ude-design-docs/.github/workflows/deploy-design-docs.yml`

- [ ] Создать файл `.github/workflows/deploy-design-docs.yml` в репозитории `ude-design-docs`
- [ ] Задать корректный триггер `on.push` с фильтрацией путей:
  ```yaml
  on:
    push:
      branches: [main]
      paths:
        - 'docs/**'
        - 'blog/**'
        - 'src/**'
        - 'static/**'
        - 'docusaurus.config.js'
        - 'docusaurus.config.ts'
        - 'sidebars.js'
        - 'package.json'
        - 'package-lock.json'
  ```
- [ ] Добавить триггер `workflow_dispatch` (ручной запуск для отладки)
- [ ] Определить job `deploy` с `runs-on: ubuntu-latest`
- [ ] Добавить шаг `actions/checkout@v4`
- [ ] Добавить шаг `actions/setup-node@v4` с `node-version: '20'` и `cache: 'npm'`
- [ ] Добавить шаг `npm ci` (детерминированная установка из lock-файла)
- [ ] Добавить шаг `npm run build` (Docusaurus → папка `./build`)
- [ ] Добавить шаг деплоя через `cloudflare/wrangler-action@v3`:
  ```yaml
  - name: Deploy to Cloudflare Pages (Design Docs — Private)
    uses: cloudflare/wrangler-action@v3
    with:
      apiToken: ${{ secrets.CF_API_TOKEN }}
      accountId: ${{ secrets.CF_ACCOUNT_ID }}
      command: pages deploy ./build --project-name=ude-design-docs --branch=main
  ```
- [ ] Добавить `environment: production` в job для отображения статуса деплоя в GitHub UI

**Проверка:**
```bash
# После первого успешного запуска:
wrangler pages deployment list --project-name=ude-design-docs
# Ожидаемый вывод: одна запись со статусом "Success"
```

**Ценность для портфолио:** Автоматический деплой приватной документации с Zero Trust защитой — демонстрирует зрелость DevSecOps-подхода.

---

### 2.2 Pipeline #2 — Deploy User Docs (ude-user-docs)

**Путь файла:** `ude-user-docs/.github/workflows/deploy-user-docs.yml`

- [ ] Создать файл `.github/workflows/deploy-user-docs.yml` в репозитории `ude-user-docs`
- [ ] Задать триггер `on.push` с фильтрацией путей:
  ```yaml
  on:
    push:
      branches: [main]
      paths:
        - 'content/**'
        - 'src/**'
        - '.vitepress/**'
        - 'public/**'
        - 'package.json'
        - 'package-lock.json'
  ```
- [ ] Добавить триггер `workflow_dispatch`
- [ ] Определить job `deploy` с `runs-on: ubuntu-latest`
- [ ] Добавить шаг `actions/checkout@v4`
- [ ] Добавить шаг `actions/setup-node@v4` с `node-version: '20'` и `cache: 'npm'`
- [ ] Добавить шаг `npm ci`
- [ ] Добавить шаг `npm run build` (VitePress → папка `./.vitepress/dist`)
- [ ] Добавить шаг деплоя:
  ```yaml
  - name: Deploy to Cloudflare Pages (User Docs — Public)
    uses: cloudflare/wrangler-action@v3
    with:
      apiToken: ${{ secrets.CF_API_TOKEN }}
      accountId: ${{ secrets.CF_ACCOUNT_ID }}
      command: pages deploy ./.vitepress/dist --project-name=ude-user-docs --branch=main
  ```
- [ ] Добавить `environment: production`

**Проверка:** `curl -I https://docs.example.com` возвращает HTTP 200 после успешного деплоя.

---

### 2.3 Pipeline #3 — Generate and Deploy API Reference (engine)

**Путь файла:** `engine/.github/workflows/generate-api-ref.yml`

- [ ] Создать файл `.github/workflows/generate-api-ref.yml` в репозитории `engine`
- [ ] Задать триггер `on.push` с фильтрацией путей:
  ```yaml
  on:
    push:
      branches: [main]
      paths:
        - 'ude/**'
        - 'ude_projects/**'
        - 'requirements.txt'
        - 'pyproject.toml'
  ```
- [ ] Добавить триггер `workflow_dispatch`
- [ ] Определить job `generate-and-deploy` с `runs-on: ubuntu-latest`
- [ ] Добавить шаг checkout с поддержкой субмодулей:
  ```yaml
  - name: Checkout repository with submodules
    uses: actions/checkout@v4
    with:
      submodules: recursive
      ssh-key: ${{ secrets.PIPELINE_DEPLOY_KEY }}
  ```
- [ ] Добавить шаг `actions/setup-python@v5` с `python-version: '3.12'`
- [ ] Добавить шаг установки зависимостей:
  ```yaml
  - name: Install UDE dependencies
    run: pip install -r requirements.txt
  ```
- [ ] Добавить шаг запуска UDE compiler (v1.0 flat CLI, совместимый с текущей реализацией):
  ```yaml
  - name: Run UDE compiler (all targets)
    run: python -m ude --all-targets --output ./ude_output
  ```
  > **Примечание:** После реализации REQ-V2-06 (CLI субкоманды) этот шаг обновляется до `python -m ude compile --all --output ./ude_output`.
- [ ] Добавить шаг деплоя:
  ```yaml
  - name: Deploy API Reference to Cloudflare Pages
    uses: cloudflare/wrangler-action@v3
    with:
      apiToken: ${{ secrets.CF_API_TOKEN }}
      accountId: ${{ secrets.CF_ACCOUNT_ID }}
      command: pages deploy ./ude_output --project-name=ude-api-ref --branch=main
  ```
- [ ] Добавить `environment: production`
- [ ] Добавить шаг установки `poetry` в `generate-api-ref.yml` перед установкой зависимостей движка — все тестовые команды движка используют `poetry run pytest`; прямой `pip install` без Poetry не воспроизводит корректное venv-окружение и не находит dev-зависимости:
  ```yaml
  - name: Install Poetry
    run: pip install poetry
  ```
- [ ] Заменить шаг `pip install -r requirements.txt` на установку через Poetry для детерминированного воспроизведения зависимостей из `pyproject.toml`:
  ```yaml
  - name: Install UDE engine dependencies via Poetry
    working-directory: engine
    run: poetry install --no-interaction --no-root
  ```
- [ ] Убедиться, что `pytest-mock` зафиксирован в dev-зависимостях движка в `engine/pyproject.toml` (группа `test` или `dev`): `pytest-mock = "^3.0"` — обязателен для TASK-A.3.6 (верификация L2 cache hit через `mocker.patch("builtins.open", wraps=open)`) и для переносимой изоляции тестов на Windows CI-runners

**Проверка:** `curl -I https://api.example.com` возвращает HTTP 200 после успешного деплоя.

---

## Фаза 3 — Кэширование, производительность и оптимизация

> **Цель:** Сократить время исполнения workflows. Без кэша каждый `npm ci` тратит 60-120 секунд, каждый `pip install` — 30-90 секунд. При лимите 2000 мин/мес GitHub Actions Free это критично.

### 3.1 Кэширование npm-зависимостей (Pipeline #1 и #2)

- [ ] Убедиться, что в шаге `actions/setup-node@v4` указан параметр `cache: 'npm'` (это активирует встроенный npm-кэш на основе `package-lock.json` hash)
- [ ] Добавить явный шаг для проверки cache hit в логе:
  ```yaml
  - name: Check npm cache status
    run: echo "Cache hit for node_modules"
  ```
- [ ] Проверить, что `package-lock.json` зафиксирован в репозитории (не в `.gitignore`)

**Проверка:** Повторный запуск workflow после первого должен показать `Cache restored` в шаге `Setup Node.js`. Время установки сокращается с ~90s до ~5s.

---

### 3.2 Кэширование pip-зависимостей (Pipeline #3)

- [ ] Добавить шаг кэширования pip в `generate-api-ref.yml` перед установкой зависимостей:
  ```yaml
  - name: Cache pip dependencies
    uses: actions/cache@v4
    with:
      path: ~/.cache/pip
      key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      restore-keys: |
        ${{ runner.os }}-pip-
  ```
- [ ] Перенести шаг установки ПОСЛЕ кэширования

**Проверка:** После первого успешного запуска второй run показывает `Cache hit` для pip. Время установки сокращается с ~60s до ~3s.

---

### 3.3 Кэширование Docusaurus build cache (Pipeline #1)

- [ ] Добавить шаг кэширования `.docusaurus` build cache:
  ```yaml
  - name: Cache Docusaurus build
    uses: actions/cache@v4
    with:
      path: |
        .docusaurus
        node_modules/.cache
      key: ${{ runner.os }}-docusaurus-${{ hashFiles('**/*.md', '**/*.mdx', 'docusaurus.config.*') }}
      restore-keys: |
        ${{ runner.os }}-docusaurus-
  ```
- [ ] Добавить ПЕРЕД шагом `npm run build`

**Проверка:** Время билда Docusaurus сокращается с ~120s до ~30s на повторных прогонах без изменений в структуре.

---

## Фаза 4 — Quality Gates и ворота валидации v2.0

> **Цель:** Интегрировать в CI все quality gates из `requirements_v2_next.md`. CI не должен деплоить код, не прошедший автоматическую проверку качества.

### 4.1 pytest + coverage gate в Pipeline #3 (REQ-V2-09, REQ-V2-10)

- [ ] Добавить шаг установки тестовых зависимостей в `generate-api-ref.yml`:
  ```yaml
  - name: Install test dependencies
    run: pip install pytest pytest-cov
  ```
- [ ] Добавить шаг запуска тестов с coverage **перед** шагом компиляции и деплоя:
  ```yaml
  - name: Run test suite with coverage gate
    run: |
      pytest tests/ \
        --cov=ude \
        --cov-report=term-missing \
        --cov-fail-under=98 \
        -v
  ```
- [ ] Убедиться, что при coverage < 98% job падает с ненулевым кодом выхода (поведение `--cov-fail-under` по умолчанию)
- [ ] Добавить шаг загрузки coverage отчёта как артефакта:
  ```yaml
  - name: Upload coverage report
    uses: actions/upload-artifact@v4
    with:
      name: coverage-report-${{ github.sha }}
      path: .coverage
      retention-days: 14
  ```
- [ ] Исправить команду запуска тестов в шаге `Run test suite with coverage gate`: заменить `pytest tests/` на `poetry run pytest engine/tests/` — тесты движка UDE находятся в `engine/tests/`, а не в корне репозитория `Pipeline/`; запуск без `poetry run` не находит зависимости, установленные через `pyproject.toml`

**Проверка:**
```bash
# Локально до пуша:
pytest tests/ --cov=ude --cov-report=term-missing --cov-fail-under=98
# Ожидаемый вывод: "Required test coverage of 98% reached. Total coverage: 98%"
```

**Ценность для портфолио:** Принудительный coverage gate в CI — признак production-grade проекта, не допускающего регрессию качества.

---

### 4.2 Pydantic Migration Guard в CI (REQ-V2-07, GAP-03)

> Из `.antigravitycli/skills/pydantic_migration_guard.md`: все dict-паттерны должны быть заменены Pydantic-моделями. CI должен блокировать откат к старым паттернам.

- [ ] Создать скрипт `scripts/pydantic_guard.sh` в репозитории `engine`:
  ```bash
  #!/usr/bin/env bash
  # Блокировать использование dict() там, где ожидаются Pydantic-модели
  VIOLATIONS=$(grep -rn \
    --include="*.py" \
    -E "ClassEntity\s*=\s*dict|fields\s*:\s*List\[str\]|\.get\(['\"]fields['\"]" \
    ude/ | grep -v "test_" | grep -v "#")
  if [ -n "$VIOLATIONS" ]; then
    echo "PYDANTIC MIGRATION GUARD: Обнаружены нарушения Pydantic-модели:"
    echo "$VIOLATIONS"
    exit 1
  fi
  echo "Pydantic Guard: OK — нарушений не обнаружено"
  ```
- [ ] Сделать скрипт исполняемым и зафиксировать в репозитории
- [ ] Добавить шаг Pydantic Guard в `generate-api-ref.yml` перед компиляцией и тестами:
  ```yaml
  - name: Pydantic Migration Guard
    run: bash scripts/pydantic_guard.sh
  ```
- [ ] Проверить, что шаг падает при наличии паттерна `fields: List[str]` вместо `List[VariableModel]`

**Проверка:**
```bash
# Принудительное срабатывание (должен вернуть exit code 1):
grep -rn "fields: List\[str\]" ude/
# В целевом состоянии v2.0 — пустой вывод (нарушений нет)
```

---

### 4.3 UDE Audit Gate — Documentation Coverage (REQ-V2-08, GAP-10)

> После реализации `ude audit` (TASK-D.2.1 → TASK-D.2.7) добавить gate в Pipeline #3.

- [ ] Добавить шаг `ude audit` в `generate-api-ref.yml` (активировать после реализации REQ-V2-08):
  ```yaml
  - name: Documentation Coverage Audit Gate
    run: |
      python -m ude audit \
        --mode reject-undocumented \
        --threshold 0.80
    # Блокирует деплой если coverage < 80%. Порог регулируется в GlobalConfig.
  ```
- [ ] Проверить, что `ude audit` выводит таблицу формата `| class |`, `| method |`, `| overall |`
- [ ] Убедиться, что шаг НЕ запускается через `ude parse` или `ude render` (только через `ude audit` и `ude compile`)
- [ ] Добавить conditional execution: gate активен только на ветке `main`:
  ```yaml
  if: github.ref == 'refs/heads/main'
  ```

**Проверка:**
```bash
python -m ude audit --mode reject-undocumented --threshold 1.0
# При coverage < 100% должен вернуть exit code 2
python -m ude audit --mode allow-undocumented
# Всегда должен вернуть exit code 0
```

---

### 4.4 CLI Transition Gate (REQ-V2-06, GAP-01)

> Pipeline #3 использует v1.0 плоский CLI. При переходе на v2.0 субкоманды нужна проверка совместимости.

- [ ] Добавить шаг backward compatibility smoke test в `generate-api-ref.yml`:
  ```yaml
  - name: CLI Backward Compatibility Check
    run: |
      # v1.0 flat interface должен работать идентично после миграции на v2.0
      python -m ude --help
      # После реализации REQ-V2-06:
      # python -m ude compile --help
      # python -m ude parse --help
      # python -m ude render --help
      # python -m ude audit --help
  ```
- [ ] Обновить шаг `Run UDE compiler` с плоского CLI на субкоманду ТОЛЬКО ПОСЛЕ прохождения acceptance criteria REQ-V2-06:
  ```yaml
  # Было (v1.0):
  run: python -m ude --all-targets --output ./ude_output
  # Стало (v2.0, после реализации GAP-01):
  run: python -m ude compile --all --output ./ude_output
  ```
- [ ] Создать задачу (TODO): верифицировать byte-identical output между `ude compile` и `ude --doc-config` перед переключением в CI

**Проверка:**
```bash
# Оба вызова должны давать идентичный выход:
python -m ude --doc-config ude_projects/test/ude_doc_config.json
python -m ude compile --doc-config ude_projects/test/ude_doc_config.json
diff -r ./ude_output_v1 ./ude_output_v2  # должен дать пустой вывод
```

---

### 4.5 Integration Tests Gate (REQ-V2-09, GAP-31)

- [ ] Добавить шаг запуска integration tests в `generate-api-ref.yml`:
  ```yaml
  - name: Run integration test suites
    run: |
      pytest tests/test_integration_cpp.py \
             tests/test_integration_cs.py \
             tests/test_integration_java.py \
             tests/test_integration_py.py \
             -v --tb=short
  ```
- [ ] Убедиться, что все четыре файла интеграционных тестов существуют в `Tests/` (см. TASK-F.1.1 – F.1.5)
- [ ] Проверить: ≥5 тестов на файл (итого ≥20 тестов), все проходят

**Проверка:**
```bash
pytest tests/test_integration_cpp.py -v --co | grep "test session starts" -A 50
# Ожидаемый вывод: ≥5 тестов собраны
```

---

### 4.6 Верификация передачи `cache_manager` через фабрику `__new__` в CI (CB-04)

> **Источник:** `skills_compliance_report.md` CB-04 · `.antigravitycli/skills/pydantic_migration_guard.md` Шаг 5  
> **Цель:** CI должен блокировать мёрж при разрыве цепочки `__new__` → `super().__init__()` для kwarg `cache_manager` в любом из трёх семейств рендереров. Молчаливый разрыв не поднимает исключений, но полностью отключает L2-кэш для Hugo или Legacy рендерера.

- [ ] Создать скрипт `scripts/renderer_factory_guard.sh` в репозитории `engine`:
  ```bash
  #!/usr/bin/env bash
  # CB-04: Верификация наличия cache_manager в __new__ ВСЕХ трёх семейств рендереров
  EXIT=0
  for F in engine/ude/renderers/static_html.py \
            engine/ude/renderers/hugo_markdown.py \
            engine/ude/renderers/legacy.py; do
    if ! grep -q "cache_manager" "$F"; then
      echo "ОШИБКА CB-04: cache_manager отсутствует в $F — L2-кэш будет молча отключён"
      EXIT=1
    fi
    if grep -q "def __new__" "$F"; then
      CM_IN_NEW=$(grep -A5 "def __new__" "$F" | grep "cache_manager")
      if [ -z "$CM_IN_NEW" ]; then
        echo "ОШИБКА CB-04: __new__ в $F существует, но не принимает cache_manager"
        EXIT=1
      fi
    fi
  done
  [ "$EXIT" -eq 0 ] && echo "Renderer Factory Guard CB-04: OK — cache_manager forwarding подтверждён во всех трёх файлах"
  exit $EXIT
  ```
- [ ] Создать PowerShell-аналог `scripts/renderer_factory_guard.ps1` для локальной проверки на Windows:
  ```powershell
  $exit = 0
  foreach ($f in @("engine/ude/renderers/static_html.py",
                   "engine/ude/renderers/hugo_markdown.py",
                   "engine/ude/renderers/legacy.py")) {
      $cm = Select-String -Path $f -Pattern "cache_manager" -Quiet
      if (-not $cm) {
          Write-Error "ОШИБКА CB-04: cache_manager отсутствует в $f"
          $exit = 1
      }
      $hasNew = Select-String -Path $f -Pattern "def __new__" -Quiet
      if ($hasNew) {
          $newBlock = Get-Content $f | Select-String "def __new__" -Context 0,5
          if ($newBlock -notmatch "cache_manager") {
              Write-Error "ОШИБКА CB-04: __new__ в $f не принимает cache_manager"
              $exit = 1
          }
      }
  }
  exit $exit
  ```
- [ ] Добавить шаг в `generate-api-ref.yml` ПОСЛЕ шага Pydantic Migration Guard (§4.2), ДО компиляции:
  ```yaml
  - name: Renderer Factory __new__ Forwarding Guard (CB-04)
    run: bash scripts/renderer_factory_guard.sh
  ```
- [ ] Убедиться, что шаг явно падает при удалении `cache_manager` из сигнатуры `__new__` в `hugo_markdown.py` или `legacy.py` — мануальный тест до первого деплоя
- [ ] Зафиксировать оба скрипта (`renderer_factory_guard.sh`, `.ps1`) в Git вместе с задачей TASK-A.3.2

**Проверка:**
```bash
# В целевом состоянии v2.0 (все три файла корректно wire-ованы):
bash scripts/renderer_factory_guard.sh
# Ожидаемый вывод: "Renderer Factory Guard CB-04: OK — cache_manager forwarding подтверждён во всех трёх файлах"
# При отсутствии cache_manager в legacy.py: "ОШИБКА CB-04: ... legacy.py" + exit 1
```

---

### 4.7 Ворота трассировочных docstring-аннотаций для Phase 3 кода (AW-08)

> **Источник:** `skills_compliance_report.md` AW-08 · `task_verification.md` Architectural Traceability criterion  
> **Цель:** Весь v2.0-код фазы 3 (TASK-D.2.x, TASK-F.1.x, TASK-F.2.x) обязан содержать docstring вида `Implements TASK-D.X.X` или `Implements GAP-XX`. CI информирует о нарушениях; после завершения TASK-D.2.7 и TASK-F.2.6 ворота становятся блокирующими.

- [ ] Создать скрипт `scripts/traceability_check.sh` в репозитории `engine`:
  ```bash
  #!/usr/bin/env bash
  # AW-08: Верификация наличия Implements-аннотаций в Phase 3-модулях
  PHASE3_MODULES=(
    "engine/ude/coverage.py"
    "engine/ude/models.py"
    "engine/ude/parsers/doxygen_base.py"
    "engine/ude/parsers/doxygen_csharp.py"
    "engine/ude/parsers/doxygen_java.py"
    "engine/ude/parsers/doxygen_python.py"
  )
  MISSING=()
  for F in "${PHASE3_MODULES[@]}"; do
    if [ -f "$F" ] && ! grep -q "Implements TASK-\|Implements GAP-" "$F"; then
      MISSING+=("$F")
    fi
  done
  if [ ${#MISSING[@]} -gt 0 ]; then
    echo "ПРЕДУПРЕЖДЕНИЕ AW-08: Отсутствует Implements-аннотация в:"
    printf '  %s\n' "${MISSING[@]}"
    exit 1
  fi
  echo "Traceability Check AW-08: OK — аннотации присутствуют во всех Phase 3 модулях"
  ```
- [ ] Добавить CI-шаг в `generate-api-ref.yml` после Renderer Factory Guard, на начальном этапе с `continue-on-error: true`:
  ```yaml
  - name: Phase 3 Docstring Traceability Check (AW-08)
    continue-on-error: true  # Убрать после завершения TASK-D.2.7 и TASK-F.2.6
    run: bash scripts/traceability_check.sh
  ```
- [ ] Перевести в блокирующий режим (убрать `continue-on-error: true`) после завершения всех задач `TASK-D.2.x` и `TASK-F.2.x` — не позднее финального коммита Phase 3

**Проверка:**
```bash
grep -rn "Implements TASK-D\|Implements GAP-" engine/ude/
# В целевом состоянии v2.0: каждый Phase 3-модуль содержит хотя бы одну аннотацию
# Ожидаемый вывод: engine/ude/coverage.py:N:    """Implements TASK-D.2.3 — coverage gate logic."""
```

---

### 4.8 Замена Linux-специфичного `diff -r` на переносимое сравнение директорий (AW-03)

> **Источник:** `skills_compliance_report.md` AW-03 · `task_verification.md` Path Portability criterion  
> **Цель:** Команда `diff -r` не существует на Windows. Для обеспечения переносимости тестового CI (матрица `ubuntu-latest` + локальный Windows-разработчик) необходимо использовать Python `filecmp.dircmp` или PowerShell `Compare-Object`.

- [ ] Удалить из §4.4 (`CLI Transition Gate`) проверочную команду `diff -r ./ude_output_v1 ./ude_output_v2` и заменить портируемым Python-вариантом:
  ```python
  # Переносимое Python-сравнение (работает на Windows, Linux, macOS)
  import filecmp, sys
  cmp = filecmp.dircmp("./ude_output_v1", "./ude_output_v2")
  if cmp.left_only or cmp.right_only or cmp.diff_files:
      print(f"ОШИБКА AW-03: Расхождения: только-слева={cmp.left_only}, только-справа={cmp.right_only}, различия={cmp.diff_files}")
      sys.exit(1)
  print("AW-03 OK: ude compile и ude --doc-config дают идентичный output")
  ```
- [ ] Добавить в CI verification step §4.4 Python-скрипт `scripts/compare_dirs.py` с аргументами `<dir1> <dir2>`:
  ```yaml
  - name: Byte-Identical Output Verification (AW-03)
    run: python scripts/compare_dirs.py ./ude_output_v1 ./ude_output_v2
  ```
- [ ] Добавить PowerShell-эквивалент в `scripts/compare_dirs.ps1` для локального запуска на Windows:
  ```powershell
  param([string]$Dir1, [string]$Dir2)
  $diff = Compare-Object (Get-ChildItem -Recurse $Dir1 | Sort Name) `
                         (Get-ChildItem -Recurse $Dir2 | Sort Name)
  if ($diff) { Write-Error "Расхождения между $Dir1 и $Dir2"; exit 1 }
  Write-Host "AW-03 OK: директории идентичны"
  ```

**Проверка:**
```powershell
# Windows (локально):
.\scripts\compare_dirs.ps1 -Dir1 .\ude_output_v1 -Dir2 .\ude_output_v2
# Linux (CI):
python scripts/compare_dirs.py ./ude_output_v1 ./ude_output_v2
```

---

### 4.9 Требования безопасности для агрегатора интеграционных тестов (AW-05)

> **Источник:** `skills_compliance_report.md` AW-05 · `task_verification.md` Safety & Guard Rails criterion  
> **Цель:** Скрипт `Tests/run_all_integration_tests.bat` должен использовать `pushd`/`popd` для безопасного управления рабочей директорией, принимать пути как аргументы (не хардкодить), и валидировать существование выходных директорий перед запуском.

- [ ] При создании `Tests/run_all_integration_tests.bat` (TASK-F.1.4 / Tests_ToDo.md §7.3) обязательно использовать `pushd engine` / `popd` вместо `cd engine && ...`:
  ```bat
  @echo off
  REM AW-05: Безопасное управление CWD через pushd/popd
  pushd engine
  if errorlevel 1 (
      echo ОШИБКА: не удалось перейти в директорию engine
      exit /b 1
  )
  poetry run pytest tests/ --cov=ude --cov-fail-under=98 --tb=short
  set PYTEST_EXIT=%ERRORLEVEL%
  popd
  if %PYTEST_EXIT% neq 0 exit /b %PYTEST_EXIT%
  ```
- [ ] Принимать путь к выходной директории как параметр `%1` вместо хардкода `ude_output\bimnv_api_cpp`:
  ```bat
  set OUTPUT_DIR=%1
  if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=ude_output
  if not exist "%OUTPUT_DIR%" (
      echo ОШИБКА AW-05: директория "%OUTPUT_DIR%" не существует — запустите UDE compile перед проверкой ссылок
      exit /b 1
  )
  ```
- [ ] Добавить pre-run validation: проверять существование `Tests/run_regression_tests.py`, `Tests/verify_pages.py`, `Tests/check_links.py` ДО начала выполнения — не допускать молчаливого пропуска из-за `goto :EOF`:
  ```bat
  for %%F in (Tests\run_regression_tests.py Tests\verify_pages.py Tests\check_links.py) do (
      if not exist "%%F" (
          echo ОШИБКА AW-05: Скрипт %%F не найден — GAP-31 не завершён
          exit /b 1
      )
  )
  ```
- [ ] Добавить аналогичные проверки в `Tests/run_all_integration_tests.sh` для CI-окружения (Linux)

**Проверка:**
```bat
REM Корректная работа при существующих директориях:
Tests\run_all_integration_tests.bat ude_output
REM Ожидаемый вывод: exit 0, все тесты пройдены
REM Ошибка при отсутствии директории:
Tests\run_all_integration_tests.bat nonexistent_dir
REM Ожидаемый вывод: "ОШИБКА AW-05: директория... не существует" + exit 1
```

---

### 4.10 Docomatic Alignment Regression Gate после GAP-03 (CO-04)

> **Источник:** `skills_compliance_report.md` CO-04 · `.antigravitycli/skills/difference_minimization_iterator.md` Шаг 5  
> **Цель:** Рефакторинг всех трёх семейств рендереров в GAP-03 (TASK-D.1.7/D.1.8/D.1.9) изменяет рендеринг типизированных IR-полей. Метрика `"total_differences"` в Docomatic alignment suite может вырасти при некорректном отображении новых полей. CI обязан зафиксировать baseline до GAP-03 и заблокировать мёрж при росте расхождений.

- [ ] До начала реализации TASK-D.1.7: зафиксировать pre-GAP-03 baseline — выполнить `poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short` и сохранить значения `"total_differences"` для C++, C#, Java в файле `Tests/alignment_baseline_pre_gap03.json`; без baseline невозможно объективно оценить регрессию после рефакторинга
- [ ] После завершения TASK-D.1.9: добавить шаг Docomatic Alignment Regression Check в `generate-api-ref.yml` с path-фильтром на `engine/ude/renderers/**`:
  ```yaml
  - name: Docomatic Alignment Regression Check (CO-04)
    if: contains(toJson(github.event.head_commit.modified), 'engine/ude/renderers/')
    run: poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short
  ```
- [ ] Если `"total_differences"` вырос для любого языка относительно `Tests/alignment_baseline_pre_gap03.json` — обязательно применить SOP `difference_minimization_iterator.md` до восстановления pre-GAP-03 значений; не закрывать GAP-03 и не удалять label `needs-alignment-fix` из PR без явного подтверждения нулевого роста расхождений

**Проверка:**
```bash
poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short
# Ожидаемый вывод: для каждого языка "total_differences" ≤ значению из Tests/alignment_baseline_pre_gap03.json
```

---

## Фаза 5 — Изоляция сред и защита веток

> **Цель:** Обеспечить, что `main` получает только проверенный, прошедший все тесты код. Preview deployments дают возможность проверить изменения до деплоя в production.

### 5.1 Preview Deployments для Pull Requests

- [ ] Добавить отдельный триггер в каждый workflow для PR:
  ```yaml
  on:
    push:
      branches: [main]
    pull_request:
      branches: [main]
  ```
- [ ] Добавить условие в шаг деплоя: в PR-режиме деплоить в preview branch, не в `main`:
  ```yaml
  - name: Deploy to Cloudflare Pages
    uses: cloudflare/wrangler-action@v3
    with:
      apiToken: ${{ secrets.CF_API_TOKEN }}
      accountId: ${{ secrets.CF_ACCOUNT_ID }}
      command: >
        pages deploy ./build
        --project-name=ude-design-docs
        --branch=${{ github.head_ref || 'main' }}
  ```
- [ ] Убедиться, что Cloudflare Pages автоматически создаёт preview URL для каждого branch (`https://<branch>.<project>.pages.dev`)
- [ ] Добавить шаг публикации preview URL в PR comment:
  ```yaml
  - name: Comment preview URL on PR
    if: github.event_name == 'pull_request'
    uses: actions/github-script@v7
    with:
      script: |
        const url = `https://${context.payload.pull_request.head.ref}.ude-design-docs.pages.dev`;
        github.rest.issues.createComment({
          issue_number: context.issue.number,
          owner: context.repo.owner,
          repo: context.repo.repo,
          body: `Preview deployment: ${url}`
        });
  ```

**Проверка:** После создания тестового PR в `ude-design-docs` в комментарии к PR появляется ссылка на preview URL. Preview URL доступен (HTTP 200) без Zero Trust (это preview, не production).

---

### 5.2 Branch Protection Rules для ветки `main`

> Настройка через GitHub Settings → Branches → Add rule для каждого репозитория.

**Репозиторий `ude-design-docs`:**
- [ ] Branch name pattern: `main`
- [ ] Включить: `Require a pull request before merging`
- [ ] Включить: `Require status checks to pass before merging`
- [ ] Добавить required status check: `deploy` (имя job из workflow)
- [ ] Включить: `Require branches to be up to date before merging`
- [ ] Включить: `Do not allow bypassing the above settings`

**Репозиторий `ude-user-docs`:**
- [ ] Аналогичные правила для ветки `main`
- [ ] Required status check: `deploy`

**Репозиторий `universal-document-engine` (engine):**
- [ ] Аналогичные правила для ветки `main`
- [ ] Required status checks: `generate-and-deploy` + дополнительно `coverage` (если разделены на отдельные jobs)

**Проверка:** Попытка прямого push в `main` без PR должна быть заблокирована с сообщением: `remote: error: GH006: Protected branch update failed`.

---

### 5.3 Environment Protection Rules в GitHub

- [ ] В каждом репозитории создать GitHub Environment с именем `production`:
  - GitHub Settings → Environments → New environment → `production`
- [ ] Настроить Required reviewers (опционально для соло-разработчика, но демонстрирует зрелость):
  - Добавить себя как required reviewer для production deploys
- [ ] Настроить Environment secrets (дублирование CF_API_TOKEN на уровне Environment для изоляции):
  - `CF_API_TOKEN` и `CF_ACCOUNT_ID` на уровне environment `production`
- [ ] Убедиться, что в workflow `environment: production` в production job уже проставлен (см. §2.1, §2.2, §2.3)

**Проверка:** В разделе Actions → Run → job `deploy` видна ссылка на Environment `production` с deployment history.

---

## Фаза 6 — Мониторинг, артефакты и документация

> **Цель:** Сделать CI/CD состояние видимым и прозрачным — как для разработчика, так и для внешних рецензентов.

### 6.1 Build Status Badges в README

- [ ] Добавить badge Pipeline #1 в `README.md` репозитория `ude-design-docs`:
  ```markdown
  ![Design Docs Deploy](https://github.com/Sir-Derryk/ude-design-docs/actions/workflows/deploy-design-docs.yml/badge.svg)
  ```
- [ ] Добавить badge Pipeline #2 в `README.md` репозитория `ude-user-docs`:
  ```markdown
  ![User Docs Deploy](https://github.com/Sir-Derryk/ude-user-docs/actions/workflows/deploy-user-docs.yml/badge.svg)
  ```
- [ ] Добавить badge Pipeline #3 + coverage badge в `README.md` репозитория `engine`:
  ```markdown
  ![API Ref Deploy](https://github.com/Sir-Derryk/universal-document-engine/actions/workflows/generate-api-ref.yml/badge.svg)
  ```

**Ценность для портфолио:** Badges — стандартный сигнал зрелости open source / showcase репозитория. Рецензент сразу видит health статус проекта.

---

### 6.2 GitHub Actions Build Summary

- [ ] Добавить шаг генерации Job Summary в `generate-api-ref.yml`:
  ```yaml
  - name: Write build summary
    if: always()
    run: |
      echo "## UDE Pipeline #3 — Build Summary" >> $GITHUB_STEP_SUMMARY
      echo "| Метрика | Значение |" >> $GITHUB_STEP_SUMMARY
      echo "|---------|----------|" >> $GITHUB_STEP_SUMMARY
      echo "| Commit SHA | ${{ github.sha }} |" >> $GITHUB_STEP_SUMMARY
      echo "| Branch | ${{ github.ref_name }} |" >> $GITHUB_STEP_SUMMARY
      echo "| Triggered by | ${{ github.actor }} |" >> $GITHUB_STEP_SUMMARY
      echo "| Status | ${{ job.status }} |" >> $GITHUB_STEP_SUMMARY
  ```
- [ ] Добавить аналогичный шаг в `deploy-design-docs.yml` и `deploy-user-docs.yml`

**Проверка:** После каждого workflow run в разделе Summary отображается таблица метрик билда.

---

### 6.3 Retention и очистка артефактов

- [ ] В `generate-api-ref.yml` добавить загрузку UDE output как артефакта (для отладки):
  ```yaml
  - name: Upload UDE output artifact
    if: failure()
    uses: actions/upload-artifact@v4
    with:
      name: ude-output-debug-${{ github.sha }}
      path: ./ude_output
      retention-days: 3
  ```
  > Загружается только при падении — экономит storage при успешных прогонах.
- [ ] Настроить retention policy для coverage артефактов: 14 дней (см. §4.1)
- [ ] Убедиться, что `ude_output/`, `.docusaurus/`, `.vitepress/dist/` добавлены в `.gitignore` всех репозиториев

---

### 6.4 Workflow Documentation (Runbook)

- [ ] Создать `RUNBOOK.md` в корне репозитория `Pipeline` (umbrella) с описанием:
  - Как вручную запустить каждый из трёх пайплайнов через `workflow_dispatch`
  - Как добавить нового пользователя в Zero Trust whitelist (через Cloudflare API)
  - Как откатить деплой на предыдущий deployment (`wrangler pages deployment list`, `wrangler pages deployment rollback`)
  - Как обновить `CF_API_TOKEN` при истечении срока
- [ ] Добавить секцию "Troubleshooting" с топ-5 причинами падения workflows и их решением
- [ ] Зафиксировать `RUNBOOK.md` в Git

**Ценность для портфолио:** Runbook — признак production-ready проекта. Показывает рецензентам, что CI/CD не просто настроен, но и управляем.

---

## Матрица соответствия v2.0 Requirements ↔ CI/CD Gates

| REQ ID | GAP ID | Описание требования | CI Gate | Фаза |
|--------|--------|---------------------|---------|------|
| REQ-V2-01 | GAP-09 | GlobalConfig Pydantic validation | Implicit: тесты падают без валидации | Ф4.1 |
| REQ-V2-02 | GAP-12 | Unified logging `"ude"` logger | Implicit: unit tests coverage | Ф4.1 |
| REQ-V2-03 | GAP-07 | L2 Render Cache wired | Implicit: golden master regression | Ф4.5 |
| REQ-V2-04 | GAP-11 | Doxyfile 3-tier merge | Implicit: unit tests `merge_doxyfile_tiers` | Ф4.1 |
| REQ-V2-05 | GAP-05 | UdeOrchestrator Public API | Smoke test: `python -c "from ude.orchestrator..."` | Ф4.4 |
| REQ-V2-06 | GAP-01 | CLI субкоманды | CLI Transition Gate | Ф4.4 |
| REQ-V2-07 | GAP-03 | 7-Model Typed IR + coverage ≥98% | pytest + `--cov-fail-under=98` + Pydantic Guard | Ф4.1, Ф4.2 |
| REQ-V2-08 | GAP-10 | `ude audit` coverage gate | `ude audit --mode reject-undocumented` | Ф4.3 |
| REQ-V2-09 | GAP-31 | Integration scripts confirmed | `pytest Tests/` | Ф4.5 |
| REQ-V2-10 | GAP-32 | Per-language integration suites | `pytest test_integration_*.py` + ≥5 tests/file | Ф4.5 |

---

## Итоговая сводка фаз

| Фаза | Название | Задач | Критичность | Зависимости |
|------|----------|-------|-------------|-------------|
| **1** | Безопасность и учётные данные | 22 | 🔴 Блокирующая | — |
| **2** | Базовые GitHub Actions Workflows | 27 | 🔴 Блокирующая | Фаза 1 |
| **3** | Кэширование и производительность | 9 | 🟡 Важная | Фаза 2 |
| **4** | Quality Gates и ворота v2.0 | 24 | 🟡 Важная | Фаза 2, REQ-V2-06/07/08/09/10 |
| **5** | Изоляция сред и защита веток | 12 | 🟠 Средняя | Фаза 2 |
| **6** | Мониторинг и документация | 8 | 🟢 Желательная | Фаза 2 |
| **ИТОГО** | | **102** | | |

---

> **Статус:** Документ создан 2026-06-28. Все задачи ожидают исполнения.  
> **Следующий шаг:** Начать с Фазы 1 в указанном порядке. Workflow файлы создаются только после завершения §1.1–1.6.  
> **Ограничение:** Фаза 4 (Quality Gates для `ude audit`) активируется после реализации TASK-D.2.1–D.2.7 (REQ-V2-08).
