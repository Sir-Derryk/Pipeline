# Задача: TSK-PAR-01 — Интерфейсы BaseParser, BaseRenderer и Иерархия ошибок

## 📌 Часть 1: Инструкция по выполнению (Implementation Guide)
1. **Цель**: Определить жесткие контракты для расширения парсеров и рендереров, а также создать структурированную иерархию исключений UDE.
2. **Шаги реализации**:
   * Создать файл `oda_ude/interfaces.py`.
   * Использовать модуль `abc` для объявления абстрактных классов:
     * `BaseParser` с абстрактным методом `.parse(self, input_path: str) -> ProjectCatalog`.
     * `BaseRenderer` с абстрактным методом `.render(self, catalog: ProjectCatalog, output_path: str)`.
   * Объявить базовые исключения: `UdeException` (от `Exception`), `ParserError` (от `UdeException`), `RendererError` (от `UdeException`).

## 🧪 Часть 2: Инструкция по проверке результата (Verification & TDD Scenarios)
1. **Тестовый сценарий (TDD Red Phase)**:
   * Написать `tests/test_interfaces.py`.
   * Проверить:
     1. Попытка инстанцировать `BaseParser()` или `BaseRenderer()` напрямую вызывает `TypeError`.
     2. Наследник `BaseParser`, не реализовавший метод `.parse()`, также падает с `TypeError` при попытке инстанцирования.
   * Тесты должны упасть.
2. **Реализация (TDD Green Phase)**:
   * Реализовать интерфейсы и исключения в `oda_ude/interfaces.py`.
3. **Запуск и валидация (TDD Refactor Phase)**:
   * Запустить команду проверки:
     ```bash
     poetry run pytest tests/test_interfaces.py
     ```
   * **Ожидаемый успешный результат**: зеленые тесты подтверждают стабильность модульной архитектуры и запрет на создание недоопределенных модулей.

