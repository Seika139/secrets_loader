import os
from pathlib import Path

import pytest

from secrets_loader import SecretsLoader


def test_local_no_docker(tmp_path: Path) -> None:
    # local && docker なし
    env_file = tmp_path / ".env.test"
    env_file.write_text("TEST_KEY=local_no_docker_value\n")
    loader = SecretsLoader(str(env_file))
    assert loader.get("TEST_KEY") == "local_no_docker_value"


@pytest.mark.skipif(
    "GITHUB_ACTIONS" in os.environ,
    reason="This test is only for local execution.",
)
def test_github_actions_no_docker_on_local(monkeypatch: pytest.MonkeyPatch) -> None:
    # GitHub Actions && docker なしを local で実行
    monkeypatch.setenv("GITHUB_ACTIONS_SECRET_KEY", "local_github_actions_secret_value")
    loader = SecretsLoader(None)
    assert (
        loader.get("GITHUB_ACTIONS_SECRET_KEY") == "local_github_actions_secret_value"
    )


@pytest.mark.skipif(
    "GITHUB_ACTIONS" not in os.environ,
    reason="This test is only for GitHub Actions execution.",
)
def test_github_actions_no_docker_on_ci() -> None:
    # GitHub Actions && docker なしを GitHub Actions で実行
    # GitHub Actions 環境では、GITHUB_ACTIONS_SECRET_KEY は自動的に環境変数として設定される
    loader = SecretsLoader(None)
    assert (
        loader.get("GITHUB_ACTIONS_SECRET_KEY")
        == os.environ["GITHUB_ACTIONS_SECRET_KEY"]
    )


def test_local_docker_on_local() -> None:
    # local && docker あり
    loader = SecretsLoader(None)
    assert loader.get("LOCAL_DOCKER_SECRET") == "local_docker_secret_value_from_compose"


@pytest.mark.skipif(
    "GITHUB_ACTIONS" in os.environ,
    reason="This test is only for local execution.",
)
def test_github_actions_docker_on_local(monkeypatch: pytest.MonkeyPatch) -> None:
    # GigHub Actions && docker ありを local で実行
    monkeypatch.setenv("GITHUB_ACTIONS_SECRET_KEY", "github_actions_secret_value_ga")
    loader = SecretsLoader(None)
    assert loader.get("GITHUB_ACTIONS_SECRET_KEY") == "github_actions_secret_value_ga"
    assert (
        loader.get("COMPOSE_DEFAULT_KEY") == "compose_default_value"
    )  # 環境変数から読み込まれる前提


@pytest.mark.skipif(
    "GITHUB_ACTIONS" not in os.environ,
    reason="This test is only for GitHub Actions execution.",
)
def test_github_actions_docker_on_ci() -> None:
    # GitHub Actions && docker ありを GitHub Actions で実行
    loader = SecretsLoader(None)
    assert (
        loader.get("GITHUB_ACTIONS_SECRET_KEY")
        == os.environ["GITHUB_ACTIONS_SECRET_KEY"]
    )
    assert (
        loader.get("COMPOSE_DEFAULT_KEY") == "compose_default_value"
    )  # 環境変数から読み込まれる前提
