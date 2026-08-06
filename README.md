# FastShop

> Development roadmap · Architecture document · Learning guide

**FastShop** is a production-style e-commerce **administration panel**. It is also a complete FastAPI / Python backend learning path for an experienced **Laravel** developer.

This README is the source of truth. It must evolve with the project. Do not treat it as a one-time project blurb.

| | |
|---|---|
| **Backend** | Python · FastAPI · PostgreSQL |
| **Frontend** | React · **JavaScript** · Tailwind · Shadcn UI |
| **Architecture** | Laravel-inspired modular monolith |
| **Frontend language** | **JavaScript only — no TypeScript** |
| **Goal before AI engineering** | One complete, understood production-style system |

---

## Table of Contents

1. [Project Goal](#project-goal)
2. [Learning Style](#learning-style)
3. [Architecture Style](#architecture-style)
4. [Backend Structure](#backend-structure)
5. [Module File Guide](#module-file-guide)
6. [Libraries](#libraries)
7. [Frontend Stack](#frontend-stack)
8. [Laravel → FastAPI Translation](#laravel--fastapi-translation)
9. [Database Design](#database-design)
10. [Coding Rules](#coding-rules)
11. [Feature-Based Development Roadmap](#feature-based-development-roadmap)
12. [Commands](#commands)
13. [Living Learning Log](#living-learning-log)
14. [Definition of Done](#definition-of-done)

---

## Project Goal

Build **one complete admin system** while learning:

- FastAPI deeply (not surface tutorials)
- Professional Python backend habits
- How every Laravel concept maps to Python/FastAPI
- Why every library exists
- Why every folder and file exists
- Why every architectural decision exists

Then move into AI backend work on top of solid foundations.

### Domain scope

| Area | Scope |
|------|--------|
| Authentication | Register, login, JWT, Argon2 |
| Authorization | Roles, permissions, policies |
| Users | Admin CRUD |
| Catalog | Categories, products, image upload |
| Content | Posts (simple CMS) |
| Dashboard | Stats / aggregation APIs |
| Frontend | React JS admin panel |

### Out of scope (for now)

- Microservices
- TypeScript
- Enterprise over-engineering (ports/adapters everywhere, unused interfaces)
- Full storefront checkout / payments

---

## Learning Style

For **every** implementation step, document:

| Lens | Question |
|------|----------|
| **What?** | What are we building right now? |
| **Why?** | Why this approach / library / folder? |
| **How?** | Concrete steps and patterns |
| **Laravel equivalent?** | What did I already know under another name? |
| **Common mistakes?** | What traps should I avoid? |

### Habit rules

- Avoid copy/paste without understanding.
- Finish a phase before starting the next.
- After each completed phase, append to [Living Learning Log](#living-learning-log):
  - lessons learned
  - architecture decisions
  - new libraries
  - problems solved

### Mental shift: Laravel → Python

| Laravel habit | FastShop habit |
|---------------|----------------|
| Framework ships almost everything | You compose libraries |
| `artisan make:*` | You create files with intention |
| Service container feels magical | DI is visible (`Depends`, constructors) |
| Facades hide imports | Imports show wiring |
| Convention over configuration | Configuration you can see |
| Blade / Inertia optional | Separate React JS SPA + JSON API |

---

## Architecture Style

### Modular monolith (Laravel-inspired)

One deployable backend. Features live in **modules**. Cross-cutting pieces live in familiar Laravel-shaped folders (`config/`, `routes/`, `database/`, `app/`).

```text
FastShop/
├── backend/
│   ├── app/
│   ├── config/
│   ├── database/
│   │   ├── migrations/
│   │   └── seeders/
│   ├── routes/
│   ├── storage/
│   ├── public/
│   ├── modules/
│   └── tests/
└── frontend/          # React + JavaScript (no TypeScript)
```

### Why this structure?

| Reason | Detail |
|--------|--------|
| Familiar mental map | Laravel seniors navigate `config`, `routes`, `database`, feature folders quickly |
| Module ownership | Auth, users, products, … change independently |
| One deployable | Correct size for small/medium SaaS and learning |
| Future AI work | New modules (e.g. `ai/`) plug in without a rewrite |
| Not microservices | Avoid ops noise while learning FastAPI |

### What is Laravel-inspired?

| Idea | In FastShop |
|------|-------------|
| `config/` | Typed settings modules |
| `routes/` | Central route registration |
| `database/migrations` | Alembic revisions (same *role*) |
| `database/seeders` | Seed scripts |
| `app/` providers / middleware / exceptions | Core bootstrap concerns |
| Feature modules | Closer to domain modules / packages than classic `app/Http/Controllers` dump |
| Policies | `policies.py` per module |
| Service + repository split | Explicit layers (common in larger Laravel apps) |

### What is Python / FastAPI-specific?

| Idea | Detail |
|------|--------|
| ASGI + Uvicorn | Process model ≠ PHP-FPM |
| Pydantic schemas | Runtime validation + OpenAPI |
| `Depends()` | First-class request DI (not a ServiceProvider class tree) |
| SQLAlchemy 2 session | Explicit session lifecycle ≠ Eloquent facades |
| Alembic | Migration engine tied to SQLAlchemy metadata |
| JWT via PyJWT | Library choice, not framework Sanctum |
| ARQ + Redis | Async-native jobs preferred for FastAPI learning |
| No Blade | Frontend is a separate React SPA |

**Rule:** Steal Laravel *clarity*. Do not fake PHP frameworks inside Python.

---

## Backend Structure

```text
backend/
├── app/
│   ├── main.py              # ASGI entry / app factory
│   ├── providers/           # Bootstrap wiring (DI setup, startup hooks)
│   ├── middleware/          # HTTP / ASGI cross-cutting
│   ├── exceptions/          # Exception types + handlers
│   └── helpers/             # Small shared pure helpers
│
├── config/
│   ├── settings.py          # pydantic-settings (env)
│   ├── database.py          # Engine / session factory config
│   └── security.py          # JWT, password, CORS-related settings
│
├── routes/
│   ├── api.py               # Mount API routers from modules
│   └── web.py               # Optional non-API routes (health, docs redirects)
│
├── database/
│   ├── connection.py        # Engine, SessionLocal, get_db
│   ├── migrations/          # Alembic versions (or alembic/ versions linked here)
│   └── seeders/             # Roles, admin user, demo data
│
├── storage/                 # Uploads, generated files (local disk; S3 later)
├── public/                  # Static public assets if needed
│
├── modules/                 # Feature modules (see below)
│
└── tests/                   # Mirror modules + integration tests
```

### Folder responsibilities

| Folder | Owns | Must not own |
|--------|------|--------------|
| `app/` | Bootstrap, middleware, global exceptions, helpers | Product/business use cases |
| `config/` | Typed configuration | Runtime business rules |
| `routes/` | Route *registration* only | Fat handlers |
| `database/` | Connection, migrations, seeders | HTTP |
| `modules/` | Feature use cases end-to-end | Random shared junk |
| `storage/` | Files on disk | Business decisions |
| `tests/` | Verification | Production imports of test utils into app code |

### Target module map

```text
modules/
├── auth/
├── users/
├── roles/
├── permissions/
├── products/
├── categories/
├── posts/
└── dashboard/
```

### Request flow

```text
HTTP
  → routes/api.py (registration)
    → module router.py
      → schemas.py (validate in / shape out)
      → policies / auth dependencies
      → service.py (business rules)
        → repository.py (SQL)
          → PostgreSQL
```

---

## Module File Guide

Every feature module follows the same shape:

```text
modules/<feature>/
├── router.py
├── service.py
├── repository.py
├── models.py
├── schemas.py
├── policies.py
└── events.py
```

| File | Role | Laravel analogue | Rules |
|------|------|------------------|-------|
| **`router.py`** | HTTP layer: path, status codes, Depends, call service | Controller + `routes/api.php` entry | Thin. No business rules. No SQL. |
| **`service.py`** | Business logic and orchestration | Service / Action classes | Talks to repositories and other services. No raw query soup. |
| **`repository.py`** | Database operations | Repository / Eloquent query objects | SQLAlchemy lives here. No HTTP. |
| **`models.py`** | SQLAlchemy models | Eloquent models | Persistence shape, relationships. Not API output. |
| **`schemas.py`** | Pydantic validation + response serialization | Form Request + API Resource | Input/output contracts. |
| **`policies.py`** | Authorization rules | Policy + Gate checks | “Can this user do X on this resource?” |
| **`events.py`** | Domain events raised by the module | Events | Keep payloads small; listeners elsewhere or nearby. |

### Layer cheat sheet

| Layer | May | Must not |
|-------|-----|----------|
| Router | Parse HTTP, authorize deps, return schema | Business rules, SQL |
| Service | Rules, transactions orchestration | Scatter query details |
| Repository | Queries, persistence | Know about Request / JWT |
| Schema | Validate / serialize | Hit DB |
| Policy | Allow / deny | Mutate domain as side effect of “check” |

---

## Libraries

For each dependency: **what · why · Laravel equivalent · where**.

### Foundation

#### FastAPI

| | |
|---|---|
| **What** | Modern ASGI web framework for APIs |
| **Why** | OpenAPI docs, async, DI via `Depends`, Pydantic integration |
| **Laravel** | Routing + HTTP kernel + partial Form Request behavior |
| **Where** | `app/main.py`, module `router.py`, dependencies |

#### Uvicorn

| | |
|---|---|
| **What** | ASGI server |
| **Why** | Run FastAPI in dev and prod (or behind a reverse proxy) |
| **Laravel** | `php artisan serve` / php-fpm / Octane (different model) |
| **Where** | Process entry: `uvicorn app.main:app` |

### Validation & config

#### Pydantic

| | |
|---|---|
| **What** | Data validation and serialization from type hints |
| **Why** | Request/response contracts; automatic OpenAPI schemas |
| **Laravel** | Form Requests + API Resources / DTOs |
| **Where** | Every module `schemas.py` |

#### pydantic-settings

| | |
|---|---|
| **What** | Load `.env` / environment into typed Settings |
| **Why** | Fail fast on bad config; one settings object |
| **Laravel** | `.env` + `config/*.php` |
| **Where** | `config/settings.py` (and friends) |

### Database

#### SQLAlchemy 2

| | |
|---|---|
| **What** | SQL toolkit + ORM (2.0 typed style) |
| **Why** | Explicit sessions, strong querying, production ORM |
| **Laravel** | Eloquent + Query Builder |
| **Where** | `models.py`, `repository.py`, `database/connection.py` |

#### psycopg

| | |
|---|---|
| **What** | PostgreSQL driver for Python |
| **Why** | Speak to Postgres from SQLAlchemy |
| **Laravel** | `pdo_pgsql` / DB driver under the hood |
| **Where** | Connection URL / engine setup |

#### Alembic

| | |
|---|---|
| **What** | Migration tool for SQLAlchemy |
| **Why** | Versioned schema changes |
| **Laravel** | `database/migrations` + `artisan migrate` |
| **Where** | `database/migrations/` (Alembic env wired here) |

### Authentication

#### pwdlib\[argon2]

| | |
|---|---|
| **What** | Password hashing helpers with Argon2 |
| **Why** | Modern hashing; no hand-rolled crypto |
| **Laravel** | `Hash::make` / `Hash::check` |
| **Where** | Auth service (register / login) |

#### PyJWT

| | |
|---|---|
| **What** | Encode and decode JWTs |
| **Why** | Stateless API auth for React SPA |
| **Laravel** | Sanctum tokens or JWT packages |
| **Where** | Auth module, security helpers, `Depends(get_current_user)` |

### Testing & quality

#### pytest

| | |
|---|---|
| **What** | Python test framework |
| **Why** | Fixtures, API tests with httpx / TestClient |
| **Laravel** | PHPUnit / Pest |
| **Where** | `tests/` |

#### Ruff

| | |
|---|---|
| **What** | Fast linter + formatter |
| **Why** | One tool for style and many lint rules |
| **Laravel** | Pint / PHP-CS-Fixer |
| **Where** | Local + CI |

#### httpx

| | |
|---|---|
| **What** | Modern HTTP client |
| **Why** | Call external APIs; test FastAPI apps |
| **Laravel** | HTTP client facades / Guzzle |
| **Where** | Tests, integrations, optional outbound calls |

### Cache & jobs

#### Redis

| | |
|---|---|
| **What** | In-memory data store |
| **Why** | Cache, rate limits, job broker for ARQ |
| **Laravel** | Redis for cache / queues |
| **Where** | Phase 10+ queue/cache infrastructure |

#### ARQ

| | |
|---|---|
| **What** | Async Redis job queue for Python |
| **Why** | Background work without leaving the async FastAPI world |
| **Laravel** | Queues + Jobs (`ShouldQueue`) |
| **Where** | Workers, job definitions (Phase 10) |

### Tooling (not a runtime dep, but required)

#### uv

| | |
|---|---|
| **What** | Fast Python package / project manager |
| **Why** | Lockfile, speed, `uv run` |
| **Laravel** | Composer |
| **Where** | `pyproject.toml`, day-to-day commands |

---

## Frontend Stack

**Language rule: JavaScript React only. Do not introduce TypeScript.**

| Library | What | Why | Laravel / prior mental model | Where |
|---------|------|-----|------------------------------|-------|
| **React** | UI library | Dominant admin SPA approach | Inertia/Vue/React SPA against Laravel API | `frontend/src` |
| **Vite** | Dev server + bundler | Fast HMR, simple React setup | Laravel Vite plugin | `frontend/` |
| **Tailwind CSS** | Utility CSS | Speed + Shadcn fit | Breeze / Jetstream Tailwind | Styles |
| **Shadcn UI** | Copy-in UI primitives | Accessible admin components without lock-in | Filament / custom components | `components/ui` |
| **React Router** | Client routing | Auth layouts, protected pages | `routes/web.php` vs SPA router | App shell |
| **TanStack Query** | Server-state fetch/cache | Lists, cache, retries, loading states | “Smart client for API lists” | Data hooks |
| **React Hook Form** | Form state | Less pain on CRUD forms | SPA form libs | Create/edit flows |
| **Zod** | Schema validation (JS) | Client validation + parse API shapes | Form Request rules (client twin) | Form schemas, parsers |

> Zod works with JavaScript. Use JSDoc for editor hints if desired — still **not** TypeScript.

### Frontend target tree (high level)

```text
frontend/
├── src/
│   ├── app/                 # shell, router
│   ├── features/            # auth, users, products, posts, dashboard
│   ├── components/          # shared + shadcn ui
│   ├── lib/                 # api client, auth storage
│   └── main.jsx
├── index.html
├── package.json
└── vite.config.js
```

---

## Laravel → FastAPI Translation

| Laravel | FastShop / FastAPI |
|---------|-------------------|
| Controller | Module `router.py` |
| `routes/api.php` | `routes/api.py` + module routers |
| Form Request | Pydantic `schemas.py` |
| API Resource | Pydantic response schema |
| Eloquent Model | SQLAlchemy `models.py` |
| Service class | `service.py` |
| Repository | `repository.py` |
| Policy | `policies.py` |
| Gate | Permission dependency / policy helpers |
| Middleware | `app/middleware/` + dependencies |
| Service Provider | `app/providers/` + lifespan / factory |
| IoC Container | `Depends()` + explicit constructors |
| Job | ARQ task |
| Event / Listener | `events.py` + listeners |
| `config/*.php` + `.env` | `config/` + pydantic-settings |
| Migrations | Alembic under `database/migrations/` |
| Seeders | `database/seeders/` |
| `storage/` / `public/` | Same roles |
| Facades | Direct imports |
| Sanctum / JWT package | pwdlib + PyJWT |
| Policies in AuthServiceProvider | Import and use policies in deps / router |

---

## Database Design

Initial admin-domain entities:

| Entity | Notes |
|--------|--------|
| **users** | email, password_hash, profile fields, is_active |
| **roles** | name, description |
| **permissions** | code (`products.create`), description |
| **role_user** | pivot User ↔ Role |
| **permission_role** | pivot Role ↔ Permission |
| **categories** | for products (and optionally posts) |
| **products** | belongs to category; price, stock, image path |
| **posts** | belongs to author; draft/published |
| **audit_logs** (optional later) | actor, action, entity, metadata |

### Relationships

```text
users ←→ roles ←→ permissions
users 1──* posts
categories 1──* products
```

| Relationship | Type |
|--------------|------|
| User ↔ Role | Many-to-many |
| Role ↔ Permission | Many-to-many |
| Category → Product | One-to-many |
| User → Post | One-to-many |

Laravel: same cardinality you know (`belongsToMany`, `hasMany`, `belongsTo`). SQLAlchemy expresses it differently; meaning is identical.

---

## Coding Rules

1. **Business logic** → `service.py`
2. **Database queries** → `repository.py`
3. **HTTP logic** → `router.py`
4. **Validation / serialization** → `schemas.py`
5. **Configuration** → `config/`
6. **Authorization rules** → `policies.py` (+ permission deps)
7. Use **dependency injection** (`Depends`, constructors)
8. Avoid **global mutable state**
9. Prefer **simple solutions** over clever abstractions
10. Avoid **premature abstraction** (no interface until a second implementation needs it)
11. Write **readable Python**; prefer clarity over cleverness
12. Use **type hints** on backend public functions
13. Frontend stays **JavaScript** — no TypeScript creep
14. After each phase, update the **Learning Log**

---

## Feature-Based Development Roadmap

Each phase includes: **Feature · Goal · Concepts · Packages · Files · Steps · Laravel comparison · Expected result**.

Implement phases in order. One phase at a time.

---

### Phase 0 — Python Backend Preparation

| | |
|---|---|
| **Feature** | Language foundations |
| **Goal** | Python mental models FastAPI assumes |

**Concepts learned**

- Decorators
- Functions as objects
- Type hints
- Classes
- Dataclasses
- async / await
- Generators
- Context managers

**Packages installed**

- None required (stdlib). Optional: scratch scripts only.

**Files created**

```text
learning/phase0/     # optional scratch — not production app
```

**Implementation steps**

1. Practice decorators wrapping functions (log call, time call).
2. Pass functions as arguments (preview of `Depends`).
3. Annotate functions with type hints; read errors intentionally.
4. Write a small class + dataclass; compare.
5. Write async sleep + gather toy examples.
6. Write a generator and a `with` context manager (resource open/close).

**Laravel comparison**

| Laravel / PHP | Python focus |
|---------------|--------------|
| Attributes / middleware wrappers | Decorators are everyday |
| Typed properties / params | Type hints + (later) Pydantic runtime |
| Rare first-class async request cycle | async is normal for FastAPI I/O |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Core Python, no FastAPI |
| **Why?** | Without this, FastAPI looks like magic |
| **How?** | Short deliberate exercises |
| **Common mistakes?** | Jumping to FastAPI tutorials and memorizing snippets |

**Expected result**

You can explain what a decorator is and why `Depends(fn)` works (callable injection).

---

### Phase 1 — Project Foundation

| | |
|---|---|
| **Feature** | Application bootstrap |
| **Goal** | Running FastAPI app with config and structure |

**Concepts learned**

- uv project / lockfile
- Application factory
- Environment files
- pydantic-settings
- Logging basics
- Laravel-like folder map in Python

**Packages installed**

```text
fastapi
uvicorn
pydantic-settings
```

(Dev: `ruff`, project via `uv`)

**Files created**

```text
backend/
  app/main.py
  app/providers/
  app/middleware/          # may be empty stubs
  app/exceptions/
  app/helpers/
  config/settings.py
  routes/api.py
  routes/web.py
  .env.example
  pyproject.toml
```

**Implementation steps**

1. Init project with `uv`; add FastAPI, Uvicorn, pydantic-settings.
2. Create Laravel-inspired folders (empty modules OK).
3. Implement `Settings` from env.
4. Implement `create_app()` / `main.py` factory.
5. Register a `/health` route via `routes/web.py` or `api.py`.
6. Configure basic logging.
7. Run OpenAPI docs (`/docs`).

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| `bootstrap/app.php` | `app/main.py` factory |
| Service providers | `app/providers/` |
| `config/*.php` + `.env` | `config/settings.py` |
| `artisan serve` | `uv run uvicorn ...` |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Bootable skeleton |
| **Why?** | Every later phase mounts onto this |
| **How?** | Factory + settings + one health route |
| **Common mistakes?** | Dumping everything in one `main.py` forever; hardcoding secrets |

**Expected result**

Running FastAPI application. `/health` OK. Settings load from `.env`.

---

### Phase 2 — Database Foundation

| | |
|---|---|
| **Feature** | Database system |
| **Goal** | PostgreSQL + SQLAlchemy + Alembic ready |

**Concepts learned**

- SQLAlchemy 2 engine / session
- Base model + timestamps
- Alembic revision workflow
- Connection dependency `get_db`

**Packages installed**

```text
sqlalchemy
psycopg
alembic
```

**Files created**

```text
backend/
  config/database.py
  database/connection.py
  database/migrations/     # Alembic versions
  database/seeders/
  # shared DeclarativeBase (location you choose under database/ or app/)
```

**Implementation steps**

1. Add Postgres to local Docker or host; set `DATABASE_URL`.
2. Configure engine + session factory in `database/connection.py`.
3. Create Declarative `Base` with timestamp mixin.
4. Init Alembic; point metadata at Base.
5. Create first migration (empty or baseline).
6. Wire `get_db` dependency for later routers.
7. Document sync vs async choice for this project (pick one learning path).

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Eloquent model base | SQLAlchemy `Base` |
| `artisan migrate` | `alembic upgrade head` |
| `database/migrations` | `database/migrations/` |
| DB facade | `Session` via `Depends` |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Persistence backbone |
| **Why?** | Auth and modules need real tables |
| **How?** | Engine → session → Alembic |
| **Common mistakes?** | Long-lived global sessions; mixing raw SQL in routers |

**Expected result**

Database ready. Migrations apply. App can obtain a session per request.

---

### Phase 3 — Authentication

| | |
|---|---|
| **Feature** | User authentication |
| **Goal** | Complete auth system (register, login, JWT, current user) |

**Concepts learned**

- Argon2 hashing via pwdlib
- JWT create/verify via PyJWT
- FastAPI `Depends()` chains
- Bearer auth for SPA

**Packages installed**

```text
pwdlib[argon2]
pyjwt
```

**Files created**

```text
modules/auth/
  router.py
  service.py
  repository.py
  schemas.py
  policies.py          # may be thin at first
  events.py            # e.g. UserRegistered (optional stub)
modules/users/models.py
config/security.py
database/migrations/*_users.py
```

**Implementation steps**

1. Users table migration (email unique, password_hash, …).
2. Auth schemas: register, login, token response, user read.
3. Hash passwords with pwdlib Argon2.
4. Issue JWT on login; verify in `get_current_user`.
5. Routes: register, login, `GET /me`.
6. Protect a sample route with `Depends(get_current_user)`.
7. Register auth router in `routes/api.py`.

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| `Hash::make` | pwdlib Argon2 |
| Sanctum / JWT | PyJWT access tokens |
| `auth` middleware | `Depends(get_current_user)` |
| `RegisterController` / Fortify | `modules/auth/router.py` |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Identity for the API |
| **Why?** | All admin features need a user |
| **How?** | Hash → JWT → Depends |
| **Common mistakes?** | Storing plaintext; putting JWT secret in code; fat auth router with SQL |

**Expected result**

Complete authentication system. Register/login work. `/me` returns current user.

---

### Phase 4 — Authorization

| | |
|---|---|
| **Feature** | Roles and permissions |
| **Goal** | Protected resources via RBAC + policies |

**Concepts learned**

- Roles / permissions tables
- Permission dependencies
- Policy functions/classes
- Laravel Gate/Policy mapping

**Packages installed**

- None new (use existing stack)

**Files created**

```text
modules/roles/
modules/permissions/
modules/users/          # assign roles
*/policies.py
database/seeders/rbac.py
database/migrations/*_rbac.py
```

**Implementation steps**

1. Migrations: roles, permissions, pivots.
2. Seed admin role + baseline permissions (`users.view`, `products.create`, …).
3. Implement `require_permission("…")` dependency.
4. Implement module `policies.py` for object-level rules when needed.
5. Attach checks to sample protected routes.
6. Ensure 403 vs 401 distinction.

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Gate | Permission dependency helpers |
| Policy class | `policies.py` |
| `$this->authorize()` | `Depends(require_permission(...))` / policy call |
| spatie/permission | Built yourself for learning |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Who can do what |
| **Why?** | Admin panel without authz is insecure theater |
| **How?** | RBAC tables + Depends + policies |
| **Common mistakes?** | Checking roles only (`if admin`) forever; forgetting seed permissions |

**Expected result**

Protected resources. Missing permission → 403.

---

### Phase 5 — Users Module

| | |
|---|---|
| **Feature** | User management |
| **Goal** | Admin user CRUD with list UX |

**Concepts learned**

- REST API design
- Pagination, filtering, searching, sorting
- Full module vertical slice

**Packages installed**

- None new

**Files created**

```text
modules/users/
  router.py
  service.py
  repository.py
  models.py
  schemas.py
  policies.py
  events.py
```

**Implementation steps**

1. List users with page/size, search (email/name), sort.
2. Create / update / soft-disable user.
3. Assign roles (if ready).
4. Enforce permissions (`users.view`, `users.update`, …).
5. Tests for happy path + forbidden.

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| UserController + FormRequest | users router + schemas |
| Query filters / Spatie Query Builder | repository query composition |
| API Resource | response schema |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Admin user management API |
| **Why?** | Practice list patterns before products |
| **How?** | Router → service → repository with query params |
| **Common mistakes?** | N+1 role loading; allowing user to escalate own roles without policy |

**Expected result**

Admin user management API complete.

---

### Phase 6 — Products Module

| | |
|---|---|
| **Feature** | Product management |
| **Goal** | Inventory management (categories + products + images) |

**Concepts learned**

- Nested resources / FKs
- File upload to `storage/`
- Rich filtering

**Packages installed**

- None required initially (stdlib + FastAPI `UploadFile`)

**Files created**

```text
modules/categories/
modules/products/
storage/app/products/    # or similar
database/migrations/*_catalog.py
```

**Implementation steps**

1. Categories CRUD.
2. Products CRUD with `category_id`.
3. Image upload endpoint; store under `storage/`; serve safely.
4. Filters: category, price range, active flag; search name; sort; paginate.
5. Permissions on mutating routes.

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| ProductController + stores disk | products module + `storage/` |
| `$request->file()` | `UploadFile` |
| Eloquent relationships | SQLAlchemy relationships |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Catalog admin API |
| **Why?** | Core domain of FastShop |
| **How?** | Categories first, then products + upload |
| **Common mistakes?** | Trusting client filenames; storing images in git; SQL in router |

**Expected result**

Complete inventory management backend.

---

### Phase 7 — Posts Module

| | |
|---|---|
| **Feature** | CMS |
| **Goal** | Simple content management |

**Concepts learned**

- Draft vs published workflows
- Author ownership policies
- Reusing list/filter patterns

**Packages installed**

- None new

**Files created**

```text
modules/posts/
database/migrations/*_posts.py
```

**Implementation steps**

1. Posts table: title, slug, body, status, author_id, published_at.
2. CRUD + publish/unpublish actions.
3. Policy: author or admin can edit (decide and document).
4. Optional: post categories if useful (keep simple).

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| PostPolicy | `posts/policies.py` |
| Eloquent scopes (`published()`) | repository methods |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Simple CMS API |
| **Why?** | Second domain module; proves modularity |
| **How?** | Same module template as users/products |
| **Common mistakes?** | Duplicating product list code instead of tiny shared helpers |

**Expected result**

Simple CMS backend.

---

### Phase 8 — Dashboard

| | |
|---|---|
| **Feature** | Admin dashboard |
| **Goal** | Statistics + charts API |

**Concepts learned**

- Aggregation queries (`count`, `group_by`)
- Read-only dashboard service
- Payload shape for charts

**Packages installed**

- None new

**Files created**

```text
modules/dashboard/
  router.py
  service.py
  repository.py
  schemas.py
  policies.py
  events.py            # often unused — OK
```

**Implementation steps**

1. Totals: users, products, posts, published vs draft.
2. Groupings: products per category.
3. Recent activity endpoints (or last N products/posts).
4. Permission: `dashboard.view`.

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Dashboard controller + aggregates | dashboard module |
| `DB::raw` / Eloquent aggregates | SQLAlchemy `func` |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Aggregation APIs for UI |
| **Why?** | Admin home needs summary data |
| **How?** | Few purposeful SQL aggregations |
| **Common mistakes?** | Multiple chatty endpoints when one summary DTO would do |

**Expected result**

Admin dashboard APIs ready for React charts/cards.

---

### Phase 9 — React Admin Panel

| | |
|---|---|
| **Feature** | Frontend application |
| **Goal** | Complete JS React admin panel |

**Concepts learned**

- Vite + React (JavaScript)
- Tailwind + Shadcn
- Auth storage + protected routes
- TanStack Query + forms + dialogs

**Packages installed** (frontend)

```text
react
react-dom
react-router-dom
@tanstack/react-query
react-hook-form
zod
tailwindcss
# shadcn components added via CLI (JS)
```

**Files created**

```text
frontend/
  src/main.jsx
  src/app/...
  src/features/auth|users|products|posts|dashboard/
  src/components/ui/...
  src/lib/api.js
  vite.config.js
  package.json
```

**Implementation steps**

1. Scaffold Vite React **JavaScript** template (not TS).
2. Tailwind + Shadcn setup.
3. API client with JWT header.
4. Login page → store token → protected layout.
5. Dashboard cards from Phase 8 APIs.
6. Tables for users/products/posts.
7. Forms + dialogs for create/edit.
8. Logout + 401 handling.

**Laravel comparison**

Closest: **Laravel API + separate SPA**. Not Blade. Auth feels like token Bearer SPA.

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Full admin UI in JS |
| **Why?** | Prove API real-world usability |
| **How?** | Feature folders matching backend modules |
| **Common mistakes?** | Accidentally scaffolding TypeScript; putting business rules only in UI; ignoring 403 UX |

**Expected result**

Complete admin panel: auth, dashboard, tables, forms, dialogs.

---

### Phase 10 — Advanced Backend

| | |
|---|---|
| **Feature** | Middleware · Events · Queues |
| **Goal** | Production backend cross-cutting concepts |

**Concepts learned**

- Request logging middleware
- Global exception handling
- CORS for React origin
- Domain events + listeners
- Redis + ARQ background jobs

**Packages installed**

```text
redis
arq
httpx          # if not already (tests / clients)
```

**Files created**

```text
app/middleware/request_logging.py
app/exceptions/handlers.py
config/security.py          # CORS settings expanded
modules/*/events.py         # real events
# listeners package or app/listeners/
# ARQ worker settings
```

**Implementation steps**

1. Middleware: request id + timing logs.
2. Map domain/validation errors to consistent JSON.
3. Configure CORS for Vite origin.
4. Emit event on meaningful actions (e.g. product created).
5. Listener writes audit row or enqueues job.
6. Run Redis; implement one ARQ job (email stub / thumbnail / stats rebuild).

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Middleware | `app/middleware/` |
| Exception Handler | FastAPI handlers |
| Event + Listener | events + listeners |
| Queue job | ARQ task |
| `cors.php` | CORS middleware config |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Cross-cutting production plumbing |
| **Why?** | Real apps need ops-friendly behavior |
| **How?** | Middleware → errors → events → Redis/ARQ |
| **Common mistakes?** | Logging secrets; sync heavy work in request; unbounded CORS `*` in prod |

**Expected result**

Production backend concepts working: middleware, errors, events, queues.

---

### Phase 11 — Production Quality

| | |
|---|---|
| **Feature** | Ship readiness |
| **Goal** | Tests, Docker, CI/CD, security, optimization basics |

**Concepts learned**

- pytest API/unit strategy
- Docker Compose multi-service
- CI lint/test
- Security checklist (secrets, headers, uploads)
- Simple query/index optimization

**Packages installed**

- Test extras as needed (`pytest`, `httpx`, coverage optional)

**Files created**

```text
Dockerfile
docker-compose.yml
.github/workflows/ci.yml    # or equivalent
tests/ expanded
```

**Implementation steps**

1. Expand tests: auth, authz, one module CRUD.
2. Dockerize API + Postgres + Redis + worker + frontend (or FE separate).
3. CI: ruff + pytest on PR.
4. Security pass: env secrets, upload validation, JWT settings, rate limit sketch.
5. Add missing indexes for hot filters.
6. Write short deploy checklist in Learning Log.

**Laravel comparison**

| Laravel | FastShop |
|---------|----------|
| Sail | Docker Compose |
| PHPUnit in CI | pytest in CI |
| Horizon / queue workers | ARQ worker container |

**What / Why / How / Mistakes**

| | |
|---|---|
| **What?** | Production quality bar |
| **Why?** | Learning ends when ship habits exist |
| **How?** | Test → containerize → CI → harden |
| **Common mistakes?** | CI without migrations check; baking `.env` into images |

**Expected result**

Confident run path: tests green, Compose up, CI gating merges.

---

## Commands

### Backend (uv)

```bash
uv sync
uv add fastapi uvicorn pydantic-settings
uv add sqlalchemy psycopg alembic
uv add 'pwdlib[argon2]' pyjwt
uv add redis arq httpx
uv add --dev pytest ruff

uv run uvicorn app.main:app --reload
uv run pytest
uv run ruff check .
uv run ruff format .
```

### Migrations

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
uv run alembic downgrade -1
```

### Frontend (JavaScript)

```bash
cd frontend
npm create vite@latest . -- --template react   # JS template, NOT react-ts
npm install
npm install react-router-dom @tanstack/react-query react-hook-form zod
npm run dev
npm run build
```

### Workers (Phase 10+)

```bash
uv run arq app.core_or_queue.WorkerSettings   # adjust to real path when implemented
```

### Docker (Phase 11)

```bash
docker compose up --build
docker compose exec api uv run alembic upgrade head
```

---

## Living Learning Log

The README evolves. After **each completed phase**, append an entry.

### Entry template

```markdown
### Phase X — <name> — <date>

#### Lessons learned
-

#### Architecture decisions
- Decision:
- Alternatives:
- Why:

#### New libraries
- name — why it earned its place

#### Problems solved
- Symptom → cause → fix

#### What / Why / How (phase recap)
- What:
- Why:
- How:

#### Laravel equivalent (what finally clicked)
-

#### Common mistakes I made
-
```

### Log

<!-- Append below. Never delete old entries. -->

#### Phase 0

_Pending_

#### Phase 1

_Pending_

#### Phase 2

_Pending_

#### Phase 3

_Pending_

#### Phase 4

_Pending_

#### Phase 5

_Pending_

#### Phase 6

_Pending_

#### Phase 7

_Pending_

#### Phase 8

_Pending_

#### Phase 9

_Pending_

#### Phase 10

_Pending_

#### Phase 11

_Pending_

---

## Definition of Done

FastShop learning milestone complete when:

- [ ] Laravel-inspired backend tree exists and you can explain each folder
- [ ] Auth (Argon2 + JWT) works
- [ ] RBAC + policies protect resources
- [ ] Users / Products / Posts modules follow router → service → repository
- [ ] Dashboard aggregations exist
- [ ] React **JavaScript** admin works (auth, tables, forms, dialogs)
- [ ] Middleware, exception shape, events, Redis + ARQ job exist
- [ ] Tests + Docker + CI in place
- [ ] Learning Log filled for every phase

---

## How to continue

1. Start **Phase 0** (Python only — no FastAPI app required).
2. Then **Phase 1** (foundation only).
3. Tell the coding agent:  
   `Implement Phase N only, following README. No TypeScript. No skipping explanations.`

---

*FastShop — learn the why, then ship the what.*
