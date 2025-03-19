init: install-deps

install-deps:
	@pip install --upgrade pip setuptools wheel
	@pip install --upgrade poetry
	@poetry install
	@pre-commit install
	@pre-commit run --all-files

run: init
	@poetry run env $(shell grep -v ^\# .env | xargs) uvicorn src.main:app --reload --port 8080

poetry-export:
	@poetry export --with dev -vv --no-ansi --no-interaction --without-hashes --format requirements.txt --output requirements.txt

build-container:
	@docker build \
		--tag secure:jwt-validation \
		--build-arg GIT_HASH=$(shell git rev-parse HEAD) \
		-f Dockerfile \
		.

run-container: poetry-export build-container
	@docker run --rm -it \
		--name secure-jwt-validation \
		--env-file .env \
		--env PORT=8080 \
		--publish 8080:8080 \
		secure:jwt-validation

tests: init
	@poetry run env $(shell grep -v ^\# .env | xargs) pytest
