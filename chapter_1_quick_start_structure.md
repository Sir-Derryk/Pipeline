# 📂 Chapter 1: Quick Start — Detailed Structure Blueprint

This document details the page tree and hierarchical heading structure for **Chapter 1: Quick Start** of the UDE VitePress Guides.

---

## 🗺️ Page Tree

```text
Chapter 1: Quick Start (/guides/)
├── getting-started.md          # Environment setup, installation, and first compilation run.
└── first-config.md             # Schema specification for target configurations (ude_config.json).
```

---

## 📑 Page & Heading Hierarchies

### 📄 Page 1: `getting-started.md`

#### # Getting Started with UDE
*   *Description*: The main entry page for new users, offering a 60-second path to compiling code references.

#### ## 📐 Core Architecture Concept
*   *Description*: High-level visualization of the UDE three-stage pipeline (Collect ➔ Parse ➔ Render).

#### ## 💻 Environment Prerequisites
*   *Description*: Verification checklist for the user's host machine.
    *   ### ### Python Runtime Checklist (3.11+)
    *   ### ### Doxygen Preprocessor Check
    *   ### ### Package Managers (Poetry or Pip)
    *   *Traceability*: Traces to functional requirement **`REQ-FUN-01`** (Environment Verification).

#### ## 🚀 Quick Installation
*   *Description*: Step-by-step setup guides.
    *   ### ### Installing via Pip
    *   ### ### Installing via Poetry (Local Development)

#### ## ⚡ Your First Compilation (Hello World)
*   *Description*: A quick test command using mock XML outputs to verify the system works in under 10 seconds.
    *   *Traceability*: Traces to **`REQ-BUS-02`** (Execution Speed Gate).

#### ## 🔍 Troubleshooting & Verification
*   *Description*: Common issues like missing system paths or incorrect Python versions.

---

### 📄 Page 2: `first-config.md`

#### # Writing Your First Target Configuration
*   *Description*: Practical guide to configuring target compilation tasks.

#### ## 📋 Understanding target_config.json
*   *Description*: The local configurations file structure and relative path resolution rules.

#### ## 🛠️ Step-by-Step Configuration Block
*   *Description*: Break down of the three main configuration sectors.
    *   ### ### 1. Collector Block (`collector`)
        *   *Description*: Parameters for Doxygen XML pathing and custom flags.
    *   ### ### 2. Parser Block (`parser`)
        *   *Description*: Selection of SWIG filters and namespace parsing.
    *   ### ### 3. Renderer Block (`renderer`)
        *   *Description*: Specifying Hugo Markdown templates and custom frontmatter variables.

#### ## 🚀 Running the Orchestrator
*   *Description*: Launching UDE over the configured target.
    *   *Traceability*: Traces to Functional Requirement **`REQ-FUN-12`** (Path Portability and Resolution).

#### ## 🏁 Verification Checklist
*   *Description*: How to check if intermediate Gzip files and final Hugo files were generated successfully.
