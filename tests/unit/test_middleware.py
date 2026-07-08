"""Unit tests for ``UAMiddleware`` driven directly, without a framework app."""

from __future__ import annotations

from typing import Any, MutableMapping

import pytest

from asgi_user_agents import UAMiddleware


@pytest.mark.asyncio
async def test_existing_scope_user_agent_is_preserved() -> None:
    """Ensure pre-existing scope user agent is not overridden."""
    sentinel = object()
    captured = {}

    async def app(
        scope: MutableMapping[str, Any],
        _receive: Any,
        _send: Any,
    ) -> None:
        captured["ua"] = scope["ua"]

    middleware = UAMiddleware(app)

    scope: MutableMapping[str, Any] = {"type": "http", "ua": sentinel}

    async def receive() -> MutableMapping[str, Any]:
        return {"type": "http.request"}

    async def send(
        message: MutableMapping[str, Any],
    ) -> None:  # pragma: no cover - not used but required by interface
        captured["message"] = message

    await middleware(scope, receive, send)

    assert captured["ua"] is sentinel
