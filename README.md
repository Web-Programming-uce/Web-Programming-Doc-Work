# SkillCheck — Improvement and Discovery of Soft Skills

> **Status (26 November 2026):** Documentation and proposed monorepo structure only. No running application, CI success or deployed environment is claimed.

SkillCheck helps university students and job seekers practice spoken communication through 60–90-second challenges, transparent 30/40/30 assessment, progress history, and AI-assisted recommendations. The product is intended to support web, mobile and desktop experiences from a coordinated codebase.

## Project links

- **Official source repository:** https://github.com/Web-Programming-uce/Web-Programming-Doc-Work
- **Team Master Specification:** https://uce-group-webprogramming.atlassian.net/wiki/spaces/WPS/pages/295265
- **Architect / system design:** https://uce-group-webprogramming.atlassian.net/wiki/spaces/WPS/pages/328245
- **Jira project:** https://uce-group-webprogramming.atlassian.net/jira/software/projects/WP

## Mandatory technical boundaries

The requirements in [`docs/requirements/SkillCheck_Master_Specification.md`](docs/requirements/SkillCheck_Master_Specification.md) govern the system. The teacher requires Java Spring Boot and React, a monorepo, microfrontends, multiple client platforms, four distinct databases including cache/document types, AWS plus PaaS, Docker/Docker Hub, GitHub Actions tests and OWASP controls. Some architectural selections are still working proposals awaiting formal ratification.

The target **backend** is Java 21 / Spring Boot. Node.js is allowed for frontend build tooling; it does not replace the required backend.

## Repository structure

| Folder | Scope | Current state |
| --- | --- | --- |
| [`apps/api/`](apps/api/) | Spring Boot backend and APIs | Documentation-only placeholder |
| [`apps/web/`](apps/web/) | React + TypeScript web shell and microfrontends | Placeholder |
| [`apps/site/`](apps/site/) | Astro site | Placeholder |
| [`apps/mobile/`](apps/mobile/) | Capacitor packaging for the shared client | Placeholder |
| [`apps/desktop/`](apps/desktop/) | Tauri packaging for the shared client | Placeholder |
| [`packages/`](packages/) | UI and API contracts | Placeholder |
| [`infra/`](infra/) | Docker, cloud and infrastructure | Placeholder |
| [`tests/`](tests/) | Test strategy and suites | Placeholder |
| [`docs/requirements/`](docs/requirements/) | Master Specification and historical PDF snapshot | Available |
| [`docs/sprint-1/`](docs/sprint-1/) | WP-20, WP-21, WP-30, WP-31 documents and diagrams | Available |
| [`docs/workflow/`](docs/workflow/) | GitHub Flow, repo bootstrap and team practices | Available |
| [`docs/decisions/`](docs/decisions/) | Architecture decision records (`ADR-0001` format) | ADR-0001 proposed |
| [`docs/architecture/`](docs/architecture/) | System-level architecture documents | Placeholder |
| [`scripts/`](scripts/) | Dependency-free repository validation | Available |

**For a teacher review:** the current deliverables are the Master Specification and Sprint 1 architecture/technology/AI/security documentation. The application folders are planned structure, not completed code.

## How to contribute

1. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and the [team workflow](docs/workflow/GIT_WORKFLOW.md).
2. Follow the corresponding Jira issue and the Master Specification.
3. Work in a short-lived branch named after the Jira issue, not directly in `main` after bootstrap.
4. Open a PR with the provided template and include tests/evidence and reviewer approval.

## Bootstrap / setup

This repository was empty when reviewed. The initial commit must be performed by an authorized member of the GitHub organization with write access. Instructions: [`docs/workflow/REPOSITORY_BOOTSTRAP.md`](docs/workflow/REPOSITORY_BOOTSTRAP.md).

**Security:** do not commit secrets, user recordings, transcripts, access tokens, private documents, or real payment credentials. Stripe is test mode only.

**License:** not selected yet; public visibility is not equivalent to an open-source license.
