# ActuFlow Developer Onboarding Guide

## Welcome!

This guide will help you get up and running with ActuFlow development.

## Prerequisites

**Required:**
- Docker & Docker Compose (v2.0+)
- Git
- Code editor (VS Code recommended)

**Optional but helpful:**
- Python 3.12+ (for local backend development)
- Node.js 20+ (for local frontend development)
- PostgreSQL client (psql or pgAdmin)
- Redis client (redis-cli or RedisInsight)

---

## Quick Start (15 minutes)

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/your-org/actuflow.git
cd actuflow

# Copy environment template
cp .env.example .env

# Start all services
make dev
# Or: docker-compose up -d
```

### 2. Verify Services

Wait 2-3 minutes for services to start, then check:

| Service | URL | Expected |
|---------|-----|----------|
| Frontend | http://localhost:3000 | Login page |
| Backend API | http://localhost:8000/docs | Swagger UI |
| Keycloak | http://localhost:8080 | Admin console |
| MinIO | http://localhost:9001 | Console login |

### 3. Initialize Database

```bash
# Run migrations
make migrate

# Seed sample data
make seed
```

### 4. Login

Open http://localhost:3000 and login:
- Email: `admin@actuflow.com`
- Password: `admin123`

🎉 **You're up and running!**

---

## Project Structure

```
actuflow/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── repositories/ # Data access
│   ├── migrations/       # Alembic migrations
│   └── tests/
│
├── calculation_engine/   # Celery workers
│   ├── engine/           # Actuarial calculations
│   ├── tasks/            # Celery tasks
│   └── scheduler/        # Job scheduling
│
├── ai_service/           # AI/ML service (optional)
│   ├── api/              # AI endpoints
│   └── services/         # NLP, embeddings, etc.
│
├── frontend/             # React application
│   └── src/
│       ├── api/          # API client
│       ├── components/   # React components
│       ├── hooks/        # Custom hooks
│       ├── pages/        # Page components
│       └── stores/       # Zustand stores
│
├── infrastructure/       # Deployment configs
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

---

## Development Workflows

### Backend Development

**Adding a new API endpoint:**

1. Define schema in `backend/app/schemas/`
2. Add model if new entity in `backend/app/models/`
3. Create repository in `backend/app/repositories/`
4. Implement service in `backend/app/services/`
5. Add endpoint in `backend/app/api/`
6. Write tests in `backend/tests/`

**Example: Adding a new field to Policy**

```python
# 1. Update model (models/policy.py)
class Policy(Base):
    # ... existing fields
    new_field = Column(String(100), nullable=True)

# 2. Create migration
make migrate-new NAME=add_policy_new_field

# 3. Update schema (schemas/policy.py)
class PolicyResponse(BaseModel):
    # ... existing fields
    new_field: Optional[str] = None

# 4. Run migration
make migrate
```

### Frontend Development

**Adding a new page:**

1. Create page component in `frontend/src/pages/`
2. Add route in `frontend/src/routes.tsx`
3. Add API functions in `frontend/src/api/`
4. Create hooks in `frontend/src/hooks/`
5. Update sidebar navigation if needed

**Example: Adding a new detail page**

```tsx
// 1. Create page (pages/widgets/WidgetDetail.tsx)
export default function WidgetDetail() {
  const { id } = useParams();
  const { data, isLoading } = useWidget(id);
  
  if (isLoading) return <LoadingSpinner />;
  
  return (
    <PageHeader title={data.name}>
      {/* Page content */}
    </PageHeader>
  );
}

// 2. Add route (routes.tsx)
{
  path: 'widgets/:id',
  element: <WidgetDetail />
}

// 3. Add API function (api/widgets.ts)
export const getWidget = (id: string) => 
  client.get(`/widgets/${id}`).then(r => r.data);

// 4. Create hook (hooks/useWidgets.ts)
export function useWidget(id: string) {
  return useQuery(['widget', id], () => getWidget(id));
}
```

---

## Running Tests

```bash
# All tests
make test

# Backend only
make test-api

# Frontend only
make test-fe

# With coverage
make coverage
```

### Writing Tests

**Backend test example:**

```python
# backend/tests/api/test_policies.py
class TestPolicyEndpoints:
    def test_create_policy(self, client, auth_headers):
        response = client.post(
            "/api/v1/policies",
            json={
                "policy_number": "TEST-001",
                "product_type": "term_life",
                # ...
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["policy_number"] == "TEST-001"
```

**Frontend test example:**

```tsx
// frontend/src/pages/policies/__tests__/PolicyList.test.tsx
describe('PolicyList', () => {
  it('renders policy table', async () => {
    render(<PolicyList />);
    
    await waitFor(() => {
      expect(screen.getByText('POL-2024-001')).toBeInTheDocument();
    });
  });
});
```

---

## Common Tasks

### Database Operations

```bash
# Open database shell
make db-shell

# Create new migration
make migrate-new NAME=description_of_change

# Apply migrations
make migrate

# Reset database (WARNING: deletes all data)
make db-reset
```

### Debugging

**Backend:**
```bash
# View backend logs
make logs-api

# Open shell in container
make shell-api

# Run with debugger
# Add in code: import pdb; pdb.set_trace()
```

**Frontend:**
- React DevTools browser extension
- React Query DevTools (built in)
- Console logging

### Code Quality

```bash
# Lint all code
make lint

# Format code
make format

# Type check
make typecheck
```

---

## Key Concepts

### Dependency Injection (Backend)

FastAPI uses dependency injection:

```python
@router.get("/policies")
async def list_policies(
    db: Session = Depends(get_db),           # Database session
    current_user: User = Depends(get_current_user),  # Authenticated user
    pagination: PaginationParams = Depends()  # Query params
):
    # Dependencies are automatically resolved
```

### React Query (Frontend)

Server state is managed with React Query:

```tsx
// Fetching data
const { data, isLoading, error } = useQuery(
  ['policies', filters],  // Query key
  () => fetchPolicies(filters)  // Fetch function
);

// Mutations
const mutation = useMutation(createPolicy, {
  onSuccess: () => {
    queryClient.invalidateQueries(['policies']);
  }
});
```

### Celery Tasks (Calculation Engine)

Long-running jobs use Celery:

```python
# Defining a task
@celery_app.task
def run_calculation(run_id: str):
    # Long running work...
    pass

# Calling a task (async)
run_calculation.delay(run_id)

# Or with options
run_calculation.apply_async(
    args=[run_id],
    countdown=60  # Delay 60 seconds
)
```

---

## Troubleshooting

### Services won't start

```bash
# Check container status
docker-compose ps

# View logs for specific service
docker-compose logs backend

# Restart services
make down && make dev
```

### Database connection errors

```bash
# Check if postgres is running
docker-compose ps postgres

# Check database connectivity
docker-compose exec postgres pg_isready

# Reset database if corrupted
make db-reset
```

### Frontend not loading

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### Migrations failing

```bash
# Check current state
docker-compose exec backend alembic current

# View history
docker-compose exec backend alembic history

# Stamp to specific revision if needed
docker-compose exec backend alembic stamp <revision>
```

---

## Getting Help

1. Check existing documentation in `/docs`
2. Search existing issues on GitHub
3. Ask in #actuflow-dev Slack channel
4. Create a new issue with detailed description

## Contributing

1. Create feature branch from `develop`
2. Make changes with tests
3. Run `make lint` and `make test`
4. Create PR with description
5. Get review and approval
6. Merge to `develop`

Welcome to the team! 🚀
