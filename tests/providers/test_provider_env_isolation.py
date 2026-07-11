"""Tests for provider credential environment isolation."""

import os

from nanobot.providers.openai_compat_provider import OpenAICompatProvider
from nanobot.providers.registry import ProviderSpec


def test_openai_compat_provider_does_not_mutate_process_environment(monkeypatch):
    monkeypatch.delenv("TEST_PROVIDER_API_KEY", raising=False)
    monkeypatch.delenv("TEST_PROVIDER_BASE", raising=False)
    spec = ProviderSpec(
        name="test-provider",
        keywords=(),
        env_key="TEST_PROVIDER_API_KEY",
        env_extras=(("TEST_PROVIDER_BASE", "{api_base}"),),
    )

    OpenAICompatProvider(
        api_key="provider-secret",
        api_base="https://provider.example/v1",
        spec=spec,
    )

    assert "TEST_PROVIDER_API_KEY" not in os.environ
    assert "TEST_PROVIDER_BASE" not in os.environ
