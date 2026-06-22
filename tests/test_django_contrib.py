"""Tests for the Django contrib integration."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ALLOWED_HOSTS=["*"],
        INSTALLED_APPS=["asgi_user_agents.contrib.django"],
        DATABASES={},
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": False,
                "OPTIONS": {},
            }
        ],
        USE_TZ=True,
    )
    django.setup()

import parametrize_from_file as pff
import pytest
from asgiref.sync import iscoroutinefunction
from django.template import Context, Template
from django.test import RequestFactory

from asgi_user_agents import UADetails
from asgi_user_agents.contrib.django import (
    UserAgentMiddleware,
    get_user_agent,
)

rf = RequestFactory()


# --- Resolution: the three scope-first branches ---------------------------- #


def test_reuses_cached_uadetails_from_scope() -> None:
    """Branch 1: an existing `scope['ua']` UADetails is returned as-is."""
    cached = UADetails({"type": "http", "headers": [(b"user-agent", b"cached/1.0")]})
    request = SimpleNamespace(
        scope={"type": "http", "headers": [(b"user-agent", b"other/2.0")], "ua": cached}
    )
    assert get_user_agent(request) is cached  # type: ignore[arg-type]


def test_builds_from_scope_without_upstream_middleware() -> None:
    """Branch 2: a scope with no usable `ua` yields a fresh UADetails from it."""
    request = SimpleNamespace(
        scope={"type": "http", "headers": [(b"user-agent", b"scoped/3.0")]}
    )
    ua = get_user_agent(request)  # type: ignore[arg-type]
    assert isinstance(ua, UADetails)
    assert ua.ua_string == "scoped/3.0"


def test_non_uadetails_scope_value_is_ignored() -> None:
    """A `scope['ua']` that is not a UADetails must not be trusted/reused."""
    request = SimpleNamespace(
        scope={
            "type": "http",
            "headers": [(b"user-agent", b"scoped/4.0")],
            "ua": "nope",
        }
    )
    ua = get_user_agent(request)  # type: ignore[arg-type]
    assert isinstance(ua, UADetails)
    assert ua.ua_string == "scoped/4.0"


def test_wsgi_request_falls_back_to_headers() -> None:
    """Branch 3: a WSGIRequest (no `.scope`) resolves via synthesized headers."""
    request = rf.get("/", HTTP_USER_AGENT="wsgi/5.0")
    assert not hasattr(request, "scope")
    ua = get_user_agent(request)
    assert isinstance(ua, UADetails)
    assert ua.ua_string == "wsgi/5.0"


# --- Resolution correctness against the canonical fixture ------------------ #


@pff.parametrize(path="assets/test_middleware.json", key="test_user_agent_data")
def test_resolution_matches_fixture(ua_string: str, response_data: dict) -> None:
    """The WSGI fallback path produces fixture-accurate UADetails fields."""
    request = rf.get("/", HTTP_USER_AGENT=ua_string)
    ua = get_user_agent(request)
    assert ua.ua_string == response_data["ua_string"]
    assert ua.os.family == response_data["os.family"]
    assert ua.browser.family == response_data["browser.family"]
    assert ua.device.family == response_data["device.family"]
    assert ua.is_mobile is response_data["is_mobile"]
    assert ua.is_bot is response_data["is_bot"]


# --- Middleware ------------------------------------------------------------ #


def test_sync_middleware_attaches_lazy_user_agent() -> None:
    """Sync path: `request.user_agent` resolves to the correct UADetails."""
    sentinel = object()
    middleware = UserAgentMiddleware(lambda _request: sentinel)
    assert iscoroutinefunction(middleware) is False
    request = rf.get("/", HTTP_USER_AGENT="Mozilla/5.0 (iPhone)")
    response = middleware(request)
    assert response is sentinel
    assert request.user_agent.is_mobile is True  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_async_middleware_attaches_lazy_user_agent() -> None:
    """Async path: the middleware marks itself async and still attaches UA."""
    sentinel = object()

    async def get_response(_request: Any) -> object:
        return sentinel

    middleware = UserAgentMiddleware(get_response)
    assert iscoroutinefunction(middleware) is True
    request = rf.get("/", HTTP_USER_AGENT="Mozilla/5.0 (iPhone)")
    response = await middleware(request)  # type: ignore[misc]
    assert response is sentinel
    assert request.user_agent.is_mobile is True  # type: ignore[attr-defined]


# --- Template filters ------------------------------------------------------ #


@pff.parametrize(path="assets/test_middleware.json", key="test_user_agent_data")
def test_template_filters_match_fixture(ua_string: str, response_data: dict) -> None:
    """`{% load asgi_user_agents %}` filters mirror the UADetails booleans."""
    template = Template(
        "{% load asgi_user_agents %}"
        "{{ request|is_mobile }}|{{ request|is_pc }}|{{ request|is_tablet }}|"
        "{{ request|is_bot }}|{{ request|is_touch_capable }}"
    )
    request = rf.get("/", HTTP_USER_AGENT=ua_string)
    rendered = template.render(Context({"request": request}))
    expected = "|".join(
        str(response_data[key])
        for key in ("is_mobile", "is_pc", "is_tablet", "is_bot", "is_touch_capable")
    )
    assert rendered == expected
