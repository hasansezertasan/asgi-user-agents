"""Unit tests for the Litestar contrib plugin helpers, in isolation from HTTP."""

from __future__ import annotations

from litestar import Request

from asgi_user_agents import UADetails
from asgi_user_agents.contrib.litestar import provide_ua


def test_provide_ua_reuses_cached_instance_from_scope() -> None:
    """If `scope['ua']` already holds a UADetails, provide_ua reuses that instance."""
    cached = UADetails({"type": "http", "headers": [(b"user-agent", b"cached/1.0")]})
    scope: dict = {
        "type": "http",
        "headers": [(b"user-agent", b"different/2.0")],
        "ua": cached,
        "path": "/",
        "method": "GET",
        "query_string": b"",
    }
    request: Request = Request(scope)
    assert provide_ua(request) is cached
