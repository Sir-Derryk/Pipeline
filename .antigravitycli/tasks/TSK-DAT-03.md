# Task: TSK-DAT-03 — Two-Level Incremental Build Cache Manager (.build_cache.json.gz)

## 📌 Part 1: Implementation Guide
1. **Goal**: Optimize local builds and CI/CD compiler speeds by introducing a two-level cache to skip parsing unchanged XML files and writing unchanged Markdown/HTML outputs to disk (`REQ-FUN-26`, `REQ-FUN-27`).
2. **Implementation Steps**:
   * Create `BuildCacheManager` inside `ude/storage.py`, persisting cache states as compressed archives named `.build_cache.json.gz` inside targeted product directories.
   * **Level 1 (Parsing Cache)**:
     * Record for each ingested XML source file its path, modification timestamp (`mtime`), file size, content SHA-256 hash, and serialized IR output.
     * During parsing, if the file's metadata and hash match the cache, load the entities directly from the cache, skipping XML processing.
   * **Level 2 (Rendering Cache)**:
     * Record for each target output file the hash of its corresponding IR entity signature combined with the SHA-256 hash of the Jinja2 template utilized.
     * During rendering, if hashes align and the target file physically exists on disk, **skip the disk write operation**. This reduces disk I/O and prevents trigger cascades in Hugo/Docusaurus.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_caching.py`.
   * Feed a sample XML file, execute parsing/rendering twice, and assert that the second run results in zero XML parsing operations and zero disk writes. Verify tests fail since the caching system is unintegrated.
2. **TDD Green Phase**:
   * Implement `BuildCacheManager` and integrate its checks inside the parser and renderer pipelines.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_caching.py
     ```
   * **Expected Success Result**: Test suite is green, proving the caching manager accurately bypasses redundant processing and writes.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_caching.py
   ```
   *Expected Result:* Tests pass successfully, verifying that unchanged inputs bypass disk writing routines (incrementalism).

2. **Verify key task requirements**:
   * [ ] Verify the presence of class `BuildCacheManager` in `ude/storage.py`.
   * [ ] Verify that secondary parsing and rendering of unchanged sources perform zero physical file writes or XML parses.
   * [ ] Verify that cache databases are written as `.build_cache.json.gz` inside product target directories.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
