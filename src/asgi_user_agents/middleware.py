"""Middleware for ASGI applications."""
from asgi_user_agents.datastructures import UADetails
from asgi_user_agents.types import ASGIApp, Receive, Scope, Send


class UAMiddleware:
    """User Agent Middleware for ASGI applications."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize the middleware."""
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Call the middleware."""
        if scope["type"] in ("http", "websocket"):
            scope["ua"] = UADetails(scope)

        await self._app(scope, receive, send)
