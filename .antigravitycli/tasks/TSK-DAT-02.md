# Task: TSK-DAT-02 — Gzip Compression of Disk Caches (.json.gz)

## 📌 Part 1: Implementation Guide
1. **Goal**: Implement transparent compression and decompression for serialized IR structures on disk using Gzip, optimizing disk footprints and preventing Git pollution in line with `REQ-BUS-03` and `REQ-FUN-11`.
2. **Implementation Steps**:
   * Create file `ude/storage.py`.
   * Implement helper functions:
     * `save_compressed_ir(catalog: ProjectCatalog, file_path: str)`: Serializes a Pydantic model into JSON, compresses it on-the-fly using the `gzip` module, and writes it to disk with a `.json.gz` extension.
     * `load_compressed_ir(file_path: str) -> ProjectCatalog`: Reads a compressed file, decompresses it in memory, and parses it back into a typed `ProjectCatalog` instance.

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_storage.py`.
   * Verify:
     1. Writing a catalog model to a temporary file path `tests/scratch/temp_ir.json.gz`.
     2. Checking that the physical file is indeed a Gzip-compressed archive (asserting gzip magic header bytes).
     3. Loading the compressed file back and asserting that the deserialized object is equivalent to the original `ProjectCatalog`.
   * Verify tests fail due to missing modules.
2. **TDD Green Phase**:
   * Implement `save_compressed_ir` and `load_compressed_ir` in `ude/storage.py` using standard `gzip` and `json` libraries.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_storage.py
     ```
   * **Expected Success Result**: Test suite is green, verifying lossless compression and transparent disk serialization/deserialization.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_storage.py
   ```
   *Expected Result:* Tests pass successfully, proving binary equivalence and integrity of serialized caches.

2. **Verify key task requirements**:
   * [ ] Verify functions `save_compressed_ir` and `load_compressed_ir` are implemented inside `ude/storage.py`.
   * [ ] Verify that serializing a catalog writes a binary Gzip-compressed file with `.json.gz` extension.
   * [ ] Confirm that loading a compressed catalog decompresses files transparently, restoring the validated Pydantic models.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
