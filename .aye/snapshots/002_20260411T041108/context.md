Yeah, I get you completely.

You want me to be the architect — lay out the entire blueprint so another instance of me (or any capable coding AI) can just pick it up and build it, no ambiguity, no guesswork.

Let me piece together what you're after:

You want a modern replacement for FIS Prophet (the actuarial modeling and data management platform that insurance companies use). Prophet is powerful but it's old, expensive, clunky, requires specialized actuarial/technical knowledge, and has terrible UX. Your vision is something that handles the same core jobs — actuarial modeling, policy data management, reporting, regulatory compliance — but is fast, cheap, intuitive enough that a non-technical insurance employee can use it without training.

Let me build this out properly.

ACTUFLOW

Modern Insurance Data Management & Actuarial Platform

PART 1: PRODUCT VISION & PHILOSOPHY

What this is: A web-based platform that lets insurance companies manage policy data, run actuarial calculations, generate regulatory reports, and model scenarios — all through a clean, drag-and-drop, spreadsheet-familiar interface. No coding. No command lines. No actuarial software certifications needed.

Who uses it:
- Actuaries (who currently suffer through Prophet/Moses/ResQ)
- Underwriters managing policy portfolios
- Finance teams pulling reports
- Compliance officers generating regulatory filings
- C-suite executives viewing dashboards
- Data entry clerks inputting policy information

Core design principles:
If it feels like a spreadsheet, people will use it. Lean into that familiarity.
Every complex calculation happens behind the scenes. The user sees inputs and outputs, never formulas or code.
Everything is auditable. Insurance regulators demand full trails.
Role-based access. The data clerk sees different things than the Chief Actuary.
Real-time collaboration. Multiple people working on the same model simultaneously.

PART 2: CORE MODULES (What the software does)

Module 1: Policy Data Manager
The central hub. All policy data lives here — life, health, property, casualty, whatever lines of business the company writes. Import from CSV/Excel/legacy systems, manual entry through forms, bulk operations. Think of it as a purpose-built database with an interface that feels like Excel.

Module 2: Actuarial Calculation Engine
This replaces Prophet's core. Pre-built actuarial models (reserving, pricing, cash flow projections, liability calculations) that users configure through a visual interface. They pick a model template, map their data columns to the model inputs, set assumptions, and hit run. The engine handles mortality tables, lapse rates, discount curves, everything — but the user just sees dropdown menus and sliders.

Module 3: Assumptions Manager
Actuarial work lives and dies on assumptions. This module lets users create, version, approve, and audit assumption sets — mortality tables, morbidity rates, lapse assumptions, expense assumptions, economic scenarios. Full version history. Approval workflows. Compare assumption sets side by side.

Module 4: Scenario & Stress Testing
Run what-if scenarios. What happens to our reserves if interest rates drop 200bps? What if lapse rates spike 30%? Users define scenarios through a visual builder, run them against their portfolio, and see results in comparative dashboards.

Module 5: Reporting & Compliance
Pre-built report templates for IFRS 17, Solvency II, US GAAP, LDTI, local regulatory requirements. Users select the report, the reporting period, and the data scope — the system generates the filing. Custom report builder for internal reporting.

Module 6: Dashboard & Analytics
Executive dashboards showing portfolio health, reserve adequacy, profitability by product line, trend analysis. Drag-and-drop dashboard builder. Scheduled email reports.

Module 7: Workflow & Collaboration
Task assignment, approval chains, review workflows for end-of-quarter processes. Comments on any data point or calculation. Real-time multi-user editing. Notification system.

Module 8: Administration & Security
User management, role-based access control, SSO integration, audit logging of every action, data encryption, backup management.

PART 3: TECHNOLOGY STACK

Frontend: React with TypeScript, using a component library like Ant Design (which has excellent table/data components that feel spreadsheet-like). TanStack Table for the heavy data grid work. Recharts or D3 for visualizations. Zustand for state management. React Query for server state.

Backend: Python with FastAPI. Python because the actuarial calculation libraries (NumPy, SciPy, Pandas) are all Python-native. FastAPI because it's fast, async, auto-documents APIs, and handles concurrent calculation jobs well.

Calculation Engine: A dedicated Python service using NumPy/SciPy for actuarial math, Celery with Redis for job queuing (calculations can take minutes — they need to run async), and a model definition layer that translates the visual model builder into executable calculation graphs.

Database: PostgreSQL as the primary relational database (policy data is highly relational). Redis for caching, session management, and as Celery's message broker. MinIO or S3-compatible object storage for file uploads, report outputs, and large dataset storage.

Authentication: Keycloak for enterprise SSO, LDAP integration, RBAC. Insurance companies will demand this.

Infrastructure: Docker containers, orchestrated with Docker Compose for development and Kubernetes for production. Nginx as reverse proxy.

Search: Elasticsearch for searching across policies, reports, audit logs.

PART 4: COMPLETE FOLDER STRUCTURE & FILE MANIFEST


actuflow/
│
├── README.md
│       → Project overview, setup instructions, architecture summary,
│         contribution guidelines. The first thing any developer reads.
│
├── LICENSE
│       → Business source license or proprietary license header.
│
├── docker-compose.yml
│       → Defines all services for local development: frontend, backend,
│         calculation engine, PostgreSQL, Redis, MinIO, Elasticsearch,
│         Keycloak. One command to spin up the entire stack.
│
├── docker-compose.prod.yml
│       → Production-oriented compose file with proper resource limits,
│         replicas, health checks, and external volume mounts.
│
├── .env.example
│       → Template for environment variables. Database URLs, Redis URL,
│         S3 credentials, JWT secrets, Keycloak config, SMTP settings
│         for email notifications. Never committed with real values.
│
├── .gitignore
│       → Standard ignores for Python, Node, Docker, IDE files,
│         environment files, uploaded data, generated reports.
│
├── Makefile
│       → Convenience commands: make dev (start everything), make test,
│         make migrate, make seed, make lint, make build, make deploy.
│         Abstracts away complex Docker/CLI commands.
│
│
│
├── docs/
│   │       → All project documentation lives here.
│   │
│   ├── architecture.md
│   │       → High-level system architecture document. Describes how
│   │         all services communicate, data flow diagrams, deployment
│   │         topology. Includes ASCII/Mermaid diagrams.
│   │
│   ├── api-contracts.md
│   │       → Defines the API contract between frontend and backend.
│   │         Every endpoint, request/response shapes, error codes.
│   │         This is the source of truth before OpenAPI auto-generation.
│   │
│   ├── data-model.md
│   │       → Complete database schema documentation. Every table,
│   │         every column, every relationship, every index. Explains
│   │         the reasoning behind schema decisions.
│   │
│   ├── calculation-engine.md
│   │       → How the actuarial calculation engine works. Model
│   │         definition format, calculation graph execution, how
│   │         assumptions feed into models, how results are stored.
│   │         This is the most complex document in the project.
│   │
│   ├── user-roles-permissions.md
│   │       → Defines every role (Admin, Actuary, Analyst, Clerk,
│   │         Auditor, Executive), what each can see and do, how
│   │         permissions cascade, how custom roles work.
│   │
│   ├── deployment-guide.md
│   │       → Step-by-step production deployment. Infrastructure
│   │         requirements, Kubernetes manifests explanation, SSL
│   │         setup, database backup strategy, monitoring setup.
│   │
│   ├── regulatory-compliance.md
│   │       → How the system supports IFRS 17, Solvency II, US GAAP
│   │         LDTI. What calculations map to which standards. How
│   │         audit trails satisfy regulatory requirements.
│   │
│   └── onboarding-guide.md
│           → For new developers joining the project. Local setup,
│             codebase walkthrough, how to add a new feature end-to-end,
│             testing conventions, PR process.
│
│
│
├── backend/
│   │
│   ├── Dockerfile
│   │       → Multi-stage build. First stage installs dependencies,
│   │         second stage copies only what's needed for a slim
│   │         production image. Based on python:3.12-slim.
│   │
│   ├── pyproject.toml
│   │       → Python project configuration. Dependencies managed with
│   │         Poetry or pip. Includes FastAPI, SQLAlchemy, Alembic,
│   │         Pydantic, Celery, Redis, boto3 (for S3/MinIO), 
│   │         python-keycloak, elasticsearch-py, pandas, numpy, scipy.
│   │
│   ├── alembic.ini
│   │       → Alembic configuration for database migrations. Points
│   │         to the migrations directory and database URL.
│   │
│   │
│   ├── app/
│   │   │
│   │   ├── __init__.py
│   │   │       → Package init. Can contain version string.
│   │   │
│   │   ├── main.py
│   │   │       → FastAPI application factory. Creates the app instance,
│   │   │         registers all routers, sets up CORS middleware, exception
│   │   │         handlers, startup/shutdown events (DB pool init, Redis
│   │   │         connection, Elasticsearch client). Health check endpoint
│   │   │         lives here too.
│   │   │
│   │   ├── config.py
│   │   │       → Pydantic Settings class that reads from environment
│   │   │         variables. Database URL, Redis URL, S3 config, JWT
│   │   │         settings, Keycloak config, pagination defaults, file
│   │   │         upload limits, CORS origins. Validated on startup.
│   │   │
│   │   ├── dependencies.py
│   │   │       → FastAPI dependency injection functions. get_db() yields
│   │   │         a database session. get_current_user() extracts and
│   │   │         validates JWT token. get_redis() returns Redis client.
│   │   │         require_role("actuary") returns a dependency that
│   │   │         checks the user's role.
│   │   │
│   │   ├── exceptions.py
│   │   │       → Custom exception classes: NotFoundError, ForbiddenError,
│   │   │         ValidationError, CalculationError, DataImportError.
│   │   │         Each maps to an HTTP status code and error response shape.
│   │   │
│   │   │
│   │   ├── models/
│   │   │   │       → SQLAlchemy ORM models. Each file defines one or
│   │   │   │         more related database tables.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │       → Imports all models so Alembic can discover them.
│   │   │   │
│   │   │   ├── base.py
│   │   │   │       → Base model class that all others inherit from.
│   │   │   │         Includes common columns: id (UUID), created_at,
│   │   │   │         updated_at, created_by, is_deleted (soft delete).
│   │   │   │         Also defines the SQLAlchemy declarative base.
│   │   │   │
│   │   │   ├── user.py
│   │   │   │       → User model. Fields: id, email, full_name, role_id,
│   │   │   │         department, is_active, last_login, keycloak_id.
│   │   │   │         Relationships to Role, AuditLog, TaskAssignment.
│   │   │   │
│   │   │   ├── role.py
│   │   │   │       → Role and Permission models. Role has name and
│   │   │   │         description. Permission has resource and action
│   │   │   │         (e.g., resource="policy", action="delete").
│   │   │   │         Many-to-many relationship between Role and Permission
│   │   │   │         via role_permissions junction table.
│   │   │   │
│   │   │   ├── policy.py
│   │   │   │       → The big one. Policy model with fields: policy_number,
│   │   │   │         product_type (life/health/property/casualty),
│   │   │   │         product_code, status (active/lapsed/surrendered/
│   │   │   │         matured/claimed), policyholder_id, issue_date,
│   │   │   │         maturity_date, sum_assured, premium_amount,
│   │   │   │         premium_frequency, currency, branch_code,
│   │   │   │         underwriter_id. Relationships to Policyholder,
│   │   │   │         Coverage, Rider, Claim, CashFlow.
│   │   │   │
│   │   │   ├── policyholder.py
│   │   │   │       → Policyholder model. Personal info: name, date_of_birth,
│   │   │   │         gender, smoker_status, occupation_class, address,
│   │   │   │         contact info. Relationship to policies (one-to-many).
│   │   │   │
│   │   │   ├── coverage.py
│   │   │   │       → Coverage/benefit details attached to a policy.
│   │   │   │         Coverage type, benefit amount, start/end dates,
│   │   │   │         rider flag, premium allocation.
│   │   │   │
│   │   │   ├── claim.py
│   │   │   │       → Claims data. Claim number, policy_id, claim_date,
│   │   │   │         claim_type, claim_amount, status, settlement_date,
│   │   │   │         settlement_amount, adjuster_notes.
│   │   │   │
│   │   │   ├── assumption_set.py
│   │   │   │       → AssumptionSet model: name, version, status (draft/
│   │   │   │         approved/archived), effective_date, approved_by,
│   │   │   │         approval_date, description. Relationship to
│   │   │   │         individual assumption tables.
│   │   │   │
│   │   │   ├── assumption_table.py
│   │   │   │       → Individual assumption tables within a set. Table type
│   │   │   │         (mortality/lapse/expense/morbidity/discount_rate),
│   │   │   │         name, data stored as JSONB (flexible structure for
│   │   │   │         different table shapes — age-based, duration-based,
│   │   │   │         age-and-duration-based). Belongs to AssumptionSet.
│   │   │   │
│   │   │   ├── model_definition.py
│   │   │   │       → Actuarial model definitions. Name, description,
│   │   │   │         model_type (reserving/pricing/cashflow/valuation),
│   │   │   │         line_of_business, configuration stored as JSONB
│   │   │   │         (defines the calculation graph — what inputs, what
│   │   │   │         steps, what outputs), version, status, created_by.
│   │   │   │
│   │   │   ├── calculation_run.py
│   │   │   │       → Records of calculation executions. Fields: id,
│   │   │   │         model_definition_id, assumption_set_id, run_name,
│   │   │   │         status (queued/running/completed/failed/cancelled),
│   │   │   │         started_at, completed_at, duration_seconds,
│   │   │   │         triggered_by (user_id), policy_filter (JSONB —
│   │   │   │         which policies were included in this run, e.g.
│   │   │   │         {"product_code": "WL01", "status": "active"}),
│   │   │   │         parameters (JSONB — valuation date, reporting
│   │   │   │         basis, etc.), error_message (if failed),
│   │   │   │         result_summary (JSONB — high-level totals cached
│   │   │   │         here for quick dashboard display). Relationships
│   │   │   │         to ModelDefinition, AssumptionSet, CalculationResult.
│   │   │   │
│   │   │   ├── calculation_result.py
│   │   │   │       → Stores detailed calculation outputs. Fields: id,
│   │   │   │         calculation_run_id, policy_id, projection_month,
│   │   │   │         result_type (reserve/cashflow/profit_margin/etc.),
│   │   │   │         values (JSONB — flexible structure to hold whatever
│   │   │   │         the model outputs: premiums, claims, expenses,
│   │   │   │         reserves, net_cashflow, discount_factors, present
│   │   │   │         values). This table will be large — partitioned by
│   │   │   │         calculation_run_id and indexed on policy_id.
│   │   │   │
│   │   │   ├── report_template.py
│   │   │   │       → Defines report templates. Fields: id, name,
│   │   │   │         report_type (regulatory/internal/adhoc),
│   │   │   │         regulatory_standard (IFRS17/SolvencyII/USGAAP/
│   │   │   │         LDTI/null for internal), template_config (JSONB —
│   │   │   │         defines sections, data sources, formatting rules,
│   │   │   │         aggregation logic), output_format (PDF/Excel/CSV),
│   │   │   │         is_system_template (true for built-in regulatory
│   │   │   │         templates, false for user-created ones), created_by.
│   │   │   │
│   │   │   ├── generated_report.py
│   │   │   │       → Records of generated reports. Fields: id,
│   │   │   │         report_template_id, reporting_period_start,
│   │   │   │         reporting_period_end, generated_by, generated_at,
│   │   │   │         status (generating/completed/failed), file_path
│   │   │   │         (S3/MinIO path to the output file), file_size,
│   │   │   │         parameters (JSONB — any filters or options the
│   │   │   │         user selected when generating).
│   │   │   │
│   │   │   ├── scenario.py
│   │   │   │       → Scenario definitions for stress testing. Fields:
│   │   │   │         id, name, description, scenario_type (deterministic/
│   │   │   │         stochastic), base_assumption_set_id, adjustments
│   │   │   │         (JSONB — describes how to modify the base assumptions,
│   │   │   │         e.g. {"mortality": {"factor": 1.1}, "lapse":
│   │   │   │         {"factor": 1.3}, "discount_rate": {"shift": -0.02}}),
│   │   │   │         created_by, status. Relationship to ScenarioResult.
│   │   │   │
│   │   │   ├── scenario_result.py
│   │   │   │       → Results of scenario runs. Links a scenario to a
│   │   │   │         calculation_run. Fields: id, scenario_id,
│   │   │   │         calculation_run_id, comparison_base_run_id (the
│   │   │   │         "base case" run to compare against), impact_summary
│   │   │   │         (JSONB — delta in reserves, P&L impact, capital
│   │   │   │         impact, etc.).
│   │   │   │
│   │   │   ├── dashboard_config.py
│   │   │   │       → User-created dashboard configurations. Fields: id,
│   │   │   │         name, owner_id, is_shared, layout (JSONB — defines
│   │   │   │         widget positions, sizes in a grid system), widgets
│   │   │   │         (JSONB array — each widget has type, data_source,
│   │   │   │         chart_type, filters, title). Relationship to User.
│   │   │   │
│   │   │   ├── data_import.py
│   │   │   │       → Tracks data import jobs. Fields: id, file_name,
│   │   │   │         file_path, import_type (policy/claims/assumptions/
│   │   │   │         policyholder), status (uploaded/validating/validated/
│   │   │   │         importing/completed/failed), total_rows,
│   │   │   │         processed_rows, error_rows, error_details (JSONB
│   │   │   │         array — row number, column, error message for each
│   │   │   │         failed row), column_mapping (JSONB — maps source
│   │   │   │         file columns to system fields), uploaded_by,
│   │   │   │         started_at, completed_at.
│   │   │   │
│   │   │   ├── audit_log.py
│   │   │   │       → Immutable audit trail. Fields: id, timestamp,
│   │   │   │         user_id, action (create/update/delete/approve/
│   │   │   │         reject/export/login/logout/run_calculation),
│   │   │   │         resource_type (policy/assumption_set/model/report/
│   │   │   │         etc.), resource_id, old_values (JSONB), new_values
│   │   │   │         (JSONB), ip_address, user_agent. This table is
│   │   │   │         append-only — no updates or deletes ever. Indexed
│   │   │   │         on timestamp, user_id, resource_type, resource_id.
│   │   │   │
│   │   │   ├── task.py
│   │   │   │       → Workflow tasks. Fields: id, title, description,
│   │   │   │         task_type (review/approval/data_entry/calculation/
│   │   │   │         custom), status (open/in_progress/completed/
│   │   │   │         cancelled), priority (low/medium/high/critical),
│   │   │   │         assigned_to, assigned_by, due_date, related_resource_
│   │   │   │         type, related_resource_id, completion_notes.
│   │   │   │
│   │   │   ├── comment.py
│   │   │   │       → Comments/notes on any resource. Fields: id,
│   │   │   │         resource_type, resource_id, user_id, content,
│   │   │   │         parent_comment_id (for threaded replies),
│   │   │   │         is_resolved. Polymorphic — can attach to policies,
│   │   │   │         assumption sets, calculation runs, anything.
│   │   │   │
│   │   │   └── notification.py
│   │   │           → User notifications. Fields: id, user_id, type
│   │   │             (task_assigned/approval_needed/calculation_complete/
│   │   │             report_ready/comment_mention/import_complete),
│   │   │             title, message, is_read, resource_type, resource_id,
│   │   │             created_at.
│   │   │
│   │   │
│   │   ├── schemas/
│   │   │   │       → Pydantic schemas for request/response validation
│   │   │   │         and serialization. Mirrors the models directory
│   │   │   │         but defines API shapes, not DB shapes.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── common.py
│   │   │   │       → Shared schemas used across modules. PaginatedResponse
│   │   │   │         (generic wrapper with items, total, page, page_size),
│   │   │   │         SortParam, FilterParam, BulkActionRequest,
│   │   │   │         BulkActionResponse, ErrorResponse, SuccessMessage,
│   │   │   │         DateRange, FileUploadResponse.
│   │   │   │
│   │   │   ├── user.py
│   │   │   │       → UserCreate, UserUpdate, UserResponse, UserListItem,
│   │   │   │         UserProfile (for the logged-in user's own profile),
│   │   │   │         RoleResponse, PermissionResponse.
│   │   │   │
│   │   │   ├── policy.py
│   │   │   │       → PolicyCreate, PolicyUpdate, PolicyResponse,
│   │   │   │         PolicyListItem (slimmed down for table views),
│   │   │   │         PolicyFilter (all the filterable fields with
│   │   │   │         optional types), PolicyBulkUpdate,
│   │   │   │         PolicyImportMapping, PolicySummaryStats.
│   │   │   │
│   │   │   ├── policyholder.py
│   │   │   │       → PolicyholderCreate, PolicyholderUpdate,
│   │   │   │         PolicyholderResponse, PolicyholderWithPolicies.
│   │   │   │
│   │   │   ├── coverage.py
│   │   │   │       → CoverageCreate, CoverageUpdate, CoverageResponse.
│   │   │   │
│   │   │   ├── claim.py
│   │   │   │       → ClaimCreate, ClaimUpdate, ClaimResponse,
│   │   │   │         ClaimFilter, ClaimSummaryStats.
│   │   │   │
│   │   │   ├── assumption.py
│   │   │   │       → AssumptionSetCreate, AssumptionSetUpdate,
│   │   │   │         AssumptionSetResponse, AssumptionSetListItem,
│   │   │   │         AssumptionTableCreate, AssumptionTableUpdate,
│   │   │   │         AssumptionTableResponse, AssumptionApprovalRequest,
│   │   │   │         AssumptionComparison (for side-by-side comparison).
│   │   │   │
│   │   │   ├── model.py
│   │   │   │       → ModelDefinitionCreate, ModelDefinitionUpdate,
│   │   │   │         ModelDefinitionResponse, ModelDefinitionListItem,
│   │   │   │         ModelConfigSchema (validates the JSONB calculation
│   │   │   │         graph structure — this is critical for the visual
│   │   │   │         model builder to work correctly).
│   │   │   │
│   │   │   ├── calculation.py
│   │   │   │       → CalculationRunCreate (model_id, assumption_set_id,
│   │   │   │         policy_filter, parameters), CalculationRunResponse,
│   │   │   │         CalculationRunListItem, CalculationRunProgress
│   │   │   │         (for real-time progress updates via WebSocket),
│   │   │   │         CalculationResultResponse, CalculationResultFilter,
│   │   │   │         CalculationSummary.
│   │   │   │
│   │   │   ├── scenario.py
│   │   │   │       → ScenarioCreate, ScenarioUpdate, ScenarioResponse,
│   │   │   │         ScenarioAdjustment (typed structure for the
│   │   │   │         adjustments JSONB), ScenarioResultResponse,
│   │   │   │         ScenarioComparison.
│   │   │   │
│   │   │   ├── report.py
│   │   │   │       → ReportTemplateCreate, ReportTemplateResponse,
│   │   │   │         GenerateReportRequest, GeneratedReportResponse,
│   │   │   │         ReportScheduleCreate (for recurring report
│   │   │   │         generation).
│   │   │   │
│   │   │   ├── dashboard.py
│   │   │   │       → DashboardConfigCreate, DashboardConfigUpdate,
│   │   │   │         DashboardConfigResponse, WidgetConfig,
│   │   │   │         WidgetDataRequest, WidgetDataResponse.
│   │   │   │
│   │   │   ├── data_import.py
│   │   │   │       → DataImportCreate, DataImportResponse,
│   │   │   │         DataImportProgress, ColumnMappingRequest,
│   │   │   │         ValidationResultResponse (shows preview of
│   │   │   │         errors before committing import).
│   │   │   │
│   │   │   ├── task.py
│   │   │   │       → TaskCreate, TaskUpdate, TaskResponse, TaskFilter.
│   │   │   │
│   │   │   ├── comment.py
│   │   │   │       → CommentCreate, CommentResponse, CommentThread.
│   │   │   │
│   │   │   ├── notification.py
│   │   │   │       → NotificationResponse, NotificationMarkRead,
│   │   │   │         NotificationPreferences.
│   │   │   │
│   │   │   └── audit.py
│   │   │           → AuditLogResponse, AuditLogFilter (filter by user,
│   │   │             action, resource type, date range).
│   │   │
│   │   │
│   │   ├── api/
│   │   │   │       → API route handlers. Each file is a FastAPI Router
│   │   │   │         that gets registered in main.py. Thin layer — takes
│   │   │   │         request, calls service, returns response.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── router.py
│   │   │   │       → Master router that includes all sub-routers with
│   │   │   │         their URL prefixes: /api/v1/policies,
│   │   │   │         /api/v1/assumptions, /api/v1/calculations, etc.
│   │   │   │         Versioned API from day one.
│   │   │   │
│   │   │   ├── auth.py
│   │   │   │       → POST /auth/login (exchanges credentials for JWT
│   │   │   │         via Keycloak), POST /auth/refresh (refresh token),
│   │   │   │         POST /auth/logout, GET /auth/me (current user info).
│   │   │   │
│   │   │   ├── users.py
│   │   │   │       → CRUD for users. GET /users (list, paginated,
│   │   │   │         filterable), GET /users/{id}, POST /users,
│   │   │   │         PUT /users/{id}, DELETE /users/{id} (soft delete),
│   │   │   │         PUT /users/{id}/role (change role, admin only),
│   │   │   │         GET /users/{id}/activity (recent actions by user).
│   │   │   │
│   │   │   ├── roles.py
│   │   │   │       → GET /roles (list all roles), GET /roles/{id},
│   │   │   │         POST /roles (create custom role), PUT /roles/{id},
│   │   │   │         DELETE /roles/{id}, GET /roles/{id}/permissions,
│   │   │   │         PUT /roles/{id}/permissions (update permissions).
│   │   │   │
│   │   │   ├── policies.py
│   │   │   │       → The workhorse endpoint. GET /policies (list with
│   │   │   │         pagination, sorting, filtering — supports complex
│   │   │   │         filters like date ranges, multiple statuses, etc.),
│   │   │   │         GET /policies/{id} (full detail with related data),
│   │   │   │         POST /policies (create single), PUT /policies/{id},
│   │   │   │         DELETE /policies/{id}, POST /policies/bulk (bulk
│   │   │   │         create), PUT /policies/bulk (bulk update),
│   │   │   │         GET /policies/stats (summary statistics),
│   │   │   │         GET /policies/export (CSV/Excel export),
│   │   │   │         GET /policies/{id}/history (audit trail for policy),
│   │   │   │         GET /policies/{id}/coverages,
│   │   │   │         GET /policies/{id}/claims,
│   │   │   │         GET /policies/{id}/calculations (runs that included
│   │   │   │         this policy).
│   │   │   │
│   │   │   ├── policyholders.py
│   │   │   │       → GET /policyholders, GET /policyholders/{id},
│   │   │   │         POST /policyholders, PUT /policyholders/{id},
│   │   │   │         DELETE /policyholders/{id},
│   │   │   │         GET /policyholders/{id}/policies (all policies
│   │   │   │         for a person), POST /policyholders/search (search
│   │   │   │         by name, ID number, etc.).
│   │   │   │
│   │   │   ├── coverages.py
│   │   │   │       → GET /coverages, POST /coverages, PUT /coverages/{id},
│   │   │   │         DELETE /coverages/{id}. Usually accessed nested
│   │   │   │         under policies, but standalone for bulk operations.
│   │   │   │
│   │   │   ├── claims.py
│   │   │   │       → GET /claims (filterable by status, date range,
│   │   │   │         policy, claim type), GET /claims/{id},
│   │   │   │         POST /claims, PUT /claims/{id},
│   │   │   │         PUT /claims/{id}/status (workflow transitions),
│   │   │   │         GET /claims/stats (claims summary dashboard data).
│   │   │   │
│   │   │   ├── assumptions.py
│   │   │   │       → GET /assumption-sets (list all sets, filterable by
│   │   │   │         status), GET /assumption-sets/{id} (includes all
│   │   │   │         tables), POST /assumption-sets (create new set),
│   │   │   │         PUT /assumption-sets/{id}, DELETE /assumption-sets/{id},
│   │   │   │         POST /assumption-sets/{id}/clone (duplicate for
│   │   │   │         editing), POST /assumption-sets/{id}/submit
│   │   │   │         (submit for approval), POST /assumption-sets/{id}/approve
│   │   │   │         (approve — requires approver role),
│   │   │   │         POST /assumption-sets/{id}/reject (reject with notes),
│   │   │   │         GET /assumption-sets/{id}/compare/{other_id} (side-by-side),
│   │   │   │         GET /assumption-sets/{id}/tables,
│   │   │   │         POST /assumption-sets/{id}/tables (add table),
│   │   │   │         PUT /assumption-tables/{id},
│   │   │   │         DELETE /assumption-tables/{id},
│   │   │   │         POST /assumption-tables/{id}/import (import from Excel).
│   │   │   │
│   │   │   ├── models.py
│   │   │   │       → GET /models (list model definitions), GET /models/{id},
│   │   │   │         POST /models (create new model definition),
│   │   │   │         PUT /models/{id}, DELETE /models/{id},
│   │   │   │         POST /models/{id}/clone, POST /models/{id}/validate
│   │   │   │         (dry-run to check configuration validity),
│   │   │   │         GET /models/{id}/runs (calculation runs using this model),
│   │   │   │         GET /model-templates (pre-built model templates for
│   │   │   │         common use cases — reserve calculation, pricing, etc.).
│   │   │   │
│   │   │   ├── calculations.py
│   │   │   │       → POST /calculations (trigger new calculation run),
│   │   │   │         GET /calculations (list runs, filterable by status,
│   │   │   │         date, model, user), GET /calculations/{id},
│   │   │   │         DELETE /calculations/{id}/cancel (cancel running job),
│   │   │   │         GET /calculations/{id}/progress (polling endpoint or
│   │   │   │         WebSocket for real-time), GET /calculations/{id}/results
│   │   │   │         (paginated results), GET /calculations/{id}/results/export
│   │   │   │         (CSV/Excel), GET /calculations/{id}/summary,
│   │   │   │         POST /calculations/{id}/rerun (re-run with same params),
│   │   │   │         GET /calculations/compare?run_ids=x,y,z (compare multiple).
│   │   │   │
│   │   │   ├── scenarios.py
│   │   │   │       → GET /scenarios, GET /scenarios/{id}, POST /scenarios,
│   │   │   │         PUT /scenarios/{id}, DELETE /scenarios/{id},
│   │   │   │         POST /scenarios/{id}/run (execute scenario against
│   │   │   │         a base calculation), GET /scenarios/{id}/results,
│   │   │   │         GET /scenarios/compare (compare scenario impacts).
│   │   │   │
│   │   │   ├── reports.py
│   │   │   │       → GET /report-templates (list available templates),
│   │   │   │         GET /report-templates/{id}, POST /report-templates
│   │   │   │         (create custom template), PUT /report-templates/{id},
│   │   │   │         DELETE /report-templates/{id},
│   │   │   │         POST /reports/generate (generate a report),
│   │   │   │         GET /reports (list generated reports),
│   │   │   │         GET /reports/{id}, GET /reports/{id}/download,
│   │   │   │         DELETE /reports/{id},
│   │   │   │         POST /report-schedules (schedule recurring generation),
│   │   │   │         GET /report-schedules, DELETE /report-schedules/{id}.
│   │   │   │
│   │   │   ├── dashboards.py
│   │   │   │       → GET /dashboards (user's dashboards + shared),
│   │   │   │         GET /dashboards/{id}, POST /dashboards,
│   │   │   │         PUT /dashboards/{id}, DELETE /dashboards/{id},
│   │   │   │         POST /dashboards/{id}/share,
│   │   │   │         POST /dashboards/{id}/clone,
│   │   │   │         POST /widgets/data (fetch data for a widget config —
│   │   │   │         used by the frontend to render charts).
│   │   │   │
│   │   │   ├── imports.py
│   │   │   │       → POST /imports/upload (upload file, returns import_id),
│   │   │   │         GET /imports/{id} (status and progress),
│   │   │   │         POST /imports/{id}/mapping (set column mappings),
│   │   │   │         POST /imports/{id}/validate (run validation, return
│   │   │   │         preview of errors), POST /imports/{id}/commit
│   │   │   │         (actually import the data), DELETE /imports/{id}/cancel,
│   │   │   │         GET /imports (history of imports),
│   │   │   │         GET /imports/{id}/errors (download error report).
│   │   │   │
│   │   │   ├── tasks.py
│   │   │   │       → GET /tasks (user's tasks, filterable by status,
│   │   │   │         priority, due date), GET /tasks/{id}, POST /tasks,
│   │   │   │         PUT /tasks/{id}, PUT /tasks/{id}/status,
│   │   │   │         PUT /tasks/{id}/assign, DELETE /tasks/{id},
│   │   │   │         GET /tasks/my (shortcut for current user's tasks).
│   │   │   │
│   │   │   ├── comments.py
│   │   │   │       → GET /comments?resource_type=x&resource_id=y
│   │   │   │         (get comments for any resource), POST /comments,
│   │   │   │         PUT /comments/{id}, DELETE /comments/{id},
│   │   │   │         PUT /comments/{id}/resolve.
│   │   │   │
│   │   │   ├── notifications.py
│   │   │   │       → GET /notifications (current user's notifications),
│   │   │   │         PUT /notifications/{id}/read, PUT /notifications/read-all,
│   │   │   │         GET /notifications/unread-count,
│   │   │   │         PUT /notifications/preferences.
│   │   │   │
│   │   │   ├── audit.py
│   │   │   │       → GET /audit-logs (filterable by user, action, resource,
│   │   │   │         date range — admin/auditor only),
│   │   │   │         GET /audit-logs/export (CSV export for compliance).
│   │   │   │
│   │   │   ├── search.py
│   │   │   │       → GET /search?q=term (global search across policies,
│   │   │   │         policyholders, claims, reports — uses Elasticsearch),
│   │   │   │         GET /search/policies, GET /search/policyholders
│   │   │   │         (scoped searches).
│   │   │   │
│   │   │   └── websocket.py
│   │   │           → WebSocket endpoints for real-time features:
│   │   │             /ws/calculations/{id} (progress updates),
│   │   │             /ws/notifications (push notifications to connected
│   │   │             clients), /ws/collaboration/{resource_type}/{id}
│   │   │             (real-time co-editing cursors/presence).
│   │   │
│   │   │
│   │   ├── services/
│   │   │   │       → Business logic layer. Routes call services, services
│   │   │   │         call repositories. This keeps routes thin and logic
│   │   │   │         testable. Each service class handles one domain area.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── user_service.py
│   │   │   │       → UserService class: create_user(), update_user(),
│   │   │   │         delete_user(), get_user(), list_users(),
│   │   │   │         change_role(), sync_from_keycloak() (sync user data
│   │   │   │         from Keycloak on login).
│   │   │   │
│   │   │   ├── auth_service.py
│   │   │   │       → AuthService: authenticate() (validate credentials
│   │   │   │         with Keycloak), create_tokens(), refresh_token(),
│   │   │   │         validate_token(), logout() (invalidate tokens).
│   │   │   │
│   │   │   ├── policy_service.py
│   │   │   │       → PolicyService: create_policy(), update_policy(),
│   │   │   │         delete_policy(), get_policy(), list_policies()
│   │   │   │         (with complex filtering), bulk_create(),
│   │   │   │         bulk_update(), get_statistics(), export_to_csv(),
│   │   │   │         get_policy_history().
│   │   │   │
│   │   │   ├── policyholder_service.py
│   │   │   │       → PolicyholderService: CRUD operations, search(),
│   │   │   │         get_policies_for_holder(), merge_duplicates().
│   │   │   │
│   │   │   ├── claim_service.py
│   │   │   │       → ClaimService: CRUD, transition_status() (handles
│   │   │   │         workflow rules — can't go from open to paid without
│   │   │   │         going through approved), get_statistics().
│   │   │   │
│   │   │   ├── assumption_service.py
│   │   │   │       → AssumptionService: CRUD for sets and tables,
│   │   │   │         clone_set(), submit_for_approval(), approve(),
│   │   │   │         reject(), compare_sets() (generates diff),
│   │   │   │         import_table_from_excel(), validate_table_data()
│   │   │   │         (checks that mortality table has valid ages, rates
│   │   │   │         between 0-1, etc.).
│   │   │   │
│   │   │   ├── model_service.py
│   │   │   │       → ModelService: CRUD, clone(), validate_configuration()
│   │   │   │         (ensures the model definition JSON is valid and
│   │   │   │         complete), get_model_templates().
│   │   │   │
│   │   │   ├── calculation_service.py
│   │   │   │       → CalculationService: trigger_run() (creates run record,
│   │   │   │         dispatches Celery task), cancel_run(), get_run_status(),
│   │   │   │         get_results() (paginated), get_summary(),
│   │   │   │         compare_runs() (side-by-side comparison of outputs),
│   │   │   │         export_results().
│   │   │   │
│   │   │   ├── scenario_service.py
│   │   │   │       → ScenarioService: CRUD, apply_scenario() (takes base
│   │   │   │         assumptions + adjustments, creates modified assumption
│   │   │   │         set), run_scenario(), compare_scenarios().
│   │   │   │
│   │   │   ├── report_service.py
│   │   │   │       → ReportService: CRUD for templates, generate_report()
│   │   │   │         (dispatches Celery task for generation), get_generated(),
│   │   │   │         schedule_report(), unschedule_report().
│   │   │   │
│   │   │   ├── dashboard_service.py
│   │   │   │       → DashboardService: CRUD, share(), clone(),
│   │   │   │         get_widget_data() (this is the key method — takes
│   │   │   │         a widget config, queries the database, returns
│   │   │   │         chart-ready data).
│   │   │   │
│   │   │   ├── import_service.py
│   │   │   │       → ImportService: handle_upload() (saves file to S3,
│   │   │   │         creates import record), set_mapping(), validate()
│   │   │   │         (parses file, checks each row, returns errors),
│   │   │   │         commit() (actually inserts data — dispatches Celery
│   │   │   │         task for large files), get_import_status().
│   │   │   │
│   │   │   ├── task_service.py
│   │   │   │       → TaskService: CRUD, assign(), complete(),
│   │   │   │         get_user_tasks(), create_approval_task() (helper
│   │   │   │         to create tasks when something needs approval).
│   │   │   │
│   │   │   ├── comment_service.py
│   │   │   │       → CommentService: CRUD, get_thread(), resolve(),
│   │   │   │         extract_mentions() (parses @username from content,
│   │   │   │         triggers notification).
│   │   │   │
│   │   │   ├── notification_service.py
│   │   │   │       → NotificationService: create_notification(),
│   │   │   │         get_user_notifications(), mark_read(), mark_all_read(),
│   │   │   │         get_preferences(), update_preferences(),
│   │   │   │         send_email_notification() (for users with email
│   │   │   │         notifications enabled).
│   │   │   │
│   │   │   ├── audit_service.py
│   │   │   │       → AuditService: log() (creates audit record — called
│   │   │   │         from everywhere), query_logs(), export_logs().
│   │   │   │         This is called by other services after every
│   │   │   │         significant action.
│   │   │   │
│   │   │   └── search_service.py
│   │   │           → SearchService: global_search(), index_policy()
│   │   │             (keeps Elasticsearch in sync), index_policyholder(),
│   │   │             reindex_all() (admin function to rebuild indices).
│   │   │
│   │   │
│   │   ├── repositories/
│   │   │   │       → Data access layer. Thin wrappers around SQLAlchemy
│   │   │   │         queries. Services call repositories, repositories
│   │   │   │         call the database. Keeps SQL/ORM code isolated.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── base.py
│   │   │   │       → BaseRepository class with generic CRUD methods:
│   │   │   │         get(id), get_all(filters, pagination, sorting),
│   │   │   │         create(data), update(id, data), delete(id),
│   │   │   │         bulk_create(items), bulk_update(items).
│   │   │   │         All other repositories inherit from this.
│   │   │   │
│   │   │   ├── user_repository.py
│   │   │   │       → UserRepository: inherits base, adds get_by_email(),
│   │   │   │         get_by_keycloak_id(), get_by_role().
│   │   │   │
│   │   │   ├── policy_repository.py
│   │   │   │       → PolicyRepository: inherits base, adds complex filter
│   │   │   │         methods: get_by_policyholder(), get_by_product(),
│   │   │   │         get_by_status(), get_expiring_soon(),
│   │   │   │         get_statistics() (aggregation queries).
│   │   │   │
│   │   │   ├── policyholder_repository.py
│   │   │   │       → PolicyholderRepository: search_by_name(),
│   │   │   │         search_by_id_number().
│   │   │   │
│   │   │   ├── claim_repository.py
│   │   │   │       → ClaimRepository: get_by_policy(), get_by_status(),
│   │   │   │         get_pending_settlement(), get_statistics().
│   │   │   │
│   │   │   ├── assumption_repository.py
│   │   │   │       → AssumptionRepository: get_approved_sets(),
│   │   │   │         get_pending_approval(), get_tables_for_set().
│   │   │   │
│   │   │   ├── model_repository.py
│   │   │   │       → ModelRepository: get_by_type(), get_active_models().
│   │   │   │
│   │   │   ├── calculation_repository.py
│   │   │   │       → CalculationRepository: get_by_model(), get_by_user(),
│   │   │   │         get_running(), get_results_for_run() (paginated),
│   │   │   │         get_results_for_policy().
│   │   │   │
│   │   │   ├── scenario_repository.py
│   │   │   │       → ScenarioRepository: standard CRUD.
│   │   │   │
│   │   │   ├── report_repository.py
│   │   │   │       → ReportRepository: get_templates_by_type(),
│   │   │   │         get_generated_by_user(), get_scheduled().
│   │   │   │
│   │   │   ├── dashboard_repository.py
│   │   │   │       → DashboardRepository: get_user_dashboards(),
│   │   │   │         get_shared_dashboards().
│   │   │   │
│   │   │   ├── import_repository.py
│   │   │   │       → ImportRepository: get_by_status(), get_user_imports().
│   │   │   │
│   │   │   ├── task_repository.py
│   │   │   │       → TaskRepository: get_assigned_to_user(),
│   │   │   │         get_created_by_user(), get_overdue().
│   │   │   │
│   │   │   ├── comment_repository.py
│   │   │   │       → CommentRepository: get_for_resource(), get_thread().
│   │   │   │
│   │   │   ├── notification_repository.py
│   │   │   │       → NotificationRepository: get_unread_for_user(),
│   │   │   │         get_unread_count().
│   │   │   │
│   │   │   └── audit_repository.py
│   │   │           → AuditRepository: query() (complex filtering),
│   │   │             get_for_resource(), get_for_user().
│   │   │
│   │   │
│   │   └── utils/
│   │       │       → Utility functions and helpers used across the app.
│   │       │
│   │       ├── __init__.py
│   │       │
│   │       ├── security.py
│   │       │       → Password hashing (if needed beyond Keycloak),
│   │       │         JWT token encoding/decoding, permission checking
│   │       │         utilities.
│   │       │
│   │       ├── pagination.py
│   │       │       → Pagination helpers: paginate() function that takes
│   │       │         a query and pagination params, returns paginated
│   │       │         response wrapper.
│   │       │
│   │       ├── filters.py
│   │       │       → Generic filter building: takes filter params,
│   │       │         builds SQLAlchemy filter expressions. Handles
│   │       │         date ranges, IN clauses, LIKE searches, etc.
│   │       │
│   │       ├── file_handling.py
│   │       │       → Upload to S3/MinIO, download from S3, generate
│   │       │         presigned URLs, file type validation, CSV/Excel
│   │       │         parsing utilities.
│   │       │
│   │       ├── excel_parser.py
│   │       │       → Parse Excel files for imports and assumption tables.
│   │       │         Uses openpyxl. Handles different sheet structures,
│   │       │         data type detection, date parsing.
│   │       │
│   │       ├── csv_generator.py
│   │       │       → Generate CSV exports. Streaming CSV generation for
│   │       │         large datasets.
│   │       │
│   │       ├── pdf_generator.py
│   │       │       → Generate PDF reports. Uses ReportLab or WeasyPrint.
│   │       │         Takes report template config, data, renders to PDF.
│   │       │
│   │       ├── email.py
│   │       │       → Send emails via SMTP or SendGrid. Email templates
│   │       │         for notifications, report delivery, password reset.
│   │       │
│   │       ├── date_utils.py
│   │       │       → Date parsing, formatting, fiscal period calculations,
│   │       │         actuarial age calculations (age nearest birthday,
│   │       │         age last birthday).
│   │       │
│   │       └── validators.py
│   │               → Custom Pydantic validators, business rule validation
│   │                 (policy number format, valid age ranges, etc.).
│   │
│   │
│   ├── migrations/
│   │   │       → Alembic database migrations. Each migration is a
│   │   │         Python file with upgrade() and downgrade() functions.
│   │   │
│   │   ├── env.py
│   │   │       → Alembic environment configuration. Points to models,
│   │   │         database URL.
│   │   │
│   │   ├── script.py.mako
│   │   │       → Template for new migration files.
│   │   │
│   │   └── versions/
│   │       │       → Migration files, named with timestamps.
│   │       │
│   │       ├── 001_initial_schema.py
│   │       │       → Creates all base tables: users, roles, permissions,
│   │       │         policies, policyholders, coverages.
│   │       │
│   │       ├── 002_assumptions_tables.py
│   │       │       → Creates assumption_sets and assumption_tables.
│   │       │
│   │       ├── 003_models_and_calculations.py
│   │       │       → Creates model_definitions, calculation_runs,
│   │       │         calculation_results.
│   │       │
│   │       ├── 004_scenarios.py
│   │       │       → Creates scenarios and scenario_results.
│   │       │
│   │       ├── 005_reports.py
│   │       │       → Creates report_templates and generated_reports.
│   │       │
│   │       ├── 006_dashboards.py
│   │       │       → Creates dashboard_configs.
│   │       │
│   │       ├── 007_imports.py
│   │       │       → Creates data_imports.
│   │       │
│   │       ├── 008_workflow.py
│   │       │       → Creates tasks, comments, notifications.
│   │       │
│   │       ├── 009_audit_log.py
│   │       │       → Creates audit_log table.
│   │       │
│   │       └── 010_claims.py
│   │               → Creates claims table.
│   │
│   │
│   └── tests/
│       │       → All backend tests. Pytest with fixtures, factories,
│       │         test database.
│       │
│       ├── conftest.py
│       │       → Pytest configuration. Test database setup/teardown,
│       │         test client fixture, authenticated user fixtures,
│       │         factory fixtures for creating test data.
│       │
│       ├── factories/
│       │   │       → Test data factories using factory_boy.
│       │   │
│       │   ├── __init__.py
│       │   ├── user_factory.py
│       │   ├── policy_factory.py
│       │   ├── assumption_factory.py
│       │   ├── model_factory.py
│       │   └── calculation_factory.py
│       │
│       ├── unit/
│       │   │       → Unit tests for services, utils, isolated logic.
│       │   │
│       │   ├── test_policy_service.py
│       │   ├── test_assumption_service.py
│       │   ├── test_calculation_service.py
│       │   ├── test_date_utils.py
│       │   └── test_validators.py
│       │
│       ├── integration/
│       │   │       → Integration tests hitting the database.
│       │   │
│       │   ├── test_policy_repository.py
│       │   ├── test_assumption_repository.py
│       │   └── test_calculation_repository.py
│       │
│       └── api/
│           │       → API endpoint tests using TestClient.
│           │
│           ├── test_auth.py
│           ├── test_policies.py
│           ├── test_assumptions.py
│           ├── test_calculations.py
│           ├── test_scenarios.py
│           ├── test_reports.py
│           └── test_imports.py
│
│
│
├── calculation_engine/
│   │       → Separate service for actuarial calculations. Runs as
│   │         Celery workers processing calculation jobs from Redis.
│   │
│   ├── Dockerfile
│   │       → Based on python:3.12-slim. Installs NumPy, SciPy, Pandas,
│   │         Celery. Runs celery worker command.
│   │
│   ├── pyproject.toml
│   │       → Dependencies: celery, redis, numpy, scipy, pandas,
│   │         sqlalchemy (to read/write results), boto3, pydantic.
│   │
│   ├── celery_app.py
│   │       → Celery application configuration. Connects to Redis,
│   │         sets up task routes, concurrency settings, result backend.
│   │
│   ├── config.py
│   │       → Configuration from environment: database URL, Redis URL,
│   │         S3 settings, logging.
│   │
│   │
│   ├── tasks/
│   │   │       → Celery tasks. Each task is a function decorated with
│   │   │         @celery_app.task.
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── calculation_task.py
│   │   │       → run_calculation(calculation_run_id) — the main task.
│   │   │         Loads model definition, assumption set, policy data.
│   │   │         Executes calculation graph. Writes results to database.
│   │   │         Updates run status. Sends completion notification.
│   │   │
│   │   ├── report_generation_task.py
│   │   │       → generate_report(generated_report_id) — generates a
│   │   │         report from template and data. Uploads to S3.
│   │   │
│   │   └── import_task.py
│   │           → process_import(data_import_id) — for large imports,
│   │             processes file in chunks, updates progress.
│   │
│   │
│   ├── engine/
│   │   │       → The actual calculation logic. The most complex part
│   │   │         of the entire system.
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── executor.py
│   │   │       → CalculationExecutor class. Takes a model definition,
│   │   │         assumption set, and policy data. Orchestrates the
│   │   │         calculation flow. Handles parallelization across
│   │   │         policies. Manages progress reporting.
│   │   │
│   │   ├── graph.py
│   │   │       → CalculationGraph class. Parses the model definition
│   │   │         JSON into a directed acyclic graph of calculation
│   │   │         nodes. Handles dependency resolution — nodes execute
│   │   │         in correct order based on what they depend on.
│   │   │
│   │   ├── nodes/
│   │   │   │       → Individual calculation node types. Each node
│   │   │   │         performs one type of calculation.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── base.py
│   │   │   │       → BaseNode class. Defines interface: execute(inputs),
│   │   │   │         validate_inputs(), get_outputs().
│   │   │   │
│   │   │   ├── input_nodes.py
│   │   │   │       → PolicyDataNode (reads policy fields), AssumptionNode
│   │   │   │         (reads from assumption tables), ParameterNode (reads
│   │   │   │         run parameters like valuation date).
│   │   │   │
│   │   │   ├── mortality_nodes.py
│   │   │   │       → MortalityLookupNode (looks up qx from mortality table),
│   │   │   │         SurvivalProbabilityNode (calculates tPx),
│   │   │   │         DeathProbabilityNode (calculates tQx).
│   │   │   │
│   │   │   ├── lapse_nodes.py
│   │   │   │       → LapseLookupNode, PersistencyNode (calculates
│   │   │   │         probability of policy still in force).
│   │   │   │
│   │   │   ├── discount_nodes.py
│   │   │   │       → DiscountRateLookupNode, DiscountFactorNode
│   │   │   │         (calculates v^t), PresentValueNode.
│   │   │   │
│   │   │   ├── cashflow_nodes.py
│   │   │   │       → PremiumCashflowNode, ClaimCashflowNode,
│   │   │   │         ExpenseCashflowNode, NetCashflowNode,
│   │   │   │         PVCashflowNode (present value of cashflows).
│   │   │   │
│   │   │   ├── reserve_nodes.py
│   │   │   │       → GrossReserveNode, NetReserveNode, StatReserveNode
│   │   │   │         (statutory), BELNode (Best Estimate Liability for
│   │   │   │         IFRS 17), CSMNode (Contractual Service Margin).
│   │   │   │
│   │   │   ├── aggregation_nodes.py
│   │   │   │       → SumNode, AverageNode, GroupByNode (aggregate
│   │   │   │         results by product, cohort, etc.).
│   │   │   │
│   │   │   └── output_nodes.py
│   │   │           → ResultWriterNode (writes to calculation_results
│   │   │             table), SummaryNode (computes run-level summaries).
│   │   │
│   │   │
│   │   ├── tables/
│   │   │   │       → Assumption table handling and interpolation.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── mortality_table.py
│   │   │   │       → MortalityTable class. Loads table data from JSONB.
│   │   │   │         Methods: get_qx(age), get_lx(age), get_npx(age, n),
│   │   │   │         get_nqx(age, n). Handles select and ultimate tables.
│   │   │   │
│   │   │   ├── lapse_table.py
│   │   │   │       → LapseTable class. Methods: get_lapse_rate(duration),
│   │   │   │         get_persistency(duration, n).
│   │   │   │
│   │   │   ├── discount_curve.py
│   │   │   │       → DiscountCurve class. Methods: get_spot_rate(term),
│   │   │   │         get_forward_rate(t1, t2), get_discount_factor(term).
│   │   │   │         Handles interpolation between given points.
│   │   │   │
│   │   │   └── interpolation.py
│   │   │           → Linear, cubic, and Whittaker-Henderson interpolation
│   │   │             for assumption tables.
│   │   │
│   │   │
│   │   ├── projections/
│   │   │   │       → Projection logic for different product types.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── term_life.py
│   │   │   │       → TermLifeProjection: project cashflows for term
│   │   │   │         life insurance. Handles level premium, decreasing
│   │   │   │         term, renewable term.
│   │   │   │
│   │   │   ├── whole_life.py
│   │   │   │       → WholeLifeProjection: project cashflows for whole
│   │   │   │         life (with or without participating dividends).
│   │   │   │
│   │   │   ├── endowment.py
│   │   │   │       → EndowmentProjection: handles maturity benefits.
│   │   │   │
│   │   │   ├── annuity.py
│   │   │   │       → AnnuityProjection: immediate annuities, deferred
│   │   │   │         annuities, life annuities, period certain.
│   │   │   │
│   │   │   ├── universal_life.py
│   │   │   │       → ULProjection: account value projection, COI
│   │   │   │         charges, credited interest, surrender charges.
│   │   │   │
│   │   │   └── health.py
│   │   │           → HealthProjection: disability income, critical
│   │   │             illness, long-term care.
│   │   │
│   │   │
│   │   └── standards/
│   │       │       → Regulatory standard-specific calculations.
│   │       │
│   │       ├── __init__.py
│   │       │
│   │       ├── ifrs17.py
│   │       │       → IFRS17Calculator: Building Block Approach,
│   │       │         Premium Allocation Approach, Variable Fee Approach.
│   │       │         BEL, RA, CSM, LRC, LIC calculations.
│   │       │
│   │       ├── solvency2.py
│   │       │       → Solvency2Calculator: Best Estimate, Risk Margin,
│   │       │         SCR calculations.
│   │       │
│   │       ├── us_gaap.py
│   │       │       → USGAAPCalculator: DAC, DPAC, AUB, LDTI calculations.
│   │       │
│   │       └── statutory.py
│   │               → StatutoryCalculator: CRVM, NLP, XXX-AXXX reserves.
│   │
│   │
│   └── tests/
│       │       → Tests for the calculation engine.
│       │
│       ├── conftest.py
│       ├── test_executor.py
│       ├── test_graph.py
│       ├── test_mortality_table.py
│       ├── test_discount_curve.py
│       ├── test_term_life_projection.py
│       ├── test_ifrs17.py
│       └── test_scenarios.py
│
│
│
├── frontend/
│   │       → React application. TypeScript throughout.
│   │
│   ├── Dockerfile
│   │       → Multi-stage build. First stage runs npm build, second
│   │         stage is nginx serving the static files.
│   │
│   ├── nginx.conf
│   │       → Nginx configuration for serving SPA. Routes all requests
│   │         to index.html except /api (proxied to backend).
│   │
│   ├── package.json
│   │       → Dependencies: react, react-dom, react-router-dom,
│   │         @tanstack/react-query, @tanstack/react-table, zustand,
│   │         antd, @ant-design/icons, recharts, dayjs, axios,
│   │         react-hook-form, zod, socket.io-client.
│   │         DevDependencies: typescript, vite, eslint, prettier.
│   │
│   ├── tsconfig.json
│   │       → TypeScript configuration. Strict mode enabled.
│   │
│   ├── vite.config.ts
│   │       → Vite bundler configuration. Proxy /api to backend in dev.
│   │
│   ├── index.html
│   │       → Entry HTML file.
│   │
│   │
│   └── src/
│       │
│       ├── main.tsx
│       │       → Application entry point. Renders App into DOM.
│       │
│       ├── App.tsx
│       │       → Root component. Sets up providers (QueryClientProvider,
│       │         AuthProvider, ThemeProvider), routing.
│       │
│       ├── routes.tsx
│       │       → React Router route definitions. Protected routes,
│       │         role-based access.
│       │
│       ├── vite-env.d.ts
│       │       → TypeScript declarations for Vite.
│       │
│       │
│       ├── api/
│       │   │       → API client layer. Functions that call backend.
│       │   │
│       │   ├── client.ts
│       │   │       → Axios instance configured with base URL, auth
│       │   │         interceptor (adds JWT), error interceptor (handles
│       │   │         401, refreshes token).
│       │   │
│       │   ├── auth.ts
│       │   │       → login(), logout(), refreshToken(), getMe().
│       │   │
│       │   ├── users.ts
│       │   │       → getUsers(), getUser(), createUser(), updateUser(),
│       │   │         deleteUser().
│       │   │
│       │   ├── policies.ts
│       │   │       → getPolicies(), getPolicy(), createPolicy(),
│       │   │         updatePolicy(), deletePolicy(), getPolicyStats(),
│       │   │         exportPolicies().
│       │   │
│       │   ├── policyholders.ts
│       │   │       → CRUD functions.
│       │   │
│       │   ├── claims.ts
│       │   │       → CRUD functions.
│       │   │
│       │   ├── assumptions.ts
│       │   │       → getAssumptionSets(), getAssumptionSet(),
│       │   │         createAssumptionSet(), cloneAssumptionSet(),
│       │   │         submitForApproval(), approve(), reject(),
│       │   │         getTables(), createTable(), updateTable(),
│       │   │         importTableFromExcel(), compareAssumptionSets().
│       │   │
│       │   ├── models.ts
│       │   │       → getModels(), getModel(), createModel(), updateModel(),
│       │   │         validateModel(), getModelTemplates().
│       │   │
│       │   ├── calculations.ts
│       │   │       → triggerCalculation(), getCalculationRuns(),
│       │   │         getCalculationRun(), cancelCalculation(),
│       │   │         getResults(), exportResults(), compareRuns().
│       │   │
│       │   ├── scenarios.ts
│       │   │       → CRUD + runScenario(), compareScenarios().
│       │   │
│       │   ├── reports.ts
│       │   │       → getTemplates(), generateReport(), getReports(),
│       │   │         downloadReport(), scheduleReport().
│       │   │
│       │   ├── dashboards.ts
│       │   │       → getDashboards(), getDashboard(), saveDashboard(),
│       │   │         deleteDashboard(), getWidgetData().
│       │   │
│       │   ├── imports.ts
│       │   │       → uploadFile(), setMapping(), validate(), commit(),
│       │   │         getImportStatus().
│       │   │
│       │   ├── tasks.ts
│       │   │       → getTasks(), getTask(), createTask(), updateTask(),
│       │   │         completeTask().
│       │   │
│       │   ├── comments.ts
│       │   │       → getComments(), createComment(), resolveComment().
│       │   │
│       │   ├── notifications.ts
│       │   │       → getNotifications(), markRead(), markAllRead(),
│       │   │         getUnreadCount().
│       │   │
│       │   ├── audit.ts
│       │   │       → getAuditLogs(), exportAuditLogs().
│       │   │
│       │   └── search.ts
│       │           → globalSearch(), searchPolicies().
│       │
│       │
│       ├── hooks/
│       │   │       → Custom React hooks.
│       │   │
│       │   ├── useAuth.ts
│       │   │       → Authentication hook. Returns user, login(), logout(),
│       │   │         isAuthenticated, hasRole(), hasPermission().
│       │   │
│       │   ├── usePolicies.ts
│       │   │       → React Query hooks: useQuery for fetching,
│       │   │         useMutation for create/update/delete. Returns
│       │   │         { policies, isLoading, error, createPolicy, ... }.
│       │   │
│       │   ├── useAssumptions.ts
│       │   │       → Query hooks for assumption sets.
│       │   │
│       │   ├── useCalculations.ts
│       │   │       → Query hooks for calculations. Includes polling
│       │   │         for in-progress runs.
│       │   │
│       │   ├── useScenarios.ts
│       │   ├── useReports.ts
│       │   ├── useDashboards.ts
│       │   ├── useImports.ts
│       │   ├── useTasks.ts
│       │   │
│       │   ├── useNotifications.ts
│       │   │       → Notifications hook. Includes WebSocket connection
│       │   │         for real-time updates.
│       │   │
│       │   ├── useWebSocket.ts
│       │   │       → Generic WebSocket hook.
│       │   │
│       │   ├── useDebounce.ts
│       │   │       → Debounce hook for search inputs.
│       │   │
│       │   └── useLocalStorage.ts
│       │           → Persist state to localStorage.
│       │
│       │
│       ├── stores/
│       │   │       → Zustand state stores.
│       │   │
│       │   ├── authStore.ts
│       │   │       → Auth state: user, tokens, isAuthenticated.
│       │   │         Actions: setUser(), clearAuth().
│       │   │
│       │   ├── uiStore.ts
│       │   │       → UI state: sidebarCollapsed, theme, activeTab.
│       │   │
│       │   └── notificationStore.ts
│       │           → Notification state: unreadCount, notifications.
│       │
│       │
│       ├── components/
│       │   │       → Reusable UI components.
│       │   │
│       │   ├── common/
│       │   │   │       → Generic components used everywhere.
│       │   │   │
│       │   │   ├── Layout.tsx
│       │   │   │       → Main layout with sidebar, header, content area.
│       │   │   │
│       │   │   ├── Sidebar.tsx
│       │   │   │       → Navigation sidebar. Role-aware — only shows
│       │   │   │         menu items user has access to.
│       │   │   │
│       │   │   ├── Header.tsx
│       │   │   │       → Top header with search, notifications, user menu.
│       │   │   │
│       │   │   ├── DataTable.tsx
│       │   │   │       → Generic data table component using TanStack Table.
│       │   │   │         Pagination, sorting, filtering, column visibility,
│       │   │   │         row selection. The most important component —
│       │   │   │         this is what makes the app feel like a spreadsheet.
│       │   │   │
│       │   │   ├── PageHeader.tsx
│       │   │   │       → Page title, breadcrumbs, action buttons.
│       │   │   │
│       │   │   ├── FilterPanel.tsx
│       │   │   │       → Collapsible filter panel with various input types.
│       │   │   │
│       │   │   ├── SearchInput.tsx
│       │   │   │       → Debounced search input.
│       │   │   │
│       │   │   ├── ConfirmModal.tsx
│       │   │   │       → Confirmation dialog.
│       │   │   │
│       │   │   ├── LoadingSpinner.tsx
│       │   │   ├── ErrorBoundary.tsx
│       │   │   ├── EmptyState.tsx
│       │   │   │
│       │   │   ├── FileUpload.tsx
│       │   │   │       → Drag-and-drop file upload component.
│       │   │   │
│       │   │   ├── DateRangePicker.tsx
│       │   │   │       → Date range selection.
│       │   │   │
│       │   │   └── StatusBadge.tsx
│       │   │           → Colored status badges (active/inactive/pending/etc.).
│       │   │
│       │   │
│       │   ├── charts/
│       │   │   │       → Chart components using Recharts.
│       │   │   │
│       │   │   ├── LineChart.tsx
│       │   │   ├── BarChart.tsx
│       │   │   ├── PieChart.tsx
│       │   │   ├── AreaChart.tsx
│       │   │   └── CashflowChart.tsx
│       │   │           → Specialized chart for actuarial cashflow
│       │   │             waterfall visualization.
│       │   │
│       │   │
│       │   ├── forms/
│       │   │   │       → Form components using react-hook-form.
│       │   │   │
│       │   │   ├── PolicyForm.tsx
│       │   │   │       → Create/edit policy form.
│       │   │   │
│       │   │   ├── PolicyholderForm.tsx
│       │   │   ├── ClaimForm.tsx
│       │   │   ├── AssumptionSetForm.tsx
│       │   │   ├── AssumptionTableForm.tsx
│       │   │   ├── ModelDefinitionForm.tsx
│       │   │   ├── CalculationRunForm.tsx
│       │   │   ├── ScenarioForm.tsx
│       │   │   ├── ReportTemplateForm.tsx
│       │   │   ├── TaskForm.tsx
│       │   │   └── UserForm.tsx
│       │   │
│       │   │
│       │   ├── modals/
│       │   │   │       → Modal dialogs for specific actions.
│       │   │   │
│       │   │   ├── ImportModal.tsx
│       │   │   │       → Multi-step import wizard: upload → map columns
│       │   │   │         → validate → review errors → commit.
│       │   │   │
│       │   │   ├── ExportModal.tsx
│       │   │   │       → Select format, columns, filters for export.
│       │   │   │
│       │   │   ├── ColumnMappingModal.tsx
│       │   │   │       → Map import file columns to system fields.
│       │   │   │
│       │   │   ├── ApprovalModal.tsx
│       │   │   │       → Approve/reject with comments.
│       │   │   │
│       │   │   ├── ComparisonModal.tsx
│       │   │   │       → Side-by-side comparison view.
│       │   │   │
│       │   │   └── CalculationProgressModal.tsx
│       │   │           → Shows real-time calculation progress.
│       │   │
│       │   │
│       │   └── widgets/
│       │       │       → Dashboard widget components.
│       │       │
│       │       ├── WidgetContainer.tsx
│       │       │       → Generic widget wrapper with title, menu, resize.
│       │       │
│       │       ├── PolicyCountWidget.tsx
│       │       ├── ReservesSummaryWidget.tsx
│       │       ├── ClaimsStatusWidget.tsx
│       │       ├── RecentCalculationsWidget.tsx
│       │       ├── TasksWidget.tsx
│       │       └── TrendChartWidget.tsx
│       │
│       │
│       ├── pages/
│       │   │       → Page components. Each corresponds to a route.
│       │   │
│       │   ├── Login.tsx
│       │   │       → Login page with Keycloak redirect.
│       │   │
│       │   ├── Dashboard.tsx
│       │   │       → Main dashboard with configurable widgets.
│       │   │
│       │   ├── policies/
│       │   │   │
│       │   │   ├── PolicyList.tsx
│       │   │   │       → Policy listing page with DataTable.
│       │   │   │
│       │   │   ├── PolicyDetail.tsx
│       │   │   │       → Single policy view with tabs: details, coverages,
│       │   │   │         claims, calculation history, comments.
│       │   │   │
│       │   │   ├── PolicyCreate.tsx
│       │   │   └── PolicyEdit.tsx
│       │   │
│       │   ├── policyholders/
│       │   │   ├── PolicyholderList.tsx
│       │   │   ├── PolicyholderDetail.tsx
│       │   │   └── PolicyholderCreate.tsx
│       │   │
│       │   ├── claims/
│       │   │   ├── ClaimList.tsx
│       │   │   ├── ClaimDetail.tsx
│       │   │   └── ClaimCreate.tsx
│       │   │
│       │   ├── assumptions/
│       │   │   │
│       │   │   ├── AssumptionSetList.tsx
│       │   │   │       → List of assumption sets with status filters.
│       │   │   │
│       │   │   ├── AssumptionSetDetail.tsx
│       │   │   │       → Single set view with tables. Visual table editor
│       │   │   │         that feels like Excel. Approval workflow actions.
│       │   │   │
│       │   │   ├── AssumptionSetCreate.tsx
│       │   │   ├── AssumptionTableEditor.tsx
│       │   │   │       → Spreadsheet-like editor for assumption table data.
│       │   │   │
│       │   │   └── AssumptionComparison.tsx
│       │   │           → Side-by-side comparison of two assumption sets.
│       │   │
│       │   ├── models/
│       │   │   │
│       │   │   ├── ModelList.tsx
│       │   │   │       → List of model definitions.
│       │   │   │
│       │   │   ├── ModelDetail.tsx
│       │   │   │       → Model detail with visual calculation graph view.
│       │   │   │
│       │   │   ├── ModelCreate.tsx
│       │   │   │       → Model creation with visual builder.
│       │   │   │
│       │   │   └── ModelBuilder.tsx
│       │   │           → THE KEY COMPONENT. Visual drag-and-drop builder
│       │   │             for defining calculation models. Nodes represent
│       │   │             calculation steps. Connections show data flow.
│       │   │             Users can build complex models without coding.
│       │   │             Uses react-flow or similar library.
│       │   │
│       │   ├── calculations/
│       │   │   │
│       │   │   ├── CalculationList.tsx
│       │   │   │       → List of calculation runs with status, filters.
│       │   │   │
│       │   │   ├── CalculationDetail.tsx
│       │   │   │       → Single run: status, progress, results (paginated
│       │   │   │         table), summary, export.
│       │   │   │
│       │   │   ├── CalculationCreate.tsx
│       │   │   │       → Form to trigger new calculation: select model,
│       │   │   │         assumption set, policy filter, parameters.
│       │   │   │
│       │   │   └── CalculationComparison.tsx
│       │   │           → Compare multiple calculation runs side-by-side.
│       │   │
│       │   ├── scenarios/
│       │   │   ├── ScenarioList.tsx
│       │   │   ├── ScenarioDetail.tsx
│       │   │   ├── ScenarioCreate.tsx
│       │   │   │       → Visual scenario builder: base assumptions +
│       │   │   │         adjustment sliders (mortality +10%, lapse +20%).
│       │   │   │
│       │   │   └── ScenarioComparison.tsx
│       │   │
│       │   ├── reports/
│       │   │   ├── ReportTemplateList.tsx
│       │   │   ├── ReportTemplateDetail.tsx
│       │   │   ├── ReportGenerate.tsx
│       │   │   │       → Form to generate a report.
│       │   │   │
│       │   │   ├── GeneratedReportList.tsx
│       │   │   └── ReportSchedules.tsx
│       │   │
│       │   ├── dashboards/
│       │   │   ├── DashboardList.tsx
│       │   │   ├── DashboardView.tsx
│       │   │   │       → Renders dashboard with widgets.
│       │   │   │
│       │   │   └── DashboardEditor.tsx
│       │   │           → Drag-and-drop dashboard builder. Add widgets,
│       │   │             configure data sources, arrange layout.
│       │   │
│       │   ├── imports/
│       │   │   ├── ImportList.tsx
│       │   │   └── ImportWizard.tsx
│       │   │           → Step-by-step import process.
│       │   │
│       │   ├── tasks/
│       │   │   ├── TaskList.tsx
│       │   │   └── TaskDetail.tsx
│       │   │
│       │   ├── audit/
│       │   │   └── AuditLog.tsx
│       │   │           → Searchable, filterable audit log viewer.
│       │   │
│       │   ├── admin/
│       │   │   ├── UserList.tsx
│       │   │   ├── UserDetail.tsx
│       │   │   ├── RoleList.tsx
│       │   │   ├── RoleDetail.tsx
│       │   │   │       → Role editor with permission checkboxes.
│       │   │   │
│       │   │   └── Settings.tsx
│       │   │           → System settings (admin only).
│       │   │
│       │   └── NotFound.tsx
│       │           → 404 page.
│       │
│       │
│       ├── styles/
│       │   │       → Global styles and Ant Design theme customization.
│       │   │
│       │   ├── globals.css
│       │   │       → Global CSS variables, fonts, reset.
│       │   │
│       │   └── theme.ts
│       │           → Ant Design theme configuration: colors, typography,
│       │             component overrides.
│       │
│       │
│       ├── types/
│       │   │       → TypeScript type definitions.
│       │   │
│       │   ├── api.ts
│       │   │       → API response types, matching backend schemas.
│       │   │
│       │   ├── models.ts
│       │   │       → Domain model types: Policy, Policyholder, Claim,
│       │   │         AssumptionSet, ModelDefinition, etc.
│       │   │
│       │   └── ui.ts
│       │           → UI-specific types: TableColumn, Filter, WidgetConfig.
│       │
│       │
│       └── utils/
│           │       → Utility functions.
│           │
│           ├── formatters.ts
│           │       → Number formatting (currency, percentage), date
│           │         formatting, status display.
│           │
│           ├── validators.ts
│           │       → Zod schemas for form validation.
│           │
│           ├── constants.ts
│           │       → App constants: status values, product types, etc.
│           │
│           └── helpers.ts
│                   → Misc helpers: buildQueryString(), downloadFile(),
│                     debounce(), etc.
│
│
│
├── infrastructure/
│   │       → Infrastructure-as-code and deployment configs.
│   │
│   ├── kubernetes/
│   │   │       → Kubernetes manifests for production deployment.
│   │   │
│   │   ├── namespace.yaml
│   │   │       → Creates 'actuflow' namespace.
│   │   │
│   │   ├── configmap.yaml
│   │   │       → Non-sensitive configuration.
│   │   │
│   │   ├── secrets.yaml
│   │   │       → Template for secrets (actual values come from
│   │   │         secret management system).
│   │   │
│   │   ├── backend/
│   │   │   ├── deployment.yaml
│   │   │   │       → Backend deployment: 2+ replicas, resource limits,
│   │   │   │         health checks, rolling update strategy.
│   │   │   │
│   │   │   ├── service.yaml
│   │   │   │       → ClusterIP service for backend.
│   │   │   │
│   │   │   └── hpa.yaml
│   │   │           → Horizontal Pod Autoscaler based on CPU/memory.
│   │   │
│   │   ├── calculation-engine/
│   │   │   ├── deployment.yaml
│   │   │   │       → Celery worker deployment. Multiple replicas,
│   │   │   │         higher resource limits (calculations are CPU-heavy).
│   │   │   │
│   │   │   └── hpa.yaml
│   │   │           → Scale workers based on queue length.
│   │   │
│   │   ├── frontend/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   │
│   │   ├── ingress.yaml
│   │   │       → Ingress resource with TLS. Routes / to frontend,
│   │   │         /api to backend.
│   │   │
│   │   ├── postgresql/
│   │   │   ├── statefulset.yaml
│   │   │   │       → PostgreSQL StatefulSet with persistent volume.
│   │   │   │
│   │   │   ├── service.yaml
│   │   │   └── pvc.yaml
│   │   │
│   │   ├── redis/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   │
│   │   ├── elasticsearch/
│   │   │   ├── statefulset.yaml
│   │   │   ├── service.yaml
│   │   │   └── pvc.yaml
│   │   │
│   │   ├── minio/
│   │   │   ├── statefulset.yaml
│   │   │   ├── service.yaml
│   │   │   └── pvc.yaml
│   │   │
│   │   └── keycloak/
│   │       ├── deployment.yaml
│   │       └── service.yaml
│   │
│   │
│   ├── terraform/
│   │   │       → Terraform for cloud infrastructure (optional, for
│   │   │         cloud deployments).
│   │   │
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── provider.tf
│   │   │
│   │   ├── modules/
│   │   │   ├── vpc/
│   │   │   ├── eks/
│   │   │   ├── rds/
│   │   │   └── s3/
│   │   │
│   │   └── environments/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── production/
│   │
│   │
│   └── monitoring/
│       │       → Monitoring and observability setup.
│       │
│       ├── prometheus/
│       │   ├── prometheus.yaml
│       │   └── alerts.yaml
│       │
│       ├── grafana/
│       │   ├── grafana.yaml
│       │   └── dashboards/
│       │       ├── backend.json
│       │       ├── calculations.json
│       │       └── database.json
│       │
│       └── loki/
│           └── loki.yaml
│
│
│
├── scripts/
│   │       → Utility scripts for development and operations.
│   │
│   ├── seed_db.py
│   │       → Seeds database with sample data for development.
│   │         Creates sample users, policies, assumption sets, etc.
│   │
│   ├── create_superuser.py
│   │       → Creates initial admin user.
│   │
│   ├── load_mortality_tables.py
│   │       → Loads standard mortality tables (CSO, VBT) into the system.
│   │
│   ├── backup_db.sh
│   │       → Database backup script.
│   │
│   ├── restore_db.sh
│   │       → Database restore script.
│   │
│   └── migrate.sh
│           → Runs Alembic migrations.
│
│
│
└── .github/
    │       → GitHub configuration (CI/CD, issue templates, etc.).
    │
    ├── workflows/
    │   │
    │   ├── ci.yml
    │   │       → Continuous Integration: lint, test, build on every PR.
    │   │         Runs backend tests, frontend tests, builds Docker images.
    │   │
    │   ├── cd.yml
    │   │       → Continuous Deployment: deploy to staging on merge to
    │   │         main, deploy to production on release tag.
    │   │
    │   └── security.yml
    │           → Security scanning: dependency audit, SAST.
    │
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    │
    └── PULL_REQUEST_TEMPLATE.md



PART 5: IMPLEMENTATION PHASES

Phase 1 — Foundation (Weeks 1-4):
- Set up project structure, Docker environment
- Implement authentication with Keycloak
- User management, roles, permissions
- Basic audit logging
- Core database schema (users, roles, policies, policyholders)
- Basic policy CRUD with data table
- Data import (CSV) for policies

Phase 2 — Actuarial Core (Weeks 5-10):
- Assumptions module: sets, tables, versioning
- Approval workflows for assumptions
- Model definition module
- Calculation engine: basic executor, graph, core nodes
- Integration: trigger calculations from UI, view results
- Term life projection implementation

Phase 3 — Reporting & Scenarios (Weeks 11-14):
- Report templates module
- Report generation (PDF, Excel)
- Scenario definition
- Scenario running and comparison
- Dashboard module with basic widgets

Phase 4 — Polish & Scale (Weeks 15-18):
- Advanced calculation nodes (IFRS 17, Solvency II)
- More product projections (whole life, annuity)
- Performance optimization
- Real-time features (WebSocket)
- Comprehensive testing
- Documentation

Phase 5 — Production Readiness (Weeks 19-22):
- Security hardening
- Kubernetes deployment refinement
- Monitoring and alerting setup
- Backup and disaster recovery
- User acceptance testing
- Bug fixes and polish



PART 6: KEY TECHNICAL DECISIONS EXPLAINED

Why FastAPI over Django?
FastAPI's async support is better for long-running calculation jobs. Auto-generated OpenAPI docs reduce frontend/backend sync issues. Type hints with Pydantic catch errors at development time. For a modern API-first app, FastAPI is cleaner than Django REST Framework.

Why PostgreSQL?
Actuarial data is highly relational. Policies have policyholders, coverages, claims. Assumptions have sets with tables. PostgreSQL handles complex joins efficiently. JSONB columns give flexibility for semi-structured data (model configs, calculation outputs). Partitioning support for large result tables.

Why Celery for calculations?
Actuarial calculations can run for minutes. You can't hold an HTTP connection that long. Celery lets you queue jobs, process them in the background, scale workers independently. Redis as the broker is simple and fast. Workers can be scaled horizontally for heavy calculation periods.

Why Keycloak?
Insurance companies already have LDAP/AD. They want SSO. Keycloak integrates with enterprise identity providers. It handles the security-critical auth code so we don't have to implement it. RBAC is built in. Audit trails on auth events.

Why separate calculation engine service?
Separation of concerns. The backend is stateless, fast, handles CRUD and API. The calculation engine is stateful (long-running jobs), resource-intensive. They scale differently. You might need 10 backend pods but 50 calculation workers during quarter-end.

Why JSONB for model configs and results?
Actuarial models vary widely. A term life model has different inputs/outputs than a variable annuity model. Fixed schema would require constant migrations. JSONB gives flexibility — store whatever the model needs. Query performance is still good with GIN indexes.

Why Ant Design?
Best data table components in the React ecosystem. Insurance apps are data-heavy — tables, forms, filters everywhere. Ant Design's Table component handles sorting, filtering, pagination, row selection out of the box. Pro components for even more complex scenarios.



PART 7: CRITICAL BUSINESS LOGIC NOTES

Assumption Approval Workflow:
1. User creates assumption set in "draft" status
2. User edits tables, validates data
3. User submits for approval (status → "pending_approval")
4. Task created for users with approver role
5. Approver reviews, compares to previous approved set
6. Approver approves (status → "approved", effective_date set) or rejects (status → "draft", notes added)
7. Only one assumption set per type can be "approved" and effective at a time
8. Previous approved sets archived (status → "archived")
9. All actions logged to audit trail

Calculation Run Flow:
1. User selects model, assumption set, policy filter, parameters
2. System creates calculation_run record (status = "queued")
3. Celery task dispatched
4. Worker picks up task, updates status to "running"
5. Worker loads model definition, builds calculation graph
6. Worker loads assumption tables into memory
7. Worker queries policies matching filter
8. Worker processes policies in batches (configurable batch size)
9. For each policy: execute calculation graph, store results
10. Worker updates progress periodically (for real-time UI updates)
11. On completion: status → "completed", summary computed
12. On failure: status → "failed", error_message stored
13. Notification sent to user who triggered

Policy Status Transitions:
Active → Lapsed (non-payment, auto after grace period)
Active → Surrendered (policyholder request)
Active → Matured (reached maturity date)
Active → Claimed (death/event claim)
Lapsed → Active (reinstatement)
Any status change triggers audit log

Claim Processing:
Open → Under Review (assigned to adjuster)
Under Review → Approved (ready for payment)
Under Review → Denied (with reason)
Approved → Paid (settlement processed)
Can't skip statuses. Each transition logged.



PART 8: DATABASE INDEXES AND PERFORMANCE

Critical indexes to create:

policies:
- (product_code, status) — for filtered queries
- (policyholder_id) — for holder lookups
- (issue_date) — for date range queries
- (branch_code) — for branch filtering

calculation_results:
- (calculation_run_id) — partition key
- (policy_id) — for policy-level queries
- (result_type) — for filtering output types

assumption_tables:
- (assumption_set_id, table_type) — for loading tables

audit_log:
- (timestamp DESC) — for recent logs
- (resource_type, resource_id) — for resource history
- (user_id, timestamp DESC) — for user activity

Partitioning:
- calculation_results partitioned by calculation_run_id (range)
- audit_log partitioned by timestamp (monthly)



PART 9: SECURITY CHECKLIST

□ All API endpoints require authentication (except /auth/login)
□ Role-based access enforced at API layer
□ Sensitive fields encrypted at rest (PII, health data)
□ Audit log captures all data access and modifications
□ Database connections use SSL
□ Secrets stored in Kubernetes secrets or vault
□ File uploads validated (type, size, malware scan)
□ SQL injection prevented (ORM, parameterized queries)
□ XSS prevented (React escapes by default, CSP headers)
□ CSRF prevented (SameSite cookies, CORS configured)
□ Rate limiting on auth endpoints
□ Session timeout configured
□ Password policy enforced (via Keycloak)
□ Dependency vulnerabilities scanned regularly



PART 10: TESTING STRATEGY

Backend:
- Unit tests for service layer (mock repositories)
- Unit tests for calculation engine nodes
- Integration tests for repositories (test DB)
- API tests for endpoints (TestClient, authenticated)
- Calculation accuracy tests (known policy, expected results)

Frontend:
- Unit tests for utility functions
- Component tests with React Testing Library
- Integration tests for complex flows (import wizard)
- E2E tests with Playwright for critical paths (login, run calculation, generate report)

Calculation Engine:
- Mathematical accuracy tests against known results
- Performance tests for large portfolios
- Regression tests to ensure changes don't alter outputs



This is the complete blueprint. Every file, every folder, every endpoint, every model, every component — it's all mapped out. An AI coding assistant should be able to pick this up and implement it section by section, starting with the foundation and building up.

The critical success factor is the calculation engine. That's where the actual actuarial value lives. The rest is data management around it. Start with the foundation, get policies flowing in, then build the calculation engine piece by piece (start with simple term life, then expand).