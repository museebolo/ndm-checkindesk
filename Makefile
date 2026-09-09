#-----------------------------------------------------------------------------------------------------------------------
# Makefile for NdM CheckInDesk
#-----------------------------------------------------------------------------------------------------------------------

prefix    ?= canelrom1
name      ?= ndm-checkindesk
tag       ?= $(shell date +%Y%m%d.%H%M%S)

VENV      ?= build
PY        := $(VENV)/bin/python
PIP       := $(VENV)/bin/pip
DATA_PATH ?= /tmp/state-test.json

APP       ?= app.main:app
PORT      ?= 8080

YEAR      := $(shell date +%Y)

.PHONY: help \
        py-venv py-deps-install py-deps-dev py-deps-outdated py-deps-audit py-deps-check \
        py-test py-test-unit py-test-api py-lint py-format py-check py-ci py-run py-clean-venv \
        build run rm up down

.DEFAULT_GOAL := help

#-----------------------------------------------------------------------------------------------------------------------
# Help
#-----------------------------------------------------------------------------------------------------------------------

help: ## Show this help
	@echo "NdM CheckInDesk"
	@echo
	@echo "Usage:"
	@echo "  make <target> [VARIABLE=value ...]"
	@echo
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo
	@echo "Variables:"
	@echo "  prefix=$(prefix)"
	@echo "  name=$(name)"
	@echo "  tag=$(tag)"
	@echo "  VENV=$(VENV)"
	@echo "  DATA_PATH=$(DATA_PATH)"
	@echo "  APP=$(APP)"
	@echo "  PORT=$(PORT)"

#-----------------------------------------------------------------------------------------------------------------------
# Docker
#-----------------------------------------------------------------------------------------------------------------------

build: Dockerfile ## Build the Docker image
	docker build --build-arg YEAR=$(YEAR) -t $(prefix)/$(name):$(tag) .
	docker tag $(prefix)/$(name):$(tag) $(prefix)/$(name):latest

run: ## Run the Docker container
	docker run -d -p 80:8080 --name $(name) $(prefix)/$(name):latest

rm: ## Stop and remove the Docker container
	docker stop $(name)
	docker rm $(name)

up: ## Start the application with Docker Compose
	docker compose up -d

down: ## Stop the application with Docker Compose
	docker compose down

#-----------------------------------------------------------------------------------------------------------------------
# Python (without Docker)
#-----------------------------------------------------------------------------------------------------------------------

py-venv: ## Create the Python virtual environment
	@test -d "$(VENV)" || python3 -m venv "$(VENV)"
	@$(PY) -m pip install -U pip setuptools wheel >/dev/null

py-deps-install: py-venv ## Install Python dependencies
	@$(PIP) install -e .

py-deps-dev: py-deps-install ## Install development and test dependencies
	@$(PIP) install -e ".[dev]"

py-deps-outdated: py-deps-install ## List outdated Python packages
	@echo "-> Outdated packages (info only) <-"
	@$(PIP) list --outdated || true

py-deps-audit: py-deps-install ## Audit Python dependencies for vulnerabilities
	@$(PIP) install -q pip-audit
	@echo "-> Security audit (fails on findings) <-"
	@$(VENV)/bin/pip-audit

py-deps-check: py-deps-outdated py-deps-audit ## Check Python dependencies
	@echo "✅ dependency check complete."

#-----------------------------------------------------------------------------------------------------------------------
# Quality
#-----------------------------------------------------------------------------------------------------------------------

py-lint: py-deps-dev ## Run Python linting
	@$(PY) -m ruff check .

py-format: py-deps-dev ## Format Python sources
	@$(PY) -m ruff format .
	@$(PY) -m black .

#-----------------------------------------------------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------------------------------------------------

py-test: py-test-unit py-test-api ## Run all Python tests

py-test-unit: py-deps-dev ## Run unit tests
	@$(PY) -m pytest -q tests/test_state.py

py-test-api: py-deps-dev ## Run API tests
	@DATA_PATH="$(DATA_PATH)" $(PY) -m pytest -q tests/test_api.py

#-----------------------------------------------------------------------------------------------------------------------
# Meta
#-----------------------------------------------------------------------------------------------------------------------

py-check: py-format py-lint py-test py-deps-check ## Run all local checks
	@echo "✅ all checks passed."

py-ci: py-lint py-test py-deps-audit ## Run CI checks
	@echo "✅ CI target ok."

py-run: py-deps-install ## Run the application locally with Uvicorn
	@DATA_PATH="$(DATA_PATH)" $(VENV)/bin/uvicorn $(APP) --reload --port $(PORT)

py-clean-venv: ## Remove the Python virtual environment
	rm -rf "$(VENV)"

# vim: ft=make
