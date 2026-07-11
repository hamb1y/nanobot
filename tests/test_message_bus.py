"""Tests for MessageBus backpressure."""

import asyncio

import pytest

from nanobot.bus.events import InboundMessage, OutboundMessage
from nanobot.bus.queue import DEFAULT_QUEUE_MAXSIZE, MessageBus


def test_message_bus_uses_bounded_default_queue():
    bus = MessageBus()

    assert bus.inbound.maxsize == DEFAULT_QUEUE_MAXSIZE
    assert bus.outbound.maxsize == DEFAULT_QUEUE_MAXSIZE


def test_message_bus_rejects_non_positive_maxsize():
    with pytest.raises(ValueError, match="maxsize must be positive"):
        MessageBus(maxsize=0)


@pytest.mark.asyncio
async def test_inbound_publish_applies_backpressure_when_full():
    bus = MessageBus(maxsize=1)
    first = InboundMessage(channel="test", sender_id="u", chat_id="c", content="1")
    second = InboundMessage(channel="test", sender_id="u", chat_id="c", content="2")

    await bus.publish_inbound(first)
    blocked = asyncio.create_task(bus.publish_inbound(second))
    await asyncio.sleep(0)
    assert not blocked.done()

    assert await bus.consume_inbound() is first
    await asyncio.wait_for(blocked, timeout=1)
    assert await bus.consume_inbound() is second


@pytest.mark.asyncio
async def test_outbound_publish_applies_backpressure_when_full():
    bus = MessageBus(maxsize=1)
    first = OutboundMessage(channel="test", chat_id="c", content="1")
    second = OutboundMessage(channel="test", chat_id="c", content="2")

    await bus.publish_outbound(first)
    blocked = asyncio.create_task(bus.publish_outbound(second))
    await asyncio.sleep(0)
    assert not blocked.done()

    assert await bus.consume_outbound() is first
    await asyncio.wait_for(blocked, timeout=1)
    assert await bus.consume_outbound() is second
