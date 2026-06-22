"""Resolve a :class:`UADetails` for a Django request (scope-first)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asgi_user_agents.datastructures import UADetails

if TYPE_CHECKING:
    from django.http import HttpRequest

    from asgi_user_agents._types import Scope


def _synthetic_scope(request: HttpRequest) -> Scope:
    """Build a minimal ASGI-shaped scope from a request's headers.

    ``UADetails`` only reads ``scope["headers"]`` -- a list of
    ``(bytes, bytes)`` pairs. Under WSGI there is no ``request.scope``, so we
    fabricate just enough for ``UADetails`` to find the User-Agent. Header
    values are latin-1 encoded to match the ASGI byte convention that
    ``UADetails._get_header`` decodes against.

    Returns:
        A scope-shaped mapping carrying only the ``User-Agent`` header.
    """
    ua_string = request.headers.get("user-agent", "")
    return {"headers": [(b"user-agent", ua_string.encode("latin-1"))]}


def get_user_agent(request: HttpRequest) -> UADetails:
    """Return a :class:`UADetails` for ``request``, reusing work when possible.

    Resolution order (scope-first):

    1. **Reuse.** If the request carries an ASGI ``scope`` (``request.scope``)
       and that scope already holds a ``UADetails`` under ``"ua"`` -- i.e. the
       upstream ``UAMiddleware`` ran -- return *that same instance*. No re-parse.
    2. **ASGI, no upstream middleware.** If ``request.scope`` exists but has no
       usable ``"ua"``, build ``UADetails(request.scope)`` from it.
    3. **WSGI fallback.** No ``request.scope`` at all -> build a ``UADetails``
       from :func:`_synthetic_scope`.

    Args:
        request: The Django request (``ASGIRequest`` or ``WSGIRequest``).

    Returns:
        A ``UADetails`` describing the request's User-Agent.
    """
    scope: Scope | None = getattr(request, "scope", None)
    if scope is not None:
        cached = scope.get("ua")
        if isinstance(cached, UADetails):
            return cached
        return UADetails(scope)
    return UADetails(_synthetic_scope(request))
