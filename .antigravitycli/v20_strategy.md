# UDE v2.0 — Resource Allocation Strategy & AI Automation Plan

## Strategy Rationale: Quota Synergy (Claude CLI + Antigravity CLI)

Our free assets are restricted as follows:
1. **Claude CLI (Sonnet)**: Daily limit of **1,000,000 tokens**. One local TDD cycle (Red-Green-Refactor with test run and fixing code) consumes **30k–50k tokens**. This allows only **20–33 runs/day**.
2. **Antigravity CLI (Google AI Pro)**: Strict limit of **1,500 requests/day** (tokens are free/unlimited). Context window: **2M tokens** for Gemini 3.1 Pro, **1M+ tokens** for Gemini 3.5 Flash.

### Optimal Synergy Principle (Asymmetric TDD & Context Offloading)
* **Context Offloading (Gemini 3.1 Pro)**: Avoid feeding large codebase/test files to Claude (which would eat 300k–400k tokens per single prompt). Instead, pass the entire project context to Gemini 3.1 Pro to analyze architecture, find gaps, and generate precise test cases (Phase RED). This costs **1 request** out of 1,500 (0% of Claude's token limit).
* **Local Micro-TDD (Claude CLI)**: Run Claude CLI on a very narrow context (only the target file and the generated test file, e.g., 10k–15k tokens). Claude runs local test feedback loops (`pytest` -> fix -> `pytest`) until GREEN. At 15k tokens context, each loop costs only 15k–20k tokens, allowing **50–60 iterations/day** within the 1M token budget.
* **Routine Task Offloading (Gemini 3.5 Flash)**: Offload all markdown files, Docusaurus configuration, YAML CI/CD, and file management tasks to Gemini 3.5 Flash. These tasks are low logical risk but text-heavy, preserving Claude's tokens for core logic.

## Backlog Mapping Table (Sections 0-9)

| Section | Description | Complexity | Tool & Model | Allocation Rationale |
|---------|-------------|------------|--------------|----------------------|
| **0** | Repository & Env Prep | Low / Med | **Gemini 3.5 Flash** (routine) + **Claude Sonnet** (TDD fixes) | Flash performs all file moves/deletions. Claude fixes the existing test logger and configurations (`pytest` verification). |
| **1** | Phase 1: Engine Infra | High | **Gemini 3.1 Pro** (RED) + **Claude Sonnet** (GREEN) | Gemini 3.1 Pro designs `GlobalConfig` and `BuildCacheManager`, drafting RED tests. Claude implements code and fixes tests to GREEN. |
| **2** | Phase 2: Library API & CLI | High | **Gemini 3.1 Pro** (design) + **Claude Sonnet** (integration) | Gemini designs the `Library API` facade and CLI subcommands schema. Claude rewrites CLI commands and debugs local integration test failures. |
| **3** | Phase 3/D: Typed IR | High | **Gemini 3.1 Pro** (IR models) + **Claude Sonnet** (TDD loops) | Gemini designs Pydantic models/schemas for Typed IR. Claude integrates them into collectors/renderers and runs local TDD loops. |
| **4** | Phase 3/F: QA & Testing | Medium | **Gemini 3.1 Pro / Flash** (test generation) + **Claude Sonnet** (fix gaps) | Gemini generates bulk test files/mocks. Claude runs code-fixing loops to hit the $\ge 98\%$ coverage gate. |
| **5** | CI/CD Deploy Infra | Low | **Gemini 3.5 Flash** | Routine YAML workflow writing, secrets doc, and dependency caching. No Claude token usage. |
| **6** | User Documentation | Low | **Gemini 3.5 Flash** | VitePress/Docusaurus markdown pages, folder restructuring, kebab-case checks. |
| **7** | Pipeline & CI/CD Docs | Low | **Gemini 3.5 Flash** | Technical guides and Mermaid diagrams. |
| **8** | Doc Quality Reqs | Medium | **Gemini 3.5 Flash** (rules) + **Claude Sonnet** (CI smoke tests) | Flash writes markdownlint checks. Claude debugs CLI smoke test failures. |
| **9** | Finalization & Release | Low | **Gemini 3.5 Flash** | Check release manifests, clean branches, tag release, update metadata. |

## 5-Day Parallel Developer Workflow

* **Track A (Routine / Docs / CI/CD -> Gemini 3.5 Flash)**: branch `feature/infra-docs`
* **Track B (Core Logic / TDD -> Gemini 3.1 Pro + Claude Sonnet)**: branch `feature/core-engine`

* **Day 1**: Validate baseline (209 tests, 98% coverage). Rename folders/files on Track A. Draft and implement `GlobalConfig` on Track B.
* **Day 2**: Draft Docusaurus docs and CI/CD yaml on Track A. Integrate logging and `BuildCacheManager` L2 cache on Track B.
* **Day 3**: Generate pipeline docs/Mermaid on Track A. Implement Library API facade and CLI subcommands on Track B.
* **Day 4**: Integrate Docusaurus build gates on Track A. Implement Typed IR models and generate bulk QA tests to hit 98% coverage on Track B.
* **Day 5**: Finalize release notes and run linting on Track A. Perform confidentiality audit, submodule pointer updates, and tag release on Track B.
