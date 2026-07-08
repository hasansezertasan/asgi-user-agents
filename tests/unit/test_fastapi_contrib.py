"""Unit tests for the FastAPI contrib helpers, in isolation from HTTP."""

from __future__ import annotations

from fastapi.applications import FastAPI
from starlette.requests import Request as StarletteRequest

from asgi_user_agents import UADetails, UAMiddleware
from asgi_user_agents.contrib.fastapi import (
    get_ua,
    get_user_agent,
    install_ua,
)


def test_install_ua_is_idempotent() -> None:
    """Calling install_ua twice must result in exactly one UAMiddleware entry."""
    fresh = FastAPI()
    install_ua(fresh)
    install_ua(fresh)
    ua_entries = [m for m in fresh.user_middleware if m.cls is UAMiddleware]
    assert len(ua_entries) == 1


def test_install_ua_returns_app() -> None:
    """install_ua must return the app for chaining."""
    fresh = FastAPI()
    assert install_ua(fresh) is fresh


def test_plain_dependency_functions_exist() -> None:
    """get_ua and get_user_agent must be importable and callable."""
    assert callable(get_ua)
    assert callable(get_user_agent)


def test_get_ua_reuses_cached_instance_from_scope() -> None:
    """If `scope['ua']` already holds a UADetails, get_ua reuses that instance."""
    cached = UADetails({"type": "http", "headers": [(b"user-agent", b"cached/1.0")]})
    scope: dict = {
        "type": "http",
        "headers": [(b"user-agent", b"different/2.0")],
        "ua": cached,
    }
    request = StarletteRequest(scope)
    assert get_ua(request) is cached
