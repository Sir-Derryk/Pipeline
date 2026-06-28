# Architectural Styles and Paradigms

This document defines the primary architectural paradigms and design principles of the UDE codebase.

---

## 🏛️ 1. Object-Oriented Programming (OOP)

**Object-Oriented Programming (OOP)** is chosen as the unified primary programming paradigm for all project components (both in **Python** and **TypeScript**).

This ensures codebase consistency and simplifies reading and maintenance for developers writing in different languages.

### Key OOP Principles:
1.  **Encapsulation**:
    *   All internal states of classes (e.g., build configurations, parser intermediate structures) must be hidden from direct external access. They must be accessed via getters/setters or specialized public methods.
2.  **Inheritance and Polymorphism**:
    *   **Common Base Classes**: Creation of abstract classes or interfaces for key components (e.g., the base class `Parser` or `Collector`), from which specific implementations for different product types or languages inherit.
    *   **Unified Contract**: Polymorphic method calls (e.g., calling `.collect()` on all registered collectors) provide flexibility to the generation pipeline.
3.  **Decomposition**:
    *   Each class must solve one clearly defined task (the Single Responsibility Principle from SOLID). For example, the `ConfigLoader` class is only responsible for reading and validating settings, while `HtmlRenderer` is only responsible for building pages from templates.

---

## 🏗️ 2. Design Patterns and Logical Structure

To implement the object-oriented architecture, it is recommended to use proven design patterns:

*   **Factory Method / Abstract Factory**:
    - Used to instantiate parsers, processors, and renderers depending on the passed configuration (e.g., creating a C++ collector or a Java collector).
*   **Strategy**:
    - Isolating parsing or rendering algorithms into separate strategy classes for convenient on-the-fly logic replacement without modifying the main orchestrator code.
*   **Template Method**:
    - Defining the general skeleton of the documentation generation pipeline in the base orchestrator class with specific steps overridden in subclasses.

---

## 🌐 3. Asynchronous Architecture and Integration

Although OOP is the primary paradigm, an asynchronous approach is actively used in the code (especially in TypeScript) for parallel processing of large datasets:

*   **TS Promises & async/await**: All I/O operations (file reading, parsing, writing completed HTML) must be performed asynchronously to avoid blocking the main execution thread.
*   **Thread Isolation**: When building large documentation projects, tasks can be distributed across parallel processes/threads (worker threads) to speed up computations.
