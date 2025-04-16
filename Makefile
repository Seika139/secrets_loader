.PHONY: check
.PHONY: format
.PHONY: test
.PHONY: test-local
.PHONY: test-local-no-docker
.PHONY: test-github-actions-no-docker
.PHONY: test-local-docker
.PHONY: test-github-actions-docker

check:
	@# 先頭に - をつけることで、エラーが発生しても処理を続行する
	-poetry run black --check src/ tests/
	-poetry run isort --check src/ tests/
	-poetry run flake8
	-poetry run mypy src/ tests/

format:
	poetry run isort src/ tests/
	poetry run black src/ tests/

test: test-local test-github-actions-no-docker test-local-docker test-github-actions-docker

test-local:
	poetry run pytest tests/test_secrets_loader.py

test-local-no-docker:
	poetry run pytest tests/test_secrets_loader.py::test_local_no_docker

test-github-actions-no-docker:
	poetry run pytest tests/test_secrets_loader.py::test_github_actions_no_docker

test-local-docker:
	docker-compose -f tests/docker-compose.local.yml up -d
	poetry run pytest tests/test_secrets_loader.py::test_local_docker_compose_secrets
	docker-compose -f tests/docker-compose.local.yml down

test-github-actions-docker:
	docker-compose -f tests/docker-compose.github.yml up -d
	poetry run pytest tests/test_secrets_loader.py::test_github_actions_docker_compose_secrets
	docker-compose -f tests/docker-compose.github.yml down
