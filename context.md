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
Intelligent assistance. AI helps where it adds value — data quality, insights, natural language — but never replaces deterministic, auditable calculations.

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

Module 9: AI & Intelligent Automation
The differentiator. AI-powered features that augment human work without replacing auditable calculations:

9.1 Smart Data Import
- Auto-detect column mappings when uploading CSV/Excel files
- Identify and flag data quality issues (missing values, outliers, format mismatches)
- Suggest corrections for common data errors (e.g., "Did you mean 'Male' instead of 'M'?")
- Learn from user corrections to improve future suggestions
- Extract structured data from PDF documents and scanned applications (OCR + entity extraction)

9.2 Natural Language Query Interface
- Ask questions in plain English: "Show me all term life policies issued in 2023 with sum assured over $1M"
- Generate filters, create ad-hoc reports, navigate to specific records
- Works across policies, claims, calculations, reports
- Translates user intent into API calls, never into direct SQL (security)

9.3 Anomaly Detection & Alerts
- Flag calculation results that deviate significantly from historical norms
- Identify potentially suspicious claims patterns
- Detect data entry errors in real-time ("This premium seems unusually high for this product")
- Alert when actual vs. expected experience diverges beyond thresholds
- All flags are suggestions for human review, never auto-actions

9.4 Narrative Generation
- Auto-generate executive summaries for calculation runs
- Create plain-English explanations of reserve movements
- Draft variance commentary for board reports
- Summarize scenario comparison results
- User always reviews and edits before finalizing

9.5 Assumption Experience Analysis
- Compare assumed rates to actual experience
- Suggest assumption updates based on credible experience
- Generate experience study reports
- Identify segments where assumptions are most off

9.6 Intelligent Search
- Semantic search across all content (policies, documents, notes, reports)
- Find similar policies, related claims, relevant past calculations
- Search by meaning, not just keywords

9.7 Predictive Insights (Optional/Advanced)
- Lapse propensity scoring for in-force policies
- Claims likelihood indicators
- Premium persistency forecasting
- Clearly labeled as "predictive" — not used in regulatory calculations

Module 10: Automation Engine
Non-AI automation for operational efficiency:

10.1 Scheduled Jobs
- Automated calculation runs (daily/weekly/monthly/quarterly)
- Scheduled report generation with email delivery
- Periodic data quality checks
- Assumption set archival after superseded

10.2 Triggered Workflows
- Auto-create approval tasks when assumptions submitted
- Auto-notify users when calculations complete
- Auto-lapse policies after grace period expires
- Auto-escalate overdue tasks
- Webhook integrations for external system notifications

10.3 Data Pipeline Automation
- Scheduled imports from SFTP/S3 sources
- Automated data transformation rules
- Incremental sync from source systems
- Automated backup verification

10.4 Batch Operations
- Bulk policy status updates
- Mass recalculation triggers
- Portfolio-wide assumption updates
- Automated month-end/quarter-end job sequences


PART 3: TECHNOLOGY STACK

Frontend: React with TypeScript, using a component library like Ant Design (which has excellent table/data components that feel spreadsheet-like). TanStack Table for the heavy data grid work. Recharts or D3 for visualizations. Zustand for state management. React Query for server state.

Backend: Python with FastAPI. Python because the actuarial calculation libraries (NumPy, SciPy, Pandas) are all Python-native. FastAPI because it's fast, async, auto-documents APIs, and handles concurrent calculation jobs well.

Calculation Engine: A dedicated Python service using NumPy/SciPy for actuarial math, Celery with Redis for job queuing (calculations can take minutes — they need to run async), and a model definition layer that translates the visual model builder into executable calculation graphs.

AI Service: A dedicated Python service for AI/ML features. Uses OpenAI API (or self-hosted LLM for enterprise deployments), sentence-transformers for embeddings, scikit-learn for anomaly detection. Isolated from core calculation engine — AI features are assistive, never in the critical calculation path.

Database: PostgreSQL as the primary relational database (policy data is highly relational). Redis for caching, session management, and as Celery's message broker. MinIO or S3-compatible object storage for file uploads, report outputs, and large dataset storage. pgvector extension for vector embeddings (semantic search).

Authentication: Keycloak for enterprise SSO, LDAP integration, RBAC. Insurance companies will demand this.

Infrastructure: Docker containers, orchestrated with Docker Compose for development and Kubernetes for production. Nginx as reverse proxy.

Search: Elasticsearch for searching across policies, reports, audit logs. Vector search via pgvector for semantic queries.

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
│         calculation engine, AI service, PostgreSQL, Redis, MinIO,
│         Elasticsearch, Keycloak. One command to spin up the entire stack.
│
├── docker-compose.prod.yml
│       → Production-oriented compose file with proper resource limits,
│         replicas, health checks, and external volume mounts.
│
├── .env.example
│       → Template for environment variables. Database URLs, Redis URL,
│         S3 credentials, JWT secrets, Keycloak config, SMTP settings
│         for email notifications, OpenAI API key (optional).
│         Never committed with real values.
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
│   ├── ai-features.md
│   │       → Documents all AI/ML features: what models are used,
│   │         what data they access, how to disable them, privacy
│   │         implications, accuracy expectations, human-in-the-loop
│   │         requirements. Critical for enterprise sales.
│   │
│   ├── automation-guide.md
│   │       → How to configure scheduled jobs, triggers, workflows.
│   │         Cron syntax reference, webhook setup, job dependencies.
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
│   │         python-keycloak, elasticsearch-py, pandas, numpy, scipy,
│   │         openai, sentence-transformers, pgvector.
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
│   │   │         upload limits, CORS origins, AI feature flags,
│   │   │         OpenAI API key. Validated on startup.
│   │   │
│   │   ├── dependencies.py
│   │   │       → FastAPI dependency injection functions. get_db() yields
│   │   │         a database session. get_current_user() extracts and
│   │   │         validates JWT token. get_redis() returns Redis client.
│   │   │         require_role("actuary") returns a dependency that
│   │   │         checks the user's role. get_ai_service() returns AI
│   │   │         service client (if enabled).
│   │   │
│   │   ├── exceptions.py
│   │   │       → Custom exception classes: NotFoundError, ForbiddenError,
│   │   │         ValidationError, CalculationError, DataImportError,
│   │   │         AIServiceError. Each maps to an HTTP status code and
│   │   │         error response shape.
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
│   │   │   │         department, is_active, last_login, keycloak_id,
│   │   │   │         ai_preferences (JSONB — user's AI feature settings).
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
│   │   │   │         underwriter_id, embedding (vector for semantic search).
│   │   │   │         Relationships to Policyholder, Coverage, Rider,
│   │   │   │         Claim, CashFlow.
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
│   │   │   │         settlement_amount, adjuster_notes, anomaly_score
│   │   │   │         (float — AI-generated suspicion indicator, nullable).
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
│   │   │   │         triggered_by (user_id), trigger_type (manual/
│   │   │   │         scheduled/automated), policy_filter (JSONB —
│   │   │   │         which policies were included in this run),
│   │   │   │         parameters (JSONB — valuation date, reporting
│   │   │   │         basis, etc.), error_message (if failed),
│   │   │   │         result_summary (JSONB — high-level totals),
│   │   │   │         ai_narrative (text — AI-generated summary, nullable).
│   │   │   │         Relationships to ModelDefinition, AssumptionSet,
│   │   │   │         CalculationResult.
│   │   │   │
│   │   │   ├── calculation_result.py
│   │   │   │       → Stores detailed calculation outputs. Fields: id,
│   │   │   │         calculation_run_id, policy_id, projection_month,
│   │   │   │         result_type (reserve/cashflow/profit_margin/etc.),
│   │   │   │         values (JSONB), anomaly_flag (boolean — AI-detected
│   │   │   │         unusual result). This table will be large —
│   │   │   │         partitioned by calculation_run_id.
│   │   │   │
│   │   │   ├── report_template.py
│   │   │   │       → Defines report templates. Fields: id, name,
│   │   │   │         report_type (regulatory/internal/adhoc),
│   │   │   │         regulatory_standard (IFRS17/SolvencyII/USGAAP/
│   │   │   │         LDTI/null for internal), template_config (JSONB),
│   │   │   │         output_format (PDF/Excel/CSV),
│   │   │   │         is_system_template, created_by,
│   │   │   │         include_ai_narrative (boolean — whether to auto-
│   │   │   │         generate executive summary).
│   │   │   │
│   │   │   ├── generated_report.py
│   │   │   │       → Records of generated reports. Fields: id,
│   │   │   │         report_template_id, reporting_period_start,
│   │   │   │         reporting_period_end, generated_by, generated_at,
│   │   │   │         status (generating/completed/failed), file_path,
│   │   │   │         file_size, parameters (JSONB), ai_summary (text).
│   │   │   │
│   │   │   ├── scenario.py
│   │   │   │       → Scenario definitions for stress testing. Fields:
│   │   │   │         id, name, description, scenario_type (deterministic/
│   │   │   │         stochastic), base_assumption_set_id, adjustments
│   │   │   │         (JSONB), created_by, status.
│   │   │   │
│   │   │   ├── scenario_result.py
│   │   │   │       → Results of scenario runs. Links scenario to
│   │   │   │         calculation_run. Fields: id, scenario_id,
│   │   │   │         calculation_run_id, comparison_base_run_id,
│   │   │   │         impact_summary (JSONB), ai_narrative (text).
│   │   │   │
│   │   │   ├── dashboard_config.py
│   │   │   │       → User-created dashboard configurations. Fields: id,
│   │   │   │         name, owner_id, is_shared, layout (JSONB), widgets
│   │   │   │         (JSONB array). Relationship to User.
│   │   │   │
│   │   │   ├── data_import.py
│   │   │   │       → Tracks data import jobs. Fields: id, file_name,
│   │   │   │         file_path, import_type, status, total_rows,
│   │   │   │         processed_rows, error_rows, error_details (JSONB),
│   │   │   │         column_mapping (JSONB), ai_suggested_mapping (JSONB
│   │   │   │         — AI's auto-detected column mappings),
│   │   │   │         ai_data_issues (JSONB — AI-detected quality issues),
│   │   │   │         uploaded_by, started_at, completed_at.
│   │   │   │
│   │   │   ├── audit_log.py
│   │   │   │       → Immutable audit trail. Fields: id, timestamp,
│   │   │   │         user_id, action, resource_type, resource_id,
│   │   │   │         old_values (JSONB), new_values (JSONB),
│   │   │   │         ip_address, user_agent. Append-only.
│   │   │   │
│   │   │   ├── task.py
│   │   │   │       → Workflow tasks. Fields: id, title, description,
│   │   │   │         task_type, status, priority, assigned_to,
│   │   │   │         assigned_by, due_date, related_resource_type,
│   │   │   │         related_resource_id, completion_notes,
│   │   │   │         auto_generated (boolean — was this task created
│   │   │   │         by automation?).
│   │   │   │
│   │   │   ├── comment.py
│   │   │   │       → Comments/notes on any resource. Fields: id,
│   │   │   │         resource_type, resource_id, user_id, content,
│   │   │   │         parent_comment_id, is_resolved.
│   │   │   │
│   │   │   ├── notification.py
│   │   │   │       → User notifications. Fields: id, user_id, type,
│   │   │   │         title, message, is_read, resource_type, resource_id,
│   │   │   │         created_at.
│   │   │   │
│   │   │   ├── scheduled_job.py
│   │   │   │       → Scheduled automation jobs. Fields: id, name,
│   │   │   │         job_type (calculation/report/import/data_check),
│   │   │   │         cron_expression, config (JSONB — job parameters),
│   │   │   │         is_active, last_run, next_run, created_by.
│   │   │   │
│   │   │   ├── job_execution.py
│   │   │   │       → Records of scheduled job executions. Fields: id,
│   │   │   │         scheduled_job_id, started_at, completed_at,
│   │   │   │         status (running/completed/failed), result_summary,
│   │   │   │         error_message.
│   │   │   │
│   │   │   ├── automation_rule.py
│   │   │   │       → Trigger-based automation rules. Fields: id, name,
│   │   │   │         trigger_type (policy_status_change/calculation_complete/
│   │   │   │         threshold_breach/time_based), trigger_config (JSONB),
│   │   │   │         action_type (send_notification/create_task/run_calculation/
│   │   │   │         call_webhook), action_config (JSONB), is_active,
│   │   │   │         created_by.
│   │   │   │
│   │   │   ├── ai_query_log.py
│   │   │   │       → Logs natural language queries for learning/auditing.
│   │   │   │         Fields: id, user_id, query_text, interpreted_intent
│   │   │   │         (JSONB — what the AI understood), executed_action,
│   │   │   │         was_helpful (user feedback), timestamp.
│   │   │   │
│   │   │   ├── document.py
│   │   │   │       → Uploaded documents (PDFs, images). Fields: id,
│   │   │   │         file_name, file_path, document_type, related_resource_
│   │   │   │         type, related_resource_id, extracted_text (text —
│   │   │   │         OCR result), extracted_data (JSONB — structured
│   │   │   │         data extracted by AI), embedding (vector),
│   │   │   │         uploaded_by, uploaded_at.
│   │   │   │
│   │   │   └── experience_analysis.py
│   │   │           → Experience study results. Fields: id, analysis_type
│   │   │             (mortality/lapse/morbidity), study_period_start,
│   │   │             study_period_end, parameters (JSONB), results (JSONB),
│   │   │             ai_recommendations (JSONB — suggested assumption
│   │   │             updates), created_by, created_at.
│   │   │
│   │   │
│   │   ├── schemas/
│   │   │   │       → Pydantic schemas for request/response validation
│   │   │   │         and serialization.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── common.py
│   │   │   │       → Shared schemas: PaginatedResponse, SortParam,
│   │   │   │         FilterParam, BulkActionRequest, BulkActionResponse,
│   │   │   │         ErrorResponse, SuccessMessage, DateRange,
│   │   │   │         FileUploadResponse.
│   │   │   │
│   │   │   ├── user.py
│   │   │   │       → UserCreate, UserUpdate, UserResponse, UserListItem,
│   │   │   │         UserProfile, RoleResponse, PermissionResponse.
│   │   │   │
│   │   │   ├── policy.py
│   │   │   │       → PolicyCreate, PolicyUpdate, PolicyResponse,
│   │   │   │         PolicyListItem, PolicyFilter, PolicyBulkUpdate,
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
│   │   │   │         ClaimFilter, ClaimSummaryStats, ClaimAnomalyAlert.
│   │   │   │
│   │   │   ├── assumption.py
│   │   │   │       → AssumptionSetCreate, AssumptionSetUpdate,
│   │   │   │         AssumptionSetResponse, AssumptionSetListItem,
│   │   │   │         AssumptionTableCreate, AssumptionTableUpdate,
│   │   │   │         AssumptionTableResponse, AssumptionApprovalRequest,
│   │   │   │         AssumptionComparison, ExperienceRecommendation.
│   │   │   │
│   │   │   ├── model.py
│   │   │   │       → ModelDefinitionCreate, ModelDefinitionUpdate,
│   │   │   │         ModelDefinitionResponse, ModelDefinitionListItem,
│   │   │   │         ModelConfigSchema.
│   │   │   │
│   │   │   ├── calculation.py
│   │   │   │       → CalculationRunCreate, CalculationRunResponse,
│   │   │   │         CalculationRunListItem, CalculationRunProgress,
│   │   │   │         CalculationResultResponse, CalculationResultFilter,
│   │   │   │         CalculationSummary, CalculationNarrative.
│   │   │   │
│   │   │   ├── scenario.py
│   │   │   │       → ScenarioCreate, ScenarioUpdate, ScenarioResponse,
│   │   │   │         ScenarioAdjustment, ScenarioResultResponse,
│   │   │   │         ScenarioComparison.
│   │   │   │
│   │   │   ├── report.py
│   │   │   │       → ReportTemplateCreate, ReportTemplateResponse,
│   │   │   │         GenerateReportRequest, GeneratedReportResponse,
│   │   │   │         ReportScheduleCreate.
│   │   │   │
│   │   │   ├── dashboard.py
│   │   │   │       → DashboardConfigCreate, DashboardConfigUpdate,
│   │   │   │         DashboardConfigResponse, WidgetConfig,
│   │   │   │         WidgetDataRequest, WidgetDataResponse.
│   │   │   │
│   │   │   ├── data_import.py
│   │   │   │       → DataImportCreate, DataImportResponse,
│   │   │   │         DataImportProgress, ColumnMappingRequest,
│   │   │   │         ValidationResultResponse, AISuggestedMapping,
│   │   │   │         AIDataIssue.
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
│   │   │   ├── audit.py
│   │   │   │       → AuditLogResponse, AuditLogFilter.
│   │   │   │
│   │   │   ├── automation.py
│   │   │   │       → ScheduledJobCreate, ScheduledJobUpdate,
│   │   │   │         ScheduledJobResponse, AutomationRuleCreate,
│   │   │   │         AutomationRuleResponse, JobExecutionResponse.
│   │   │   │
│   │   │   ├── ai.py
│   │   │   │       → NaturalLanguageQuery, NaturalLanguageResponse,
│   │   │   │         AnomalyAlert, NarrativeRequest, NarrativeResponse,
│   │   │   │         DocumentExtractionResult, SemanticSearchRequest,
│   │   │   │         SemanticSearchResult.
│   │   │   │
│   │   │   └── experience.py
│   │   │           → ExperienceAnalysisRequest, ExperienceAnalysisResponse,
│   │   │             ExperienceStudyResult, AssumptionRecommendation.
│   │   │
│   │   │
│   │   ├── api/
│   │   │   │       → API route handlers. Each file is a FastAPI Router.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── router.py
│   │   │   │       → Master router that includes all sub-routers with
│   │   │   │         their URL prefixes: /api/v1/policies,
│   │   │   │         /api/v1/assumptions, /api/v1/calculations,
│   │   │   │         /api/v1/ai, /api/v1/automation, etc.
│   │   │   │
│   │   │   ├── auth.py
│   │   │   │       → POST /auth/login, POST /auth/refresh,
│   │   │   │         POST /auth/logout, GET /auth/me.
│   │   │   │
│   │   │   ├── users.py
│   │   │   │       → CRUD for users. GET /users, GET /users/{id},
│   │   │   │         POST /users, PUT /users/{id}, DELETE /users/{id},
│   │   │   │         PUT /users/{id}/role, GET /users/{id}/activity.
│   │   │   │
│   │   │   ├── roles.py
│   │   │   │       → GET /roles, GET /roles/{id}, POST /roles,
│   │   │   │         PUT /roles/{id}, DELETE /roles/{id},
│   │   │   │         PUT /roles/{id}/permissions.
│   │   │   │
│   │   │   ├── policies.py
│   │   │   │       → GET /policies, GET /policies/{id}, POST /policies,
│   │   │   │         PUT /policies/{id}, DELETE /policies/{id},
│   │   │   │         POST /policies/bulk, PUT /policies/bulk,
│   │   │   │         GET /policies/stats, GET /policies/export,
│   │   │   │         GET /policies/{id}/history, GET /policies/{id}/similar
│   │   │   │         (AI-powered similar policy finder).
│   │   │   │
│   │   │   ├── policyholders.py
│   │   │   │       → CRUD + GET /policyholders/{id}/policies,
│   │   │   │         POST /policyholders/search.
│   │   │   │
│   │   │   ├── coverages.py
│   │   │   │       → CRUD for coverages.
│   │   │   │
│   │   │   ├── claims.py
│   │   │   │       → CRUD + PUT /claims/{id}/status, GET /claims/stats,
│   │   │   │         GET /claims/anomalies (AI-flagged suspicious claims).
│   │   │   │
│   │   │   ├── assumptions.py
│   │   │   │       → CRUD for assumption-sets and tables,
│   │   │   │         POST /assumption-sets/{id}/clone,
│   │   │   │         POST /assumption-sets/{id}/submit,
│   │   │   │         POST /assumption-sets/{id}/approve,
│   │   │   │         POST /assumption-sets/{id}/reject,
│   │   │   │         GET /assumption-sets/{id}/compare/{other_id},
│   │   │   │         GET /assumption-sets/{id}/experience-recommendations
│   │   │   │         (AI-suggested updates based on actual vs expected).
│   │   │   │
│   │   │   ├── models.py
│   │   │   │       → CRUD for model definitions, POST /models/{id}/clone,
│   │   │   │         POST /models/{id}/validate, GET /model-templates.
│   │   │   │
│   │   │   ├── calculations.py
│   │   │   │       → POST /calculations, GET /calculations,
│   │   │   │         GET /calculations/{id}, DELETE /calculations/{id}/cancel,
│   │   │   │         GET /calculations/{id}/progress,
│   │   │   │         GET /calculations/{id}/results,
│   │   │   │         GET /calculations/{id}/results/export,
│   │   │   │         GET /calculations/{id}/summary,
│   │   │   │         GET /calculations/{id}/narrative (AI-generated summary),
│   │   │   │         GET /calculations/{id}/anomalies (AI-flagged results),
│   │   │   │         POST /calculations/{id}/rerun,
│   │   │   │         GET /calculations/compare.
│   │   │   │
│   │   │   ├── scenarios.py
│   │   │   │       → CRUD + POST /scenarios/{id}/run,
│   │   │   │         GET /scenarios/{id}/results, GET /scenarios/compare.
│   │   │   │
│   │   │   ├── reports.py
│   │   │   │       → CRUD for templates, POST /reports/generate,
│   │   │   │         GET /reports, GET /reports/{id}/download,
│   │   │   │         POST /report-schedules.
│   │   │   │
│   │   │   ├── dashboards.py
│   │   │   │       → CRUD + POST /dashboards/{id}/share,
│   │   │   │         POST /widgets/data.
│   │   │   │
│   │   │   ├── imports.py
│   │   │   │       → POST /imports/upload, GET /imports/{id},
│   │   │   │         POST /imports/{id}/mapping, POST /imports/{id}/validate,
│   │   │   │         POST /imports/{id}/commit, DELETE /imports/{id}/cancel,
│   │   │   │         GET /imports/{id}/ai-suggestions (AI column mapping
│   │   │   │         and data quality suggestions).
│   │   │   │
│   │   │   ├── tasks.py
│   │   │   │       → CRUD + PUT /tasks/{id}/status, PUT /tasks/{id}/assign,
│   │   │   │         GET /tasks/my.
│   │   │   │
│   │   │   ├── comments.py
│   │   │   │       → CRUD + PUT /comments/{id}/resolve.
│   │   │   │
│   │   │   ├── notifications.py
│   │   │   │       → GET /notifications, PUT /notifications/{id}/read,
│   │   │   │         PUT /notifications/read-all, GET /notifications/unread-count.
│   │   │   │
│   │   │   ├── audit.py
│   │   │   │       → GET /audit-logs, GET /audit-logs/export.
│   │   │   │
│   │   │   ├── search.py
│   │   │   │       → GET /search?q=term (keyword search),
│   │   │   │         POST /search/semantic (AI-powered semantic search).
│   │   │   │
│   │   │   ├── ai.py
│   │   │   │       → POST /ai/query (natural language queries),
│   │   │   │         POST /ai/extract-document (extract data from PDF),
│   │   │   │         POST /ai/generate-narrative (generate text summary),
│   │   │   │         GET /ai/query-history (user's past queries),
│   │   │   │         POST /ai/query/{id}/feedback (was result helpful).
│   │   │   │
│   │   │   ├── automation.py
│   │   │   │       → CRUD for /scheduled-jobs, GET /scheduled-jobs/{id}/runs,
│   │   │   │         POST /scheduled-jobs/{id}/run-now,
│   │   │   │         CRUD for /automation-rules,
│   │   │   │         POST /automation-rules/{id}/test.
│   │   │   │
│   │   │   ├── experience.py
│   │   │   │       → POST /experience-analysis (run experience study),
│   │   │   │         GET /experience-analysis, GET /experience-analysis/{id},
│   │   │   │         GET /experience-analysis/{id}/recommendations.
│   │   │   │
│   │   │   ├── documents.py
│   │   │   │       → POST /documents/upload, GET /documents,
│   │   │   │         GET /documents/{id}, GET /documents/{id}/extracted-data,
│   │   │   │         POST /documents/search (semantic search in documents).
│   │   │   │
│   │   │   └── websocket.py
│   │   │           → /ws/calculations/{id}, /ws/notifications,
│   │   │             /ws/collaboration/{resource_type}/{id}.
│   │   │
│   │   │
│   │   ├── services/
│   │   │   │       → Business logic layer.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── user_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── policy_service.py
│   │   │   ├── policyholder_service.py
│   │   │   ├── claim_service.py
│   │   │   ├── assumption_service.py
│   │   │   ├── model_service.py
│   │   │   ├── calculation_service.py
│   │   │   ├── scenario_service.py
│   │   │   ├── report_service.py
│   │   │   ├── dashboard_service.py
│   │   │   ├── import_service.py
│   │   │   ├── task_service.py
│   │   │   ├── comment_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── audit_service.py
│   │   │   ├── search_service.py
│   │   │   │
│   │   │   ├── ai_service.py
│   │   │   │       → AIService class: process_natural_language_query()
│   │   │   │         (parses user intent, generates API calls),
│   │   │   │         generate_narrative() (creates text summaries),
│   │   │   │         detect_anomalies() (flags unusual patterns),
│   │   │   │         extract_document_data() (OCR + entity extraction),
│   │   │   │         suggest_column_mapping() (for imports),
│   │   │   │         analyze_data_quality() (find issues in import),
│   │   │   │         semantic_search() (vector similarity search),
│   │   │   │         generate_embedding() (create vector for text/record).
│   │   │   │         Wraps calls to OpenAI API or local model.
│   │   │   │
│   │   │   ├── automation_service.py
│   │   │   │       → AutomationService: create_scheduled_job(),
│   │   │   │         update_scheduled_job(), delete_scheduled_job(),
│   │   │   │         execute_job(), get_next_runs(), process_trigger(),
│   │   │   │         evaluate_automation_rules() (check if rule conditions met),
│   │   │   │         execute_automation_action() (perform the configured action).
│   │   │   │
│   │   │   ├── experience_service.py
│   │   │   │       → ExperienceService: run_experience_study(),
│   │   │   │         calculate_actual_vs_expected(), generate_recommendations(),
│   │   │   │         compare_to_assumptions().
│   │   │   │
│   │   │   └── document_service.py
│   │   │           → DocumentService: upload_document(), extract_text(),
│   │   │             extract_structured_data(), index_for_search(),
│   │   │             search_documents().
│   │   │
│   │   │
│   │   ├── repositories/
│   │   │   │       → Data access layer.
│   │   │   │
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── user_repository.py
│   │   │   ├── policy_repository.py
│   │   │   ├── policyholder_repository.py
│   │   │   ├── claim_repository.py
│   │   │   ├── assumption_repository.py
│   │   │   ├── model_repository.py
│   │   │   ├── calculation_repository.py
│   │   │   ├── scenario_repository.py
│   │   │   ├── report_repository.py
│   │   │   ├── dashboard_repository.py
│   │   │   ├── import_repository.py
│   │   │   ├── task_repository.py
│   │   │   ├── comment_repository.py
│   │   │   ├── notification_repository.py
│   │   │   ├── audit_repository.py
│   │   │   ├── scheduled_job_repository.py
│   │   │   ├── automation_rule_repository.py
│   │   │   ├── ai_query_repository.py
│   │   │   ├── document_repository.py
│   │   │   └── experience_repository.py
│   │   │
│   │   │
│   │   └── utils/
│   │       │
│   │       ├── __init__.py
│   │       ├── security.py
│   │       ├── pagination.py
│   │       ├── filters.py
│   │       ├── file_handling.py
│   │       ├── excel_parser.py
│   │       ├── csv_generator.py
│   │       ├── pdf_generator.py
│   │       ├── email.py
│   │       ├── date_utils.py
│   │       ├── validators.py
│   │       │
│   │       ├── embeddings.py
│   │       │       → Generate text embeddings using sentence-transformers
│   │       │         or OpenAI. Used for semantic search and document
│   │       │         similarity.
│   │       │
│   │       ├── llm_client.py
│   │       │       → Abstraction layer for LLM calls. Supports OpenAI API,
│   │       │         Azure OpenAI, and local models (Ollama). Handles
│   │       │         retries, rate limiting, cost tracking.
│   │       │
│   │       ├── ocr.py
│   │       │       → OCR utilities using pytesseract or cloud OCR API.
│   │       │         Extracts text from scanned documents and images.
│   │       │
│   │       └── scheduler.py
│   │               → Cron expression parsing, next run calculation,
│   │                 job scheduling utilities using APScheduler.
│   │
│   │
│   ├── migrations/
│   │   │
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   │
│   │   └── versions/
│   │       ├── 001_initial_schema.py
│   │       ├── 002_assumptions_tables.py
│   │       ├── 003_models_and_calculations.py
│   │       ├── 004_scenarios.py
│   │       ├── 005_reports.py
│   │       ├── 006_dashboards.py
│   │       ├── 007_imports.py
│   │       ├── 008_workflow.py
│   │       ├── 009_audit_log.py
│   │       ├── 010_claims.py
│   │       ├── 011_automation.py
│   │       │       → Creates scheduled_jobs, job_executions,
│   │       │         automation_rules tables.
│   │       ├── 012_ai_features.py
│   │       │       → Creates ai_query_log, documents tables.
│   │       │         Adds embedding columns, AI-related fields.
│   │       │         Enables pgvector extension.
│   │       └── 013_experience_analysis.py
│   │               → Creates experience_analysis table.
│   │
│   │
│   └── tests/
│       │
│       ├── conftest.py
│       ├── factories/
│       ├── unit/
│       │   ├── test_policy_service.py
│       │   ├── test_assumption_service.py
│       │   ├── test_calculation_service.py
│       │   ├── test_ai_service.py
│       │   ├── test_automation_service.py
│       │   ├── test_date_utils.py
│       │   └── test_validators.py
│       ├── integration/
│       └── api/
│           ├── test_auth.py
│           ├── test_policies.py
│           ├── test_assumptions.py
│           ├── test_calculations.py
│           ├── test_scenarios.py
│           ├── test_reports.py
│           ├── test_imports.py
│           ├── test_ai.py
│           └── test_automation.py
│
│
│
├── calculation_engine/
│   │       → Separate service for actuarial calculations.
│   │
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── celery_app.py
│   ├── config.py
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── calculation_task.py
│   │   ├── report_generation_task.py
│   │   ├── import_task.py
│   │   ├── scheduled_job_task.py
│   │   │       → Celery task that executes scheduled jobs.
│   │   │         Called by the scheduler at configured times.
│   │   └── experience_analysis_task.py
│   │           → Long-running experience study calculations.
│   │
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── executor.py
│   │   ├── graph.py
│   │   ├── nodes/
│   │   ├── tables/
│   │   ├── projections/
│   │   └── standards/
│   │
│   ├── scheduler/
│   │   │       → Job scheduling subsystem.
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── scheduler_service.py
│   │   │       → Main scheduler service using APScheduler.
│   │   │         Loads active scheduled jobs from database,
│   │   │         creates APScheduler jobs, handles dynamic
│   │   │         add/remove/update of schedules.
│   │   │
│   │   └── job_dispatcher.py
│   │           → Dispatches jobs to appropriate Celery task based
│   │             on job_type. Handles job context preparation.
│   │
│   └── tests/
│
│
│
├── ai_service/
│   │       → Dedicated service for AI/ML features. Can be disabled
│   │         entirely for deployments that don't want AI.
│   │
│   ├── Dockerfile
│   │       → Based on python:3.12-slim. Includes torch (CPU),
│   │         sentence-transformers, scikit-learn, openai.
│   │
│   ├── pyproject.toml
│   │       → Dependencies: fastapi, uvicorn, openai, sentence-
│   │         transformers, scikit-learn, pytesseract, pdf2image,
│   │         numpy, pandas, redis.
│   │
│   ├── main.py
│   │       → FastAPI application for AI service. Internal API
│   │         called by main backend, not exposed externally.
│   │
│   ├── config.py
│   │       → AI-specific configuration: OpenAI API key, model names,
│   │         embedding model, anomaly detection thresholds, feature
│   │         flags for each AI capability.
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── nlp.py
│   │   │       → POST /nlp/parse-query (parse natural language),
│   │   │         POST /nlp/generate-text (generate narratives).
│   │   │
│   │   ├── embeddings.py
│   │   │       → POST /embeddings/generate (create embedding),
│   │   │         POST /embeddings/search (similarity search).
│   │   │
│   │   ├── extraction.py
│   │   │       → POST /extract/document (OCR + entity extraction),
│   │   │         POST /extract/table (extract tabular data from image).
│   │   │
│   │   └── anomaly.py
│   │           → POST /anomaly/detect (detect anomalies in data),
│   │             POST /anomaly/train (train anomaly model on history).
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   │
│   │   ├── nlp_service.py
│   │   │       → NLPService: parse_user_query() (understand intent,
│   │   │         extract entities, generate structured query),
│   │   │         generate_narrative() (create text from data),
│   │   │         summarize_results() (condense calculation outputs).
│   │   │
│   │   ├── embedding_service.py
│   │   │       → EmbeddingService: generate_embedding() (text to vector),
│   │   │         batch_generate() (multiple texts), find_similar()
│   │   │         (nearest neighbors search).
│   │   │
│   │   ├── extraction_service.py
│   │   │       → ExtractionService: ocr_document() (image to text),
│   │   │         extract_entities() (identify policy numbers, names,
│   │   │         dates, amounts), extract_table() (structured tabular data).
│   │   │
│   │   └── anomaly_service.py
│   │           → AnomalyService: train_model() (fit isolation forest
│   │             or similar on historical data), detect() (score new
│   │             records), explain_anomaly() (why is this flagged).
│   │
│   ├── models/
│   │   │       → ML model artifacts and loaders.
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── intent_classifier.py
│   │   │       → Classifies user query intent (search, filter, navigate,
│   │   │         aggregate, report). Can be rules-based or ML.
│   │   │
│   │   ├── entity_extractor.py
│   │   │       → Extracts entities from text (dates, amounts, policy
│   │   │         numbers, names). Uses spaCy or regex patterns.
│   │   │
│   │   └── anomaly_detector.py
│   │           → Isolation Forest or similar model for detecting
│   │             unusual records/results.
│   │
│   └── tests/
│       ├── test_nlp_service.py
│       ├── test_embedding_service.py
│       ├── test_extraction_service.py
│       └── test_anomaly_service.py
│
│
│
├── frontend/
│   │       → React application. TypeScript throughout.
│   │
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   │       → Dependencies include: react, react-dom, react-router-dom,
│   │         @tanstack/react-query, @tanstack/react-table, zustand,
│   │         antd, @ant-design/icons, recharts, dayjs, axios,
│   │         react-hook-form, zod, socket.io-client, react-flow
│   │         (for model builder), react-grid-layout (for dashboards).
│   │
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   │
│   └── src/
│       │
│       ├── main.tsx
│       ├── App.tsx
│       ├── routes.tsx
│       ├── vite-env.d.ts
│       │
│       ├── api/
│       │   ├── client.ts
│       │   ├── auth.ts
│       │   ├── users.ts
│       │   ├── policies.ts
│       │   ├── policyholders.ts
│       │   ├── claims.ts
│       │   ├── assumptions.ts
│       │   ├── models.ts
│       │   ├── calculations.ts
│       │   ├── scenarios.ts
│       │   ├── reports.ts
│       │   ├── dashboards.ts
│       │   ├── imports.ts
│       │   ├── tasks.ts
│       │   ├── comments.ts
│       │   ├── notifications.ts
│       │   ├── audit.ts
│       │   ├── search.ts
│       │   │
│       │   ├── ai.ts
│       │   │       → sendNaturalLanguageQuery(), getQueryHistory(),
│       │   │         submitQueryFeedback(), extractDocumentData(),
│       │   │         semanticSearch(), generateNarrative().
│       │   │
│       │   ├── automation.ts
│       │   │       → getScheduledJobs(), createScheduledJob(),
│       │   │         updateScheduledJob(), deleteScheduledJob(),
│       │   │         triggerJobNow(), getJobExecutions(),
│       │   │         getAutomationRules(), createAutomationRule(),
│       │   │         updateAutomationRule(), deleteAutomationRule(),
│       │   │         testAutomationRule().
│       │   │
│       │   ├── experience.ts
│       │   │       → runExperienceStudy(), getExperienceStudies(),
│       │   │         getExperienceStudy(), getRecommendations().
│       │   │
│       │   └── documents.ts
│       │           → uploadDocument(), getDocuments(), getDocument(),
│       │             getExtractedData(), searchDocuments().
│       │
│       │
│       ├── hooks/
│       │   ├── useAuth.ts
│       │   ├── usePolicies.ts
│       │   ├── useAssumptions.ts
│       │   ├── useCalculations.ts
│       │   ├── useScenarios.ts
│       │   ├── useReports.ts
│       │   ├── useDashboards.ts
│       │   ├── useImports.ts
│       │   ├── useTasks.ts
│       │   ├── useNotifications.ts
│       │   ├── useWebSocket.ts
│       │   ├── useDebounce.ts
│       │   ├── useLocalStorage.ts
│       │   │
│       │   ├── useAI.ts
│       │   │       → useNaturalLanguageQuery() (send query, get result),
│       │   │         useQueryHistory(), useSemanticSearch(),
│       │   │         useDocumentExtraction().
│       │   │
│       │   ├── useAutomation.ts
│       │   │       → useScheduledJobs(), useAutomationRules(),
│       │   │         useJobExecutions().
│       │   │
│       │   └── useExperience.ts
│       │           → useExperienceStudies(), useRecommendations().
│       │
│       │
│       ├── stores/
│       │   ├── authStore.ts
│       │   ├── uiStore.ts
│       │   ├── notificationStore.ts
│       │   │
│       │   └── aiStore.ts
│       │           → AI feature state: isAIEnabled, lastQuery,
│       │             queryHistory, pendingQuery.
│       │
│       │
│       ├── components/
│       │   ├── common/
│       │   │   ├── Layout.tsx
│       │   │   ├── Sidebar.tsx
│       │   │   ├── Header.tsx
│       │   │   │       → Header now includes AI search bar (CommandK style).
│       │   │   │
│       │   │   ├── DataTable.tsx
│       │   │   ├── PageHeader.tsx
│       │   │   ├── FilterPanel.tsx
│       │   │   ├── SearchInput.tsx
│       │   │   ├── ConfirmModal.tsx
│       │   │   ├── LoadingSpinner.tsx
│       │   │   ├── ErrorBoundary.tsx
│       │   │   ├── EmptyState.tsx
│       │   │   ├── FileUpload.tsx
│       │   │   ├── DateRangePicker.tsx
│       │   │   └── StatusBadge.tsx
│       │   │
│       │   ├── charts/
│       │   │   ├── LineChart.tsx
│       │   │   ├── BarChart.tsx
│       │   │   ├── PieChart.tsx
│       │   │   ├── AreaChart.tsx
│       │   │   └── CashflowChart.tsx
│       │   │
│       │   ├── forms/
│       │   │   ├── PolicyForm.tsx
│       │   │   ├── PolicyholderForm.tsx
│       │   │   ├── ClaimForm.tsx
│       │   │   ├── AssumptionSetForm.tsx
│       │   │   ├── AssumptionTableForm.tsx
│       │   │   ├── ModelDefinitionForm.tsx
│       │   │   ├── CalculationRunForm.tsx
│       │   │   ├── ScenarioForm.tsx
│       │   │   ├── ReportTemplateForm.tsx
│       │   │   ├── TaskForm.tsx
│       │   │   ├── UserForm.tsx
│       │   │   ├── ScheduledJobForm.tsx
│       │   │   │       → Form for creating/editing scheduled jobs.
│       │   │   │         Cron expression builder, job type selection,
│       │   │   │         parameters configuration.
│       │   │   │
│       │   │   └── AutomationRuleForm.tsx
│       │   │           → Form for trigger/action rule configuration.
│       │   │             Trigger type selection, condition builder,
│       │   │             action configuration.
│       │   │
│       │   ├── modals/
│       │   │   ├── ImportModal.tsx
│       │   │   │       → Now includes AI suggestions panel showing
│       │   │   │         auto-detected column mappings and data issues.
│       │   │   │
│       │   │   ├── ExportModal.tsx
│       │   │   ├── ColumnMappingModal.tsx
│       │   │   ├── ApprovalModal.tsx
│       │   │   ├── ComparisonModal.tsx
│       │   │   ├── CalculationProgressModal.tsx
│       │   │   │
│       │   │   └── DocumentPreviewModal.tsx
│       │   │           → Preview uploaded documents with extracted
│       │   │             text and entities highlighted.
│       │   │
│       │   ├── widgets/
│       │   │   ├── WidgetContainer.tsx
│       │   │   ├── PolicyCountWidget.tsx
│       │   │   ├── ReservesSummaryWidget.tsx
│       │   │   ├── ClaimsStatusWidget.tsx
│       │   │   ├── RecentCalculationsWidget.tsx
│       │   │   ├── TasksWidget.tsx
│       │   │   ├── TrendChartWidget.tsx
│       │   │   │
│       │   │   ├── AnomalyAlertWidget.tsx
│       │   │   │       → Shows recent AI-detected anomalies requiring
│       │   │   │         human review.
│       │   │   │
│       │   │   └── ScheduledJobsWidget.tsx
│       │   │           → Shows upcoming scheduled jobs and recent
│       │   │             execution status.
│       │   │
│       │   │
│       │   └── ai/
│       │       │       → AI-specific components.
│       │       │
│       │       ├── AISearchBar.tsx
│       │       │       → Command-K style search bar that accepts
│       │       │         natural language queries. Shows suggestions,
│       │       │         recent queries. Keyboard navigable.
│       │       │
│       │       ├── AIQueryResult.tsx
│       │       │       → Displays result of natural language query.
│       │       │         Shows interpreted intent, generated filters/
│       │       │         actions, results. Allows feedback.
│       │       │
│       │       ├── NarrativeSummary.tsx
│       │       │       → Displays AI-generated narrative with edit
│       │       │         capability. Shows "AI Generated" badge.
│       │       │
│       │       ├── AnomalyIndicator.tsx
│       │       │       → Visual indicator that a record has been
│       │       │         flagged as anomalous. Shows tooltip with reason.
│       │       │
│       │       ├── DataQualityPanel.tsx
│       │       │       → Shows AI-detected data quality issues during
│       │       │         import. Grouped by issue type, with fix suggestions.
│       │       │
│       │       ├── ExperienceRecommendations.tsx
│       │       │       → Displays AI-suggested assumption updates based
│       │       │         on experience analysis. Shows comparison,
│       │       │         confidence, affected calculations.
│       │       │
│       │       └── DocumentExtractor.tsx
│       │               → Upload zone for documents. Shows extraction
│       │                 progress, extracted fields, confidence scores.
│       │                 Allows manual correction.
│       │
│       │
│       ├── pages/
│       │   ├── Login.tsx
│       │   ├── Dashboard.tsx
│       │   │       → Now includes AI search bar, anomaly alert widget,
│       │   │         and scheduled jobs status.
│       │   │
│       │   ├── policies/
│       │   ├── policyholders/
│       │   ├── claims/
│       │   │   │
│       │   │   ├── ClaimList.tsx
│       │   │   │       → Includes filter for "AI Flagged" claims.
│       │   │   │
│       │   │   ├── ClaimDetail.tsx
│       │   │   │       → Shows anomaly indicator if flagged.
│       │   │   │
│       │   │   └── ClaimCreate.tsx
│       │   │
│       │   ├── assumptions/
│       │   │   │
│       │   │   ├── AssumptionSetList.tsx
│       │   │   ├── AssumptionSetDetail.tsx
│       │   │   │       → Now includes "Experience Recommendations" tab
│       │   │   │         showing AI-suggested updates.
│       │   │   │
│       │   │   ├── AssumptionSetCreate.tsx
│       │   │   ├── AssumptionTableEditor.tsx
│       │   │   └── AssumptionComparison.tsx
│       │   │
│       │   ├── models/
│       │   ├── calculations/
│       │   │   │
│       │   │   ├── CalculationList.tsx
│       │   │   ├── CalculationDetail.tsx
│       │   │   │       → Now includes AI narrative summary and
│       │   │   │         anomaly view for results.
│       │   │   │
│       │   │   ├── CalculationCreate.tsx
│       │   │   └── CalculationComparison.tsx
│       │   │
│       │   ├── scenarios/
│       │   ├── reports/
│       │   ├── dashboards/
│       │   ├── imports/
│       │   │   │
│       │   │   ├── ImportList.tsx
│       │   │   └── ImportWizard.tsx
│       │   │           → Enhanced with AI suggestions: auto column
│       │   │             mapping, data quality warnings, fix suggestions.
│       │   │
│       │   ├── tasks/
│       │   ├── audit/
│       │   ├── admin/
│       │   │
│       │   ├── automation/
│       │   │   │       → New section for automation management.
│       │   │   │
│       │   │   ├── ScheduledJobList.tsx
│       │   │   │       → List scheduled jobs, status, next run time.
│       │   │   │
│       │   │   ├── ScheduledJobDetail.tsx
│       │   │   │       → Job detail, execution history, logs.
│       │   │   │
│       │   │   ├── ScheduledJobCreate.tsx
│       │   │   │
│       │   │   ├── AutomationRuleList.tsx
│       │   │   │       → List trigger-based automation rules.
│       │   │   │
│       │   │   ├── AutomationRuleDetail.tsx
│       │   │   └── AutomationRuleCreate.tsx
│       │   │
│       │   ├── experience/
│       │   │   │       → Experience analysis section.
│       │   │   │
│       │   │   ├── ExperienceStudyList.tsx
│       │   │   ├── ExperienceStudyDetail.tsx
│       │   │   │       → Shows actual vs expected, graphs, AI recommendations.
│       │   │   │
│       │   │   └── ExperienceStudyCreate.tsx
│       │   │           → Configure experience study parameters.
│       │   │
│       │   ├── documents/
│       │   │   │       → Document management section.
│       │   │   │
│       │   │   ├── DocumentList.tsx
│       │   │   ├── DocumentDetail.tsx
│       │   │   │       → View document, extracted text, structured data.
│       │   │   │
│       │   │   └── DocumentUpload.tsx
│       │   │           → Upload with AI extraction preview.
│       │   │
│       │   └── NotFound.tsx
│       │
│       │
│       ├── styles/
│       │   ├── globals.css
│       │   └── theme.ts
│       │
│       ├── types/
│       │   ├── api.ts
│       │   ├── models.ts
│       │   ├── ui.ts
│       │   │
│       │   └── ai.ts
│       │           → AI-specific types: NaturalLanguageQuery,
│       │             ParsedIntent, AnomalyAlert, ExtractionResult,
│       │             Recommendation.
│       │
│       └── utils/
│           ├── formatters.ts
│           ├── validators.ts
│           ├── constants.ts
│           └── helpers.ts
│
│
│
├── infrastructure/
│   │
│   ├── kubernetes/
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secrets.yaml
│   │   │
│   │   ├── backend/
│   │   ├── calculation-engine/
│   │   ├── frontend/
│   │   ├── ingress.yaml
│   │   ├── postgresql/
│   │   ├── redis/
│   │   ├── elasticsearch/
│   │   ├── minio/
│   │   ├── keycloak/
│   │   │
│   │   └── ai-service/
│   │       │       → AI service deployment (optional).
│   │       │
│   │       ├── deployment.yaml
│   │       │       → AI service deployment. Higher memory for models.
│   │       │         Can be scaled to 0 if AI disabled.
│   │       │
│   │       └── service.yaml
│   │
│   ├── terraform/
│   │
│   └── monitoring/
│       ├── prometheus/
│       │   ├── prometheus.yaml
│       │   └── alerts.yaml
│       │           → Includes alerts for: scheduled job failures,
│       │             high anomaly flag rate, AI service latency.
│       │
│       ├── grafana/
│       │   ├── grafana.yaml
│       │   └── dashboards/
│       │       ├── backend.json
│       │       ├── calculations.json
│       │       ├── database.json
│       │       ├── automation.json
│       │       │       → Scheduled job success rate, execution times,
│       │       │         automation rule triggers.
│       │       │
│       │       └── ai-service.json
│       │               → AI query latency, extraction success rate,
│       │                 anomaly detection stats.
│       │
│       └── loki/
│
│
│
├── scripts/
│   ├── seed_db.py
│   ├── create_superuser.py
│   ├── load_mortality_tables.py
│   ├── backup_db.sh
│   ├── restore_db.sh
│   ├── migrate.sh
│   │
│   ├── train_anomaly_models.py
│   │       → Script to train anomaly detection models on historical data.
│   │         Run periodically to improve detection accuracy.
│   │
│   └── generate_embeddings.py
│           → Script to generate embeddings for existing records
│             (backfill for semantic search).
│
│
│
└── .github/
    ├── workflows/
    │   ├── ci.yml
    │   ├── cd.yml
    │   └── security.yml
    │
    ├── ISSUE_TEMPLATE/
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
- Basic scheduled job framework (infrastructure only)

Phase 2 — Actuarial Core (Weeks 5-10):
- Assumptions module: sets, tables, versioning
- Approval workflows for assumptions
- Model definition module
- Calculation engine: basic executor, graph, core nodes
- Integration: trigger calculations from UI, view results
- Term life projection implementation
- Scheduled calculation runs

Phase 3 — Reporting & Scenarios (Weeks 11-14):
- Report templates module
- Report generation (PDF, Excel)
- Scheduled report generation
- Scenario definition
- Scenario running and comparison
- Dashboard module with basic widgets
- Automation rules (triggers + actions)

Phase 4 — AI & Intelligence (Weeks 15-18):
- AI service deployment
- Smart import (auto column mapping, data quality)
- Natural language query interface
- Anomaly detection for calculations and claims
- Narrative generation for reports
- Semantic search
- Document extraction (OCR + entity extraction)

Phase 5 — Polish & Scale (Weeks 19-22):
- Advanced calculation nodes (IFRS 17, Solvency II)
- More product projections (whole life, annuity)
- Experience analysis module with AI recommendations
- Performance optimization
- Real-time features (WebSocket)
- Comprehensive testing
- Documentation

Phase 6 — Production Readiness (Weeks 23-26):
- Security hardening
- Kubernetes deployment refinement
- Monitoring and alerting setup
- Backup and disaster recovery
- User acceptance testing
- Bug fixes and polish



PART 6: KEY TECHNICAL DECISIONS EXPLAINED

Why FastAPI over Django?
FastAPI's async support is better for long-running calculation jobs. Auto-generated OpenAPI docs reduce frontend/backend sync issues. Type hints with Pydantic catch errors at development time.

Why PostgreSQL?
Actuarial data is highly relational. JSONB columns give flexibility. pgvector extension enables semantic search without a separate vector database.

Why Celery for calculations?
Actuarial calculations can run for minutes. Celery lets you queue jobs, process them in the background, scale workers independently.

Why Keycloak?
Insurance companies already have LDAP/AD. They want SSO. Keycloak handles enterprise auth.

Why separate AI service?
AI features are optional. Enterprises may disable them for compliance. Separate service means: 1) can scale independently, 2) can disable entirely, 3) different resource profile (more memory), 4) can swap LLM providers easily.

Why not put AI in critical calculation path?
Regulatory calculations must be deterministic and auditable. "The AI computed the reserve" won't fly with regulators. AI assists humans with data prep, search, summarization — never replaces auditable formulas.

Why APScheduler + Celery for automation?
APScheduler handles cron-like scheduling in-process. Celery handles the actual job execution (potentially long-running, needs retry/fault tolerance). Clean separation.



PART 7: CRITICAL BUSINESS LOGIC NOTES

[Previous sections on Assumption Approval Workflow, Calculation Run Flow, Policy Status Transitions, Claim Processing remain the same]

Automation Rule Evaluation:
1. Trigger event occurs (policy status change, calculation complete, etc.)
2. System queries active automation rules matching trigger_type
3. For each rule: evaluate trigger_config conditions against event data
4. If conditions match: execute configured action
5. Actions can be: send notification, create task, trigger calculation, call webhook
6. All automation actions are logged to audit trail with auto_generated=true
7. Failed actions are retried with exponential backoff

AI Feature Safeguards:
1. All AI suggestions require human confirmation before action
2. AI-detected anomalies are flagged for review, never auto-handled
3. Generated narratives are marked as "AI Generated" and editable
4. Natural language queries are logged for audit and improvement
5. Users can disable AI features in their preferences
6. Admins can disable AI features system-wide
7. AI never has write access to financial/regulatory data directly



PART 8: DATABASE INDEXES AND PERFORMANCE

[Previous indexes remain the same, adding:]

New indexes for AI/Automation:

scheduled_jobs:
- (is_active, next_run) — for scheduler queries

job_executions:
- (scheduled_job_id, started_at DESC) — for execution history

automation_rules:
- (is_active, trigger_type) — for rule evaluation

ai_query_log:
- (user_id, timestamp DESC) — for query history

documents:
- Embedding index using pgvector IVFFlat or HNSW
- (related_resource_type, related_resource_id) — for document lookup



PART 9: SECURITY CHECKLIST

[Previous items remain, adding:]

AI-Specific Security:
□ AI service only accessible from internal network (not exposed)
□ OpenAI API key stored in secrets manager, rotated quarterly
□ No PII sent to external AI APIs (or use Azure OpenAI with data residency)
□ AI query logs retained for audit but can be purged per retention policy
□ Rate limiting on AI endpoints to prevent abuse
□ AI feature flags checked at both API and service layer
□ Document extraction sandboxed (uploaded files scanned before processing)



PART 10: TESTING STRATEGY

[Previous items remain, adding:]

AI Service:
- Unit tests for intent parsing with known queries
- Unit tests for entity extraction with annotated samples
- Integration tests for full query → result flow
- Accuracy benchmarks for anomaly detection (precision/recall)
- Latency tests for embedding generation
- Mock external AI API for deterministic testing

Automation:
- Unit tests for cron expression parsing
- Unit tests for trigger condition evaluation
- Integration tests for rule → action flow
- Tests for retry behavior on failed actions
- Tests for concurrent job execution



PART 11: AI FEATURE FLAGS

All AI features are gated by feature flags:

AI_ENABLED=true                    # Master switch for all AI features
AI_SMART_IMPORT=true              # Auto column mapping + data quality
AI_NATURAL_LANGUAGE=true          # Natural language query interface
AI_ANOMALY_DETECTION=true         # Anomaly flagging for claims/calculations
AI_NARRATIVE_GENERATION=true      # Auto-generate executive summaries
AI_SEMANTIC_SEARCH=true           # Vector similarity search
AI_DOCUMENT_EXTRACTION=true       # OCR + entity extraction from documents
AI_EXPERIENCE_RECOMMENDATIONS=true # Suggest assumption updates

If AI_ENABLED=false:
- AI service doesn't start
- AI endpoints return 404
- AI UI components don't render
- All functionality works without AI (graceful degradation)

This allows enterprises to:
- Disable AI for compliance reasons
- Enable only specific AI features
- Roll out AI features gradually
- Run in "AI-free" mode for regulatory environments



This is the complete enhanced blueprint with AI and automation capabilities. The AI features are genuinely useful (not gimmicks), the automation saves real operational time, and everything degrades gracefully if AI is disabled.

The core actuarial platform works perfectly without AI — AI just makes it smarter.