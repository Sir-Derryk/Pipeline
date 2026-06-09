# Task: TSK-INF-02 — Preparation of Doxygen XML Testing Assets

## 📌 Part 1: Implementation Guide
1. **Goal**: Set up a test fixture suite with static Doxygen XML assets and source files to validate parsing, macro/SWIG filtering, and requirements traceability (in alignment with project development Recommendation 2).
2. **Implementation Steps**:
   * Create the testing asset manager helper class `MockAssetLoader` in `tests/utils.py`.
   * Create a directory for raw testing mock source files: `tests/assets/src/`.
     * Add minimal synthetic code files (e.g., `MyClass.h` with compiler export macros like `NWDBEXPORT`, and `class_swig_wrapper.cs` containing `swigCPtr` fields or the `Dispose()` method).
   * Create a directory for Doxygen XML snapshots: `tests/assets/doxygen/`.
   * Add minimal, valid XML files simulating actual Doxygen outputs:
     * `index.xml` — root catalog mapping code entities.
     * `class_definition.xml` — standard C++ class definition containing fields and public methods.
     * `class_with_macros.xml` — class utilizing compiler export macros (`NWDBEXPORT`, `MAPEXPORT`, etc.) to verify automatic removal (`REQ-FUN-19`).
     * `class_swig_wrapper.xml` — class wrapping SWIG-specific metadata fields (`swigCPtr`, `swigCMemOwn`, `Dispose()`, `getCPtr()`) to verify filtration under specific switches (`REQ-FUN-20`).

## 🧪 Part 2: Verification & TDD Scenarios
1. **TDD Red Phase**:
   * Write unit test `tests/test_assets.py` attempting to initialize `MockAssetLoader().load_xml("index.xml")` and assert that it returns a non-empty string.
   * Verify that the loader successfully ingests newer assets: `class_with_macros.xml` and `class_swig_wrapper.xml`.
   * Run the test suite and confirm failure due to missing paths and helper modules.
2. **TDD Green Phase**:
   * Implement class `MockAssetLoader` in `tests/utils.py` using standard file I/O to read from `tests/assets/doxygen/`.
3. **TDD Refactor Phase**:
   * Run verification command:
     ```bash
     poetry run pytest tests/test_assets.py
     ```
   * **Expected Success Result**: Test suite is green, confirming correct resolution, loading, and streaming of all test XML fixtures.

## 👥 Part 3: User Acceptance Scenario
After the AI completes Part 1 (development) and Part 2 (test validation), you need to perform the final acceptance check:

1. **Run automated tests for manual validation**:
   Execute in your terminal:
   ```bash
   cd engine
   poetry run pytest tests/test_assets.py
   ```
   *Expected Result:* All assertions pass successfully (green status).

2. **Verify key task requirements**:
   * [ ] Verify the presence of the helper class `MockAssetLoader` in `tests/utils.py`.
   * [ ] Verify that testing XML files `index.xml` and `class_definition.xml` exist under `tests/assets/doxygen/`.
   * [ ] Verify that tests read these files and return their valid contents as XML string buffers.

3. **Verify path portability**:
   * [ ] Ensure that there are no hardcoded absolute developer paths in the codebase (all paths must resolve dynamically).

4. **Update compliance registry**:
   * [ ] Verify that the task status in `design-docs/docs/srs/task_compliance.md` is updated to reflect its current state and test coverage percentage.
