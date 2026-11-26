# GitHub Repository & Collaboration Workflow

**Project:** SkillCheck — Improvement and Discovery of Soft Skills  
**Repository:** https://github.com/Web-Programming-uce/Web-Programming-Doc-Work  
**Status:** Proposed process, pending team adoption and GitHub configuration.  
**Scope:** Shared team ownership; applies to all contributors and development agents.  

## 1. Source of truth and traceability

- **Confluence Master Specification:** project requirements, business rules, architecture baseline and approved decisions. https://uce-group-webprogramming.atlassian.net/wiki/spaces/WPS/pages/295265
- **Jira:** one issue per planned unit of work, assignee, review status, sprint, evidence and acceptance criteria. https://uce-group-webprogramming.atlassian.net/jira/software/projects/WP
- **GitHub:** the real version-controlled source of code, documentation snapshots, CI configuration and PR discussions.
- Link every PR to an appropriate Jira key and link merged implementation evidence in Jira. Do not duplicate Jira's backlog as separate GitHub issues unless the team explicitly decides otherwise.
- Architectural or business-rule changes need a recorded decision (ADR) and a coordinated update of the Master Specification; neither agents nor individual contributors may silently redefine the product.

## 2. GitHub Flow for a small team

**Proposal:** Use short-lived branches and code review rather than maintaining long-lived `develop`, `qa` and `prod` branches. QA and PROD are separate environments and evidence gates, not necessarily branch names. The proposal awaits team ratification and is recorded as `ADR-0001`.

1. Start from a synchronized `main` and read the relevant Jira issue and Master Specification.
2. Create a short-lived branch named `feat/WP-XX-feature`, `fix/WP-XX-bug`, `docs/WP-XX-topic`, `test/WP-XX-topic` or `chore/WP-XX-topic`.
3. Make the smallest change that meets the issue's acceptance criteria, with tests and docs.
4. Commit with Conventional Commits, e.g. `feat(WP-42): add challenge list endpoint` or `docs(WP-21): clarify data stores`.
5. Open a PR into `main` using the included template. Include a linked Jira issue, scope, test evidence and security/contract impact.
6. Obtain one review from a different contributor in the affected area. Resolve comments and pass configured CI checks.
7. Squash-merge after approval. Delete the branch, update Jira with the merged PR, and synchronize linked Confluence/ADR pages when required.

**No direct pushes to main after the initial bootstrap.** Never force-push shared branches, commit credentials, or bypass review to meet a deadline.

## 3. Roles and review ownership

| Area | Expected review responsibility |
| --- | --- |
| Product Owner / UI/UX | User flows, access rights, Free vs. Premium demo, scoring rules, UX acceptance |
| Architect | System boundaries, APIs, major technology changes, security design impacts |
| Backend | Java/Spring Boot, persistence, authentication enforcement and third-party APIs |
| Front-end | React microfrontends, shared UI, microphone and platform packaging |
| Scrum / QA | Jira traceability, release evidence, acceptance checks, CI status |

These are **review areas**, not new Jira assignments. Assign actual reviewers using the team's GitHub usernames after membership is verified. Do not add guessed usernames to `CODEOWNERS`.

## 4. Branch protection and merge controls

After the initial commit, the repository's administrator should configure **Settings → Rules → Rulesets** (or Branch protection) for `main`:

- Require pull requests before merging and at least **one** approving review, ideally by someone other than the PR author.
- Require all applicable status checks, including `Repository checks` from the initial workflow.
- Require conversations to be resolved; disallow force-push and branch deletion.
- Restrict broad bypass permissions and ensure collaborators have only the access they need.
- Enable squash merge if that option is available and accepted by the team.

Rules are **recommendations until configured**. They cannot be enforced from Markdown alone.

## 5. CI/CD and QA/PROD evidence

### Initial documentation baseline

The supplied `.github/workflows/repository-checks.yml` runs `scripts/check_repository.py` on pull requests and pushes to `main`. It verifies that required documentation and module descriptions exist and are nonempty. This is **not** a production build or a completed test suite.

### Development gates (future implementation)

- Frontend: TypeScript typecheck, lint, unit and component/functional tests.
- Backend: `mvn -B verify` using Java 21, unit tests, integration/API contract tests, and vulnerability analysis.
- End-to-end: Playwright through the challenge/record/result flow against QA services and safe test data.
- Load: documented workloads, p95 latency and bottleneck evidence without paid inference or real payment charges.
- Security: secrets scanning, OWASP-aligned tests, authorization and RAG isolation checks.
- Containerized builds: Docker image build and versioned publication to Docker Hub **only when configured and authorized**.
- Deployment: GitHub Environments named QA and PROD with separate secrets and approvals; publish evidence for each without claiming production HA from free-tier infrastructure.

Ensure any mandatory checks are configured only after those jobs exist; otherwise every PR could remain blocked indefinitely.

## 6. Documentation and decision changes

- Update the relevant source Markdown in `docs/` along with code changes, not afterward in an unrelated task.
- Keep the Confluence Master Specification the governing product/requirements record. Versioned repo files are snapshots and must be reconciled with Confluence through a documented PR.
- A proposed architecture change needs an ADR with context, options, risks, status and approval. Publishing a proposed ADR does not automatically approve it.
- Do not erase historical requirements or suggest that QA/PROD checkmarks in the teacher's original list mean tests have passed.

## 7. Security and secrets

- Commit **no** `.env` files, private keys, access tokens, user audio, transcripts, private uploaded documents, user exports or production credentials.
- Use GitHub Actions Secrets / Environments or an approved external secrets manager after cloud accounts are established.
- Use test-only Stripe credentials and synthetic data. Never store real payment details.
- Limit access to user records, vector search results and documents according to roles and user ownership.
- For public repositories, documentation and screenshots must not expose student personal information, credentials or private Confluence content unless authorized for publication.

## 8. Pull request definition of done

A PR is ready to merge only when:

- [ ] Jira issue and acceptance criteria are linked.
- [ ] Implementation/technical decisions align with the current Master Specification.
- [ ] Tests/checks appropriate to this change have been executed and reported.
- [ ] Documentation, ADR and Confluence impacts are recorded.
- [ ] Security, access and secrets exposure were reviewed.
- [ ] One other contributor has reviewed and approvals/checks are satisfied.
- [ ] The merge and final evidence are linked back to Jira.

A document or directory being present is **not evidence that an application exists or a service runs**.

## 9. Initial repository setup

The repository was empty when reviewed on 26 November 2026. The first commit requires GitHub **write** permission in the organization. On 26 November 2026 the connected GitHub account (`ByDarwinT`) was verified with the `write` collaborator role through the GitHub API; the push itself remains the definitive confirmation.

1. Download and extract `SkillCheck_Repository_Starter_v1.zip`.
2. Clone the empty GitHub repository using an authorized account, then copy the **contents** of the extracted starter folder into the clone.
3. Run `python scripts/check_repository.py` and confirm it succeeds.
4. Stage the files, commit `chore(repo): bootstrap SkillCheck monorepo`, and push to `main`.
5. Enable branch protection, invite/access-check the team, then require all future changes through issue-named PRs.

See `docs/workflow/REPOSITORY_BOOTSTRAP.md` for specific terminal commands.
