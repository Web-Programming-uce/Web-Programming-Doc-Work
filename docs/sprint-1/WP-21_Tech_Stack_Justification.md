---
title: "WP-21 | Technology Stack Justification and Architecture Decision Record"
project: SkillCheck | Improvement and Discovery of Soft Skills
owner: Darwin Toapanta
issue: WP-21
version: 1.0-review
status: Review-ready / pending team ratification
baseline: SkillCheck Master Project Specification 1.0-RC1
prepared: 26 November 2026
---

# WP-21 — Technology Stack Justification

## Decision paper | Sprint 1

**Project:** SkillCheck — Improvement and Discovery of Soft Skills  
**Work item:** WP-21 · Tech Stack Justification (Research)  
**Owner:** Darwin Toapanta  
**Status:** **REVIEW-READY — Technical recommendation, not a team-approved ADR**  
**Scope:** Technology choices, alternatives, trade-offs, traceability, adoption gates and evidence for future QA/PROD. No provisioning or implementation has occurred.

> **Executive decision:** Design SkillCheck as a Java Spring Boot / React product with modular React microfrontends, an Astro public site, Capacitor mobile and Tauri desktop clients, Keycloak identity, four purpose-specific data stores, a Spring API Gateway, AWS target infrastructure plus a Supabase PaaS, an adapter-based AI platform and Stripe test-only checkout. This coherent stack satisfies the clearly specified technology and minimum-count constraints. Formal team ratification and instructor clarification of R23 remain open.

## 1. Business drivers and architectural principles

SkillCheck serves **students and job seekers** seeking structured speaking practice. The initial supported skill is **oral communication**, not a diagnosis or automatic measurement of personality or other soft skills. Users complete 60–90-second exercises, receive explainable scoring (duration 30%, filler control 40%, clarity 30%), follow personalized learning paths, and use the same essential journey on web, mobile and desktop. Spanish is Free; English belongs to the Premium *demonstration* plan. Stripe is operated exclusively in sandbox, with no real charges.

Selection criteria are: **(1)** compliance with mandatory requirements, **(2)** security and privacy of learner audio/documents, **(3)** sustainable learning and maintainability, **(4)** portable local development, **(5)** measurable testability, and **(6)** a controlled USD 0 demonstration budget. A mandatory technology is not traded away for simplicity. Engineering risk is contained through adapter boundaries and separated LOCAL, QA, PROD-DEMO and funded PROD-TARGET environments.

### 1.1 Decision authority

| Classification | Meaning | Application |
|---|---|---|
| MANDATORY | Instructor requirement R01–R26 | Must be designed, implemented and evidenced; R23 terminology unresolved |
| PRODUCT | Stakeholder-defined behavior | Audience, languages, platforms, checkout sandbox, 30/40/30 score, limited audio retention |
| RECOMMENDED | This paper's architecture selection | Used as the implementation blueprint after team ratification |
| APPROVED | Recorded project approval | **None evidenced in the reviewed record** |
| VERIFIED | Demonstrated by running software / QA | **Not claimed in Sprint 1** |

## 2. Technology decision summary

| ID | Selection | Justification and system responsibility | Constraint |
|---|---|---|---|
| TD-01 | One monorepo: pnpm workspaces + Maven multi-module | Single source with bounded Java, TypeScript, infrastructure and documentation packages | R01 |
| TD-02 | Java 21, Spring Boot, Maven, Spring Web MVC | Required backend, typed domain logic, test support and mature OAuth2 resource server | R02 |
| TD-03 | React + TypeScript + Vite | Required web framework, shared UI/contracts, typed interfaces | R02 |
| TD-04 | React Module Federation | Actual microfrontend ownership: challenges, progress and administration, one React shell | R04 |
| TD-05 | Astro | Separate public landing/docs surface, not a duplicate authenticated app | R22 |
| TD-06 | Capacitor and Tauri | Deliver real mobile and desktop packages; share UI and API, validate mic and OAuth per platform | R03 |
| TD-07 | Keycloak + Google identity broker; Cloudflare | Email/Google login, OIDC/JWT, roles USER/ADMIN, edge controls | R05 |
| TD-08 | PostgreSQL (Supabase), Redis, MongoDB, Qdrant | Transactions, cache, document content and ACL-filtered vectors; four distinct database engines | R11 |
| TD-09 | Spring Cloud Gateway | Auth-aware routing, audit/correlation and request quota perimeter | R12 |
| TD-10 | AWS Application Load Balancer | Distributed health-checked routing to target multi-AZ application replicas | R13, R17 |
| TD-11 | REST/HTTPS + WebSocket/WSS + signed webhooks | Core API, async status, payment/automation event delivery | R14 |
| TD-12 | Hexagonal backend + MVVM client | Two concrete styles with observable boundaries and substitution tests | R15 |
| TD-13 | AWS target + Supabase PaaS | Meets both provider categories; local simulation precedes any paid provisioning | R06 |
| TD-14 | Docker, Docker Hub, GitHub Actions | Portable QA, versioned images, test and review gates | R08, R09 |
| TD-15 | OpenAI transcription pilot + LLM provider adapter | Reliable product-level integration without vendor lock-in; offline/local fallback in zero-cost tests | R19 |
| TD-16 | MongoDB/Qdrant retrieval + n8n | Permission-aware RAG, versioned embeddings, opt-in reminder automation | R20, R21, R25 |
| TD-17 | Rust/WebAssembly audio features | Real client-side waveform/clipping/silence work with JS comparison benchmark | R24 |
| TD-18 | Stripe Checkout *test only* | Controlled Premium demonstration; signed event grants DEMO_PREMIUM | R07 |
| TD-19 | OWASP Top 10:2025 and ASVS 5.0 | Threat-driven secure design and verification, with ASVS L2 target subject to review | R26 |
| TD-20 | SOLID, DRY, KISS, low coupling | Four named principles with audit-able implementation patterns | R10 |

## 3. Required comparison: why these options

### 3.1 Supabase versus Keycloak: distinguish the architectural roles

Supabase is a **PaaS/data and object-storage provider** in the selected topology. Keycloak is the **identity provider and OIDC authorization authority**. They are not identical categories; choosing one does not automatically replace the other.

| Criterion | Supabase Auth | Keycloak | Selection |
|---|---|---|---|
| Email login and external identity | Built-in | Supported through identity brokering | Both viable |
| Dedicated roles and realm/client policies | Application claims / policies require design | First-class identity administration and brokering | **Keycloak authority** |
| Instructor's named security technologies | Does not explicitly supply Keycloak | Directly addresses R05 working interpretation | **Keycloak** |
| PostgreSQL and private object storage | Integrated PaaS | Not its core purpose | **Supabase** |
| Hosting / operations | Lower setup for managed service | Requires team-run or managed operation and recovery | Cost/ops trade-off |

**Decision TD-07:** login flows use OIDC Authorization Code + PKCE; Google is federated through Keycloak. Spring validates the Keycloak-issued access token. Supabase Auth is not a second issuer, preventing inconsistent roles and duplicated user identities. Supabase PostgreSQL/Storage are only data/storage services and remain behind backend authorization.

### 3.2 Vercel versus AWS Amplify versus AWS + PaaS

| Option | Advantages | Shortcomings for SkillCheck |
|---|---|---|
| Vercel | Strong frontend deployment UX, preview environments | Alone cannot prove instructor-required AWS app tier, ALB or multi-AZ target |
| AWS Amplify | AWS-integrated frontend/hosting workflow | Does not by itself implement the full Java app tier, load balancer or four-store topology |
| **AWS application tier + Supabase PaaS** | Explicit AWS and PaaS; deploy Spring containers and model ALB/redundancy | Multi-AZ and ALB have real costs; account ownership is still absent |

**Decision TD-13:** local Compose is the operative no-charge test environment. AWS is the planned application target, Supabase the named PaaS. Neither Vercel nor Amplify is required, although the team can later use a static frontend hosting service if it does not replace the mandated components. No production availability claim is made until funded deployment and tests exist.

### 3.3 OpenAI versus AssemblyAI and local transcription

| Option | Transcription | LLM reasoning | Operational trade-off |
|---|---|---|---|
| OpenAI `gpt-4o-mini-transcribe` + separate LLM | Hosted STT | Structured clarity/scenario coaching with provider integration | API charges and data-handling approval; no assumed free quota |
| AssemblyAI STT + independent LLM | Hosted STT | Separate LLM needed for R19/clarity | More integrations, different cost and privacy model |
| Local Whisper-family STT + local/mock scorer | Locally reproducible | Local evaluation model only if hardware supports it; otherwise fixtures | Cost-controlled tests but resource/quality constraints |

**Decision TD-15:** the Java backend calls an AI *adapter*, not an SDK embedded in React. For pilot evaluation, use verified provider model IDs and track provider, model, prompt and rubric versions. STT alone does not satisfy the LLM reasoning requirement; a distinct structured LLM evaluation is included. Production keys are never provisioned merely to pass an academic check.

## 4. Data, architecture and communication design

### 4.1 Four databases with unambiguous ownership

| Store | Primary data | Non-overlap rule |
|---|---|---|
| Supabase PostgreSQL | Users, profiles, challenges, attempts, scores, subscriptions, entitlements and relational audit index | **System of record** for transactional invariants |
| Redis | Per-user/API rate limits, status cache, catalog cache and temporary locks | TTL; never durable transcripts |
| MongoDB | Extracted text, document metadata, chunk manifests, consent/versioned feedback records | Document-oriented content and provenance |
| Qdrant | Vector embeddings with `owner_id`, `visibility`, `document_id`, `model_version` | Similarity retrieval, filtered before recall |

Private **Supabase Storage** holds audio and uploaded files as object blobs; it is not counted as a fifth database. The backend enforces tenant/user authorization before every store access. No client gets service-role or administrator keys. Deletion must traverse storage, MongoDB, Qdrant, caches and transactional indexes with logged retries.

### 4.2 Two styles, three methods, two distinct edge layers

- **Hexagonal architecture:** application services call domain ports; adapters implement PostgreSQL, file storage, AI, Keycloak-related claims and payment gateways. Controllers are inbound REST adapters. This supports isolated testing and provider replacement.
- **MVVM on React:** views contain presentation; typed hooks/view-models mediate state and validation; service adapters call the API. Independent microfrontends share design tokens and contracts.
- **REST/HTTPS:** synchronous CRUD/catalog/upload intents/score retrieval.
- **WebSocket/WSS:** authenticated processing status; fallback polling via REST.
- **Signed webhooks:** Stripe test event and backend-to-n8n automation. Verify signature and event IDs, reject replays and honor retries.
- **Spring Cloud Gateway:** API boundary and policies. **AWS ALB:** distribution across healthy service replicas. A gateway is not by itself evidence of load balancing or HA.

## 5. Platform, integration and nonfunctional decisions

### 5.1 User journeys and parity

A single source of business truth powers **web, mobile and desktop**. The React shell hosts challenge, progress and administration microfrontends; mobile and desktop packages use compatible bundled assets and platform-specific secure storage, microphone permission, redirect and session flows. Astro handles public content. English challenge entitlements are asserted by the backend, not merely hidden in the UI.

**Client-side WASM** computes waveform and simple audio health indicators. The official score remains server-generated from uploaded-media duration, transcript-derived metrics and a structured clarity evaluator. The WASM module must have tests and a measurable performance/accuracy purpose.

### 5.2 Quality and operational strategy

| Area | Stack | Engineering gate |
|---|---|---|
| Java unit + contract | JUnit 5, Mockito, Spring test, OpenAPI | Core scoring tests are deterministic and must pass |
| Frontend unit | Vitest, React Testing Library, TypeScript | CI lint + type check + UI logic tests |
| Functional / integration | Spring Boot Test, Testcontainers or Compose QA | OIDC roles, 4-store health, uploads, webhook idempotency |
| E2E | Playwright on web; packaged-platform smoke tests | Free/Premium, audio, delete and RBAC paths |
| Load | k6 | Define and publish p95/error-rate and throughput from QA load profile |
| Security | dependency/secret/container scanning + OWASP ZAP baseline | No exposed secrets or high-severity untriaged findings |
| CI/CD | GitHub Actions, PR review, Docker Hub semver/SHA tags | No deploy from unreviewed default branch; immutable version tags |
| Observability | Spring Actuator/Micrometer + Sentry or comparable; AWS CloudWatch when funded | Job fail, 5xx, payment signature, cost and expiry alerts |

**Principles evidence:** SOLID = single-responsibility use cases/interfaces; DRY = centralized scoring and shared UI contracts; KISS = minimal services behind a gateway rather than gratuitous microservices; low coupling = ports/adapters and message contracts. Security and the four stores require extra operational care; design complexity exists to meet mandatory scope, not to maximize tool count.

### 5.3 Local demo versus high-availability target

- **LOCAL/QA:** local Docker Compose with the four databases, Keycloak, API, gateway, n8n and a fake provider; local load tests and synthetic data. A single-machine demo is **not** high availability.
- **PROD-DEMO:** only provision if free plans/credits/accounts exist; record any availability limitation and verify charges cannot occur.
- **PROD-TARGET:** ALB → at least two healthy Spring API replicas in separate AWS availability zones; Keycloak and every stateful tier need backed-up or replicated recovery; monitor RTO/RPO and failover. Proposed 99.9% availability, RTO 4h, RPO 24h are targets subject to funded testing, not SLAs.
- **Cost:** team limit USD 0; do not create chargeable public IPv4, ALB, compute, database replicas or paid LLM calls without named budget owner and explicit permission.

## 6. Mandatory requirement traceability

This table covers **all 26 mandatory items plus the optional item**. `DESIGN` means a concrete planned mechanism exists in this paper and the master specification; **it does not mean implemented, QA-tested or PROD-proven**. `OPEN` is unresolved in the teacher wording. Validation must attach evidence at the corresponding milestone.

| ID | Planned proof / evidence to collect | Design state |
|---|---|---|
| R01 | Single repository tree, pnpm/Maven root build, per-package workflow | DESIGN |
| R02 | Java Spring Boot REST API + React web application builds | DESIGN |
| R03 | Web/mobile/desktop parity matrix and USER/ADMIN authorization tests | DESIGN |
| R04 | Separately routed challenge/progress/admin React microfrontends | DESIGN |
| R05 | Cloudflare edge, Keycloak OIDC and CORS allowlist tests | DESIGN |
| R06 | AWS application services plus Supabase PaaS deployment records | DESIGN / ACCOUNT PENDING |
| R07 | Stripe test session and signed webhook DEMO_PREMIUM event | DESIGN |
| R08 | CI artifacts for four test types, FE/BE, GitHub Actions | DESIGN |
| R09 | Dockerfiles/Compose and Docker Hub image digests | DESIGN |
| R10 | SOLID, DRY, KISS, low coupling with PR/code examples | DESIGN |
| R11 | PostgreSQL + Redis + MongoDB + Qdrant, health/ownership tests | DESIGN |
| R12 | Spring Cloud Gateway route policies | DESIGN |
| R13 | AWS ALB health check and replica distribution evidence | DESIGN / FUNDING PENDING |
| R14 | REST, WSS, signed webhook contracts and integration tests | DESIGN |
| R15 | Hexagonal backend and MVVM frontend architecture code reviews | DESIGN |
| R16 | Alert rules, dashboard, synthetic incidents, owner acknowledgements | DESIGN |
| R17 | Funded multi-AZ architecture, failover/recovery test, signed availability review | DESIGN / FUNDING PENDING |
| R18 | OpenAPI, README, ADRs, Conventional Commits, PR template | DESIGN |
| R19 | Separate STT + structured LLM evaluation with model/version/cost evidence | DESIGN |
| R20 | n8n opt-in reminder/summary flow with secure webhook callback | DESIGN |
| R21 | ACL-filtered RAG retrieval, cited recommendation and rejection tests | DESIGN |
| R22 | Astro landing/docs build and deployment | DESIGN |
| R23 | **Instructor interpretation of “SDD, ODD”** plus applicable evidence | **OPEN** |
| R24 | Rust/WASM audio feature module benchmark and tests | DESIGN |
| R25 | Embedding ingestion, version and deletion/re-index tests | DESIGN |
| R26 | OWASP Top 10:2025 controls and ASVS 5.0 test evidence | DESIGN |
| OPT-01 | Optional SSR/SSG/ISR/CSR evaluation, no current completion claim | OPTIONAL / DEFERRED |

## 7. Ratification, unresolved decisions and immediate handoffs

| Item | Technical position | Approval / external action |
|---|---|---|
| DEC-01 | Adopt TD-01–TD-20 as integrated stack | Product Owner + technical team sign-off |
| DEC-02 | Adopt proposed scoring calibration and rank thresholds | Product Owner and pilot evaluation |
| DEC-03 | Local-first demonstration and separate funded target | Project sponsor / cloud owner |
| DEC-04 | Confirm whether SOAP is additionally mandatory | Instructor clarification |
| DEC-05 | Confirm R23 acronym expansions | Instructor clarification, **open** |
| DEC-06 | Confirm Keycloak/Cloudflare literal interpretation | Instructor clarification as needed; working baseline includes both |
| DEC-07 | Confirm retention default 7 days, adjustable 1–30 | Product + security review |
| DEC-08 | Confirm mobile WebView microfrontend loading and identity redirects | Architecture proof before packaging |

**Acceptance of this planning deliverable:** review-ready comparative reasoning for the named choices; 27-row traceability; meaningful four-store, gateway, load-balancer, HA and AWS+PaaS design; no false implementation claims; clear architecture handoff. The completion of a *documentation* deliverable does **not** satisfy production implementation requirements.

### Reference materials (official technical documentation)

- Spring Security JWT Resource Server — https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
- Spring Cloud Gateway — https://docs.spring.io/spring-cloud-gateway/reference/intro.html
- Keycloak Server Administration / identity brokering — https://www.keycloak.org/docs/latest/server_admin/
- OWASP Top 10:2025 — https://top10.owasp.org/2025/
- OWASP ASVS 5.0 — https://owasp.org/projects/ASVS
- OpenAI pricing and STT model listing — https://platform.openai.com/pricing/
- Stripe test keys / sandbox — https://docs.stripe.com/keys
- Supabase plans and service boundaries — https://supabase.com/pricing

**Review signature:** Product Owner __________ | Architecture Reviewer __________ | Security Reviewer __________ | Date __________  
**Jira status:** unchanged by preparation of this document.
