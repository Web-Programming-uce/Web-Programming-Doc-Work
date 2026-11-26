# Initial repository bootstrap

**Who:** a member authorized by the organization to push the first commit to `https://github.com/Web-Programming-uce/Web-Programming-Doc-Work`. On 26 November 2026 the connected GitHub identity (`ByDarwinT`) was verified with the `write` collaborator role; a 403 on push still means the organization owner must grant access.

## On Windows PowerShell

Open PowerShell from a normal working directory, for example `C:\Proyectos` (create it if needed). These commands are **not** for Confluence or Jira.

```powershell
cd C:\Proyectos
git clone https://github.com/Web-Programming-uce/Web-Programming-Doc-Work.git
cd .\Web-Programming-Doc-Work
```

A warning that the repository is empty is normal. Extract the starter ZIP and copy the **contents** of its root folder into your newly cloned repository folder. Do not nest `SkillCheck_Repository_Starter_v1` inside the clone.

Now run from **inside** `C:\Proyectos\Web-Programming-Doc-Work`:

```powershell
python scripts/check_repository.py
git status
git add .
git commit -m "chore(repo): bootstrap SkillCheck monorepo"
git push -u origin main
```

If `main` does not yet exist locally, first run `git switch -c main`. If Git reports 403 or permission denied, **stop and ask the organization owner for Write permission**; do not push to another unrelated repository or rewrite remote history.

## Organization administration after the first push

1. Configure protection/ruleset for `main`: PR required, 1 approving reviewer, checks, conversation resolution, no force pushes.
2. Ensure all team contributors have appropriate access, and at least two trusted maintainers can administer project continuity.
3. Choose actual reviewer usernames before adding a CODEOWNERS file; do not guess them.
4. Enable GitHub Actions as allowed by the organization. Confirm the `Repository checks` workflow passes.
5. Link Jira tickets and the Confluence Master Specification in the README (already included).
6. Decide the license explicitly; do not assume that public visibility equals an open-source license.

## Subsequent work

```powershell
git switch main
git pull --ff-only origin main
git switch -c feat/WP-XX-description
# edit files and run relevant checks
git add .
git commit -m "feat(WP-XX): describe completed change"
git push -u origin feat/WP-XX-description
```

Open a PR targeting `main`, request another teammate's review, and update the Jira issue with its link. See `GIT_WORKFLOW.md` for the full policy.
