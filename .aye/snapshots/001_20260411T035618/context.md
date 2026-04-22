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
│   │   ├── init.py
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
│   │   │         a database session. getcurrentuser() extracts and
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
│   │   │   ├── init.py
│   │   │   │       → Imports all models so Alembic can discover them.
│   │   │   │
│   │   │   ├── base.py
│   │   │   │       → Base model class that all others inherit from.
│   │   │   │         Includes common columns: id (UUID), created_at,
│   │   │   │         updatedat, createdby, is_deleted (soft delete).
│   │   │   │         Also defines the SQLAlchemy declarative base.
│   │   │   │
│   │   │   ├── user.py
│   │   │   │       → User model. Fields: id, email, fullname, roleid,
│   │   │   │         department, isactive, lastlogin, keycloak_id.
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
│   │   │   │         matured/claimed), policyholderid, issuedate,
│   │   │   │         maturitydate, sumassured, premium_amount,
│   │   │   │         premiumfrequency, currency, branchcode,
│   │   │   │         underwriter_id. Relationships to Policyholder,
│   │   │   │         Coverage, Rider, Claim, CashFlow.
│   │   │   │
│   │   │   ├── policyholder.py
│   │   │   │       → Policyholder model. Personal info: name, dateofbirth,
│   │   │   │         gender, smokerstatus, occupationclass, address,
│   │   │   │         contact info. Relationship to policies (one-to-many).
│   │   │   │
│   │   │   ├── coverage.py
│   │   │   │       → Coverage/benefit details attached to a policy.
│   │   │   │         Coverage type, benefit amount, start/end dates,
│   │   │   │         rider flag, premium allocation.
│   │   │   │
│   │   │   ├── claim.py
│   │   │   │       → Claims data. Claim number, policyid, claimdate,
│   │   │   │         claimtype, claimamount, status, settlement_date,
│   │   │   │         settlementamount, adjusternotes.
│   │   │   │
│   │   │   ├── assumption_set.py
│   │   │   │       → AssumptionSet model: name, version, status (draft/
│   │   │   │         approved/archived), effectivedate, approvedby,
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
│   │   │   │         modeltype (reserving/pricing/cashflow/valuation),
│   │   │   │         lineofbusiness, configuration stored as JSONB
│   │   │   │         (defines the calculation graph — what inputs, what
│   │   │   │         steps, what outputs), version, status, created_by.
│   │   │   │
│   │   │   ├── calculation_run.py
│   │   │   │       → Records of calculation executions
Picking up exactly where I left off:


│   │   │   ├── calculation_run.py
│   │   │   │       → Records of calculation executions. Fields: id,
│   │   │   │         modeldefinitionid, assumptionsetid, run_name,
│   │   │   │         status (queued/running/completed/failed/cancelled),
│   │   │   │         startedat, completedat, duration_seconds,
│   │   │   │         triggeredby (userid), policy_filter (JSONB —
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
│   │   │   │         calculationrunid, policyid, projectionmonth,
│   │   │   │         resulttype (reserve/cashflow/profit_margin/etc.),
│   │   │   │         values (JSONB — flexible structure to hold whatever
│   │   │   │         the model outputs: premiums, claims, expenses,
│   │   │   │         reserves, netcashflow, discount_factors, present
│   │   │   │         values). This table will be large — partitioned by
│   │   │   │         calculationrunid and indexed on policy_id.
│   │   │   │
│   │   │   ├── report_template.py
│   │   │   │       → Defines report templates. Fields: id, name,
│   │   │   │         reporttype (regulatory/internal/adhoc),
│   │   │   │         regulatory_standard (IFRS17/SolvencyII/USGAAP/
│   │   │   │         LDTI/null for internal), template_config (JSONB —
│   │   │   │         defines sections, data sources, formatting rules,
│   │   │   │         aggregation logic), output_format (PDF/Excel/CSV),
│   │   │   │         issystemtemplate (true for built-in regulatory
│   │   │   │         templates, false for user-created ones), created_by.
│   │   │   │
│   │   │   ├── generated_report.py
│   │   │   │       → Records of generated reports. Fields: id,
│   │   │   │         reporttemplateid, reportingperiodstart,
│   │   │   │         reportingperiodend, generatedby, generatedat,
│   │   │   │         status (generating/completed/failed), file_path
│   │   │   │         (S3/MinIO path to the output file), file_size,
│   │   │   │         parameters (JSONB — any filters or options the
│   │   │   │         user selected when generating).
│   │   │   │
│   │   │   ├── scenario.py
│   │   │   │       → Scenario definitions for stress testing. Fields:
│   │   │   │         id, name, description, scenario_type (deterministic/
│   │   │   │         stochastic), baseassumptionset_id, adjustments
│   │   │   │         (JSONB — describes how to modify the base assumptions,
│   │   │   │         e.g. {"mortality": {"factor": 1.1}, "lapse":
│   │   │   │         {"factor": 1.3}, "discount_rate": {"shift": -0.02}}),
│   │   │   │         created_by, status. Relationship to ScenarioResult.
│   │   │   │
│   │   │   ├── scenario_result.py
│   │   │   │       → Results of scenario runs. Links a scenario to a
│   │   │   │         calculationrun. Fields: id, scenarioid,
│   │   │   │         calculationrunid, comparisonbaserun_id (the
│   │   │   │         "base case" run to compare against), impact_summary
│   │   │   │         (JSONB — delta in reserves, P&L impact, capital
│   │   │   │         impact, etc.).
│   │   │   │
│   │   │   ├── dashboard_config.py
│   │   │   │       → User-created dashboard configurations. Fields: id,
│   │   │   │         name, ownerid, isshared, layout (JSONB — defines
│   │   │   │         widget positions, sizes in a grid system), widgets
│   │   │   │         (JSONB array — each widget has type, data_source,
│   │   │   │         chart_type, filters, title). Relationship to User.
│   │   │   │
│   │   │   ├── data_import.py
│   │   │   │       → Tracks data import jobs. Fields: id, file_name,
│   │   │   │         filepath, importtype (policy/claims/assumptions/
│   │   │   │         policyholder), status (uploaded/validating/validated/
│   │   │   │         importing/completed/failed), total_rows,
│   │   │   │         processedrows, errorrows, error_details (JSONB
│   │   │   │         array — row number, column, error message for each
│   │   │   │         failed row), column_mapping (JSONB — maps source
│   │   │   │         file columns to system fields), uploaded_by,
│   │   │   │         startedat, completedat.
│   │   │   │
│   │   │   ├── audit_log.py
│   │   │   │       → Immutable audit trail. Fields: id, timestamp,
│   │   │   │         user_id, action (create/update/delete/approve/
│   │   │   │         reject/export/login/logout/run_calculation),
│   │   │   │         resourcetype (policy/assumptionset/model/report/
│   │   │   │         etc.), resourceid, oldvalues (JSONB), new_values
│   │   │   │         (JSONB), ipaddress, useragent. This table is
│   │   │   │         append-only — no updates or deletes ever. Indexed
│   │   │   │         on timestamp, userid, resourcetype, resource_id.
│   │   │   │
│   │   │   ├── task.py
│   │   │   │       → Workflow tasks. Fields: id, title, description,
│   │   │   │         tasktype (review/approval/dataentry/calculation/
│   │   │   │         custom), status (open/in_progress/completed/
│   │   │   │         cancelled), priority (low/medium/high/critical),
│   │   │   │         assignedto, assignedby, duedate, relatedresource
│   │   │   │         type, relatedresourceid, completionnotes.
│   │   │   │
│   │   │   ├── comment.py
│   │   │   │       → Comments/notes on any resource. Fields: id,
│   │   │   │         resourcetype, resourceid, user_id, content,
│   │   │   │         parentcommentid (for threaded replies),
│   │   │   │         is_resolved. Polymorphic — can attach to policies,
│   │   │   │         assumption sets, calculation runs, anything.
│   │   │   │
│   │   │   └── notification.py
│   │   │           → User notifications. Fields: id, user_id, type
│   │   │             (taskassigned/approvalneeded/calculation_complete/
│   │   │             reportready/commentmention/import_complete),
│   │   │             title, message, isread, resourcetype, resource_id,
│   │   │             created_at.
│   │   │
│   │   │
│   │   ├── schemas/
│   │   │   │       → Pydantic schemas for request/response validation
│   │   │   │         and serialization. Mirrors the models directory
│   │   │   │         but defines API shapes, not DB shapes.
│   │   │   │
│   │   │   ├── init.py
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
│   │   │   │       → CalculationRunCreate (modelid, assumptionset_id,
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
│   │   │   ├── init.py
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
│   │   │   │         PUT /