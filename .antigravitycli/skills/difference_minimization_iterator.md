---
name: difference-minimization-iterator
description: >-
  Iterative diagnostic and development workflow for reducing formatting, structural, 
  and semantic differences between UDE compiled outputs and legacy Docomatic references 
  using Golden Master and alignment suite test feedback.
---

# Skill: Golden Master and Docomatic Difference Minimization Iterator

## 🎯 Core Philosophy
To systematically achieve alignment between the Universal Documentation Engine (UDE) and the legacy Docomatic output, the agent must avoid trying to solve multiple unrelated differences at once. 

Instead, follow a strict, single-focused iterative cycle: **Isolate exactly ONE discrepancy, clarify if it is an acceptable deviation or a bug, apply the appropriate action, verify, and ask the user how to proceed.**

---

## ⚙️ Step-by-Step SOP (The Minimization Loop)

Follow these steps in a recursive, user-guided loop to reduce differences:

### Step 1: Run Diagnostics
Run the Docomatic Semantic Alignment tests inside the `engine` environment to generate an up-to-date difference report:
```powershell
poetry run pytest engine/tests/test_docomatic_alignment.py
```
Locate the generated language-specific discrepancy report (e.g., `difference_mock_sdk_{lang}.json`).
> [!TIP]
> **Total Count Tracking**: The first key inside every generated discrepancy report is `"total_differences"`. You can open or parse the first few lines of the JSON file to get the exact current count of active mismatches instantly without loading the full file.

### Step 2: Isolate & Gate (Allowance Check)
Open the discrepancy report, analyze the mismatches, and **select exactly one specific difference** to focus on.
1. Explicitly present the details of the chosen mismatch in the chat (its path, legacy output vs. current UDE output).
2. **Mandatory Allowance Check**: Before conducting any technical analysis or attempting a code fix, you MUST clarify with the user whether this mismatch is an acceptable deviation (allowance) or a bug that needs to be fixed.
3. **Strict Double-Confirmation Gating**:
   * **First Confirmation**: Ask the user in the chat *(use the session's active language)*:
     > **EN**: "Can we add this as an accepted deviation (allowance)?"
     > **RU**: "Можно ли добавить это в допущения?"
   * **Second Confirmation**: If the user replies affirmatively, ask once more:
     > **EN**: "Are you certain this should be registered as a permanent allowance?"
     > **RU**: "Вы уверены, что мы можем добавить это в допущения?"
   * Accept "yes", "да", "confirm", "approved" as affirmative — reject "maybe", "probably", "I think so".
   * **Action upon Approval**: Only if the user responds affirmatively to BOTH questions consecutively, you are authorized to update the allowances database and regenerate baselines:
     ```powershell
     $env:UPDATE_ALLOWANCES="1"
     poetry run pytest engine/tests/test_docomatic_alignment.py
     poetry run python Tests/prepare_baseline.py
     ```
     Once complete, skip directly to **Step 6**.
   * **Action if Rejected**: If the user states that it is NOT an allowance, it is a bug. Proceed directly to **Step 3** to begin the bug-fixing flow.

### Step 3: Root-Cause Analysis (For Bugs)
Trace the isolated bug to its exact origin in the UDE engine codebase:
- **Sidebar & ToC Structure**: Map to `engine/ude/renderers/static_html.py` (HTML) or `engine/ude/renderers/hugo_markdown.py` (Hugo tree building/pruning).
- **Naming, Routing & Capitalization**: Map to parser logic in `engine/ude/parsers/doxygen.py` or signature strategizer strategies in `engine/ude/strategies/`.
- **Text & Code Formatting**: Map to Jinja2 templates in `engine/ude/templates/` or docstring normalizers in `engine/ude/processors/`.
- **Doxyfile / Input Collection Difference** *(v2.0+)*: Map to `engine/ude/collectors/doxyfile.py` — specifically `merge_doxyfile_tiers()` if the issue is wrong INPUT paths or GENERATE_XML settings.
- **Global Config / Log Level / Doxygen Path Difference** *(v2.0+)*: Map to `engine/ude/config.py` — `GlobalConfig.log_level` or `apply_global_cfg_env()` if Doxygen binary resolution changed output paths.
- **Coverage-Gated Output Missing** *(v2.0+)*: Map to `engine/ude/coverage.py` — `apply_coverage_gate()` suppressing output silently when `coverage_mode` or `coverage_threshold` is misconfigured.
- **L2 Cache Stale Hit Producing Stale Output** *(v2.0+, CRITICAL)*: If the discrepancy appears in the second or later build run ONLY, suspect the L2 cache. **Before any code fix**: clear the cache directory and re-run diagnostics. If the discrepancy disappears, the root cause is a stale L2 entry, not a renderer bug. Do NOT write any renderer code until the cache hypothesis is ruled out.

### Step 4: Propose Resolution (Consent-First)
Formulate the minimal code/template change required to resolve this specific bug. 
- Show the exact code diff to the user in the chat.
- Request the user's explicit consent before writing any changes to disk.

### Step 5: Verify and Check Coverage
Once the user approves and the bug-fix is written to disk:
1. Run the local unit test suite to verify code health and ensure statement coverage is `>= 98%`:
   ```powershell
   poetry run pytest
   ```
2. Re-run the alignment test suite to confirm that the chosen difference has successfully disappeared and the overall discrepancy count decreased:
   ```powershell
   poetry run pytest engine/tests/test_docomatic_alignment.py -v --tb=short
   ```
3. **Cross-Language Regression Check** *(mandatory after any change to shared renderer base classes or Jinja2 templates)*: If the fix touched any file in `engine/ude/renderers/` (not a language-specific subclass only) or any `.html`/`.j2` template, verify the full-language alignment suite:
   - Inspect the `"total_differences"` key in each language's discrepancy report.
   - If the total differences count INCREASED for any language that was NOT being worked on, the fix introduced a cross-language regression and MUST be reverted before proceeding.

> [!NOTE]
> **Golden Master Exception Lists**:
> If a change temporarily or permanently modifies generated output structures or file contents, the Golden Master regression tests (`test_golden_master_pipeline` in `engine/tests/test_golden_master.py`) might fail.
> To prevent tests from failing during intermediate development phases or when working on specific files, you can use the `exceptions` list parameter in the Golden Master test.
> - **How it works**: Pass a list of relative file paths, basenames, or patterns to the `exceptions` fixture or parameter in `test_golden_master.py`.
> - If any structural (missing/extra files) or content differences are found strictly within the excepted files, the Golden Master regression test will treat it as acceptable and **will not crash**.
> - Use this option carefully to bypass strict assertions on in-progress files, while keeping the rest of the regression suite fully green.

### Step 6: User-Gated Continuation
After completing the cycle for the selected difference (either by adding it to allowances in Step 2, or fixing it in Step 5):
1. Present the updated alignment statistics (e.g., remaining differences count) to the user.
2. **Golden Master Baseline Check**: If a bug fix was applied in Step 5 that changed the output structure or file contents, explicitly ask the user in the chat *(use the session's active language)*:
   > **EN**: "The fix changed output structure or file contents. Shall I regenerate the Golden Master baselines?"
   > **RU**: "Нужно ли обновлять эталон (образец) Золотого стандарта?"
   * **Action upon Approval**: If the user responds affirmatively, update the Golden Master baselines:
     ```powershell
     $env:UPDATE_BASELINES="1"
     poetry run pytest engine/tests/test_golden_master.py
     ```
3. **Explicitly ask the user what to do next**:
   * Ask whether you should proceed to isolate and resolve the next mismatch, or stop/pause the minimization process here.
4. Wait for the user's response before executing any further commands or starting another iteration.

---

## 📋 Common Discrepancy Patterns & Reference Fixes

| Discrepancy Symptom | Probable Cause | Recommended Fix |
| :--- | :--- | :--- |
| **Missing Class Member folders** | Emptiness pruning algorithm is too aggressive or missed a member type. | Check child-node count checks in `prune_empty_folders` inside `static_html.py`. |
| **Mismatched entity file paths** | Difference in translation of symbols like `&`, `*`, or `< >`. | Add or correct mappings in `special_characters_translation` under the language's strategy class. |
| **Differing member list order** | Legacy Docomatic sorts members alphabetically, whereas UDE sorts by type first. | Update sorting algorithms in the target Strategy or Renderer to match legacy order if strict alignment is requested. |
| **Tag nested tables output diff** | SWIG wrapper docstring parsing missing type mapping brackets. | Refactor RST parser in `docstring.py` to handle nested parameter bracket conversions. |
| **Stale output on 2nd+ build run only** | L2 cache has a stale entry from a prior run. | Clear the cache directory, re-run diagnostics. If discrepancy disappears, root cause is cache, not code. See Step 3 L2 Cache entry. Do NOT write renderer code until the cache hypothesis is ruled out. |
| **Missing typed entity section (Constants, TypeAliases)** | Typed IR models (GAP-03) not wired to renderer, or template does not iterate the new collections. | Check `entity.constants`, `entity.type_aliases` iteration in `static_html.py` or the relevant Jinja2 template. |
| **Doxyfile-driven input path mismatch** | `merge_doxyfile_tiers()` in `doxyfile.py` let T2 override T3 runtime INPUT setting. | Verify T3 keys always win; check argument order in `merge_doxyfile_tiers()` call site in `doxygen.py`. |
| **Empty output after global config change** | `apply_coverage_gate()` blocking render in `reject-undocumented` mode with a threshold too high for the current catalog. | Check `GlobalConfig.coverage_mode` and `coverage_threshold` values in the active global config JSON file. |
