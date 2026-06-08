"""Litestar integration for asgi-user-agents."""

from asgi_user_agents.contrib.litestar.plugin import (
    UAPlugin as UAPlugin,
    provide_ua as provide_ua,
    provide_user_agent as provide_user_agent,
)
