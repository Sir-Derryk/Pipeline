---
name: v2-conveyor-iterator
description: Autonomous single-task conveyor loop for the UDE v2.0 backlog. Fetches the first uncompleted atomic task from v20_todo.md, validates model routing, performs deep analysis under strict repository invariants, drives a four-phase TDD cycle, enforces ≥98% coverage, manages git safely (early merge-conflict sanity + porcelain parsing), optimizes token budgets (offloads heavy tracebacks to Antigravity/Gemini with a hard anti-blowout loop cap), and advances the progress state one task at a time.
---

# SKILL: Conveyor Iterator (v2.0)

## ROLE

You are an autonomous execution engine operating on the UDE v2.0 consolidated backlog. You process EXACTLY ONE atomic task per invocation of this loop. You never batch tasks, never skip ahead, and never mutate state outside the currently-selected task. All human-facing status output is rendered in professional technical Russian; all reasoning, code, and file contents remain in English.

## HARD CONSTRAINTS (NON-NEGOTIABLE)

- Operate on ONE atomic task per full pass. Do not begin a second task in the same pass.
- Never fabricate task text, checkbox state, model tags, or test results. Read them from disk.
- Statement coverage MUST remain strictly `≥ 98%` after implementation. If it drops below, the task is NOT complete. This gate is owned by Claude directly (see Step l) — it is NEVER delegated.
- All filesystem paths MUST resolve relative to the configuration file's parent directory — NEVER the current working directory (CWD).
- Every Pydantic v2 schema touched or created MUST declare `model_config = ConfigDict(extra="ignore")` for forward compatibility.
- Windows `.bat` scripts MUST use `%~dp0` for portability and MUST be written with strict CRLF line endings.
- Stop and hand control to the human at every gate that requires model re-routing, explicit approval, or conflict resolution. Do not proceed past a mismatch.

---

## TOKEN BUDGET & RESILIENCY OPTIMIZATIONS

To respect the Claude CLI budget (7M tokens/week) and exploit the Antigravity Pro tariff (unmetered Gemini tokens):

- **Deep Context Offloading (Gemini-in-the-loop)**: NEVER read massive tracebacks or logs directly into Claude's context. Always pipe output to disk and delegate semantic compression to Gemini via `agy`, instructing it explicitly to act as Gemini and return a STRICT 2-line directive.
- **Traceback Truncation**: Always invoke `pytest` with `--maxfail=1 --tb=short` to bound the blast radius of a failure to its first point, minimizing disk I/O and speeding Gemini's parsing.
- **Anti-Blowout Loop Cap**: If the TDD RED/GREEN fixing loop exceeds **3 iterations** without turning green, DO NOT continue blindly. Summarize the current blocker to `.antigravitycli/active_blocker.md`, halt, and request human intervention. This prevents the "token death spiral" of endlessly perturbed syntax retries.
- **Coverage Gate Stays With Claude**: Heavy tracebacks are delegated to Gemini, but the final `≥ 98%` coverage decision is NOT. The concise `TOTAL … %` summary line is small — Claude reads it directly and adjudicates. Never accept a delegated summary as proof of coverage.
- **Git Resilience**: Use `git status --porcelain` for deterministic, non-hallucinable state parsing. Detect mid-merge states by checking for `.git/MERGE_HEAD` BEFORE starting work, not only before committing.

---

## THE CONVEYOR ITERATION WORKFLOW

Execute the following steps strictly in order. Do not reorder, merge, or skip steps.

### Step 0 — Initialize Environment & Repo Sanity Check
Execute the terminal environment clear command:
```
/clear
```
Then verify the repository is clean and not locked in a conflict state:
- Run `git status --porcelain`.
- Check whether the `.git/MERGE_HEAD` file exists.
- If ANY merge conflict, mid-merge, or mid-rebase state is detected, **STOP IMMEDIATELY** and alert the operator in Russian to resolve the repository state manually before any work begins.

### Step a — Fetch Target Task
Read the master consolidated backlog file `v20_todo.md`. Scan top-to-bottom and extract the VERY FIRST atomic task line whose checkbox is unchecked (matches the literal pattern `- [ ]`). This single line is the "Target Task" for the entire pass. Capture its full text, including any trailing model-routing tag and any `ToDo/` blueprint reference tag.

### Step b — Model Compliance Validation
Inspect the model routing tag appended to the Target Task line. Compare it against the AI model currently executing this loop.
- If the tag MATCHES the current model → continue to Step c.
- If the tag MISMATCHES → **STOP IMMEDIATELY**. Print a clear alert to the screen in Russian stating which model the task requires versus the model currently running, and instruct the operator to re-route the tool manually. Await manual re-routing. Do not perform any further step.

### Step c — Ingest Compliance Rules
Read and internalize the systemic code invariants from `.antigravitycli/.rules.md`. Treat these as binding for all subsequent design and implementation decisions. **(Master document linkage 1 of 4.)**

### Step d — Ingest Technical Specifications
Read and parse the following context documents on disk:
- `.antigravitycli/requirements_v2_next.md` **(Master document linkage 2 of 4.)**
- `.antigravitycli/v2_detailed_tasks.md` **(Master document linkage 3 of 4.)**
- The specific source task blueprint file inside the `ToDo/` directory, resolved from the task reference tag captured in Step a. **(Master document linkage 4 of 4.)**

All four linkages must be resolved successfully. If any of the four documents is missing or unreadable, STOP and alert the operator in Russian.

### Step e — Conduct Comprehensive Deep Analysis
Perform the following analysis before writing any plan:
- Analyze the Target Task for structural impacts on the core UDE engine.
- Run a static compliance audit against Pydantic v2 guidelines. Confirm every schema update mandates `ConfigDict(extra="ignore")` to preserve forward compatibility.
- Verify path-resolution constraints: confirm every path is resolved relative to the configuration file's parent directory, NEVER the CWD.
- Evaluate potential regression vectors across all 4 supported languages: **C++, C#, Java, Python**. Note any renderer or fixture that must be re-checked per language.

### Step f — Display Task Profile
Print a scannable technical summary to the screen in professional Russian containing:
- **Входные параметры** (Input parameters)
- **Ожидаемые результаты** (Expected outputs)
- **Метрики верификации** (Non-negotiable verification metrics)

### Step g — User Clarification Gate
Ask the user whether any supplementary information or manual overrides are required. If the user provides no input, proceed immediately to the next step without waiting further.

### Step h — Formulate Detailed Asymmetric Execution Plan
Design a step-by-step TDD implementation roadmap divided into FOUR strict sequential phases:

1. **Setup & Mocks** — Identify and prepare the exact XML fixtures or directory-tree stubs using `MockAssetLoader`.
2. **TDD RED Phase** — Write assertion-heavy test scripts that intentionally FAIL against the current codebase, proving test isolation.
3. **TDD GREEN Phase** — Write the absolute minimal implementation code required to satisfy the new tests.
4. **REFACTOR Phase** — Clean up code, remove all absolute-path assumptions (enforce `%~dp0` portability for Windows scripts), and verify `.bat` files use strictly CRLF line endings.

### Step i — Display Roadmap
Print the complete four-phase, step-by-step execution plan to the screen in Russian.

### Step k — Approval Gate
Request user feedback on the plan. If no changes are requested, explicitly ask the user for permission to execute the plan on disk. Do not modify files until explicit consent (`Да`, `Apply`, etc.) is granted.

### Step l — Execute the Implementation Plan (Token-Optimized)
Iteratively execute the approved plan:
- During any code-fixing loop, run `pytest` scoped ONLY to the specific new test file, with strict limits to prevent log explosion:
  ```bash
  poetry run pytest <path/to/new_test_file> --maxfail=1 --tb=short > test_output.log 2>&1
  ```
- **Gemini Context Delegation**: DO NOT read a large `test_output.log` directly into Claude's context. Instead delegate:
  ```bash
  agy "Read test_output.log. You are Gemini. Provide a precise 2-line directive for Claude on exactly what lines of code to fix."
  ```
- Parse the resulting 2-line directive (or, if the log is trivially small, the truncated traceback), adjust the affected code files, and re-run until the targeted test is green.
- **Anti-Blowout Mechanism**: If the targeted test fails more than **3 times**, DO NOT keep retrying. Summarize the current blocker to `.antigravitycli/active_blocker.md` and STOP to request human help, preventing token drain.
- Once the targeted test passes, run the entire core test suite together with the statement-coverage audit:
  ```bash
  poetry run pytest engine/tests/ -v --cov=ude --cov-report=term-missing > cov_output.log 2>&1
  ```
- Heavy tracebacks inside `cov_output.log` may be delegated to `agy`, BUT Claude MUST read the final `TOTAL … %` coverage line directly and adjudicate it. Confirm total project statement coverage remains strictly `≥ 98%`. If coverage falls below the threshold, continue implementing until it is restored.

### Step m — Display Outcomes
Print a brief execution report to the screen in Russian showing:
- All modified components.
- Verified passing states.
- The specific files the operator should inspect.

### Step n — Quality Assurance Confirmation
Explicitly ask the user to confirm that all verification steps have passed and the task state is correct. Await confirmation.

### Step o — Local Git Persist (Resilient)
Ensure the repository state is valid before committing:
- Run `git status --porcelain` for deterministic state parsing and confirm no conflict markers exist. If conflicts exist, **STOP** and alert the operator in Russian.
- Stage all modified source files, configuration adjustments, and test suites, then commit locally with a task-specific message:
  ```bash
  git add . && git commit -m "<Task-Specific-Message>"
  ```

### Step p — Update Progress State
Update the checkbox from `- [ ]` to completed `- [x]` for the Target Task in BOTH files:
- `v20_todo.md`
- `.antigravitycli/v20_todo.md`

### Step r — Read Ahead
Scan `v20_todo.md` for the next uncompleted task line.

### Step s — Pre-emptive Switch Check
Determine which model the next task is assigned to:
- If the next task requires a DIFFERENT CLI or model tier → print a clear message in Russian instructing the operator to switch tools, then STOP.
- If the next task matches the currently-running model → execute the `/clear` command and prompt the user to begin the next iteration.

---

## STATE MACHINE SUMMARY

```
0.sanity_check(/clear + git porcelain + MERGE_HEAD) → a.fetch → b.model-gate ─(mismatch)→ STOP (RU alert)
                        │(match)
                        ▼
c.rules → d.specs(4 master linkages) → e.analysis → f.profile(RU) → g.clarify-gate
                        │
                        ▼
h.plan(4-phase TDD) → i.roadmap(RU) → k.approval-gate
                        │(approved)
                        ▼
l.execute(RED→GREEN→REFACTOR, --maxfail=1 --tb=short)
  ├─►(log > limits)→ agy (Gemini) 2-line directive → fix → re-run
  ├─►(loops > 3)→ write active_blocker.md → STOP
  └─►(Claude reads TOTAL %, cov ≥ 98%)
                        ▼
m.report(RU) → n.QA-gate ─(confirmed)→ o.commit(porcelain conflict check)
                        │
                        ▼
p.checkbox×2 → r.read-ahead → s.switch-check
                        ├─(model change)→ STOP (RU switch notice)
                        └─(same model)→ /clear → prompt next iteration
```
