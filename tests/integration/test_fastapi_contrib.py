"""Integration tests for the FastAPI contrib dependencies."""

from __future__ import annotations

from typing import Any, Dict

import parametrize_from_file as pff
import pytest
from fastapi.applications import FastAPI
from httpx import ASGITransport, AsyncClient
from starlette.responses import JSONResponse, Response

from asgi_user_agents import UADetails
from asgi_user_agents.contrib.fastapi import (
    UADep,
    UserAgentDep,
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
@pff.parametrize(path="../assets/test_middleware.json")
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
