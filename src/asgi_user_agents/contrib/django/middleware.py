"""Django middleware attaching a lazy ``request.user_agent``."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.utils.functional import SimpleLazyObject

from asgi_user_agents.contrib.django.utils import get_user_agent

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from django.http import HttpRequest, HttpResponse


class UserAgentMiddleware:
    """Attach ``request.user_agent`` as a lazily-resolved ``UADetails``.

    Supports both sync and async ``get_response`` callables. Parsing is deferred
    via ``SimpleLazyObject`` so a request that never touches ``user_agent`` pays
    nothing, and -- under ASGI with the upstream ``UAMiddleware`` installed --
    resolution reuses the already-parsed ``scope["ua"]``.
    """

    async_capable = True
    sync_capable = True

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse]
        | Callable[[HttpRequest], Awaitable[HttpResponse]],
    ) -> None:
        """Store ``get_response`` and adapt to its sync/async nature."""
        self.get_response = get_response
        self._is_async = iscoroutinefunction(get_response)
        if self._is_async:
            markcoroutinefunction(self)

    def __call__(self, request: HttpRequest) -> HttpResponse | Awaitable[HttpResponse]:
        """Dispatch to the sync or async path.

        Returns:
            The downstream response, or an awaitable resolving to it when the
            middleware is operating in async mode.
        """
        if self._is_async:
            return self._acall(request)
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))  # type: ignore[attr-defined]
        return self.get_response(request)  # type: ignore[return-value]

    async def _acall(self, request: HttpRequest) -> HttpResponse:
        """Async path: attach the lazy user agent, then await downstream.

        Returns:
            The awaited downstream response.
        """
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))  # type: ignore[attr-defined]
        return await self.get_response(request)  # type: ignore[misc]
