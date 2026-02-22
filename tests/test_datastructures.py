"""Tests for the ``UADetails`` data structure."""

from __future__ import annotations

from typing import List, Tuple

from asgi_user_agents.datastructures import UADetails

Headers = List[Tuple[bytes, bytes]]


def make_scope(headers: Headers) -> dict:
    """Create a minimal ASGI scope with the given headers."""
    return {"headers": headers}


def test_missing_header_does_not_parse_user_agent(monkeypatch) -> None:
    """Ensure the ``UserAgent`` parser is not invoked when the header is absent."""
    calls: list[str] = []

    class SpyUserAgent:
        def __init__(self, ua_string: str) -> None:
            calls.append(ua_string)
            self.ua_string = ua_string

    monkeypatch.setattr("asgi_user_agents.datastructures.UserAgent", SpyUserAgent)

    scope = make_scope([])
    details = UADetails(scope)

    assert details.ua_string == ""
    assert details.is_provided is False
    assert calls == []


def test_user_agent_cached(monkeypatch) -> None:
    """The ``UserAgent`` parser should only run once and be cached."""
    calls: list[str] = []

    class SpyUserAgent:
        def __init__(self, ua_string: str) -> None:
            calls.append(ua_string)
            self.ua_string = ua_string

    monkeypatch.setattr("asgi_user_agents.datastructures.UserAgent", SpyUserAgent)

    scope = make_scope([(b"user-agent", b"Test-UA")])
    details = UADetails(scope)

    first = details.ua
    second = details.ua

    assert first is second
    assert calls == ["Test-UA"]
    assert details.ua_string == "Test-UA"
    assert details.is_provided is True
