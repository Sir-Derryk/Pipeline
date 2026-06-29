# Pipeline Umbrella — RepoStruct ToDo

> Сводный план структурных улучшений репозитория.  
> Источники: `RepoStruct.md` (R1–R8) + сессионный анализ (A1–A5), объединены в единую нумерацию T1–T10.  
> Дата: 2026-06-28

---

## 🔴 Срочно / нулевой риск

### T1. Закоммитить документы структуры *(бывш. R5)*

`CICD.md`, `RepoStruct.md`, `RepoStruct_ToDo.md` — untracked. Ценные архитектурные документы.

```bash
git add CICD.md RepoStruct.md RepoStruct_ToDo.md
git commit -m "docs: add repo structure analysis and improvement plan"
```

**Трудозатраты:** 5 мин | **Риск:** нулевой

---

### T2. Удалить `FutureImprovements/` *(бывш. R1 + A5)*

Содержимое `CPP_Archive/` — 4 файла, все без ценности:

| Файл | Вывод |
|---|---|
| `doxygen_cpp.py` | 3-строчный stub, нулевая ценность |
| `cpp_signature_formatter.py` | Дубликат, удалённый из активного кода |
| `legacy_cpp_sidebar.json` | Тестовая фикстура, заменена Mock-данными в `Tests/` |
| `cpp_class_layout.html` | Устаревший шаблон с CDN-зависимостями, заменён текущими |

Архивная ветка не нужна — код не представляет самостоятельной ценности.

```bash
git rm -r FutureImprovements/
git commit -m "chore: remove over-engineered archived code"
```

**Трудозатраты:** 5 мин | **Риск:** нулевой

---

### T3. Задокументировать конвенцию `ude_` в CLAUDE.md *(бывш. A4)*

В корне `Pipeline/` действует неявное соглашение: всё, принадлежащее UDE как системе, именуется с префиксом `ude_` (`ude_projects/`, `ude_output/`, `ude_release_manifest.json`). После T6 к ним добавится `ude_tests/`. Соглашение применяется **только к первому уровню** (директориям в корне репозитория).

Добавить явную формулировку в `CLAUDE.md`.

**Трудозатраты:** 5 мин | **Риск:** нулевой

---

## 🟡 Важно / минимальные изменения в конфигах

### T4. Переименовать `refs/` → `sdk_refs/` в `.gitignore` *(бывш. A2)*

Имя `refs/` семантически конфликтует с внутренней структурой Git (`.git/refs/`). Проверка скриптов в `Tests/*.py` — совпадений нет, переименование безопасно.

```gitignore
# Было:
/refs/
# Станет:
/sdk_refs/
```

Физически переименовать локальную директорию, обновить `.gitignore`.

**Трудозатраты:** 5 мин | **Риск:** нулевой

---

### T5. Сгруппировать утилитные скрипты в `scripts/` *(бывш. R7)*

```
До:                           После:
├── compress_history.bat      ├── scripts/
├── compress_history.ps1      │   ├── compress_history.bat
└── run_swig.bat              │   ├── compress_history.ps1
                              │   └── run_swig.bat
```

```bash
mkdir scripts
git mv compress_history.bat compress_history.ps1 run_swig.bat scripts/
git commit -m "refactor: group utility scripts into scripts/"
```

**Трудозатраты:** 10 мин | **Риск:** низкий (проверить вызовы по относительным путям)

---

## 🟢 Структурные изменения / требуют координации

### T6. Объединить `Tests/` + `LoadTest/` → `ude_tests/` *(бывш. A1 + R3)*

Два разрозненных тестовых каталога объединяются в один. Отчёты LoadTest (ранее R3) при переносе уходят в `.gitignore` автоматически.

```
ude_tests/
├── regression/    ← содержимое Tests/
└── load/         ← содержимое LoadTest/
                    (скрипты + sdks.json — tracked; *.csv, *.md → .gitignore)
```

Требует обновления путей в `.github/workflows/integration_tests.yml` и любых скриптах, ссылающихся на `Tests/`.

**Трудозатраты:** 20 мин | **Риск:** средний

---

### T7. Проверить избыточность правил `.gitignore` для `ude_projects/` *(бывш. R4)*

Текущие правила:

```gitignore
ude_projects/**/output/
ude_projects/**/.build_cache.json
ude_projects/**/xml/
ude_projects/**/html/
```

Если UDE Compiler всегда пишет вывод в `ude_output/`, эти 4 правила — защита от несуществующей проблемы. Запустить генерацию, проверить `git status`, убрать лишние правила.

**Трудозатраты:** 15 мин | **Риск:** нулевой

---

## ⚪ Опционально / требуют предварительного анализа

### T8. Аудит `make_release.py`: понять логику ODA-совместимости *(бывш. A3)*

Скрипт не публикует `main/` и `Dev_Guides/` напрямую. Он переписывает пути в `ude_<>_config.json` и `toc.toml`, приводя их к структуре папок ODA. Необходимо выяснить:

- Откуда скрипт берёт имена `main` и `Dev_Guides` — хардкод или читает из конфига?
- Какие именно строки в конфигах он модифицирует?

Это prerequisite для T9.

**Трудозатраты:** 30 мин | **Риск:** нулевой (только чтение)

---

### T9. Переименовать `main/` → `sdk_sources/` *(бывш. R2, после T8)*

Имя `main/` конфликтует с git-конвенцией именования веток. Выполнять только после T8 — нужно убедиться, что `make_release.py` не хардкодит имя директории.

```bash
git mv main sdk_sources
git commit -m "refactor: rename main/ to sdk_sources/ to avoid branch name conflict"
```

Обновить `.gitignore`:

```gitignore
# Было:
/main/*
!/main/Mock*/
# Станет:
/sdk_sources/*
!/sdk_sources/Mock*/
```

**Трудозатраты:** 15 мин + время на обновление скрипта | **Риск:** средний

---

### T10. Переименовать ветку umbrella `master` → `main` *(бывш. R8)*

Расхождение: umbrella на `master`, все три сабмодуля на `main`. Требует координации с CI/CD скриптами и GitHub-настройками репозитория.

**Трудозатраты:** 30 мин | **Риск:** средний

---

### T11. Обновить `.gitignore` при выполнении T6 *(prerequisite для T6)*

При слиянии `Tests/` + `LoadTest/` → `ude_tests/` все существующие правила `.gitignore`, ссылающиеся на `Tests/` и `LoadTest/`, должны быть обновлены. Необходимо также добавить правила для предотвращения коммита тестовых output-артефактов в новой директории.

```gitignore
# После переименования — добавить в .gitignore:
/ude_tests/regression/output/
/ude_tests/regression/baseline/html/
/ude_tests/regression/baseline/hugo_md/
/ude_tests/load/*.csv
/ude_tests/load/results/
```

Дополнительно: проверить, что сама директория `ude_tests/` случайно не попадает под существующие wildcard-правила `.gitignore` (False Positive).

```bash
# Проверка после переименования:
git status --short | grep ude_tests
# Ожидаемый вывод: только tracked-файлы; output-артефакты исключены
```

**Трудозатраты:** 10 мин | **Риск:** нулевой

---

### T12. Зафиксировать CI guard-скрипты в `scripts/` *(связано с T5, CICD_ToDo.md §4.2, §4.6, §4.7, §4.8)*

Задачи CICD_ToDo.md §4.2, §4.6, §4.7, §4.8 создают новые guard-скрипты, которые должны храниться в `scripts/` вместе с утилитами из T5 (`compress_history.bat/.ps1`, `run_swig.bat`):
- `scripts/pydantic_guard.sh` (CICD §4.2)
- `scripts/renderer_factory_guard.sh` + `renderer_factory_guard.ps1` (CICD §4.6)
- `scripts/traceability_check.sh` (CICD §4.7)
- `scripts/compare_dirs.py` + `compare_dirs.ps1` (CICD §4.8)

При выполнении T5 убедиться, что CI guard-скрипты также добавляются в `scripts/`, а не создаются в корне репозитория или в `Tests/`.

```bash
git add scripts/pydantic_guard.sh scripts/renderer_factory_guard.sh scripts/renderer_factory_guard.ps1 \
        scripts/traceability_check.sh scripts/compare_dirs.py scripts/compare_dirs.ps1
```

**Трудозатраты:** 5 мин | **Риск:** нулевой

---

## Итоговая таблица

| # | Действие | Приоритет | Риск | Трудозатраты |
|---|---|---|---|---|
| T1 | Закоммитить CICD.md + RepoStruct.md + RepoStruct_ToDo.md | 🔴 | Нулевой | 5 мин |
| T2 | Удалить FutureImprovements/ | 🔴 | Нулевой | 5 мин |
| T3 | Задокументировать `ude_` конвенцию в CLAUDE.md | 🔴 | Нулевой | 5 мин |
| T4 | `refs/` → `sdk_refs/` в .gitignore | 🟡 | Нулевой | 5 мин |
| T5 | Сгруппировать скрипты в `scripts/` | 🟡 | Низкий | 10 мин |
| T6 | `Tests/` + `LoadTest/` → `ude_tests/` | 🟢 | Средний | 20 мин |
| T7 | Проверить избыточность .gitignore ude_projects/ | 🟢 | Нулевой | 15 мин |
| T8 | Аудит make_release.py (ODA-совместимость) | ⚪ | Нулевой | 30 мин |
| T9 | Переименовать `main/` → `sdk_sources/` (после T8) | ⚪ | Средний | 15 мин + |
| T10 | Ветка `master` → `main` | ⚪ | Средний | 30 мин |
| T11 | Обновить `.gitignore` при выполнении T6 | 🟢 | Нулевой | 10 мин |
| T12 | CI guard-скрипты в `scripts/` (prerequisite к T5) | 🟡 | Нулевой | 5 мин |

---

## Зафиксированные решения (выполнено)

- **R6 ✅** GitHub Actions воркфлоу реализованы в каждом сабмодуле (`design-docs`, `engine`, `user-docs`). В `Pipeline/.github/workflows/` хранится только `integration_tests.yml` — корректная архитектура: каждый сабмодуль деплоит себя сам.
