# ADR-0001 — Monorepo and collaboration baseline

- **Status:** PROPOSED (not yet formally ratified as a workflow policy)
- **Date:** 2026-11-26
- **Owners:** SkillCheck project team
- **Master:** https://uce-group-webprogramming.atlassian.net/wiki/spaces/WPS/pages/295265
- **Repository:** https://github.com/Web-Programming-uce/Web-Programming-Doc-Work

## Context

The teacher requires one monorepo, a Java Spring Boot backend, a React frontend, multi-platform clients, microfrontends and evidence in QA/PROD. The team needs one consistent place for code, documentation and PR reviews rather than disconnected personal projects.

## Proposed decision

Use the GitHub organization repository as a monorepo, with `main` protected after initial bootstrap and short-lived Jira-key branches reviewed through PRs. Use GitHub Actions for repository/documentation checks first; extend to frontend/backend builds and the mandated test categories as implementation becomes real.

- `apps/api` for Java 21 / Spring Boot.
- `apps/web` for React and microfrontend composition.
- `apps/site` for Astro.
- `apps/mobile` for Capacitor packaging.
- `apps/desktop` for Tauri packaging.
- `packages/*` for reusable frontend UI / schema assets.
- `infra` and `tests` for deployments and test evidence.

This decision records the repository/workflow proposal; it does not approve cloud spend, running services or production deployment.

## Alternatives

- **Long-lived GitFlow branches** (`develop`, `qa`, `main`): stronger ceremony but burdensome for a small course project and easy to drift.
- **Direct main commits:** quick at first, but weak review and unstable integration for several contributors.

## Consequences

- Positive: traceability to Jira, review gates, one technical baseline, easy instructor inspection.
- Trade-offs: initial protection setup, PR discipline, additional documentation and CI configuration.

## Acceptance / sign-off

- Product Owner: PENDING
- Architect: PENDING
- Backend lead: PENDING
- Frontend lead: PENDING
- Scrum/QA: PENDING
- Teacher clarifications: R23 SDD/ODD still unresolved
