"""Request classes with `scope` attribute of type `UAScope` for type-checking."""

from typing import Any, Literal, Protocol, overload

from asgi_user_agents.datastructures import UADetails
from asgi_user_agents.types import Scope

try:
    from starlette.requests import Request
except ImportError:  # pragma: no cover
    pass  # Starlette not installed.
else:

    class UAScopeProtocol(Protocol):
        """Protocol for `UAScope` class."""

        @overload
        def __getitem__(self, key: Literal["ua"]) -> UADetails: ...  # pragma: no cover

        @overload
        def __getitem__(self, key: str) -> Any: ...  # pragma: no cover

    class UAScope(UAScopeProtocol, Scope):
        """User-Agent scope object with `ua` attribute of type `UADetails`."""

    class UARequest(Request):
        """User-Agent request object with `scope` attribute of type `UAScope`.

        !!! note
            Use this class to make code editors type-check `request.scope["ua"]`.
        """

        scope: UAScope
