"""FastAPI dependencies and helpers for User-Agent access."""

from fastapi import Depends, FastAPI
from starlette.requests import Request
from typing_extensions import Annotated
from user_agents.parsers import UserAgent

from asgi_user_agents.datastructures import UADetails
from asgi_user_agents.middleware import UAMiddleware


def get_ua(request: Request) -> UADetails:
    """Return a `UADetails` instance for the current request.

    If `UAMiddleware` has already attached a `UADetails` to `request.scope`,
    that instance is returned to avoid re-parsing the header.

    Args:
        request: The Starlette/FastAPI request.

    Returns:
        A `UADetails` wrapping the request scope.

    """
    cached = request.scope.get("ua")
    if isinstance(cached, UADetails):
        return cached
    return UADetails(request.scope)


def get_user_agent(request: Request) -> UserAgent:
    """Return a raw `user_agents.UserAgent` for the current request.

    Args:
        request: The Starlette/FastAPI request.

    Returns:
        A parsed `UserAgent` instance.

    """
    return UserAgent(request.headers.get("user-agent", ""))


UADep = Annotated[UADetails, Depends(get_ua)]
UserAgentDep = Annotated[UserAgent, Depends(get_user_agent)]


def install_ua(app: FastAPI) -> FastAPI:
    """Install `UAMiddleware` on `app` if not already installed.

    Args:
        app: The FastAPI application.

    Returns:
        The same `app`, for chaining.

    """
    if not any(m.cls is UAMiddleware for m in app.user_middleware):
        app.add_middleware(UAMiddleware)
    return app
