# ActuFlow Data Model

## Overview

This document describes the complete database schema for ActuFlow. The database is PostgreSQL with pgvector extension for vector embeddings.

## Schema Conventions

- **Primary Keys**: UUID v4 for all tables
- **Timestamps**: `created_at` and `updated_at` on all tables
- **Soft Deletes**: `is_deleted` boolean flag (data is never hard deleted)
- **Audit Fields**: `created_by` references the user who created the record
- **JSONB**: Used for flexible/dynamic data structures

## Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────┐       ┌─────────────────┐
│    User     │──────<│     Task     │       │  AuditLog       │
└─────────────┘       └──────────────┘       └─────────────────┘
       │                                              ▲
       │                                              │
       ▼                                              │
┌─────────────┐                              (all tables log here)
│    Role     │
└─────────────┘
       │
       ▼
┌─────────────┐
│ Permission  │
└─────────────┘

┌──────────────────┐     ┌───────────────┐     ┌─────────────────┐
│   Policyholder   │────<│    Policy     │────<│    Coverage     │
└──────────────────┘     └───────────────┘     └─────────────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │    Claim    │
                         └─────────────┘

┌──────────────────┐     ┌───────────────────┐
│  AssumptionSet   │────<│ AssumptionTable   │
└──────────────────┘     └───────────────────┘

┌──────────────────┐     ┌────────────────┐     ┌─────────────────────┐
│ ModelDefinition  │────<│ CalculationRun │────<│ CalculationResult   │
└──────────────────┘     └────────────────┘     └─────────────────────┘
         ▲                       ▲
         │                       │
┌──────────────────┐     ┌────────────────┐
│    Scenario      │────>│ ScenarioResult │
└──────────────────┘     └────────────────┘

┌──────────────────┐     ┌────────────────────┐
│ ReportTemplate   │────<│ GeneratedReport    │
└──────────────────┘     └────────────────────┘

┌──────────────────┐     ┌────────────────────┐
│  ScheduledJob    │────<│  JobExecution      │
└──────────────────┘     └────────────────────┘
```

## Table Definitions

### Users & Authorization

#### users
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | VARCHAR(255) | Unique email address |
| full_name | VARCHAR(255) | Display name |
| role_id | UUID | FK to roles |
| department | VARCHAR(100) | Department name |
| is_active | BOOLEAN | Account active status |
| last_login | TIMESTAMP | Last login timestamp |
| keycloak_id | VARCHAR(255) | External identity ID |
| ai_preferences | JSONB | User's AI feature settings |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users (self) |
| is_deleted | BOOLEAN | Soft delete flag |

#### roles
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(100) | Role name (unique) |
| description | TEXT | Role description |
| is_system | BOOLEAN | System role (cannot be deleted) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

#### permissions
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| resource | VARCHAR(100) | Resource name (e.g., "policy") |
| action | VARCHAR(50) | Action (create/read/update/delete) |
| description | TEXT | Permission description |

#### role_permissions (junction)
| Column | Type | Description |
|--------|------|-------------|
| role_id | UUID | FK to roles |
| permission_id | UUID | FK to permissions |

### Policy Data

#### policyholders
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| external_id | VARCHAR(100) | External system ID |
| first_name | VARCHAR(100) | First name |
| last_name | VARCHAR(100) | Last name |
| date_of_birth | DATE | Date of birth |
| gender | VARCHAR(20) | Gender |
| smoker_status | VARCHAR(20) | Smoker/Non-smoker |
| occupation_class | VARCHAR(50) | Occupation risk class |
| email | VARCHAR(255) | Email address |
| phone | VARCHAR(50) | Phone number |
| address_line1 | VARCHAR(255) | Address line 1 |
| address_line2 | VARCHAR(255) | Address line 2 |
| city | VARCHAR(100) | City |
| state | VARCHAR(100) | State/Province |
| postal_code | VARCHAR(20) | Postal/ZIP code |
| country | VARCHAR(100) | Country |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users |
| is_deleted | BOOLEAN | Soft delete flag |

#### policies
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| policy_number | VARCHAR(50) | Unique policy number |
| product_type | VARCHAR(50) | life/health/property/casualty |
| product_code | VARCHAR(50) | Product code |
| product_name | VARCHAR(255) | Product display name |
| status | VARCHAR(50) | active/lapsed/surrendered/matured/claimed |
| policyholder_id | UUID | FK to policyholders |
| issue_date | DATE | Policy issue date |
| effective_date | DATE | Coverage effective date |
| maturity_date | DATE | Policy maturity date |
| termination_date | DATE | Early termination date |
| sum_assured | DECIMAL(18,2) | Face amount |
| premium_amount | DECIMAL(18,2) | Premium amount |
| premium_frequency | VARCHAR(20) | annual/semi-annual/quarterly/monthly |
| premium_due_date | DATE | Next premium due date |
| currency | VARCHAR(3) | Currency code (USD, EUR, etc.) |
| branch_code | VARCHAR(50) | Branch/agency code |
| underwriter_id | UUID | FK to users (underwriter) |
| risk_class | VARCHAR(50) | Underwriting risk class |
| policy_data | JSONB | Additional flexible data |
| embedding | VECTOR(1536) | Semantic embedding for search |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users |
| is_deleted | BOOLEAN | Soft delete flag |

**Indexes:**
- `idx_policies_policy_number` UNIQUE on policy_number
- `idx_policies_status` on status
- `idx_policies_product_type_status` on (product_type, status)
- `idx_policies_policyholder_id` on policyholder_id
- `idx_policies_issue_date` on issue_date
- `idx_policies_embedding` HNSW on embedding (vector search)

#### coverages
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| policy_id | UUID | FK to policies |
| coverage_type | VARCHAR(100) | Type of coverage |
| coverage_name | VARCHAR(255) | Coverage display name |
| benefit_amount | DECIMAL(18,2) | Benefit amount |
| premium_amount | DECIMAL(18,2) | Premium for this coverage |
| start_date | DATE | Coverage start date |
| end_date | DATE | Coverage end date |
| is_rider | BOOLEAN | Is this a rider |
| coverage_data | JSONB | Additional coverage details |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

#### claims
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| claim_number | VARCHAR(50) | Unique claim number |
| policy_id | UUID | FK to policies |
| claim_date | DATE | Date claim filed |
| incident_date | DATE | Date of incident |
| claim_type | VARCHAR(100) | Type of claim |
| claim_amount | DECIMAL(18,2) | Claimed amount |
| status | VARCHAR(50) | open/under_review/approved/denied/paid |
| settlement_date | DATE | Date claim settled |
| settlement_amount | DECIMAL(18,2) | Amount paid |
| adjuster_id | UUID | FK to users (adjuster) |
| adjuster_notes | TEXT | Adjuster notes |
| denial_reason | TEXT | Reason if denied |
| anomaly_score | FLOAT | AI anomaly score (0-1) |
| claim_data | JSONB | Additional claim data |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users |
| is_deleted | BOOLEAN | Soft delete flag |

### Actuarial Data

#### assumption_sets
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(255) | Set name |
| version | VARCHAR(50) | Version identifier |
| description | TEXT | Description |
| status | VARCHAR(50) | draft/pending_approval/approved/archived |
| effective_date | DATE | When assumptions become effective |
| expiry_date | DATE | When assumptions expire |
| approved_by | UUID | FK to users (approver) |
| approval_date | TIMESTAMP | Approval timestamp |
| approval_notes | TEXT | Approval notes |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users |
| is_deleted | BOOLEAN | Soft delete flag |

#### assumption_tables
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| assumption_set_id | UUID | FK to assumption_sets |
| table_type | VARCHAR(50) | mortality/lapse/expense/morbidity/discount_rate |
| name | VARCHAR(255) | Table name |
| description | TEXT | Table description |
| data | JSONB | Table data (flexible structure) |
| metadata | JSONB | Table metadata (source, effective dates) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

**Example JSONB data structure for mortality table:**
```json
{
  "type": "select_ultimate",
  "select_period": 25,
  "rates": [
    {"age": 20, "duration": 1, "male": 0.00045, "female": 0.00023},
    {"age": 20, "duration": 2, "male": 0.00048, "female": 0.00025}
  ]
}
```

#### model_definitions
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(255) | Model name |
| description | TEXT | Model description |
| model_type | VARCHAR(50) | reserving/pricing/cashflow/valuation |
| line_of_business | VARCHAR(100) | Line of business |
| configuration | JSONB | Model configuration (calculation graph) |
| version | VARCHAR(50) | Model version |
| status | VARCHAR(50) | draft/active/archived |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users |
| is_deleted | BOOLEAN | Soft delete flag |

#### calculation_runs
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| run_name | VARCHAR(255) | Run name/identifier |
| model_definition_id | UUID | FK to model_definitions |
| assumption_set_id | UUID | FK to assumption_sets |
| status | VARCHAR(50) | queued/running/completed/failed/cancelled |
| started_at | TIMESTAMP | Start timestamp |
| completed_at | TIMESTAMP | Completion timestamp |
| duration_seconds | INTEGER | Run duration |
| triggered_by | UUID | FK to users |
| trigger_type | VARCHAR(50) | manual/scheduled/automated |
| policy_filter | JSONB | Filter criteria for policies |
| parameters | JSONB | Run parameters (valuation date, etc.) |
| policies_count | INTEGER | Number of policies processed |
| error_message | TEXT | Error message if failed |
| result_summary | JSONB | Summary statistics |
| ai_narrative | TEXT | AI-generated summary |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

**Indexes:**
- `idx_calculation_runs_status` on status
- `idx_calculation_runs_model_id` on model_definition_id
- `idx_calculation_runs_started_at` on started_at DESC

#### calculation_results
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| calculation_run_id | UUID | FK to calculation_runs |
| policy_id | UUID | FK to policies |
| projection_month | INTEGER | Projection month (0 = valuation date) |
| result_type | VARCHAR(50) | reserve/cashflow/profit_margin/etc. |
| values | JSONB | Result values |
| anomaly_flag | BOOLEAN | AI-flagged as unusual |
| created_at | TIMESTAMP | Creation timestamp |

**Partitioning:** Partitioned by calculation_run_id (LIST partitioning)

### Reporting

#### report_templates
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(255) | Template name |
| description | TEXT | Template description |
| report_type | VARCHAR(50) | regulatory/internal/adhoc |
| regulatory_standard | VARCHAR(50) | IFRS17/SolvencyII/USGAAP/LDTI |
| template_config | JSONB | Template configuration |
| output_format | VARCHAR(20) | PDF/Excel/CSV |
| is_system_template | BOOLEAN | Built-in template |
| include_ai_narrative | BOOLEAN | Auto-generate AI summary |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users |
| is_deleted | BOOLEAN | Soft delete flag |

#### generated_reports
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| report_template_id | UUID | FK to report_templates |
| name | VARCHAR(255) | Report name |
| reporting_period_start | DATE | Period start |
| reporting_period_end | DATE | Period end |
| status | VARCHAR(50) | generating/completed/failed |
| generated_by | UUID | FK to users |
| generated_at | TIMESTAMP | Generation timestamp |
| file_path | VARCHAR(500) | S3/MinIO path |
| file_size | BIGINT | File size in bytes |
| parameters | JSONB | Generation parameters |
| ai_summary | TEXT | AI-generated summary |
| created_at | TIMESTAMP | Creation timestamp |

### Automation

#### scheduled_jobs
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(255) | Job name |
| description | TEXT | Job description |
| job_type | VARCHAR(50) | calculation/report/import/data_check |
| cron_expression | VARCHAR(100) | Cron schedule |
| config | JSONB | Job configuration |
| is_active | BOOLEAN | Job enabled |
| last_run | TIMESTAMP | Last execution time |
| next_run | TIMESTAMP | Next scheduled run |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users |

#### job_executions
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| scheduled_job_id | UUID | FK to scheduled_jobs |
| started_at | TIMESTAMP | Execution start |
| completed_at | TIMESTAMP | Execution end |
| status | VARCHAR(50) | running/completed/failed |
| result_summary | JSONB | Execution results |
| error_message | TEXT | Error if failed |
| created_at | TIMESTAMP | Creation timestamp |

#### automation_rules
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(255) | Rule name |
| description | TEXT | Rule description |
| trigger_type | VARCHAR(50) | policy_status_change/calculation_complete/etc. |
| trigger_config | JSONB | Trigger conditions |
| action_type | VARCHAR(50) | send_notification/create_task/run_calculation |
| action_config | JSONB | Action configuration |
| is_active | BOOLEAN | Rule enabled |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | FK to users |

### Audit & Compliance

#### audit_log
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| timestamp | TIMESTAMP | Event timestamp |
| user_id | UUID | FK to users (can be null for system) |
| action | VARCHAR(50) | create/update/delete/approve/login/etc. |
| resource_type | VARCHAR(100) | Table/entity name |
| resource_id | UUID | Resource identifier |
| old_values | JSONB | Values before change |
| new_values | JSONB | Values after change |
| ip_address | INET | Client IP address |
| user_agent | TEXT | Client user agent |
| request_id | UUID | Request correlation ID |

**Note:** This table is append-only. No updates or deletes are ever performed.

**Partitioning:** Partitioned by timestamp (monthly range partitions)
