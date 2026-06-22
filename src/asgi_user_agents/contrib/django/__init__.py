"""Django integration for asgi-user-agents."""

from asgi_user_agents.contrib.django.middleware import (
    UserAgentMiddleware as UserAgentMiddleware,
)
from asgi_user_agents.contrib.django.utils import (
    get_user_agent as get_user_agent,
)
