"""ASGI User Agents package initialization."""

from contextlib import suppress

from .datastructures import UADetails as UADetails
from .middleware import UAMiddleware as UAMiddleware

with suppress(ImportError):
    from .requests import UARequest as UARequest
