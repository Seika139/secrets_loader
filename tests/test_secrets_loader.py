import os
import pytest
from secrets_loader import SecretsLoader


def test_local_no_docker() -> None:
    with open(".env.test", "w") as f:
        f.write("TEST_KEY=local_no_docker_value\n")
    loader = SecretsLoader(".env.test")
    assert loader.get("TEST_KEY") == "local_no_docker_value"
    os.remove(".env.test")


def test_github_actions_no_docker(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS_SECRET_KEY", "github_actions_secret_value")
    loader = SecretsLoader(None)
    assert loader.get("GITHUB_ACTIONS_SECRET_KEY") == "github_actions_secret_value"


def test_local_docker_compose_secrets() -> None:
    with open("local_docker_secret.txt", "w") as f:
        f.write("local_docker_secret_value_from_compose\n")
    loader = SecretsLoader(None)
    assert loader.get("LOCAL_DOCKER_SECRET") == "local_docker_secret_value_from_compose"
    os.remove("local_docker_secret.txt")


def test_github_actions_docker_compose_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS_SECRET_KEY", "github_actions_secret_value_ga")
    with open("github_actions_secret.txt", "w") as f:
        f.write("github_actions_secret_value_from_compose\n")
    loader = SecretsLoader(None)
    assert loader.get("GITHUB_ACTIONS_SECRET_KEY") == "github_actions_secret_value_ga"
    assert (
        loader.get("COMPOSE_DEFAULT_KEY") == "compose_default_value"
    )  # 環境変数から読み込まれる前提
    os.remove("github_actions_secret.txt")
