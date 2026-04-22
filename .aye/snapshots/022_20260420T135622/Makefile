# =============================================================================
# ActuFlow Makefile
# =============================================================================

.PHONY: help dev dev-full stop restart logs clean test lint format migrate seed

# Default target
help:
	@echo "ActuFlow Development Commands"
	@echo "=============================="
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start core services (no AI, no Keycloak)"
	@echo "  make dev-full     - Start all services including AI and Keycloak"
	@echo "  make stop         - Stop all services"
	@echo "  make restart      - Restart all services"
	@echo "  make logs         - Show logs (follow mode)"
	@echo "  make clean        - Remove all containers and volumes"
	@echo ""
	@echo "Database:"
	@echo "  make migrate      - Run database migrations"
	@echo "  make migrate-new  - Create new migration (NAME=description)"
	@echo "  make migrate-down - Rollback last migration"
	@echo "  make seed         - Seed database with sample data"
	@echo "  make db-reset     - Reset database (dangerous!)"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-backend - Run backend tests"
	@echo "  make test-frontend- Run frontend tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make typecheck    - Run type checking"
	@echo ""
	@echo "Build:"
	@echo "  make build        - Build all Docker images"
	@echo "  make build-prod   - Build production images"

# =============================================================================
# Development
# =============================================================================

dev:
	@echo "Starting ActuFlow (core services)..."
	docker-compose up -d postgres redis minio elasticsearch
	@echo "Waiting for services to be healthy..."
	@sleep 10
	docker-compose up -d backend calculation-worker celery-beat frontend
	@echo ""
	@echo "ActuFlow is starting up!"
	@echo "  Frontend:  http://localhost:3000"
	@echo "  Backend:   http://localhost:8000"
	@echo "  API Docs:  http://localhost:8000/docs"
	@echo "  MinIO:     http://localhost:9001"

dev-full:
	@echo "Starting ActuFlow (all services including AI)..."
	docker-compose --profile ai --profile auth up -d
	@echo ""
	@echo "ActuFlow is starting up (full mode)!"
	@echo "  Frontend:   http://localhost:3000"
	@echo "  Backend:    http://localhost:8000"
	@echo "  AI Service: http://localhost:8001"
	@echo "  Keycloak:   http://localhost:8080"

stop:
	@echo "Stopping ActuFlow..."
	docker-compose --profile ai --profile auth down

restart: stop dev

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-worker:
	docker-compose logs -f calculation-worker

clean:
	@echo "Removing all containers and volumes..."
	docker-compose --profile ai --profile auth down -v
	docker system prune -f

# =============================================================================
# Database
# =============================================================================

migrate:
	@echo "Running database migrations..."
	docker-compose exec backend alembic upgrade head

migrate-new:
	@echo "Creating new migration: $(NAME)"
	docker-compose exec backend alembic revision --autogenerate -m "$(NAME)"

migrate-down:
	@echo "Rolling back last migration..."
	docker-compose exec backend alembic downgrade -1

migrate-history:
	docker-compose exec backend alembic history

seed:
	@echo "Seeding database with sample data..."
	docker-compose exec backend python -m scripts.seed_db

db-reset:
	@echo "WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	docker-compose exec postgres psql -U actuflow -d actuflow -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	$(MAKE) migrate
	$(MAKE) seed

# =============================================================================
# Testing
# =============================================================================

test: test-backend test-frontend

test-backend:
	@echo "Running backend tests..."
	docker-compose exec backend pytest -v

test-frontend:
	@echo "Running frontend tests..."
	docker-compose exec frontend npm test

test-cov:
	@echo "Running tests with coverage..."
	docker-compose exec backend pytest --cov=app --cov-report=html --cov-report=term

test-watch:
	docker-compose exec backend pytest-watch

# =============================================================================
# Code Quality
# =============================================================================

lint: lint-backend lint-frontend

lint-backend:
	@echo "Linting backend..."
	docker-compose exec backend ruff check app/
	docker-compose exec backend mypy app/

lint-frontend:
	@echo "Linting frontend..."
	docker-compose exec frontend npm run lint

format: format-backend format-frontend

format-backend:
	@echo "Formatting backend..."
	docker-compose exec backend ruff format app/
	docker-compose exec backend ruff check --fix app/

format-frontend:
	@echo "Formatting frontend..."
	docker-compose exec frontend npm run format

typecheck:
	@echo "Running type checks..."
	docker-compose exec backend mypy app/
	docker-compose exec frontend npm run typecheck

# =============================================================================
# Build
# =============================================================================

build:
	@echo "Building Docker images..."
	docker-compose build

build-prod:
	@echo "Building production Docker images..."
	docker-compose -f docker-compose.prod.yml build

# =============================================================================
# Utilities
# =============================================================================

shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend sh

shell-db:
	docker-compose exec postgres psql -U actuflow -d actuflow

shell-redis:
	docker-compose exec redis redis-cli

# Create superuser
create-superuser:
	docker-compose exec backend python -m scripts.create_superuser

# Load standard mortality tables
load-mortality-tables:
	docker-compose exec backend python -m scripts.load_mortality_tables

# Generate embeddings for existing data
generate-embeddings:
	docker-compose exec backend python -m scripts.generate_embeddings

# Backup database
backup:
	@echo "Creating database backup..."
	@mkdir -p backups
	docker-compose exec postgres pg_dump -U actuflow actuflow > backups/actuflow_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup created in backups/"

# Restore database
restore:
	@echo "Restoring database from $(FILE)..."
	docker-compose exec -T postgres psql -U actuflow actuflow < $(FILE)
