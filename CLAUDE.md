# Project Core Rules & Memories

## ⚠️ MANDATORY DIRECTIVE
- This repository is primary managed and tracked via the **Antigravity CLI** framework.
- All workspace memories, technical definitions, coding standards, and custom project rules are stored inside the `.antigravitycli/` directory.
- **Your Instruction:** At the beginning of every session and before making any structural changes, you MUST read the configuration and instruction files located inside `.antigravitycli/`. Align your behavior, TDD requirements, and architecture design strictly with the data found there.

## Renderer Naming Convention

All 16 concrete renderer classes in `engine/ude/renderers/` follow this pattern:

```
<Lang><Output><ID>Renderer
```

- **Lang**: `Cpp` | `Cs` | `Java` | `Py`
- **Output**: `Html` | `Hugo`
- **ID**: `Default` | `Legacy`

Full class matrix:

| Lang | HtmlDefault | HugoDefault | HtmlLegacy | HugoLegacy |
|------|-------------|-------------|------------|------------|
| Cpp  | `CppHtmlDefaultRenderer`  | `CppHugoDefaultRenderer`  | `CppHtmlLegacyRenderer`  | `CppHugoLegacyRenderer`  |
| Cs   | `CsHtmlDefaultRenderer`   | `CsHugoDefaultRenderer`   | `CsHtmlLegacyRenderer`   | `CsHugoLegacyRenderer`   |
| Java | `JavaHtmlDefaultRenderer` | `JavaHugoDefaultRenderer` | `JavaHtmlLegacyRenderer` | `JavaHugoLegacyRenderer` |
| Py   | `PyHtmlDefaultRenderer`   | `PyHugoDefaultRenderer`   | `PyHtmlLegacyRenderer`   | `PyHugoLegacyRenderer`   |

## Project Suffix → Lang Token Mapping

`ude_projects/` folder names use the suffix `_api_<lang>`. The final token selects the `Lang` dimension:

| Folder suffix | Lang token | Language |
|---------------|------------|----------|
| `_api_cpp`    | `Cpp`      | C++      |
| `_api_cs`     | `Cs`       | C#       |
| `_api_java`   | `Java`     | Java     |
| `_api_py`     | `Py`       | Python   |

See `.antigravitycli/rules.md` for the full audit gap analysis.