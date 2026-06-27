# UDE Renderer Naming Rules

## Naming Convention

All 16 concrete renderer classes in `engine/ude/renderers/` must follow this pattern:

```
<Lang><Output><ID>Renderer
```

| Dimension | Allowed values |
|-----------|----------------|
| `Lang`    | `Cpp`, `Cs`, `Java`, `Py` |
| `Output`  | `Html`, `Hugo` |
| `ID`      | `Default`, `Legacy` |

### Full Class Matrix (Target)

| Lang | HtmlDefault | HugoDefault | HtmlLegacy | HugoLegacy |
|------|-------------|-------------|------------|------------|
| Cpp  | `CppHtmlDefaultRenderer`  | `CppHugoDefaultRenderer`  | `CppHtmlLegacyRenderer`  | `CppHugoLegacyRenderer`  |
| Cs   | `CsHtmlDefaultRenderer`   | `CsHugoDefaultRenderer`   | `CsHtmlLegacyRenderer`   | `CsHugoLegacyRenderer`   |
| Java | `JavaHtmlDefaultRenderer` | `JavaHugoDefaultRenderer` | `JavaHtmlLegacyRenderer` | `JavaHugoLegacyRenderer` |
| Py   | `PyHtmlDefaultRenderer`   | `PyHugoDefaultRenderer`   | `PyHtmlLegacyRenderer`   | `PyHugoLegacyRenderer`   |

---

## Project Suffix → Lang Token Mapping

`ude_projects/` folder names use the pattern `<product>_api_<lang>`. The final token selects the `Lang` dimension:

| Folder suffix | Lang token | Language |
|---------------|------------|----------|
| `_api_cpp`    | `Cpp`      | C++      |
| `_api_cs`     | `Cs`       | C#       |
| `_api_java`   | `Java`     | Java     |
| `_api_py`     | `Py`       | Python   |

---

## Gap: Current Code vs. Target Convention

As of the audit (2026-06-25), the 16 classes are implemented but do **not yet** match the target naming convention. The deviations are:

| Current class name | Target class name | Issue |
|--------------------|-------------------|-------|
| `CppHtmlRenderer` | `CppHtmlDefaultRenderer` | missing `Default` |
| `CsharpHtmlRenderer` | `CsHtmlDefaultRenderer` | `Csharp`→`Cs`, missing `Default` |
| `JavaHtmlRenderer` | `JavaHtmlDefaultRenderer` | missing `Default` |
| `PythonHtmlRenderer` | `PyHtmlDefaultRenderer` | `Python`→`Py`, missing `Default` |
| `CppHugoRenderer` | `CppHugoDefaultRenderer` | missing `Default` |
| `CsharpHugoRenderer` | `CsHugoDefaultRenderer` | `Csharp`→`Cs`, missing `Default` |
| `JavaHugoRenderer` | `JavaHugoDefaultRenderer` | missing `Default` |
| `PythonHugoRenderer` | `PyHugoDefaultRenderer` | `Python`→`Py`, missing `Default` |
| `CppLegacyHtmlRenderer` | `CppHtmlLegacyRenderer` | `Legacy`/`Html` segments swapped |
| `CsharpLegacyHtmlRenderer` | `CsHtmlLegacyRenderer` | `Csharp`→`Cs`, order swap |
| `JavaLegacyHtmlRenderer` | `JavaHtmlLegacyRenderer` | order swap |
| `PythonLegacyHtmlRenderer` | `PyHtmlLegacyRenderer` | `Python`→`Py`, order swap |
| `CppLegacyHugoRenderer` | `CppHugoLegacyRenderer` | order swap |
| `CsharpLegacyHugoRenderer` | `CsHugoLegacyRenderer` | `Csharp`→`Cs`, order swap |
| `JavaLegacyHugoRenderer` | `JavaHugoLegacyRenderer` | order swap |
| `PythonLegacyHugoRenderer` | `PyHugoLegacyRenderer` | `Python`→`Py`, order swap |

The base/factory classes (`HtmlRenderer`, `HugoMarkdownRenderer`, `LegacyHtmlRenderer`, `LegacyHugoMarkdownRenderer`) are not subject to this convention — they are abstract factories, not concrete renderers.
