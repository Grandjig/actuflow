# ActuFlow

> Modern Insurance Data Management & Actuarial Platform

ActuFlow is a web-based platform that lets insurance companies manage policy data, run actuarial calculations, generate regulatory reports, and model scenarios — all through a clean, intuitive interface.

## Features

- **Policy Data Management**: Import, manage, and analyze insurance policies
- **Actuarial Calculation Engine**: Run reserving, pricing, and cash flow projections
- **Assumptions Manager**: Version-controlled assumption sets with approval workflows
- **Scenario & Stress Testing**: What-if analysis with comparative dashboards
- **Regulatory Reporting**: IFRS 17, Solvency II, US GAAP LDTI compliance
- **AI-Powered Intelligence**: Smart data import, natural language queries, anomaly detection
- **Automation**: Scheduled jobs, triggered workflows, batch operations

## Tech Stack

- **Frontend**: React 18 + TypeScript + Ant Design + TanStack Table
- **Backend**: Python 3.12 + FastAPI + SQLAlchemy
- **Calculation Engine**: Celery + NumPy/SciPy/Pandas
- **AI Service**: OpenAI API + sentence-transformers + scikit-learn
- **Database**: PostgreSQL 16 + pgvector + Redis
- **Infrastructure**: Docker + Kubernetes + Nginx

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Make (optional, for convenience commands)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-org/actuflow.git
cd actuflow

# Copy environment template
cp .env.example .env

# Start all services
make dev

# Or without Make:
docker-compose up -d

# Run database migrations
make migrate

# Seed sample data (optional)
make seed
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Keycloak Admin**: http://localhost:8080

### Default Credentials

- **Admin User**: admin@actuflow.com / admin123
- **Keycloak Admin**: admin / admin

## Project Structure

```
actuflow/
├── backend/           # FastAPI backend service
├── calculation_engine/ # Celery workers for actuarial calculations
├── ai_service/        # AI/ML microservice (optional)
├── frontend/          # React frontend application
├── infrastructure/    # Kubernetes & Terraform configs
├── docs/              # Documentation
├── scripts/           # Utility scripts
└── docker-compose.yml # Local development setup
```

## Documentation

- [Architecture Overview](docs/architecture.md)
- [API Contracts](docs/api-contracts.md)
- [Data Model](docs/data-model.md)
- [Calculation Engine](docs/calculation-engine.md)
- [AI Features](docs/ai-features.md)
- [Deployment Guide](docs/deployment-guide.md)

## Development

### Running Tests

```bash
# Backend tests
make test-backend

# Frontend tests
make test-frontend

# All tests
make test
```

### Code Quality

```bash
# Lint all code
make lint

# Format code
make format
```

## Environment Variables

See [.env.example](.env.example) for all configuration options.

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `OPENAI_API_KEY`: OpenAI API key (optional, for AI features)
- `AI_ENABLED`: Enable/disable AI features

## License

Proprietary - All rights reserved.

## Support

For support, contact support@actuflow.com
