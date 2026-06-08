"""Tests for the FastAPI contrib dependencies."""

from __future__ import annotations

from typing import Any, Dict

import parametrize_from_file as pff
import pytest
from fastapi.applications import FastAPI
from httpx import ASGITransport, AsyncClient
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse, Response

from asgi_user_agents import UADetails, UAMiddleware
from asgi_user_agents.contrib.fastapi import (
    UADep,
    UserAgentDep,
    get_ua,
    get_user_agent,
    install_ua,
)

app = install_ua(FastAPI())


@app.get("/")
async def index(ua: UADep, user_agent: UserAgentDep) -> Response:
    """Return user-agent data via injected dependencies."""
    assert isinstance(ua, UADetails)
    data: Dict[str, Any] = {
        "ua_string": ua.ua_string,
        "os.family": ua.os.family,
        "browser.family": ua.browser.family,
        "device.family": ua.device.family,
        "is_provided": ua.is_provided,
        "is_mobile": ua.is_mobile,
        "is_bot": ua.is_bot,
        "raw_family": user_agent.browser.family,
    }
    return JSONResponse(data)


@pytest.mark.asyncio
@pff.parametrize(path="assets/test_middleware.json")
async def test_user_agent_data(ua_string: str, response_data: dict) -> None:
    """Test that both injected dependencies match the expected data."""
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver"
    ) as client:
        response = await client.get("/", headers={"User-Agent": ua_string})
        data = response.json()
        assert data["ua_string"] == response_data["ua_string"]
        assert data["os.family"] == response_data["os.family"]
        assert data["browser.family"] == response_data["browser.family"]
        assert data["device.family"] == response_data["device.family"]
        assert data["is_bot"] is response_data["is_bot"]
        assert data["is_mobile"] is response_data["is_mobile"]
        assert data["raw_family"] == response_data["browser.family"]


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
