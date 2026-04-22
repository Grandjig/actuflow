# ActuFlow Automation Guide

## Overview

ActuFlow provides two types of automation:

1. **Scheduled Jobs**: Time-based execution (cron-style)
2. **Automation Rules**: Event-triggered actions

## Scheduled Jobs

### Job Types

| Type | Description |
|------|-------------|
| `calculation` | Run actuarial calculations |
| `report` | Generate reports |
| `import` | Import data from external sources |
| `data_check` | Run data quality checks |
| `cleanup` | Archive old data |

### Cron Expression Format

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday = 0)
│ │ │ │ │
* * * * *
```

**Examples:**
- `0 2 * * *` - Daily at 2:00 AM
- `0 8 1 * *` - First day of each month at 8:00 AM
- `0 6 * * 1` - Every Monday at 6:00 AM
- `0 0 1 1,4,7,10 *` - Quarterly (Jan, Apr, Jul, Oct 1st at midnight)

### Creating a Scheduled Job

**Via API:**
```bash
POST /api/v1/scheduled-jobs
{
  "name": "Monthly Reserve Calculation",
  "description": "Run reserve calculation on first business day",
  "job_type": "calculation",
  "cron_expression": "0 2 1 * *",
  "is_active": true,
  "config": {
    "model_definition_id": "uuid-of-model",
    "assumption_set_id": "uuid-of-assumptions",
    "policy_filter": {
      "status": "active",
      "product_type": "life"
    },
    "parameters": {
      "valuation_date": "{{LAST_DAY_OF_PREV_MONTH}}",
      "reporting_basis": "IFRS17"
    }
  }
}
```

### Dynamic Parameters

Scheduled jobs support dynamic date parameters:

| Placeholder | Description |
|-------------|-------------|
| `{{TODAY}}` | Current date |
| `{{YESTERDAY}}` | Previous day |
| `{{FIRST_DAY_OF_MONTH}}` | First day of current month |
| `{{LAST_DAY_OF_MONTH}}` | Last day of current month |
| `{{LAST_DAY_OF_PREV_MONTH}}` | Last day of previous month |
| `{{FIRST_DAY_OF_QUARTER}}` | First day of current quarter |
| `{{LAST_DAY_OF_PREV_QUARTER}}` | Last day of previous quarter |

### Job Configuration Examples

**Calculation Job:**
```json
{
  "job_type": "calculation",
  "config": {
    "model_definition_id": "uuid",
    "assumption_set_id": "uuid",
    "policy_filter": {"status": "active"},
    "parameters": {
      "valuation_date": "{{LAST_DAY_OF_PREV_MONTH}}"
    },
    "notify_on_complete": ["actuary@company.com"],
    "auto_generate_narrative": true
  }
}
```

**Report Job:**
```json
{
  "job_type": "report",
  "config": {
    "report_template_id": "uuid",
    "parameters": {
      "period_start": "{{FIRST_DAY_OF_PREV_QUARTER}}",
      "period_end": "{{LAST_DAY_OF_PREV_QUARTER}}"
    },
    "output_format": "PDF",
    "email_to": ["cfo@company.com", "board@company.com"]
  }
}
```

**Data Import Job:**
```json
{
  "job_type": "import",
  "config": {
    "source_type": "sftp",
    "source_path": "/exports/policies_{{TODAY}}.csv",
    "import_type": "policy",
    "column_mapping_id": "uuid",
    "on_error": "skip_row",
    "notify_on_errors": ["data-team@company.com"]
  }
}
```

## Automation Rules

### Trigger Types

| Trigger | Description |
|---------|-------------|
| `policy_status_change` | Policy status changes |
| `calculation_complete` | Calculation run completes |
| `assumption_approved` | Assumption set approved |
| `threshold_breach` | Metric exceeds threshold |
| `claim_filed` | New claim submitted |
| `task_overdue` | Task passes due date |

### Action Types

| Action | Description |
|--------|-------------|
| `send_notification` | Send in-app notification |
| `send_email` | Send email |
| `create_task` | Create workflow task |
| `run_calculation` | Trigger calculation run |
| `call_webhook` | Call external webhook |
| `update_status` | Update resource status |

### Creating Automation Rules

**Example: Notify on Calculation Anomalies**
```json
{
  "name": "Alert on High Anomaly Rate",
  "trigger_type": "calculation_complete",
  "trigger_config": {
    "conditions": [
      {
        "field": "anomaly_rate",
        "operator": ">",
        "value": 0.05
      }
    ]
  },
  "action_type": "send_notification",
  "action_config": {
    "recipients": ["Chief Actuary"],
    "title": "High Anomaly Rate Detected",
    "message": "Calculation {{run_name}} has {{anomaly_rate}}% anomalous results",
    "priority": "high"
  }
}
```

**Example: Auto-create Task on Assumption Rejection**
```json
{
  "name": "Revision Task on Rejection",
  "trigger_type": "assumption_rejected",
  "trigger_config": {},
  "action_type": "create_task",
  "action_config": {
    "task_type": "revision",
    "title": "Revise Rejected Assumptions: {{assumption_set_name}}",
    "description": "Rejection reason: {{rejection_notes}}",
    "assign_to": "{{created_by}}",
    "due_days": 5,
    "priority": "high"
  }
}
```

**Example: Auto-lapse Policies**
```json
{
  "name": "Auto-lapse Past Grace Period",
  "trigger_type": "scheduled",
  "trigger_config": {
    "cron": "0 1 * * *",
    "query": {
      "status": "active",
      "premium_due_date": {"$lt": "{{TODAY - 60 days}}"}
    }
  },
  "action_type": "update_status",
  "action_config": {
    "new_status": "lapsed",
    "reason": "Auto-lapsed after 60-day grace period"
  }
}
```

### Condition Operators

| Operator | Description |
|----------|-------------|
| `=` | Equals |
| `!=` | Not equals |
| `>` | Greater than |
| `>=` | Greater than or equal |
| `<` | Less than |
| `<=` | Less than or equal |
| `in` | In list |
| `not_in` | Not in list |
| `contains` | String contains |
| `starts_with` | String starts with |
| `is_null` | Value is null |
| `is_not_null` | Value is not null |

### Template Variables

Action configs support template variables:

- `{{field_name}}` - Field from trigger event
- `{{TODAY}}`, `{{NOW}}` - Current date/time
- `{{user.name}}` - Current user info
- `{{resource.field}}` - Resource field values

## Monitoring

### Viewing Job Execution History

```bash
GET /api/v1/scheduled-jobs/{id}/executions
```

Response:
```json
{
  "items": [
    {
      "id": "uuid",
      "started_at": "2024-01-01T02:00:00Z",
      "completed_at": "2024-01-01T02:15:23Z",
      "status": "completed",
      "result_summary": {
        "policies_processed": 15234,
        "calculation_run_id": "uuid"
      }
    }
  ]
}
```

### Alerts

Set up alerts for automation failures:

```json
{
  "name": "Alert on Job Failure",
  "trigger_type": "job_execution_failed",
  "action_type": "send_email",
  "action_config": {
    "to": ["ops@company.com"],
    "subject": "Scheduled Job Failed: {{job_name}}",
    "body": "Error: {{error_message}}"
  }
}
```

## Best Practices

1. **Stagger job schedules** - Don't run all jobs at the same time
2. **Use descriptive names** - Make it clear what each job does
3. **Set up failure notifications** - Know when things break
4. **Test with dry runs** - Test automation rules before enabling
5. **Review execution logs** - Regularly check for issues
6. **Document dependencies** - Note if jobs depend on each other
