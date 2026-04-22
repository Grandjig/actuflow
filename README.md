# ActuFlow

**AI-Powered Actuarial Data Management & Analysis Platform**

ActuFlow is a comprehensive platform for managing actuarial workflows, including policy administration, assumption management, actuarial calculations, and AI-assisted analysis.

## Features

- **Policy Management**: Full CRUD for policies, policyholders, and claims
- **Assumption Management**: Version-controlled assumption sets with approval workflows
- **Actuarial Calculations**: Run and monitor reserve/cash flow calculations
- **Scenario Analysis**: What-if analysis with assumption adjustments
- **AI-Powered Features**:
  - Natural language queries ("Show me all lapsed policies from Q1")
  - Smart data import with column mapping suggestions
  - Anomaly detection in claims and calculations
  - AI-generated executive summaries
  - Document extraction
- **Experience Studies**: Actual vs Expected analysis
- **Reporting**: Configurable reports with AI narratives
- **Automation**: Scheduled jobs and trigger-based rules

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/actuflow.git
cd actuflow

# Start all services
docker-compose up -d

# Seed the database
make seed

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Default Credentials

- **Admin**: admin@actuflow.com / admin123
- **Actuary**: actuary@actuflow.com / actuary123
- **Viewer**: viewer@actuflow.com / viewer123

### Local Development

```bash
# Install dependencies
make install

# Start PostgreSQL and Redis (using Docker)
docker-compose up -d db redis

# Run migrations
make migrate

# Seed database
make seed

# Start development servers
make dev
```

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  PostgreSQL │
│   (React)   │     │  (FastAPI)  │     │             │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
              ┌─────▼─────┐ ┌─────▼─────┐
              │   Redis   │ │ AI Service│
              │ (Cache)   │ │  (NLP)    │
              └───────────┘ └───────────┘
```

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Redis
- Celery
- Alembic

### Frontend
- React 18
- TypeScript
- Ant Design 5
- React Query
- Zustand
- Recharts

### AI Service
- Python
- FastAPI
- OpenAI / Azure OpenAI / Local LLM
- scikit-learn (anomaly detection)

## Project Structure

```
actuflow/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # Application entry
│   ├── migrations/       # Alembic migrations
│   └── scripts/          # Utility scripts
├── frontend/             # React frontend
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   ├── pages/        # Page components
│   │   ├── stores/       # Zustand stores
│   │   ├── types/        # TypeScript types
│   │   └── utils/        # Utilities
├── ai_service/           # AI microservice
│   ├── api/              # API routes
│   ├── models/           # ML models
│   └── services/         # AI services
├── docker-compose.yml
├── Makefile
└── README.md
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## License

Proprietary - All rights reserved
