# Contributing to SkillCheck

Thanks for helping implement SkillCheck as **one coordinated software project**.

1. Read the [Master Specification](docs/requirements/SkillCheck_Master_Specification.md) before changing design or code. Respect all mandatory requirements and the agreed business contract.
2. Choose a Jira task with clear scope and acceptance criteria; use the documented issue key in the branch and PR.
3. Sync `main` and create `feat/WP-XX-name`, `fix/WP-XX-name`, `docs/WP-XX-name` or `chore/WP-XX-name`.
4. Make an atomic change. Use Conventional Commits (`feat(WP-XX): ...`, `fix(WP-XX): ...`, `docs(WP-XX): ...`).
5. Run relevant local checks, tests and documentation validation (`python scripts/check_repository.py`).
6. Open a PR with `.github/pull_request_template.md`, include Jira and Confluence links, describe safety/contract impact and request another teammate's review.
7. Merge through the configured workflow after checks pass, and update Jira with evidence.

The team proposes **GitHub Flow**; exact branch protection/settings await repository-owner approval. Do not use a direct push to `main` after bootstrap.

Changes to application architecture, scoring, security requirements, data ownership or instructor-defined requirements require an approved architecture decision record and an update to the shared Confluence Master Specification.

Read [complete Git workflow](docs/workflow/GIT_WORKFLOW.md) and [repo bootstrap instructions](docs/workflow/REPOSITORY_BOOTSTRAP.md).

**Warning:** do not disclose API keys or user audio/transcripts in commits, pull requests or public issue comments. Do not claim unrun tests are passing.
