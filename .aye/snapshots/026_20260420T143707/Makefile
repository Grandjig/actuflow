.PHONY: help install dev build test lint clean docker-up docker-down seed migrate

help:
	@echo "ActuFlow Development Commands"
	@echo "=============================="
	@echo "make install    - Install all dependencies"
	@echo "make dev        - Start development servers"
	@echo "make docker-up  - Start all services with Docker"
	@echo "make docker-down- Stop all Docker services"
	@echo "make seed       - Seed the database"
	@echo "make migrate    - Run database migrations"
	@echo "make test       - Run all tests"
	@echo "make lint       - Run linters"
	@echo "make clean      - Clean build artifacts"

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	cd ai_service && pip install -r requirements.txt

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "AI Service: http://localhost:8001"
	make -j3 dev-backend dev-frontend dev-ai

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

dev-ai:
	cd ai_service && uvicorn main:app --reload --port 8001

docker-up:
	docker-compose up -d
	docker-compose logs -f

docker-down:
	docker-compose down

docker-build:
	docker-compose build

migrate:
	cd backend && alembic upgrade head

migrate-create:
	cd backend && alembic revision --autogenerate -m "$(msg)"

seed:
	cd backend && python -m scripts.seed_db

test:
	cd backend && pytest
	cd frontend && npm test

test-backend:
	cd backend && pytest -v

test-frontend:
	cd frontend && npm test

lint:
	cd backend && ruff check .
	cd frontend && npm run lint

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

db-reset:
	docker-compose down -v
	docker-compose up -d db redis
	@echo "Waiting for database..."
	sleep 5
	make migrate
	make seed
