# ActuFlow Makefile
# Common commands for development

.PHONY: help dev down build test lint migrate seed clean

help:
	@echo "ActuFlow Development Commands:"
	@echo "  make dev          - Start all services in development mode"
	@echo "  make down         - Stop all services"
	@echo "  make build        - Build all Docker images"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linters"
	@echo "  make migrate      - Run database migrations"
	@echo "  make seed         - Seed database with sample data"
	@echo "  make clean        - Clean up containers and volumes"

dev:
	docker-compose up -d
	@echo "Services starting... Frontend: http://localhost:3000, API: http://localhost:8000/docs"

down:
	docker-compose down

build:
	docker-compose build

test:
	@echo "Running backend tests..."
	docker-compose exec backend pytest
	@echo "Running frontend tests..."
	docker-compose exec frontend npm test

test-api:
	docker-compose exec backend pytest tests/

test-fe:
	docker-compose exec frontend npm test

lint:
	@echo "Linting backend..."
	docker-compose exec backend ruff check app/
	@echo "Linting frontend..."
	docker-compose exec frontend npm run lint

format:
	docker-compose exec backend ruff format app/

migrate:
	docker-compose exec backend alembic upgrade head

migrate-new:
	@read -p "Migration name: " NAME; \
	docker-compose exec backend alembic revision --autogenerate -m "$$NAME"

seed:
	docker-compose exec backend python scripts/seed_db.py

db-shell:
	docker-compose exec postgres psql -U actuflow -d actuflow

db-reset:
	docker-compose exec postgres psql -U actuflow -d actuflow -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	$(MAKE) migrate
	$(MAKE) seed

shell-api:
	docker-compose exec backend bash

shell-fe:
	docker-compose exec frontend sh

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f backend

logs-fe:
	docker-compose logs -f frontend

logs-calc:
	docker-compose logs -f calculation-engine

clean:
	docker-compose down -v --remove-orphans
	docker system prune -f
