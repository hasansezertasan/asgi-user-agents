"""Tests for the Litestar contrib plugin."""

from __future__ import annotations

from typing import Any, Dict

import parametrize_from_file as pff
import pytest
from httpx import ASGITransport, AsyncClient
from litestar import Litestar, get
from litestar.di import Provide
from user_agents.parsers import UserAgent

from asgi_user_agents import UADetails
from asgi_user_agents.contrib.litestar import UAPlugin


@get("/")
async def index(ua: UADetails, user_agent: UserAgent) -> Dict[str, Any]:
    """Return user-agent data via injected dependencies."""
    assert isinstance(ua, UADetails)
    assert isinstance(user_agent, UserAgent)
    return {
        "ua_string": ua.ua_string,
        "os": ua.os,
        "os.family": ua.os.family,
        "os.version": ua.os.version,
        "os.version_string": ua.os.version_string,
        "browser": ua.browser,
        "browser.family": ua.ua.browser.family,
        "browser.version": ua.ua.browser.version,
        "browser.version_string": ua.ua.browser.version_string,
        "device": ua.device,
        "device.family": ua.device.family,
        "device.brand": ua.device.brand,
        "device.model": ua.device.model,
        "is_provided": ua.is_provided,
        "is_tablet": ua.is_tablet,
        "is_mobile": ua.is_mobile,
        "is_touch_capable": ua.is_touch_capable,
        "is_pc": ua.is_pc,
        "is_bot": ua.is_bot,
        "is_email_client": ua.is_email_client,
        "raw_family": user_agent.browser.family,
    }


app = Litestar(route_handlers=[index], plugins=[UAPlugin()])


@pytest.mark.asyncio
@pff.parametrize(path="assets/test_middleware.json")
async def test_user_agent_data(ua_string: str, response_data: dict) -> None:
    """Test that both injected dependencies produce the expected data."""
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


@pytest.mark.asyncio
async def test_plugin_does_not_clobber_existing_dependencies() -> None:
    """If `ua` is already registered, the plugin must not overwrite it."""

    async def custom_ua() -> str:
        return "custom"

    @get("/custom")
    async def handler(ua: str) -> Dict[str, str]:
        return {"ua": ua}

    local_app = Litestar(
        route_handlers=[handler],
        dependencies={"ua": Provide(custom_ua)},
        plugins=[UAPlugin()],
    )

    async with AsyncClient(
        transport=ASGITransport(local_app), base_url="http://testserver"
    ) as client:
        response = await client.get("/custom")
        assert response.json() == {"ua": "custom"}
