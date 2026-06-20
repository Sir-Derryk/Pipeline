# План рефакторинга рендереров (с проверкой по Golden Master)

Этот план описывает процесс разделения универсальных параметризуемых классов рендереров UDE (`HtmlRenderer` и `HugoMarkdownRenderer`) на специализированные языковые подклассы с использованием механизма ООП-наследования. Это позволит устранить внутренние условные проверки по языкам программирования и сделать архитектуру полностью симметричной с парсерами.

---

## 1. Анализ текущего кода и фиксация эталонного состояния (Baseline)

1. **Проверка стабильности текущих тестов**:
   Перед началом любых изменений необходимо запустить существующие тесты Golden Master в виртуальном окружении `engine/`, чтобы подтвердить, что текущая кодовая база полностью исправна:
   ```bash
   cd engine
   poetry run pytest tests/test_golden_master.py
   ```
2. **Фиксация состояния репозитория**:
   Убедиться, что в репозиториях `Pipeline` и `engine` нет незакомиченных изменений, чтобы при необходимости иметь возможность легко выполнить `git reset --hard`.

---

## 2. Разработка базовых классов (Шаблонный метод)

1. **Базовый HTML-рендерер (`BaseHtmlRenderer`)**:
   * Создается абстрактный класс `BaseHtmlRenderer` (наследующий `BaseRenderer` из `ude.interfaces`).
   * В базовый класс переносятся общие для всех языков механизмы:
     * Настройка окружения шаблонизатора Jinja2.
     * Копирование общих статических ассетов (CSS, JS, шрифты).
     * Общий управляющий метод `render(self, catalog: ProjectCatalog, output_path: str)`.
     * Общие хелперы генерации ссылок и очистки имен.
   * Объявляются абстрактные методы (хуки), обязательные для реализации в наследниках:
     ```python
     @abstractmethod
     def _classify_entity(self, entity_type: str) -> str:
         """Определяет виртуальную группу папки на основе типа сущности."""
         pass

     @abstractmethod
     def _get_toc_filename(self) -> str:
         """Возвращает имя файла конфигурации TOC для данного языка."""
         pass
     ```

2. **Базовый Hugo Markdown-рендерер (`BaseHugoRenderer`)**:
   * Аналогично выделяется базовый абстрактный класс `BaseHugoRenderer` для общих операций с Markdown и структурой Hugo Content.

---

## 3. Реализация языковых наследников

1. **HTML-рендереры по языкам**:
   Создать в `engine/ude/renderers/static_html.py` (или в отдельных файлах) следующие классы:
   * `CppHtmlRenderer`
   * `CsharpHtmlRenderer`
   * `JavaHtmlRenderer`
   * `PythonHtmlRenderer`

   Каждый класс реализует методы `_classify_entity` и `_get_toc_filename` без условных переходов:
   ```python
   # Пример для CppHtmlRenderer
   class CppHtmlRenderer(BaseHtmlRenderer):
       def _classify_entity(self, entity_type: str) -> str:
           et = entity_type.lower()
           if et == "class":
               return "Classes"
           # ... специфичные для C++ правила без проверок self.language == "cpp"

       def _get_toc_filename(self) -> str:
           return "toc_cpp.json"
   ```

2. **Hugo-рендереры по языкам**:
   Создать аналогичные специализированные классы для Hugo-рендеринга:
   * `CppHugoRenderer`
   * `CsharpHugoRenderer`
   * `JavaHugoRenderer`
   * `PythonHugoRenderer`

---

## 4. Интеграция и обновление Orchestrator

1. Открыть `engine/ude/orchestrator.py`.
2. Импортировать новые языковые классы рендереров.
3. Заменить прямую инициализацию старых классов на динамическое разрешение правильного класса на основе конфигурации пайплайна:
   ```python
   # Словарь сопоставления классов рендереров
   RENDERERS_MAP = {
       ("html", "cpp"): CppHtmlRenderer,
       ("html", "csharp"): CsharpHtmlRenderer,
       ("html", "java"): JavaHtmlRenderer,
       ("html", "python"): PythonHtmlRenderer,
       ("hugo_markdown", "cpp"): CppHugoRenderer,
       ("hugo_markdown", "csharp"): CsharpHugoRenderer,
       ("hugo_markdown", "java"): JavaHugoRenderer,
       ("hugo_markdown", "python"): PythonHugoRenderer,
   }
   ```

---

## 5. Верификация по Golden Master (Регрессионное тестирование)

1. **Запуск тестов соответствия**:
   Выполнить повторный запуск тестов Golden Master:
   ```bash
   poetry run pytest tests/test_golden_master.py
   ```
2. **Анализ результатов**:
   * Тесты должны пройти успешно на 100%.
   * Новый рефакторинговый код не должен изменить структуру каталогов, состав или содержимое генерируемых HTML/Markdown файлов ни на один символ.
3. **Исправление ошибок**:
   В случае падения тестов исследовать дифф (`git diff`) в папке вывода тестов и скорректировать логику в языковых наследниках.
