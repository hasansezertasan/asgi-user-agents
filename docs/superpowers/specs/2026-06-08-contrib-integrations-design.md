# Framework Integrations via `contrib/` — Design Spec

**Date:** 2026-06-08
**Status:** Approved
**Scope:** Add first-class Litestar and FastAPI integrations under a new `asgi_user_agents.contrib` subpackage, without changing existing top-level APIs.

## Goal

Provide framework-idiomatic ways to access user-agent data:

- **Litestar:** a `UAPlugin` registering `ua: UADetails` and `user_agent: UserAgent` as DI providers.
- **FastAPI:** prebuilt `Annotated` dependencies (`UADep`, `UserAgentDep`), plain dependency functions (`get_ua`, `get_user_agent`), and an `install_ua(app)` helper.

The raw ASGI `UAMiddleware` keeps working unchanged for all frameworks. Contrib is additive convenience, never a replacement.

## Non-Goals

- A `UAPluginConfig` dataclass or custom dependency names (deferred to future iteration if requested).
- OpenAPI schema contribution from the Litestar plugin.
- An `[all]` extra.
- Quart/Starlette contrib subpackages — current ASGI-level usage already serves them.
- Modifying `UADetails`, `UAMiddleware`, or `UARequest`.

## Layout

```
src/asgi_user_agents/
├── __init__.py              # unchanged
├── middleware.py            # unchanged
├── datastructures.py        # unchanged
├── requests.py              # unchanged
├── _types.py                # unchanged
└── contrib/
    ├── __init__.py          # empty namespace
    ├── litestar/
    │   ├── __init__.py      # re-exports UAPlugin, provide_ua, provide_user_agent
    │   └── plugin.py
    └── fastapi/
        ├── __init__.py      # re-exports UADep, UserAgentDep, get_ua, get_user_agent, install_ua
        └── dependencies.py
```

- The top-level `asgi_user_agents/__init__.py` does **not** import from `contrib/`. Users without extras pay zero import cost.
- Each contrib subpackage imports its framework eagerly. If the framework is not installed, importing the subpackage raises a standard `ImportError`. No custom error wrapping — Python's default message is sufficient.
- `contrib/__init__.py` is intentionally empty to act as a namespace marker.

## Packaging

`pyproject.toml` adds:

```toml
[project.optional-dependencies]
litestar = ["litestar>=2.0.0,<3.0.0"]
fastapi  = ["fastapi>=0.110.0,<1.0.0"]
```

Install patterns:

- `pip install asgi-user-agents` — core middleware only (unchanged).
- `pip install asgi-user-agents[litestar]` — adds Litestar.
- `pip install asgi-user-agents[fastapi]` — adds FastAPI.

No `[all]` extra. Users wanting both write `[litestar,fastapi]`.

## Litestar Integration

File: `src/asgi_user_agents/contrib/litestar/plugin.py`

```python
"""Litestar plugin for User-Agent dependency injection."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import Request
from litestar.di import Provide
from litestar.plugins import InitPluginProtocol
from user_agents.parsers import UserAgent

from asgi_user_agents.datastructures import UADetails

if TYPE_CHECKING:
    from litestar.config.app import AppConfig


def provide_ua(request: Request) -> UADetails:
    """Provide a `UADetails` instance built from the current request."""
    return UADetails(request.scope)


def provide_user_agent(request: Request) -> UserAgent:
    """Provide a raw `user_agents.UserAgent` for the current request."""
    return UserAgent(request.headers.get("user-agent", ""))


class UAPlugin(InitPluginProtocol):
    """Register `ua: UADetails` and `user_agent: UserAgent` as Litestar dependencies."""

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.dependencies.setdefault(
            "ua", Provide(provide_ua, sync_to_thread=False)
        )
        app_config.dependencies.setdefault(
            "user_agent", Provide(provide_user_agent, sync_to_thread=False)
        )
        return app_config
```

`contrib/litestar/__init__.py` re-exports `UAPlugin`, `provide_ua`, `provide_user_agent`.

**Design choices:**

- `setdefault` (not assignment): if a user already registered a dependency named `"ua"` or `"user_agent"` for their own purpose, the plugin does not clobber it.
- `sync_to_thread=False`: UA parsing is microseconds. No reason to dispatch to a thread pool.
- DI-only — no `UAMiddleware` is installed. The providers reconstruct from `request.scope` per request. Users who want `request.scope["ua"]` access can still install `UAMiddleware` separately; the two paths compose cleanly.
- Dependency names `ua` and `user_agent` are hardcoded for v1. Users needing custom names can construct `Provide(provide_ua, ...)` themselves.

**Usage:**

```python
from litestar import Litestar, get
from asgi_user_agents import UADetails
from asgi_user_agents.contrib.litestar import UAPlugin


@get("/")
async def index(ua: UADetails) -> dict:
    return {"is_bot": ua.is_bot}


app = Litestar(route_handlers=[index], plugins=[UAPlugin()])
```

## FastAPI Integration

File: `src/asgi_user_agents/contrib/fastapi/dependencies.py`

```python
"""FastAPI dependencies and helpers for User-Agent access."""

from __future__ import annotations

from fastapi import Depends, FastAPI
from starlette.requests import Request
from typing_extensions import Annotated
from user_agents.parsers import UserAgent

from asgi_user_agents.datastructures import UADetails
from asgi_user_agents.middleware import UAMiddleware


def get_ua(request: Request) -> UADetails:
    """Return a `UADetails` instance for the current request."""
    return UADetails(request.scope)


def get_user_agent(request: Request) -> UserAgent:
    """Return a raw `user_agents.UserAgent` for the current request."""
    return UserAgent(request.headers.get("user-agent", ""))


UADep = Annotated[UADetails, Depends(get_ua)]
UserAgentDep = Annotated[UserAgent, Depends(get_user_agent)]


def install_ua(app: FastAPI) -> FastAPI:
    """Install `UAMiddleware` on `app` (idempotent). Returns the app for chaining."""
    if not any(m.cls is UAMiddleware for m in app.user_middleware):
        app.add_middleware(UAMiddleware)
    return app
```

`contrib/fastapi/__init__.py` re-exports `UADep`, `UserAgentDep`, `get_ua`, `get_user_agent`, `install_ua`.

**Design choices:**

- `Annotated` from `typing_extensions` (project targets Python `>=3.8`; on 3.9+ this is a passthrough).
- `install_ua` checks `app.user_middleware` (the pre-build list, populated immediately) rather than `app.middleware_stack` (which is `None` until app startup). Safe to call any time before serving begins.
- Idempotency: re-calling `install_ua` is a no-op. Important for test fixtures and factory-style app creation.
- `install_ua` returns the app so `app = install_ua(FastAPI())` reads naturally.
- Deps build `UADetails` from `request.scope` directly; they do not depend on `UAMiddleware` being installed. When both are present they coexist — the middleware caches `UADetails` on the scope; the deps reconstruct (cheap) to avoid coupling. A future optimization could read `scope.get("ua")` first.

**Usage:**

```python
from fastapi import FastAPI
from asgi_user_agents.contrib.fastapi import UADep, install_ua

app = install_ua(FastAPI())


@app.get("/")
async def index(ua: UADep) -> dict:
    return {"is_bot": ua.is_bot}
```

## Error Handling

- Missing framework: importing `asgi_user_agents.contrib.litestar` or `.contrib.fastapi` without the extra raises a standard `ImportError` from the framework `import` line. No custom wrapping.
- Missing/empty UA header: existing `UADetails` and `UserAgent` behavior tolerates this — no new error paths introduced.
- `install_ua` is idempotent and never raises on repeated calls.

## Testing

New test files (additive — existing tests stay untouched):

- `tests/test_litestar_plugin.py`
  - Builds a Litestar app with `plugins=[UAPlugin()]` and a handler taking both `ua: UADetails` and `user_agent: UserAgent`.
  - Reuses the existing parametrized fixture `assets/test_middleware.json` to assert injected values match the canonical expected output.
  - Asserts that pre-existing dependency registrations are not clobbered (test `setdefault` behavior).
- `tests/test_fastapi_contrib.py`
  - Builds a FastAPI app, calls `install_ua(app)`, defines handlers using `UADep` and `UserAgentDep`.
  - Reuses the same parametrized fixture to assert correctness.
  - Asserts `install_ua` is idempotent: calling it twice results in exactly one `UAMiddleware` in `app.user_middleware`.

No changes needed to `hatch-test` env — it already includes `litestar` and `fastapi`.

## Documentation (README)

Add a new "Framework integrations" section after the existing "Usage" section, containing two compact subsections:

- **Litestar:** ~10-line example using `UAPlugin()`.
- **FastAPI:** ~10-line example using `install_ua` + `UADep`.

Note that the raw `UAMiddleware` is still the universal path and contrib is additive convenience. Document extras (`pip install asgi-user-agents[litestar]`, `[fastapi]`).

## Backward Compatibility

- All existing top-level exports (`UAMiddleware`, `UADetails`, `UARequest`) are untouched.
- Existing tests are not modified.
- No new top-level imports added — users who don't import from `contrib/` are unaffected.
