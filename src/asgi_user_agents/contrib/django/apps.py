"""Django application configuration for the asgi-user-agents contrib."""

from django.apps import AppConfig


class AsgiUserAgentsConfig(AppConfig):
    """App config pinning a stable label for template-tag discovery.

    The package path ends in ``.django``, whose default app label would be the
    bare ``django`` -- confusing and collision-prone. We pin ``asgi_user_agents``
    so ``{% load asgi_user_agents %}`` resolves and the app is unambiguous in
    ``INSTALLED_APPS``.
    """

    name = "asgi_user_agents.contrib.django"
    label = "asgi_user_agents"
