"""Tests for WebSocket connection limits."""

from nanobot.channels.websocket import WebSocketConfig


def test_websocket_connection_limit_has_bounded_default():
    assert WebSocketConfig().max_connections == 100


def test_websocket_connection_limit_is_configurable():
    assert WebSocketConfig(max_connections=7).max_connections == 7
