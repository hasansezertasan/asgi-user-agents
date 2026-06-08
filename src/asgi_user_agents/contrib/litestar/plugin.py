"""Litestar plugin for User-Agent dependency injection."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.di import Provide
from litestar.plugins import InitPluginProtocol
from user_agents.parsers import UserAgent

from asgi_user_agents.datastructures import UADetails

if TYPE_CHECKING:
    from litestar import Request
    from litestar.config.app import AppConfig


def provide_ua(request: Request) -> UADetails:
    """Provide a `UADetails` instance built from the current request scope.

    Args:
        request: The Litestar request.

    Returns:
        A `UADetails` wrapping the request scope.

    """
    return UADetails(request.scope)


def provide_user_agent(request: Request) -> UserAgent:
    """Provide a raw `user_agents.UserAgent` for the current request.

    Args:
        request: The Litestar request.

    Returns:
        A parsed `UserAgent` instance.

    """
    return UserAgent(request.headers.get("user-agent", ""))


class UAPlugin(InitPluginProtocol):
    """Register `ua: UADetails` and `user_agent: UserAgent` as Litestar dependencies."""

    def on_app_init(self, app_config: AppConfig) -> AppConfig:  # noqa: PLR6301
        """Register UA dependencies without clobbering user-provided ones.

        Args:
            app_config: The Litestar app configuration.

        Returns:
            The (mutated) app configuration.

        """
        app_config.dependencies.setdefault(
            "ua", Provide(provide_ua, sync_to_thread=False)
        )
        app_config.dependencies.setdefault(
            "user_agent", Provide(provide_user_agent, sync_to_thread=False)
        )
        return app_config
