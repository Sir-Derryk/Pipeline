# 📂 Chapter 4: Live Case Study & Deployment — Detailed Structure Blueprint

This document details the page tree and hierarchical heading structure for **Chapter 4: Live Case Study & Deployment** of the UDE VitePress Guides.

---

## 🗺️ Page Tree

```text
Chapter 4: Live Case Study & Deployment (/guides/)
├── case-study.md               # Self-documenting case study, junctions, self-config files.
└── admin-deployment.md         # Deployment manuals, GHA workflows, Ubuntu setup.
```

---

## 📑 Page & Heading Hierarchies

### 📄 Page 1: `case-study.md`

#### # Case Study: Building This Portal
*   *Description*: A detailed, real-world case study demonstrating how UDE uses "dogfooding" to document itself.

#### ## 🐕 The Dogfooding Concept
*   *Description*: The rationale behind compiling the UDE Python engine's own docstrings to generate `/api/` references within UDE's user documentation.

#### ## 📂 Local Workspace Directory Junctions
*   *Description*: How Windows directory links (junctions) are configured to link `user-docs/engine` to `../engine` for unified local testing.

#### ## 📑 Self-Configuration Block Walkthrough
*   *Description*: Analysis of `user-docs/ude_config_self.json` mapping.
    *   ### ### 1. Source Collectors & XML Destinations
    *   ### ### 2. Selecting the Hugo Markdown Renderer
    *   ### ### 3. Defining Submodule Target Roots

#### ## ⚙️ Build Order Orchestration (The Patch)
*   *Description*: Why Hugo must be built directly into VitePress's compilation folder (`.vitepress/dist/api/`) *after* VitePress finishes compiling, preventing routing errors (404s).

---

### 📄 Page 2: `admin-deployment.md`

#### # Admin & Automated CI/CD Deployment
*   *Description*: Operator manual for deploying and maintaining UDE portals inside production automated environments.

#### ## 🛠️ Admin Installation Specs
*   *Description*: Commands for pip, pipenv, and poetry installation.

#### ## 🤖 Continuous Integration Workflow
*   *Description*: Detailed breakdown of the automated pipeline runner (`deploy.yml`).
    *   ### ### Step 1: Submodule Checkouts & Authorization
        *   *Description*: Checking out multiple private/public submodules using access tokens.
    *   ### ### Step 2: Runner Environment Setup
        *   *Description*: Installing Doxygen on standard Ubuntu runners.
    *   ### ### Step 3: Python & Node.js Cache Strategies
        *   *Description*: Caching pip packages and npm node_modules to decrease runtimes to under 30 seconds.
    *   ### ### Step 4: Multi-Engine Compilations
        *   *Description*: Step-by-step trigger calls for `ude.cli`, `vitepress build`, and `hugo`.

#### ## 🌐 GitHub Pages Deployment
*   *Description*: Publishing the compiled bundle using pages action uploaders.

#### ## 📂 Multi-Tenant Hosting & SSO Options
*   *Description*: Discussion of future single sign-on (SSO) strategies for private enterprise documentation portals.
