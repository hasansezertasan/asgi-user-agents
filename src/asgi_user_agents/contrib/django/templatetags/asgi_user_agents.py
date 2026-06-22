"""Template filters exposing User-Agent device classes.

Each filter takes the ``request`` and returns a device-class boolean, e.g.::

    {% load asgi_user_agents %}
    {% if request|is_mobile %}...{% endif %}

The filters resolve through :func:`get_user_agent`, so they reuse a
``UADetails`` already attached by ``UserAgentMiddleware`` or by the upstream
ASGI ``UAMiddleware`` (``scope["ua"]``).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django import template

from asgi_user_agents.contrib.django.utils import get_user_agent

if TYPE_CHECKING:
    from django.http import HttpRequest

register = template.Library()


@register.filter()
def is_mobile(request: HttpRequest) -> bool:
    """Whether the request comes from a mobile device.

    Returns:
        ``True`` if the User-Agent identifies a mobile device.
    """
    return get_user_agent(request).is_mobile


@register.filter()
def is_pc(request: HttpRequest) -> bool:
    """Whether the request comes from a PC.

    Returns:
        ``True`` if the User-Agent identifies a PC.
    """
    return get_user_agent(request).is_pc


@register.filter()
def is_tablet(request: HttpRequest) -> bool:
    """Whether the request comes from a tablet.

    Returns:
        ``True`` if the User-Agent identifies a tablet.
    """
    return get_user_agent(request).is_tablet


@register.filter()
def is_bot(request: HttpRequest) -> bool:
    """Whether the request comes from a bot/crawler.

    Returns:
        ``True`` if the User-Agent identifies a bot or crawler.
    """
    return get_user_agent(request).is_bot


@register.filter()
def is_touch_capable(request: HttpRequest) -> bool:
    """Whether the requesting device is touch-capable.

    Returns:
        ``True`` if the User-Agent identifies a touch-capable device.
    """
    return get_user_agent(request).is_touch_capable
