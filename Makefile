COMPOSE_LOCAL := docker compose -f tests/compose.local.yml
COMPOSE_GITHUB := docker compose -f tests/compose.github.yml
export COMMAND := poetry run isort --check src/ tests/ && \
    poetry run black --check src/ tests/ && \
    poetry run flake8 src/ tests/ && \
    poetry run mypy src/ tests/ && \
    poetry run pytest tests/test_secrets_loader.py::test_local_docker_on_local


# For local development

.PHONY: check
check:
	@echo "Running checks..."
	-poetry run black --check src/ tests/
	-poetry run isort --check src/ tests/
	-poetry run flake8 src/ tests/
	-poetry run mypy src/ tests/

.PHONY: format
format:
	@echo "Running formatters..."
	poetry run isort src/ tests/
	poetry run black src/ tests/


# For test in local without Docker

.PHONY: test-local-no-docker
test-local-no-docker:
	poetry run pytest tests/test_secrets_loader.py::test_local_no_docker

.PHONY: test-github-actions-no-docker
test-github-actions-no-docker:
	poetry run pytest tests/test_secrets_loader.py::test_github_actions_no_docker_on_local


# For test in Docker

.PHONY: build-local
build-local:
	@${COMPOSE_LOCAL} build --no-cache

.PHONY: build-github
build-github:
	@${COMPOSE_GITHUB} build --no-cache

.PHONY: up-local
up-local: build-local
	@${COMPOSE_LOCAL} up -d

.PHONY: up-github
up-github: build-github
	@${COMPOSE_GITHUB} up -d

.PHONY: test-local
test-local: up-local
	${COMPOSE_LOCAL} run --rm python_3_09 $(COMMAND)
	${COMPOSE_LOCAL} run --rm python_3_10 $(COMMAND)
	${COMPOSE_LOCAL} run --rm python_3_11 $(COMMAND)
	${COMPOSE_LOCAL} run --rm python_3_12 $(COMMAND)
	${COMPOSE_LOCAL} run --rm python_3_13 $(COMMAND)

.PHONY: test-github
test-github: up-github
	@${COMPOSE_GITHUB} run --rm python_3_09 $(COMMAND)
	@${COMPOSE_GITHUB} run --rm python_3_10 $(COMMAND)
	@${COMPOSE_GITHUB} run --rm python_3_11 $(COMMAND)
	@${COMPOSE_GITHUB} run --rm python_3_12 $(COMMAND)
	@${COMPOSE_GITHUB} run --rm python_3_13 $(COMMAND)

.PHONY: test
test: test-local test-github test-local-no-docker test-github-actions-no-docker

.PHONY: clean-local
clean-local:
	@${COMPOSE_LOCAL} down --rmi all

.PHONY: clean-github
clean-github:
	@${COMPOSE_GITHUB} down --rmi all

.PHONY: clean
clean: clean-local clean-github
	docker system prune -af --volumes
