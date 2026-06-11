# 📂 Chapter 2: Coding & Commenting Standards — Detailed Structure Blueprint

This document details the page tree and hierarchical heading structure for **Chapter 2: Coding & Commenting Standards** of the UDE VitePress Guides.

---

## 🗺️ Page Tree

```text
Chapter 2: Coding & Commenting Standards (/guides/)
├── commenting-rules.md         # Documenting source code (Javadoc, Doxygen, Google formats).
└── exclusion-gates.md          # Excluding internal classes and members from compilation.
```

---

## 📑 Page & Heading Hierarchies

### 📄 Page 1: `commenting-rules.md`

#### # Commenting Rules & Docstring Standards
*   *Description*: Guidelines on documenting software components to produce beautiful, parsed references.

#### ## 📑 Supported Commenting Styles
*   *Description*: The docstring formats parsed natively by the UDE Normalizer.
    *   ### ### 1. Javadoc Style (`@param` / `@return`)
        *   *Description*: Classic Java and C++ style documentation block.
    *   ### ### 2. Doxygen Style (`\param` / `\return`)
        *   *Description*: Industry standard C++ and C# slash-backslash commenting block.
    *   ### ### 3. Google Python Style (`Args:` / `Returns:`)
        *   *Description*: Clean indent-based Python docstring specification.
    *   *Traceability*: Traces to Functional Requirement **`REQ-FUN-20`** (Docstring Normalization Engine).

#### ## 🛠️ Parameter Mapping & Types
*   *Description*: How UDE extracts parameter types, default values, and description lists.

#### ## 🔄 The CommonMark Normalization Flow
*   *Description*: Step-by-step technical process showing how raw commenting lines are normalized into pristine CommonMark Markdown.

#### ## 🏁 Formatting Examples
*   *Description*: Inline side-by-side showcases of source docstrings vs compiled HTML output blocks.

---

### 📄 Page 2: `exclusion-gates.md`

#### # Exclusion Gates & Ignore Filters
*   *Description*: Instructions on omitting internal helper functions, wrapper classes, or undocumented APIs.

#### ## 🚪 Why Filter Documentation?
*   *Description*: Introduction to quality gates and how to separate public-facing APIs from private boilerplates.

#### ## 🛠️ Exclusion Techniques
*   *Description*: Detailed mechanics of UDE-supported exclusion tags.
    *   ### ### 1. Block Ignorance (`DOM-IGNORE-BEGIN` / `DOM-IGNORE-END`)
        *   *Description*: Omitting entire blocks of lines within a source file.
    *   ### ### 2. Conditional Blocks (`@cond` / `@endcond`)
        *   *Description*: Doxygen standard conditional exclusion regions.
    *   ### ### 3. Member & Class Tagging (`@internal` / `\internal`)
        *   *Description*: Omitting specific classes or class methods by adding inline annotation flags.
    *   *Traceability*: Traces to Functional Requirement **`REQ-FUN-30`** (Exclusion Filters).

#### ## 🤖 Automated Omissions (Swig Helper Filtering)
*   *Description*: Explaining how UDE automatically identifies and prunes C++ wrappers or memory cleanup methods like `swigCPtr` and `Dispose()`.

#### ## 📊 Validation of Ignored Metrics
*   *Description*: How excluded entities impact the overall documentation coverage score reported by the Quality Gate.
    *   *Traceability*: Traces to **`REQ-BUS-08`** (Documentation Coverage & Quality Gate Separation).
