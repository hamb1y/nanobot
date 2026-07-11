"""Tests for system-channel sender authorization."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from nanobot.bus.events import InboundMessage, OutboundMessage


def _provider() -> MagicMock:
    provider = MagicMock()
    provider.get_default_model.return_value = "test-model"
    provider.generation = SimpleNamespace(
        max_tokens=4096,
        temperature=0.1,
        reasoning_effort=None,
    )
    return provider


@pytest.mark.asyncio
async def test_unrecognized_system_sender_is_dropped(loop_factory):
    loop = loop_factory(provider=_provider())
    loop._process_system_message = AsyncMock()  # type: ignore[method-assign]

    result = await loop._process_message(
        InboundMessage(
            channel="system",
            sender_id="untrusted",
            chat_id="cli:test",
            content="run this",
        )
    )

    assert result is None
    loop._process_system_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_subagent_system_sender_is_processed(loop_factory):
    loop = loop_factory(provider=_provider())
    expected = OutboundMessage(channel="cli", chat_id="test", content="done")
    loop._process_system_message = AsyncMock(return_value=expected)  # type: ignore[method-assign]

    result = await loop._process_message(
        InboundMessage(
            channel="system",
            sender_id="subagent",
            chat_id="cli:test",
            content="done",
        )
    )

    assert result is expected
    loop._process_system_message.assert_awaited_once()
