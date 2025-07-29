"""ASGI User Agents package initialization."""

from contextlib import suppress

from asgi_user_agents.datastructures import UADetails as UADetails
from asgi_user_agents.middleware import UAMiddleware as UAMiddleware

with suppress(ImportError):
    from asgi_user_agents.requests import UARequest as UARequest
