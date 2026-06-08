"""FastAPI integration for asgi-user-agents."""

from asgi_user_agents.contrib.fastapi.dependencies import (
    UADep as UADep,
    UserAgentDep as UserAgentDep,
    get_ua as get_ua,
    get_user_agent as get_user_agent,
    install_ua as install_ua,
)
