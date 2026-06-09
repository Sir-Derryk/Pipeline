# Задача: TSK-COL-01 — Интерфейс BaseCollector и реализация DoxygenXmlCollector

## 📌 Часть 1: Инструкция по выполнению (Implementation Guide)
1. **Цель**: Создать уровень предобработки исходного кода, обеспечив запуск Doxygen для компиляции исходников в XML и гарантированное удаление временных файлов (`REQ-FUN-01`, `REQ-FUN-22`).
2. **Шаги реализации**:
   * Объявить абстрактный класс `BaseCollector` в `oda_ude/interfaces.py` с методами:
     * `validate_environment(self, config_path: Path) -> None` (проверка бинарников и путей).
     * `collect(self, config_path: Path) -> Path` (запуск сбора данных, возвращает путь к временной папке).
     * `cleanup(self, temp_path: Path) -> None` (удаление временной папки).
   * Создать файл `oda_ude/collectors/doxygen.py` и реализовать класс `DoxygenXmlCollector(BaseCollector)`:
     * `validate_environment`: Проверяет доступность Python и бинарника `doxygen` в PATH (или по путям в `ude_global.json`), наличие `Doxyfile` (если он используется) и существование исходной директории `src_dir` для целевого языка.
     * `collect`: Запускает команду `doxygen` через `subprocess.run`, динамически генерируя временный файл конфигурации Doxygen (Doxyfile) под конкретный язык программирования (`cpp` / `cs` / `java` / `python`), настраивая правильные паттерны файлов (`**/*.cs`, `**/*.py` и т.д.) и опции (например, `OPTIMIZE_OUTPUT_JAVA = YES` для C#/Java), перенаправляя вывод XML во временную изолированную папку внутри SDK проекта.
     * `cleanup`: Рекурсивно и безопасно удаляет созданную временную папку.

## 🧪 Часть 2: Инструкция по проверке результата (Verification & TDD Scenarios)
1. **Тестовый сценарий (TDD Red Phase)**:
   * Написать `tests/test_doxygen_collector.py`.
   * Написать тесты, которые проверяют вызов методов коллектора. Тесты должны падать.
2. **Реализация (TDD Green Phase)**:
   * Написать полноценную реализацию класса `DoxygenXmlCollector`.
3. **Запуск и валидация (TDD Refactor Phase)**:
   * Запустить команду проверки:
     ```bash
     poetry run pytest tests/test_doxygen_collector.py
     ```
   * **Ожидаемый успешный результат**: тесты успешно имитируют запуск Doxygen, проверяют валидацию окружения и гарантируют удаление временных директорий.
