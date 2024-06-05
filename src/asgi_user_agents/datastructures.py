"""Data structures for user-agent details."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from urllib.parse import unquote

from user_agents.parsers import Browser, Device, OperatingSystem, UserAgent

if TYPE_CHECKING:
    from asgi_user_agents.types import Scope


class UADetails:
    """User-Agent details object."""

    def __init__(self, scope: Scope) -> None:
        """Initialize the user-agent details object."""
        self._scope = scope
        self._ua: UserAgent

    def _get_header(self, name: bytes) -> Optional[str]:
        """Get header value."""
        return _get_header(self._scope, name)

    @property
    def _ua_string(self) -> Optional[str]:
        """Extract user-agent string from the headers of the request and return it."""
        return self._get_header(b"User-Agent") or ""

    @property
    def ua(self) -> UserAgent:
        """Return the user-agent object."""
        if not hasattr(self, "_ua"):
            self._ua = UserAgent(self._ua_string)
        return self._ua

    @property
    def ua_string(self) -> str:
        """Return the user-agent string."""
        return self.ua.ua_string

    @property
    def is_provided(self) -> bool:
        """Check if the user-agent string is provided."""
        return bool(self.ua_string)

    @property
    def os(self) -> OperatingSystem:
        """Return the operating system."""
        return self.ua.os

    @property
    def browser(self) -> Browser:
        """Return the browser."""
        return self.ua.browser

    @property
    def device(self) -> Device:
        """Return the device."""
        return self.ua.device

    @property
    def is_tablet(self) -> bool:
        """Check if the device is a tablet."""
        return self.ua.is_tablet

    @property
    def is_mobile(self) -> bool:
        """Check if the device is a mobile."""
        return self.ua.is_mobile

    @property
    def is_touch_capable(self) -> bool:
        """Check if the device is touch capable."""
        return self.ua.is_touch_capable

    @property
    def is_pc(self) -> bool:
        """Check if the device is a PC."""
        return self.ua.is_pc

    @property
    def is_bot(self) -> bool:
        """Check if the device is a bot."""
        return self.ua.is_bot

    @property
    def is_email_client(self) -> bool:
        """Check if the device is an email client."""
        return self.ua.is_email_client


def _get_header(scope: Scope, key: bytes) -> Optional[str]:
    key = key.lower()
    value: Optional[str] = None
    should_unquote = False

    for k, v in scope["headers"]:
        if k.lower() == key:
            value = v.decode("latin-1")
        if k.lower() == b"%s-uri-autoencoded" % key and v == b"true":
            should_unquote = True

    if value is None:
        return None

    return unquote(value) if should_unquote else value
