prefix  ?= canelrom1
name    ?= ndm-checkindesk
tag     ?= $(shell date +%Y%m%d.%H%M%S)

VENV    := build
PY      := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip

.PHONY: venv deps-check deps-outdated deps-audit deps-install clean-venv

all: build

build: Dockerfile
	docker build -t $(prefix)/$(name):$(tag) . 
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

# create a python virtual env 
venv:
	@test -d "$(VENV)" || python3 -m venv "$(VENV)"
	@$(PY) -m pip install -U pip setuptools wheel >/dev/null

# install requirements.txt
deps-install: venv
	@$(PIP) install -r requirements.txt

# check for outdated packages
deps-outdated: deps-install
	@echo "-> Outdated pckages (info only) <-"
	@$(PIP) list --outdated || true

# audit packages for vulnerable packages
deps-audit: deps-install
	@$(PIP) install -q pip-audit
	@echo "-> Security audit (fails on findings) <-"
	@$(VENV)/bin/pip-audit -r requirements.txt

# do all checks
deps-check: deps-outdated deps-audit
	@echo "✅ Dependency check complete."

# clean
clean-venv:
	rm -fr "$(VENV)"

# vim: ft=make
