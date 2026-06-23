# План доработок UDE CLI и bat-файлов

Этот документ описывает детальный пошаговый план модернизации Universal Documentation Engine (UDE) CLI и сопутствующих bat-файлов для реализации трехслойного иерархического слияния конфигураций.

## 1. Архитектура слияния (Merge Hierarchy)

Слияние конфигураций происходит последовательно снизу вверх (от общего к частному):
**`ude_global_config.json` (Глобальный)** $\rightarrow$ **`ude_sdk_config.json` (SDK/Продукт)** $\rightarrow$ **`ude_doc_config.json` (Документ)**

Для объединения словарей используется алгоритм глубокого рекурсивного слияния (`deep_merge`), при котором параметры более низкого (более специфичного) конфига перезаписывают или дополняют параметры верхних конфигов.

```mermaid
graph TD
    subgraph Входные файлы (относительные пути)
        G[ude_global_config.json <br> Глобальный уровень]
        S[ude_sdk_config.json <br> Уровень SDK]
        D[ude_doc_config.json <br> Уровень документа]
    end

    G -->|Шаг 1: deep_merge| S_Merged[Временный Merged Config]
    S -->|Добавление| S_Merged
    S_Merged -->|Шаг 2: deep_merge| Final_Cfg[Итоговый Config]
    D -->|Замещение / Дополнение| Final_Cfg
```

---

## 2. Пошаговые задачи

### Шаг 1. Переименование конфигурационных файлов на диске
В каталоге `Pipeline\ude` необходимо выполнить переименования:
1. `ude\ude_global.json` $\rightarrow$ `ude\ude_global_config.json`
2. Все файлы `product.json` во всех продуктовых каталогах $\rightarrow$ `ude_sdk_config.json`:
   - `ude\FacetModeler\product.json` $\rightarrow$ `ude_sdk_config.json`
   - `ude\IGES\product.json` $\rightarrow$ `ude_sdk_config.json`
   - `ude\Map\product.json` $\rightarrow$ `ude_sdk_config.json`
   - `ude\bimnv\product.json` $\rightarrow$ `ude_sdk_config.json`
3. Все файлы `ude_config.json` во всех целевых каталогах генерации $\rightarrow$ `ude_doc_config.json` (всего 11 файлов).

### Шаг 2. Модернизация ядра CLI (`engine/ude/cli.py`)
1. Добавить вспомогательную функцию `deep_merge(dict1: dict, dict2: dict) -> dict` для рекурсивного слияния вложенных словарей конфигураций.
2. Расширить парсер аргументов CLI `argparse.ArgumentParser` новыми параметрами:
   - `--global-config` / `-g` (обязательный)
   - `--sdk-config` / `-s` (обязательный)
   - `--doc-config` / `-d` (основной)
   - `--config` / `-c` (сделать устаревшим алиасом для `--doc-config` для обратной совместимости)
3. Модернизировать функцию `run_pipeline`:
   - Считывать и валидировать все три конфигурационных файла.
   - Сливать их по цепочке `global_config` $\rightarrow$ `sdk_config` $\rightarrow$ `doc_config`.
   - Обеспечить корректное комбинирование путей вывода: при наличии `output_base_dir` и `output_subdir` в итоговом конфиге объединять их, вычисляя абсолютный путь вывода относительно директории глобального конфига.
   - Передавать в метаданные каталога `catalog.metadata` объединенный SDK-конфиг.

### Шаг 3. Адаптация оркестратора (`engine/ude/orchestrator.py`)
1. Обновить `find_global_config` для поиска `ude_global_config.json` (с резервным поиском `ude_global.json`).
2. Обновить `find_product_json` для поиска `ude_sdk_config.json` (с резервным поиском `product.json`).
3. Заменить имя временного файла конфигурации `ude_config_temp.json` на `ude_doc_config_temp.json`.

### Шаг 4. Модернизация bat-файлов генерации
Обновить все 11 файлов `generate_docs.bat` в целевых подкаталогах, чтобы они передавали относительные пути ко всем трем конфигурационным файлам:
- `--global-config "..\..\ude_global_config.json"`
- `--sdk-config "..\ude_sdk_config.json"`
- `--doc-config "ude_doc_config.json"`

### Шаг 5. Обновление автотестов и регрессионного скрипта
1. Обновить юнит-тесты в `engine/tests/test_cli.py` и `engine/tests/test_orchestrator.py` с учетом новых аргументов командной строки и переименованных файлов.
2. В файле `Tests/prepare_baseline.py` обновить списки `FACETMODELER_PROJECTS` и `BIMNV_PROJECTS`, переименовав `ude_config.json` в `ude_doc_config.json`.

---

## 3. Ожидаемые результаты
- Полная поддержка относительных путей, передаваемых из любого bat-файла.
- Децентрализованное и прозрачное слияние конфигураций.
- Исправление проблемы с локальной генерацией папки `output` вместо общей папки вывода `ude_output`.
