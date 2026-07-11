"""Tests for CLI app subprocess environment isolation."""

from nanobot.apps.cli.service import CliAppManager


def test_cli_app_environment_excludes_provider_credentials(monkeypatch):
    monkeypatch.setenv("PATH", "safe-path")
    monkeypatch.setenv("HOME", "safe-home")
    monkeypatch.setenv("OPENAI_API_KEY", "secret")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "secret")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "secret")

    env = CliAppManager._build_app_env()

    assert env["PATH"] == "safe-path"
    assert env["HOME"] == "safe-home"
    assert "OPENAI_API_KEY" not in env
    assert "ANTHROPIC_API_KEY" not in env
    assert "AWS_SECRET_ACCESS_KEY" not in env
