# FastShop

> A production-style FastAPI learning roadmap disguised as an e-commerce admin panel backend.

**FastShop** is not only a coding project. It is a complete FastAPI / Python backend learning path for a senior Laravel developer who wants to understand *why* every line, library, and architectural decision exists — not just how to copy patterns.

| | |
|---|---|
| **Type** | Modular monolith API + React admin |
| **Domain** | E-commerce administration panel |
| **Audience** | Senior Laravel → FastAPI / Python |
| **Goal** | Deep understanding → production habits → future AI backends |

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Learning Philosophy](#learning-philosophy)
3. [Tech Stack](#tech-stack)
4. [Architecture](#architecture)
5. [Laravel → FastAPI Translation](#laravel--fastapi-translation)
6. [Folder Structure Evolution](#folder-structure-evolution)
7. [Database Design](#database-design)
8. [Development Roadmap](#development-roadmap)
9. [Coding Rules](#coding-rules)
10. [Commands](#commands)
11. [Learning Notes](#learning-notes)

---

## Project Overview

### What we build

A simple e-commerce **administration panel backend** with:

| Area | Features |
|------|----------|
| **Auth** | Registration, login, JWT, password hashing (Argon2) |
| **Authorization** | Roles, permissions, policy-style checks |
| **Users** | CRUD, role assignment |
| **Catalog** | Products, categories |
| **Content** | Posts (CMS-style) |
| **Dashboard** | Stats, aggregations |
| **API** | REST JSON API |
| **Frontend** | React + Shadcn UI admin |

### What we deliberately do *not* build (yet)

- Microservices
- Event sourcing
- CQRS as a religion
- Hexagonal “ports everywhere”
- Premature multi-tenant SaaS complexity

We build a **modular monolith**: clear module boundaries inside one deployable app. Good enough for small SaaS and medium apps; ready to extract modules later if needed.

### Future direction

After FastShop foundations are solid:

- Background AI jobs (embeddings, classification, summaries)
- Streaming responses
- Tool-calling backends
- Observability for LLM costs / latency

The same modular layout scales into AI features without rewriting the app.

---

## Learning Philosophy

This project exists to understand:

1. **Why every line exists** — not cargo-cult snippets
2. **Why every dependency exists** — what problem it solves
3. **Why every architecture decision exists** — trade-offs, not dogma

### Avoid copy/paste development

Before writing or accepting any implementation step, answer:

| Question | Purpose |
|----------|---------|
| **What** are we building? | Scope clarity |
| **Why** this way? | Design intent |
| **What problem** does it solve? | Avoid accidental complexity |
| **Laravel equivalent?** | Transfer existing mental models |
| **Python / FastAPI concept?** | Name the new tool correctly |

### How to use this README

1. Read the phase goal and concepts **before** coding.
2. Implement only that phase.
3. Fill [Learning Notes](#learning-notes) after each phase.
4. Do not skip Phase 0 (Python mental models). Laravel seniority does not replace Python fluency.

### Mentality shift: Laravel → Python

| Laravel habit | Python / FastAPI habit |
|---------------|------------------------|
| Framework provides almost everything | You compose libraries |
| `artisan make:*` scaffolds | You create files intentionally |
| Service container is magical | DI is explicit (`Depends`) |
| Eloquent is the default ORM style | SQLAlchemy 2.0 is explicit / typed |
| Facades hide wiring | Imports and constructors show wiring |
| “Convention over configuration” | “Configuration you can see” |

---

## Tech Stack

For each tool: **what**, **why**, **Laravel equivalent**, **where in FastShop**.

### Backend

#### Python

| | |
|---|---|
| **What** | Language runtime and ecosystem |
| **Why** | Native async, typing, data/AI ecosystem, FastAPI home |
| **Laravel eq.** | PHP |
| **Where** | Entire backend |

#### FastAPI

| | |
|---|---|
| **What** | Modern ASGI web framework for APIs |
| **Why** | OpenAPI auto-docs, first-class async, Pydantic validation, DI via `Depends` |
| **Laravel eq.** | Laravel HTTP kernel + routing + Form Requests (partial) |
| **Where** | `app/main.py`, routers, dependencies |

#### Pydantic

| | |
|---|---|
| **What** | Data validation and serialization via type hints |
| **Why** | Request/response contracts; replace ad-hoc arrays and `$casts` |
| **Laravel eq.** | Form Requests + API Resources / DTOs |
| **Where** | `schemas/` in each module |

#### pydantic-settings

| | |
|---|---|
| **What** | Settings loaded from env / `.env` into typed objects |
| **Why** | Fail fast on bad config; no scattered `os.getenv` |
| **Laravel eq.** | `config/*.php` + `.env` |
| **Where** | `app/core/config.py` |

#### SQLAlchemy 2.0

| | |
|---|---|
| **What** | SQL toolkit + ORM (2.0 style: typed, explicit) |
| **Why** | Production ORM, clear session lifecycle, powerful queries |
| **Laravel eq.** | Eloquent + Query Builder |
| **Where** | `models/`, repositories, `core/database.py` |

#### PostgreSQL

| | |
|---|---|
| **What** | Relational database |
| **Why** | Constraints, JSON, full-text, reliability for admin data |
| **Laravel eq.** | MySQL / PostgreSQL via Laravel |
| **Where** | All persistent entities |

#### Alembic

| | |
|---|---|
| **What** | Database migration tool for SQLAlchemy |
| **Why** | Versioned schema like Laravel migrations |
| **Laravel eq.** | `database/migrations` + `artisan migrate` |
| **Where** | `alembic/`, `alembic.ini` |

#### pwdlib\[argon2]

| | |
|---|---|
| **What** | Password hashing helpers; Argon2 backend |
| **Why** | Modern hashing; avoid rolling your own crypto |
| **Laravel eq.** | `Hash::make` / `Hash::check` (bcrypt by default) |
| **Where** | Auth service (register / login) |

#### PyJWT

| | |
|---|---|
| **What** | Encode / decode JSON Web Tokens |
| **Why** | Stateless API auth for SPA frontend |
| **Laravel eq.** | Laravel Sanctum token auth or JWT packages (less built-in) |
| **Where** | Auth module, security dependencies |

#### Redis

| | |
|---|---|
| **What** | In-memory store |
| **Why** | Cache, rate limits, queue broker / job backend |
| **Laravel eq.** | Redis for cache / queues |
| **Where** | Cache layer, ARQ/Celery, optional sessions |

#### ARQ or Celery

| | |
|---|---|
| **What** | Background job runners (pick one; ARQ is async-native and lighter; Celery is the Laravel-Queue-scale veteran) |
| **Why** | Emails, reports, AI tasks off the request path |
| **Laravel eq.** | Queues + Jobs |
| **Where** | `app/core/queue/`, job modules (Phase 9) |

> **Decision later:** Prefer **ARQ** for a FastAPI-first async learning path unless you need Celery’s ecosystem. Document the choice in Learning Notes.

#### pytest

| | |
|---|---|
| **What** | Python test framework |
| **Why** | Fixtures, parametrize, FastAPI `TestClient` / httpx |
| **Laravel eq.** | PHPUnit / Pest |
| **Where** | `tests/` |

#### Ruff

| | |
|---|---|
| **What** | Extremely fast linter + formatter |
| **Why** | One tool instead of flake8 + isort + black chaos |
| **Laravel eq.** | Pint / PHP-CS-Fixer |
| **Where** | CI + local `ruff check` / `ruff format` |

#### Docker

| | |
|---|---|
| **What** | Container runtime / Compose |
| **Why** | Reproducible Postgres, Redis, API, frontend |
| **Laravel eq.** | Laravel Sail / Docker Compose |
| **Where** | `Dockerfile`, `docker-compose.yml` (Phase 10) |

#### uv (tooling)

| | |
|---|---|
| **What** | Fast Python package + project manager |
| **Why** | Replaces slow pip/venv rituals; lockfile; `uv run` |
| **Laravel eq.** | Composer |
| **Where** | `pyproject.toml`, `uv.lock` |

---

### Frontend

#### React

| | |
|---|---|
| **What** | UI library |
| **Why** | Dominant admin SPA ecosystem |
| **Laravel eq.** | Blade / Inertia / Livewire (different model) — closest: Vue/React SPA with Laravel API |
| **Where** | `frontend/` |

#### TypeScript

| | |
|---|---|
| **What** | Typed JavaScript |
| **Why** | Align FE contracts with Pydantic schemas |
| **Laravel eq.** | PHP types / Form Request rules (server-side) |
| **Where** | All frontend source |

#### Vite

| | |
|---|---|
| **What** | Frontend build tool / dev server |
| **Why** | Fast HMR, simple React setup |
| **Laravel eq.** | Vite via Laravel (`laravel-vite-plugin`) |
| **Where** | `frontend/` |

#### Tailwind CSS

| | |
|---|---|
| **What** | Utility-first CSS |
| **Why** | Speed + consistency with Shadcn |
| **Laravel eq.** | Tailwind in Laravel Breeze/Jetstream |
| **Where** | Component styles |

#### Shadcn UI

| | |
|---|---|
| **What** | Copy-in accessible component primitives (Radix + Tailwind) |
| **Why** | Production admin look without a heavy UI kit lock-in |
| **Laravel eq.** | No single equivalent; Filament / custom Blade components |
| **Where** | `frontend/src/components/ui/` |

#### React Router

| | |
|---|---|
| **What** | Client-side routing |
| **Why** | Protected admin routes, nested layouts |
| **Laravel eq.** | `routes/web.php` (server) vs SPA router |
| **Where** | App shell, auth gates |

#### TanStack Query

| | |
|---|---|
| **What** | Server-state cache / fetch library |
| **Why** | Caching, retries, loading/error states for API data |
| **Laravel eq.** | Livewire reactivity / Inertia partial reloads (different) — mental model: “smart HTTP client for lists” |
| **Where** | Data hooks for products, users, dashboard |

#### React Hook Form

| | |
|---|---|
| **What** | Performant form state |
| **Why** | Less re-render pain on admin forms |
| **Laravel eq.** | Form + validation on server; FE form libs if SPA |
| **Where** | Create/edit modals and pages |

#### Zod

| | |
|---|---|
| **What** | Schema validation for TypeScript |
| **Why** | Client validation mirroring Pydantic; parse API shapes |
| **Laravel eq.** | Form Request rules (client-side twin) |
| **Where** | Form schemas, API response parsing |

---

## Architecture

### Style: Modular Monolith

One codebase, one deployable API, **modules** with clear ownership:

```
backend/
├── app/
│   ├── main.py                 # ASGI entry / app factory
│   ├── core/                   # Cross-cutting: config, db, security, logging
│   ├── modules/                # Feature modules (auth, users, products, ...)
│   │   ├── auth/
│   │   ├── users/
│   │   ├── roles/
│   │   ├── products/
│   │   ├── categories/
│   │   ├── posts/
│   │   └── dashboard/
│   └── shared/                 # Truly shared types, exceptions, utils
├── alembic/                    # Migrations
├── tests/
├── pyproject.toml
└── README.md                   # This document (repo root or mirrored)
```

Frontend lives beside backend:

```
frontend/                       # React + Vite admin
```

### Folder meanings

| Folder | Responsibility | Rule |
|--------|----------------|------|
| **`core/`** | App-wide wiring: settings, engine/session, security primitives, middleware, logging | No product business rules |
| **`modules/<name>/`** | One feature area: router, schemas, service, repository, models (or model package) | Module owns its use cases |
| **`shared/`** | Exceptions, base schemas, pagination helpers used by many modules | Keep thin — not a junk drawer |
| **`tests/`** | Unit + API tests | Mirror module structure |

### Typical module layout

```
modules/products/
├── router.py          # HTTP endpoints (thin)
├── schemas.py         # Pydantic in/out
├── service.py         # Business rules
├── repository.py      # DB queries only
├── models.py          # SQLAlchemy models
└── dependencies.py    # Module-specific Depends
```

### Request flow

```
HTTP Request
    → Router (validate input via schema, auth deps)
        → Service (business rules, orchestration)
            → Repository (SQLAlchemy queries)
                → PostgreSQL
        ← Service (domain result)
    ← Router (map to response schema)
HTTP Response
```

| Layer | May do | Must not do |
|-------|--------|-------------|
| **Router** | Parse HTTP, call service, return schema | Business rules, raw SQL |
| **Service** | Rules, transactions orchestration, call repos / other services | Scatter SQLAlchemy query details |
| **Repository** | Queries, persistence | HTTP awareness, auth policy decisions |
| **Schema** | Validate / serialize | Hit the database |

### Why modular monolith (not microservices)

| Need | Modular monolith | Microservices |
|------|------------------|---------------|
| Learn FastAPI deeply | Excellent | Distracts with ops |
| Small / medium SaaS | Excellent | Overkill |
| Clear boundaries | Modules | Network boundaries |
| Future extract | Possible per module | Already split |
| Local DX | One `uv run` | Many services |

Suitable for: **small SaaS**, **medium apps**, **later scaling by extracting hot modules**.

### Dependency Injection (mental model)

Laravel: container resolves controller constructor / method injection.

FastAPI: `Depends()` builds a call graph per request.

```text
get_db() → Session
get_current_user(token, db) → User
require_permission("products.update")(user) → User or 403
product_service(db) → ProductService
```

No service provider classes required for basic wiring. Prefer functions and small factories over a custom IoC framework.

---

## Laravel → FastAPI Translation

| Laravel concept | FastAPI / Python equivalent |
|-----------------|----------------------------|
| Controller | Router functions / APIRouter |
| `routes/api.php` | `APIRouter` + `include_router` |
| Form Request | Pydantic request schema (`BaseModel`) |
| API Resource / JsonResource | Pydantic response schema |
| Eloquent Model | SQLAlchemy `Mapped` model |
| Service class | Service module / class |
| Policy | Permission checks + policy functions/classes |
| Gate | Dependency or helper: `require_permission("…")` |
| Middleware | Middleware / dependencies / ASGI middleware |
| Service Provider | App factory + lifespan hooks (`lifespan`) |
| IoC Container | FastAPI DI (`Depends`) + explicit constructors |
| Method / ctor injection | `Depends` parameters |
| Job | ARQ / Celery task |
| Event | Custom event dispatch (or library) |
| Listener | Handler subscribed to event |
| `config/*.php` + `.env` | `pydantic-settings` Settings class |
| Migrations | Alembic revisions |
| Queues (`ShouldQueue`) | Redis + ARQ/Celery |
| Facades | Direct imports (no facades) |
| Eloquent scopes | Repository methods / SQLAlchemy query helpers |
| `artisan` | `uv run`, Alembic CLI, custom scripts |
| `phpunit.xml` / Pest | `pytest` + `conftest.py` |
| Policies in `AuthServiceProvider` | Register checks in deps or a small authz module |

### Side-by-side intuition

**Laravel**

```php
Route::post('/products', [ProductController::class, 'store']);
// FormRequest validates → Controller → Service → Eloquent
```

**FastAPI**

```python
@router.post("/products", response_model=ProductRead)
async def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_product_service),
    _: User = Depends(require_permission("products.create")),
):
    return await service.create(payload)
```

Same story: validate → authorize → service → persistence. Different wiring.

---

## Folder Structure Evolution

We **do not** start with the full modular tree. Complexity is earned.

### Stage A — Simple FastAPI app

```
backend/
├── main.py
├── requirements or pyproject.toml
└── .env
```

**Why:** Learn app factory, routing, OpenAPI, settings. Zero ceremony.

### Stage B — Routers + services

```
backend/app/
├── main.py
├── core/config.py
├── routers/
├── services/
└── schemas/
```

**Why:** Separate HTTP from business logic. Still one “domain pile”.

### Stage C — Repositories + DB

```
... + models/, repositories/, alembic/
```

**Why:** Queries leave services; migrations exist.

### Stage D — Modular monolith

```
app/modules/{auth,users,products,...}/
app/core/
app/shared/
```

**Why:** Features grow; modules prevent a god-folder. Extract only when pain appears.

### Why not start at Stage D?

| Starting complex | Cost |
|------------------|------|
| Empty module scaffolding | Ceremony without understanding |
| Abstractions before use cases | Wrong boundaries |
| “Enterprise” folders | Fear of deleting code you never needed |

**Rule:** Promote structure when a folder hurts — not when a blog post says so.

---

## Database Design

Initial entities (admin-focused; not a full storefront checkout).

### ER overview

```text
users ←→ roles ←→ permissions
  │
  └── audit_logs

categories 1──* products

posts (author → users)
```

### Entities

#### users

| Column | Notes |
|--------|-------|
| id | PK |
| email | Unique |
| password_hash | Argon2 |
| full_name | |
| is_active | Soft disable |
| created_at / updated_at | |

#### roles

| Column | Notes |
|--------|-------|
| id | PK |
| name | Unique (`admin`, `editor`, …) |
| description | |

#### permissions

| Column | Notes |
|--------|-------|
| id | PK |
| code | Unique string (`products.create`) |
| description | |

#### role_user (pivot)

Many-to-many: **User belongs to many Roles**.

#### permission_role (pivot)

Many-to-many: **Role has many Permissions**.

#### categories

| Column | Notes |
|--------|-------|
| id | PK |
| name | |
| slug | Unique |
| parent_id | Optional self-FK for trees (keep flat in v1 if preferred) |

#### products

| Column | Notes |
|--------|-------|
| id | PK |
| category_id | FK → categories |
| name | |
| slug | Unique |
| description | |
| price | Numeric |
| stock | Int |
| is_active | |
| created_at / updated_at | |

**Product belongs to Category.**

#### posts

| Column | Notes |
|--------|-------|
| id | PK |
| author_id | FK → users |
| title | |
| slug | Unique |
| body | |
| status | draft / published |
| published_at | Nullable |
| created_at / updated_at | |

**Post belongs to User (author).**

#### audit_logs

| Column | Notes |
|--------|-------|
| id | PK |
| actor_id | FK → users (nullable for system) |
| action | e.g. `product.updated` |
| entity_type / entity_id | Polymorphic-ish reference |
| metadata | JSON |
| created_at | |

### Relationship summary

| Relationship | Type |
|--------------|------|
| User ↔ Role | Many-to-many |
| Role ↔ Permission | Many-to-many |
| Category → Product | One-to-many |
| User → Post | One-to-many |
| User → AuditLog | One-to-many |

Laravel mental model: Eloquent `belongsToMany`, `hasMany`, `belongsTo` map 1:1 to SQLAlchemy relationships — syntax differs; cardinality same.

---

## Development Roadmap

Each phase: **Goal → Concepts → Files → Libraries → Laravel comparison → Result**.

Do phases in order. Tick Learning Notes after each.

---

### Phase 0 — Python Backend Preparation

**Goal:** Gain Python mental models FastAPI assumes you already have.

**Concepts learned**

| Concept | Why it matters for FastAPI |
|---------|----------------------------|
| Decorators | `@app.get`, `@router.post`, middleware-style wrappers |
| Functions as objects | Pass callables into `Depends` |
| Type hints | Pydantic + OpenAPI + editor help |
| async / await | Concurrent I/O endpoints |
| Generators | Streaming, some resource patterns |
| Context managers | DB sessions, `with` resources |
| Dataclasses | Simple structured data (alongside Pydantic) |
| Protocols | Structural typing (“duck interfaces”) without heavy ABC trees |

**Files created**

- Optional: `learning/phase0/` scratch notebooks or scripts (not production code)

**Libraries used**

- Stdlib only (+ maybe `mypy` later)

**Laravel comparison**

- Decorators ≈ attributes / middleware wrappers, but more central in Python
- Type hints ≈ PHP types + docblocks, but runtime-validated via Pydantic
- async ≈ rarely first-class in classic Laravel request cycle (Octane/Swoole aside)

**Expected result**

You can read FastAPI source examples without panic. You know what `Depends(get_db)` *is* (a callable).

---

### Phase 1 — Project Foundation

**Goal:** Runnable FastAPI app with typed settings and clean tooling.

**Concepts learned**

- `uv` projects and lockfiles
- Ruff lint/format
- Environment variables + `.env`
- pydantic-settings
- Application factory / lifespan
- Configuration as a typed object

**Files created (target)**

```
backend/
├── pyproject.toml
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── core/
│       └── config.py
└── README.md (link to this roadmap)
```

**Libraries used**

- FastAPI, Uvicorn (or Hypercorn), pydantic-settings, Ruff, uv

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| `composer create-project` | `uv init` + deps |
| `.env` + `config/app.php` | `.env` + `Settings` |
| `bootstrap/app.php` | `create_app()` / `main.py` |

**Expected result**

`GET /health` returns OK. Settings load from env. `ruff check` passes. OpenAPI at `/docs`.

---

### Phase 2 — Database Layer

**Goal:** PostgreSQL connected; models and migrations work.

**Concepts learned**

- SQLAlchemy 2.0 `Mapped` / `mapped_column`
- Engine + session lifecycle
- Alembic revision workflow
- Sync vs async SQLAlchemy (choose one path and stick to it for learning clarity)

**Files created**

```
app/core/database.py
app/modules/.../models.py   # or app/models/ early, then move
alembic.ini
alembic/env.py
alembic/versions/*.py
```

**Libraries used**

- SQLAlchemy 2.0, asyncpg or psycopg, Alembic, PostgreSQL

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Eloquent model | SQLAlchemy model |
| `artisan migrate` | `alembic upgrade head` |
| DB facade / Eloquent | `Session` / repository |

**Expected result**

Migration creates empty tables (or first tables). App obtains a session per request via `Depends`.

---

### Phase 3 — Basic Architecture

**Goal:** Establish Router → Service → Repository → Database.

**Concepts learned**

- APIRouter composition
- Service layer
- Repository pattern (pragmatic, not enterprise theater)
- Pydantic schemas (create / update / read)
- Dependency injection with `Depends`

**Files created**

```
app/modules/example/   # or products skeleton
  router.py
  schemas.py
  service.py
  repository.py
  dependencies.py
app/main.py            # include routers
```

**Libraries used**

- FastAPI, Pydantic, SQLAlchemy (existing)

**Laravel comparison**

| Layer | Laravel | FastAPI |
|-------|---------|---------|
| HTTP | Controller | Router |
| Rules | Action / Service | Service |
| DB | Eloquent in model/repo | Repository |
| Input | Form Request | Schema |
| Wiring | Container | `Depends` |

**Expected result**

One vertical slice (e.g. list/create resource) proves the layering. No business logic in routers. No SQL in services.

---

### Phase 4 — Authentication

**Goal:** Register / login with Argon2 + JWT; protect routes.

**Concepts learned**

- Password hashing with **pwdlib** (Argon2)
- JWT create / verify with **PyJWT**
- `OAuth2PasswordBearer` or custom bearer dependency
- `get_current_user` dependency chain
- Safe error messages (no user enumeration if desired)

**Files created**

```
app/modules/auth/
  router.py
  schemas.py
  service.py
  dependencies.py
app/modules/users/models.py
app/core/security.py
```

**Libraries used**

- pwdlib[argon2], PyJWT, FastAPI security utilities

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| `Hash::make` | pwdlib Argon2 |
| Sanctum / Passport / JWT | PyJWT access tokens |
| `auth` middleware | `Depends(get_current_user)` |
| `RegisterController` | `auth/router.py` |

**Expected result**

Register + login return tokens. Protected route rejects missing/invalid JWT. Password never stored plaintext.

**Explain focus**

- **pwdlib** — hashing API; Argon2 parameters matter
- **PyJWT** — claims (`sub`, `exp`), signing secret, algorithms
- **Depends()** — composes auth into any endpoint

---

### Phase 5 — Authorization

**Goal:** Roles, permissions, policy-style checks.

**Concepts learned**

- RBAC tables and seeding
- Permission codes as strings
- Reusable `require_permission("…")` dependencies
- Optional policy classes for complex rules (ownership, etc.)

**Files created**

```
app/modules/roles/
app/modules/users/  # assign roles
app/core/authz.py   # or modules/auth/policies.py
seeds / fixtures for admin role
```

**Libraries used**

- Existing stack (no Gate package required)

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Gate::define | permission helper / dep |
| Policy class | policy functions/classes |
| `$this->authorize` | `Depends(require_permission(...))` |
| spatie/permission | Your RBAC tables (learn by building) |

**Expected result**

Admin can manage products; role without permission gets 403. Permission check is one line at the endpoint.

---

### Phase 6 — Products Module

**Goal:** Full CRUD with real list UX needs.

**Concepts learned**

- Pagination (limit/offset or cursor — pick one, document why)
- Filtering, searching, sorting
- Validation edge cases (price, slug uniqueness)
- Response schemas as API resources
- Category relationship on product

**Files created**

```
app/modules/products/*
app/modules/categories/*   # at least enough for FK
```

**Libraries used**

- FastAPI Query params, Pydantic, SQLAlchemy

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| `ProductController` | `products/router.py` |
| Spatie Query Builder / manual | Repository query composition |
| API Resource | `ProductRead` schema |
| Form Request | `ProductCreate` / `ProductUpdate` |

**Expected result**

Admin can create/list/update/delete products with filter/search/sort/page. OpenAPI documents query params.

---

### Phase 7 — Admin Dashboard

**Goal:** Aggregation endpoints for UI charts/cards.

**Concepts learned**

- `func.count`, `group_by`, date trunc
- Read-only dashboard service
- Avoid N+1; single purposeful queries

**Files created**

```
app/modules/dashboard/
  router.py
  schemas.py
  service.py
  repository.py
```

**Libraries used**

- SQLAlchemy aggregation

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Dashboard controller + query | dashboard module |
| `DB::raw` / Eloquent aggregates | SQLAlchemy `func` |

**Expected result**

Endpoints like totals (users, products, posts), products per category, recent activity — ready for React cards.

---

### Phase 8 — Frontend

**Goal:** React admin that consumes the API.

**Concepts learned**

- Vite + React + TS project layout
- Auth storage + protected routes
- TanStack Query for lists
- RHF + Zod for forms
- Shadcn tables, dialogs, forms

**Files created**

```
frontend/
  src/pages/
  src/components/
  src/features/auth|products|dashboard/
  src/lib/api.ts
```

**Libraries used**

- React, TypeScript, Vite, Tailwind, Shadcn UI, React Router, TanStack Query, React Hook Form, Zod

**Laravel comparison**

Closest: **Laravel API + separate SPA** (not Blade). Auth feels like Sanctum SPA or token Bearer headers.

**Expected result**

Login → dashboard → products table → create/edit modal → logout. Unauthorized users redirected.

---

### Phase 9 — Advanced Backend

**Goal:** Production cross-cutting concerns + async work.

**Concepts learned**

- Middleware (request ID, timing)
- Structured logging
- Exception handlers → consistent error JSON
- Domain events + listeners (start simple)
- Redis
- Background jobs (ARQ or Celery)
- Audit log writes

**Files created**

```
app/core/logging.py
app/core/exceptions.py
app/core/middleware.py
app/core/events.py
app/core/queue/
app/modules/.../jobs.py
```

**Libraries used**

- Redis, ARQ or Celery, logging libs as needed

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Exception Handler | FastAPI exception handlers |
| Middleware | Middleware / deps |
| Event + Listener | Simple dispatcher |
| `ShouldQueue` Job | ARQ/Celery task |
| Log facade | `logging` / structlog |

**Expected result**

Failed validation and domain errors look consistent. A sample job (e.g. “recompute dashboard cache” or “send welcome email stub”) runs in worker. Redis up in Compose.

---

### Phase 10 — Production Preparation

**Goal:** Ship-ready habits.

**Concepts learned**

- Multi-stage Docker builds
- Compose for api + db + redis + worker + frontend
- pytest strategy (unit vs API)
- CI pipeline (lint, test, migrate check)
- Security: secrets, CORS, rate limit, HTTPS assumptions
- Deployment checklist

**Files created**

```
Dockerfile
docker-compose.yml
.github/workflows/ci.yml   # or GitLab CI
tests/ ... expanded
docs/deployment.md         # optional short checklist
```

**Libraries used**

- Docker, pytest, Ruff, CI provider

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Sail | Compose |
| GitHub Actions + PHPUnit | CI + pytest |
| `config/cors.php` | CORS middleware settings |

**Expected result**

`docker compose up` runs the stack. CI red on lint/test fail. Documented deploy steps.

---

## Coding Rules

1. **Prefer readability over clever code** — junior-you in 6 months is the reviewer.
2. **Use type hints** — everywhere public; especially function signatures.
3. **Avoid unnecessary abstraction** — no interface until a second implementation appears.
4. **Keep business logic out of routers** — routers are HTTP adapters.
5. **Keep database queries out of services** — services call repositories.
6. **Use dependency injection** — testable, explicit wiring.
7. **Write tests** — at least for authz boundaries and critical services.
8. **Follow SOLID where useful** — not as a religion; YAGNI still wins.
9. **Avoid premature optimization** — measure first; indexes when queries hurt.
10. **Name permissions like actions** — `products.create`, not `product_manager_flag`.
11. **One module, one reason to change** — resist cross-import spaghetti; share via `shared/` sparingly.
12. **Document decisions in Learning Notes** — especially Laravel ≠ FastAPI mismatches.

---

## Commands

### Project / dependencies

```bash
# Create / sync project (uv)
uv init
uv add fastapi uvicorn sqlalchemy alembic pydantic-settings ...
uv add --dev pytest ruff

# Install from lockfile
uv sync

# Run a tool in the project env
uv run uvicorn app.main:app --reload
uv run pytest
uv run ruff check .
uv run ruff format .
```

### Database

```bash
# Create revision (after model changes)
uv run alembic revision --autogenerate -m "describe change"

# Apply migrations
uv run alembic upgrade head

# Rollback one step
uv run alembic downgrade -1
```

### Testing & lint

```bash
uv run pytest
uv run pytest -k auth
uv run ruff check .
uv run ruff format .
```

### Workers / Redis (Phase 9+)

```bash
# Example shapes — exact commands depend on ARQ vs Celery choice
uv run arq app.core.queue.WorkerSettings
# or
uv run celery -A app.core.queue worker -l info
```

### Docker (Phase 10)

```bash
docker compose up --build
docker compose exec api uv run alembic upgrade head
```

### Frontend (Phase 8+)

```bash
cd frontend
npm install   # or pnpm / bun — pick one and stick to it
npm run dev
npm run build
```

---

## Learning Notes

Use this section as a living journal. Duplicate a block per week/phase.

### Template

```markdown
### Date / Phase: ____

#### New Python concepts
-

#### New libraries
- name — what I thought it did vs what it actually does

#### Architectural decisions
- Decision:
- Alternatives considered:
- Why we chose this:

#### Mistakes
- What broke:
- Root cause:
- Fix / rule for future:

#### Laravel comparisons
- Laravel way:
- FastAPI way:
- What clicked / what still feels weird:
```

### Log

<!-- Append entries below. Do not delete old notes. -->

#### Phase 0

- 

#### Phase 1

- 

#### Phase 2

- 

#### Phase 3

- 

#### Phase 4

- 

#### Phase 5

- 

#### Phase 6

- 

#### Phase 7

- 

#### Phase 8

- 

#### Phase 9

- 

#### Phase 10

- 

---

## Definition of Done (whole project)

FastShop is “complete” as a learning milestone when:

- [ ] Modular monolith layout exists and is explained in your own words
- [ ] Auth (Argon2 + JWT) works
- [ ] RBAC enforces permissions on products/admin routes
- [ ] Products CRUD supports pagination, filter, search, sort
- [ ] Dashboard aggregations exist
- [ ] React admin covers login, dashboard, products
- [ ] Errors/logging consistent; at least one background job
- [ ] Docker Compose boots API + Postgres + Redis (+ worker)
- [ ] pytest + Ruff run in CI
- [ ] Learning Notes filled for every phase

---

## How to continue from here

1. Start **Phase 0** — Python concepts (no FastAPI app required).
2. Only then **Phase 1** — foundation.
3. Resist generating the whole repo at once. Understanding > scaffolding.

**Next agent/dev instruction when ready:** “Implement Phase 1 only, following README.”

---

*FastShop — learn the why, then ship the what.*
