# Architecture decision records

Decision identifiers use four digits everywhere: `ADR-0001`, `ADR-0002`, and so on. The format is shared by this folder and the team approval register in the Master Specification (Section 10.1).

| ID | Decision | Status | File |
| --- | --- | --- | --- |
| ADR-0001 | Monorepo and collaboration baseline | PROPOSED | [ADR-0001](ADR-0001-proposed-architecture-and-workflow.md) |
| ADR-0002 – ADR-0011 | Reserved identifiers listed in the Master approval register | PENDING | No file yet |

## Rules

- A record is approved only when its own status says so and the required owners have signed off. `PROPOSED` is not approval, and a row in the register is not evidence of a decision.
- Reserved identifiers keep numbering stable; they must not be cited as approved decisions.
- Create one file per ratified decision using `ADR-XXXX-short-title.md` (four digits in place of `XXXX`), and update the Master approval register and this index in the same pull request.
- Architecture or business-rule changes need an ADR plus a coordinated Master Specification update; see [`../workflow/GIT_WORKFLOW.md`](../workflow/GIT_WORKFLOW.md).
