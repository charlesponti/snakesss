# Python project and Docker development shortcuts

# Python-related commands
.PHONY: install test lint format

install:
	pip install -r requirements.txt

test:
	pytest

lint:
	ruff check

format:
	ruff format


# Docker-related commands
.PHONY: docker-build docker-run docker-stop docker-clean

docker-build:
	docker build -t snakesss .

docker-run:
	docker run -d --name snakesss_fastapi snakesss

docker-stop:
	docker stop snakesss_fastapi

docker-clean:
	docker rm snakesss_fastapi


# Development shortcuts
.PHONY: dev clean

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Helpful shortcuts
.PHONY: help

help:
	@echo "Available commands:"
	@echo "  install      - Install project dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linter"
	@echo "  format       - Format code"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"
	@echo "  docker-stop  - Stop Docker container"
	@echo "  docker-clean - Remove Docker container"
	@echo "  dev          - Run development server"
	@echo "  setup        - Set up database and create superuser"
	@echo "  clean        - Remove compiled Python files"
	@echo "  help         - Show this help message"
