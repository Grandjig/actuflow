# ActuFlow User Roles & Permissions

## Overview

ActuFlow uses Role-Based Access Control (RBAC) with fine-grained permissions. Each user is assigned one role, and roles have multiple permissions.

## Permission Structure

Permissions follow the pattern: `resource:action`

**Resources:**
- `policy` - Policy data
- `policyholder` - Policyholder data
- `claim` - Claims data
- `assumption` - Assumption sets and tables
- `model` - Model definitions
- `calculation` - Calculation runs and results
- `scenario` - Scenarios and stress tests
- `report` - Report templates and generated reports
- `dashboard` - Dashboard configurations
- `import` - Data imports
- `task` - Workflow tasks
- `user` - User management
- `role` - Role management
- `automation` - Scheduled jobs and rules
- `audit` - Audit logs
- `ai` - AI features

**Actions:**
- `create` - Create new records
- `read` - View records
- `update` - Modify records
- `delete` - Delete records
- `approve` - Approve workflows (assumptions, etc.)
- `export` - Export data
- `admin` - Administrative actions

## Default Roles

### Administrator

**Description:** Full system access, manages users and configuration.

**Permissions:** All permissions on all resources.

**Typical Users:** IT administrators, system owners.

---

### Chief Actuary

**Description:** Senior actuarial authority with approval rights.

**Permissions:**
```
policy:read, policy:export
policyholder:read
claim:read, claim:export
assumption:create, assumption:read, assumption:update, assumption:approve
model:create, model:read, model:update, model:approve
calculation:create, calculation:read, calculation:export
scenario:create, scenario:read, scenario:update
report:create, report:read, report:approve, report:export
dashboard:create, dashboard:read, dashboard:update
import:read
task:create, task:read, task:update
automation:create, automation:read, automation:update
audit:read
ai:read, ai:use
```

**Cannot:**
- Manage users and roles
- Delete policies or assumptions
- Modify automation rules

---

### Senior Actuary

**Description:** Experienced actuary who can create and approve assumptions.

**Permissions:**
```
policy:read, policy:export
policyholder:read
claim:read
assumption:create, assumption:read, assumption:update, assumption:approve
model:read
calculation:create, calculation:read
scenario:create, scenario:read, scenario:update
report:create, report:read
dashboard:create, dashboard:read, dashboard:update
task:create, task:read, task:update
ai:read, ai:use
```

---

### Actuary

**Description:** Standard actuarial team member.

**Permissions:**
```
policy:read
policyholder:read
claim:read
assumption:create, assumption:read, assumption:update
model:read
calculation:create, calculation:read
scenario:create, scenario:read
report:create, report:read
dashboard:create, dashboard:read, dashboard:update
task:read, task:update
ai:read, ai:use
```

**Cannot:**
- Approve assumptions
- Modify models
- Export sensitive data

---

### Data Analyst

**Description:** Analyzes data, creates reports and dashboards.

**Permissions:**
```
policy:read, policy:export
policyholder:read
claim:read, claim:export
assumption:read
model:read
calculation:read
scenario:read
report:create, report:read, report:export
dashboard:create, dashboard:read, dashboard:update
import:read
task:read
ai:read, ai:use
```

---

### Data Entry Clerk

**Description:** Enters and maintains policy data.

**Permissions:**
```
policy:create, policy:read, policy:update
policyholder:create, policyholder:read, policyholder:update
claim:create, claim:read, claim:update
import:create, import:read
task:read
```

**Cannot:**
- View calculations or assumptions
- Create or view reports
- Use AI features
- Export data

---

### Claims Adjuster

**Description:** Processes insurance claims.

**Permissions:**
```
policy:read
policyholder:read
claim:create, claim:read, claim:update
task:read, task:update
ai:read (document extraction only)
```

---

### Executive / Viewer

**Description:** Read-only access to dashboards and reports.

**Permissions:**
```
policy:read
calculation:read
scenario:read
report:read
dashboard:read
```

---

### Auditor

**Description:** Read-only access to all data for audit purposes.

**Permissions:**
```
policy:read
policyholder:read
claim:read
assumption:read
model:read
calculation:read
scenario:read
report:read
dashboard:read
import:read
task:read
automation:read
audit:read
```

**Special:** Can view all records regardless of ownership.

---

## Custom Roles

Administrators can create custom roles:

```json
{
  "name": "Risk Analyst",
  "description": "Focused on scenario analysis and stress testing",
  "permissions": [
    "policy:read",
    "assumption:read",
    "calculation:read",
    "scenario:create",
    "scenario:read",
    "scenario:update",
    "scenario:delete",
    "report:read",
    "dashboard:create",
    "dashboard:read"
  ]
}
```

---

## Permission Inheritance

No inheritance by default. Each permission must be explicitly granted.

---

## Row-Level Security

Some resources support row-level access:

**Dashboards:**
- Users can only edit their own dashboards
- Shared dashboards are read-only for others

**Tasks:**
- Users see tasks assigned to them
- Managers see tasks of their team
- Admins see all tasks

**Imports:**
- Users see imports they created
- Admins see all imports

---

## API Permission Checks

```python
# Example permission check in endpoint
@router.get("/calculations/{id}")
async def get_calculation(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check permission
    if not current_user.has_permission("calculation:read"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    calculation = calculation_service.get(db, id)
    if not calculation:
        raise HTTPException(status_code=404)
    
    return calculation
```

---

## UI Permission Handling

Frontend hides/disables UI elements based on permissions:

```typescript
// useAuth hook provides permission checking
const { hasPermission } = useAuth();

// Conditionally render based on permission
{hasPermission('assumption:approve') && (
  <Button onClick={handleApprove}>Approve</Button>
)}

// Disable based on permission
<Button 
  disabled={!hasPermission('calculation:create')}
  onClick={handleRunCalculation}
>
  Run Calculation
</Button>
```
