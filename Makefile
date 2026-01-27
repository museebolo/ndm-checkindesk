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

APP       ?= main:app
PORT      ?= 8080

YEAR      := $(shell date +%Y)

.PHONY: py-venv py-deps-install py-deps-outdated py-deps-audit py-deps-check \
        py-test py-test-unit py-test-api py-lint py-format py-check py-ci py-run py-clean-venv \
        build run rm up down

all: build

# --- Docker ---

build: Dockerfile
	docker build --build-arg YEAR=$(YEAR) -t $(prefix)/$(name):$(tag) . 
	docker tag $(prefix)/$(name):$(tag) $(prefix)/$(name):latest 

run:
	docker run -d -p 80:8080 --name $(name) $(prefix)/$(name):latest

rm:
	docker stop $(name)
	docker rm $(name)

up:
	docker-compose up -d

down:
	docker-compose down

# --- Python (sans Docker) ---

# create a python virtual env 
py-venv:
	@test -d "$(VENV)" || python3 -m venv "$(VENV)"
	@$(PY) -m pip install -U pip setuptools wheel >/dev/null

# install requirements.txt
py-deps-install: py-venv
	@$(PIP) install -e .

# for development & testing
py-deps-dev: py-deps-install
	@$(PIP) install -e ".[dev]"

# check for outdated packages
py-deps-outdated: py-deps-install
	@echo "-> Outdated packages (info only) <-"
	@$(PIP) list --outdated || true

# audit packages for vulnerable packages
py-deps-audit: py-deps-install
	@$(PIP) install -q pip-audit
	@echo "-> Security audit (fails on findings) <-"
	@$(VENV)/bin/pip-audit

# do all checks
py-deps-check: py-deps-outdated py-deps-audit
	@echo "✅ dependency check complete."

# --- quality --- 
py-lint: py-deps-dev
	@$(PY) -m ruff check .

py-format: py-deps-dev
	@$(PY) -m ruff format .
	@$(PY) -m black .

# --- tests ---

py-test: py-test-unit py-test-api

py-test-unit: py-deps-dev
	@$(PY) -m pytest -q tests/test_state.py

py-test-api: py-deps-dev
	@DATA_PATH="$(DATA_PATH)" $(PY) -m pytest -q tests/test_api.py

# --- meta ---

py-check: py-format py-lint py-test py-deps-check
	@echo "✅ all checks passed."

py-ci: py-lint py-test py-deps-audit
	@echo "✅ CI target ok."

py-run: py-deps-install
	@DATA_PATH="$(DATA_PATH)" $(VENV)/bin/uvicorn $(APP) --reload --port $(PORT)

# clean
py-clean-venv:
	rm -fr "$(VENV)"

# vim: ft=make
