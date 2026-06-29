# InstallFix Guide — Диагностика и исправление ошибки установки UDE

## Причина ошибки

### 1. Отсутствие файла `README.md` (FileNotFoundError)

В файле `engine/pyproject.toml` (строка 6) задана следующая конфигурация:

```toml
readme = "README.md"
```

Poetry-core разрешает этот путь **относительно расположения самого `pyproject.toml`**, то есть ожидает файл по пути `engine/README.md`. Файл был удалён из рабочего дерева репозитория (зафиксировано в `git status` как `D engine/README.md`).

При выполнении команды `pip install ./engine` pip вызывает build-backend `poetry.core.masonry.api` для подготовки метаданных пакета (фаза `Preparing metadata (pyproject.toml)`). На этом этапе poetry-core пытается прочитать `README.md` для заполнения поля `description` пакета. Поскольку файла не существует — ни в рабочем дереве, ни в скопированном релизном каталоге — процесс завершается с ошибкой:

```
FileNotFoundError: Readme path `D:\ODARepositories\Documentation\ude\engine\README.md` does not exist.
```

**Вывод:** `README.md` является обязательным артефактом сборки, без которого `pip install` принципиально невозможен. Его отсутствие в релизном пакете — критический дефект сборочного конвейера.

---

### 2. Непереносимость виртуального окружения (Venv Non-Portability)

Текущий `install.bat` создаёт виртуальное окружение командой:

```bat
python -m venv .venv
```

При создании `.venv` Python **жёстко прописывает абсолютные пути** в нескольких местах:

| Файл / артефакт | Что прописывается |
|---|---|
| `.venv\Scripts\activate.bat` | `set VIRTUAL_ENV=<абсолютный путь>` |
| `.venv\Scripts\pip.exe` | Путь к интерпретатору Python в заголовке PE-лаунчера |
| `.venv\Scripts\ude.exe` | Аналогично — entry-point лаунчер |
| `.venv\pyvenv.cfg` | `home = <путь к Python>`, `prompt = ...` |

Если папка `.venv` скопирована из `D:\ODARepositories\Documentation\ude\` в любой другой каталог (или на другую машину), все эти пути указывают на **несуществующее исходное расположение**. В результате:

- `call .venv\Scripts\activate` устанавливает `VIRTUAL_ENV` в старый путь → pip при переустановке пишет пакеты в неверное место
- `pip.exe` не может найти свой интерпретатор → падает при запуске
- `ude.exe` аналогично нефункционален

**Вывод:** `.venv` категорически **нельзя** включать в состав релизного дистрибутива. Виртуальное окружение должно создаваться заново на целевой машине непосредственно в процессе установки.

---

## Исправление `install.bat`

Ниже приведена переписанная, переносимая версия скрипта. Ключевые изменения:

- Все пути вычисляются динамически через `%~dp0` — скрипт работает из любого каталога
- Перед созданием `.venv` любое унаследованное/скопированное старое окружение удаляется
- Виртуальное окружение создаётся свежим на целевой машине
- Добавлена проверка успешности установки пакета

```bat
@echo off
setlocal enabledelayedexpansion

:: %~dp0 — абсолютный путь к каталогу скрипта (всегда актуален)
set "ROOT=%~dp0"
:: Убираем завершающий обратный слеш
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"

pushd "%ROOT%"

echo ===================================================
echo  UDE Environment Setup
echo  Base directory: %ROOT%
echo ===================================================

:: --- Проверка Python ---
echo Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python не найден в PATH.
    echo Установите Python 3.11 или выше.
    popd & pause & exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (set PYMAJ=%%a & set PYMIN=%%b)
if %PYMAJ% LSS 3 (
    echo [ERROR] Python %PYVER% слишком старый. Требуется 3.11+.
    popd & pause & exit /b 1
)
if %PYMAJ% EQU 3 if %PYMIN% LSS 11 (
    echo [ERROR] Python %PYVER% слишком старый. Требуется 3.11+.
    popd & pause & exit /b 1
)
echo [OK] Python %PYVER% найден.

:: --- Проверка Doxygen ---
echo Checking Doxygen...
where doxygen >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Doxygen не найден в PATH.
    echo Генерация документации будет недоступна.
    echo Поместите бинарник Doxygen в: %ROOT%\tools\doxygen\ и добавьте путь в PATH.
) else (
    echo [OK] Doxygen найден.
)

:: --- Очистка старого виртуального окружения ---
:: КРИТИЧЕСКИ ВАЖНО: скопированный .venv содержит абсолютные пути
:: от машины-источника и НЕ будет работать на целевой машине.
echo.
echo Cleaning up any stale virtual environment...
if exist "%ROOT%\.venv" (
    echo [INFO] Удаляем старый .venv...
    rmdir /s /q "%ROOT%\.venv"
    if exist "%ROOT%\.venv" (
        echo [ERROR] Не удалось удалить %ROOT%\.venv. Завершите все процессы, использующие его.
        popd & pause & exit /b 1
    )
    echo [OK] Старый .venv удалён.
) else (
    echo [OK] Старый .venv не обнаружен.
)

:: --- Создание свежего виртуального окружения ---
echo.
echo Creating fresh virtual environment at: %ROOT%\.venv
python -m venv "%ROOT%\.venv"
if %errorlevel% neq 0 (
    echo [ERROR] Не удалось создать виртуальное окружение.
    popd & pause & exit /b 1
)
echo [OK] Виртуальное окружение создано.

:: --- Установка пакета UDE ---
echo.
echo Installing UDE engine...
call "%ROOT%\.venv\Scripts\activate.bat"

:: Обновляем pip перед установкой во избежание проблем с устаревшей версией
python -m pip install --upgrade pip --quiet

pip install "%ROOT%\engine"
if %errorlevel% neq 0 (
    echo [ERROR] Установка UDE завершилась с ошибкой.
    echo Убедитесь, что в каталоге engine\ присутствует файл README.md.
    popd & pause & exit /b 1
)
echo [OK] UDE успешно установлен.

:: --- Проверка установки ---
echo.
echo Verifying installation...
"%ROOT%\.venv\Scripts\ude.exe" --help
if %errorlevel% neq 0 (
    echo [WARNING] Команда 'ude --help' завершилась с ошибкой. Проверьте установку вручную.
)

popd
echo.
echo ===================================================
echo  Установка завершена успешно.
echo  Для активации окружения выполните:
echo    call "%ROOT%\.venv\Scripts\activate.bat"
echo ===================================================
pause
```

---

## Исправление сборочного конвейера

### Проблема: `README.md` не входит в релизный пакет

`engine/README.md` — обязательный артефакт сборки (`pyproject.toml`, строка `readme = "README.md"`). Существует два способа исправить ситуацию; рекомендуется **вариант A**.

---

### Вариант A (рекомендуется): Восстановить `README.md` и включить его в сборку

**Шаг 1.** Восстановить удалённый файл `engine/README.md` (минимально допустимое содержимое):

```markdown
# UDE — Universal Documentation Engine

Python-пакет для генерации API-документации.
```

**Шаг 2.** Убедиться, что скрипт упаковки релиза копирует `README.md` вместе с пакетом. Добавить в скрипт упаковки (PowerShell-пример):

```powershell
# Гарантируем наличие README.md в релизном каталоге
Copy-Item "engine\README.md" "release\ude\engine\README.md" -Force
```

Или эквивалент для bat-скрипта упаковки:

```bat
copy /Y "engine\README.md" "release\ude\engine\README.md"
```

**Шаг 3.** Добавить в `.gitignore` или в явный манифест исключений правило, **не** удаляющее `README.md` при упаковке.

---

### Вариант B (обходной): Убрать поле `readme` из `pyproject.toml`

Если файл README.md намеренно отсутствует и не планируется его добавление, удалить строку из `engine/pyproject.toml`:

```toml
# Удалить эту строку:
readme = "README.md"
```

**Недостаток:** метаданные пакета на PyPI/локальном индексе не будут содержать описание. Для внутреннего инструмента это приемлемо.

---

### Общее правило для сборочного конвейера

При формировании релизного дистрибутива `release\ude\` необходимо обеспечить следующую структуру:

```
release\ude\
├── install.bat          ← переносимый скрипт (из данного руководства)
├── engine\
│   ├── pyproject.toml
│   ├── README.md        ← ОБЯЗАТЕЛЕН, если указан в pyproject.toml
│   └── ude\
│       └── ...
└── (НЕ включать .venv\) ← .venv генерируется на целевой машине
```

Чеклист релиза:
- [ ] `engine/README.md` присутствует в каталоге `engine/`
- [ ] `.venv/` **исключён** из релизного архива (добавить в `.gitignore` и в скрипт упаковки)
- [ ] `install.bat` использует `%~dp0` для динамической адресации
- [ ] `install.bat` удаляет старый `.venv` перед созданием нового
