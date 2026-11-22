.PHONY: install test format-check format lint-check lint type-check check build ruff-cs-check ruff-cs-fix ruff-linter-check ruff-linter-fix mypy-check

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt

test:
	python3 -m unittest discover -s tests -v

ruff-cs-check format-check:
	.venv/bin/ruff format --check .

ruff-cs-fix format:
	.venv/bin/ruff format .

ruff-linter-check lint-check:
	.venv/bin/ruff check .

ruff-linter-fix lint:
	.venv/bin/ruff check --fix .

mypy-check type-check:
	.venv/bin/mypy bot

check: ruff-cs-check ruff-linter-check mypy-check test

build:
	docker build -t unn-2026-gasenin-bot .
