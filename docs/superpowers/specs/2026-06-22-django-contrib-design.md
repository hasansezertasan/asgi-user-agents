# Django Integration via `contrib/django` — Design Spec

**Date:** 2026-06-22
**Status:** Draft (awaiting approval)
**Scope:** Add a first-class Django integration under `asgi_user_agents.contrib.django`, on top of this package's `UADetails`. No changes to existing top-level APIs.

## Background

The integration provides three things: a middleware that attaches a lazy `request.user_agent`, five template filters (`is_mobile`, `is_pc`, `is_tablet`, `is_bot`, `is_touch_capable`), and (deferred) an optional cache layer for parsed user agents (ua-parser is slow).

It is implemented idiomatically and routed through our `UADetails`, gaining scope reuse for free under ASGI.

## Goal

Provide Django-idiomatic access to user-agent data:

- A **sync+async middleware** attaching `request.user_agent: UADetails` (lazy).
- The **five template filters**, plus we expose the richer `UADetails` (so `os`, `browser`, `device`, `is_email_client` are also reachable in views).

Caching is **deferred** (see Non-Goals). ua-parser is slow, but under ASGI the scope-first reuse already avoids re-parsing for the common path, and a cache layer can land additively later without changing this surface.

The raw ASGI `UAMiddleware` keeps working unchanged. Django contrib is additive convenience.

## Decision: scope-first resolution

`request.user_agent` resolves in this order:

1. **Reuse:** if `request` carries a `scope` (ASGI) and `request.scope.get("ua")` is a `UADetails` (i.e. upstream `UAMiddleware` already ran), return it — zero re-parse, shares the cached `_ua`.
2. **ASGI, no upstream middleware:** if `request.scope` exists, build `UADetails(request.scope)`.
3. **WSGI fallback:** no `request.scope` → synthesize a minimal scope `{"headers": [(b"user-agent", ua.encode("latin-1"))]}` from `request.headers` and build `UADetails(...)`.

Confirmed against Django source (`main`/6.2a and `stable/3.2.x`): `ASGIRequest` stores `self.scope = scope`; `WSGIRequest` has no `scope`; `request.headers` (`HttpHeaders(self.META)`) exists on both. So the integration is ASGI-flavored (reuses `scope["ua"]`) but degrades cleanly to header parsing under WSGI.

## Non-Goals

- **Caching** (`USER_AGENTS_CACHE`). Deferred to a later iteration; v1 ships without it. Scope-first reuse covers the hot ASGI path; a cache layer is additive and won't change this surface.
- A settings dataclass / configurable attribute name (`request.user_agent` is fixed for v1).
- An `[all]` extra.
- Async template rendering concerns (filters are pure, sync, microsecond-cheap).
- Changing `UAMiddleware` or `UADetails` semantics, or top-level exports. The contrib is purely additive — **no core files are modified**.

## Layout

```
src/asgi_user_agents/contrib/django/
├── __init__.py              # re-exports UserAgentMiddleware, get_user_agent
├── apps.py                  # AppConfig with pinned label
├── middleware.py            # UserAgentMiddleware (sync + async capable)
├── utils.py                 # get_user_agent(request) — scope-first resolution
└── templatetags/
    ├── __init__.py
    └── asgi_user_agents.py  # is_mobile, is_pc, is_tablet, is_bot, is_touch_capable
```

- Top-level `asgi_user_agents/__init__.py` does **not** import contrib — zero import cost for non-Django users.
- Importing `contrib.django` without Django installed raises a standard `ImportError` (no custom wrapping), matching the fastapi/litestar contribs.

## App label

`templatetags/` are discovered only from apps in `INSTALLED_APPS`. The package path is `asgi_user_agents.contrib.django`, whose default app label would be the bare `django` — confusing and collision-prone. `apps.py` pins it:

```python
from django.apps import AppConfig

class AsgiUserAgentsConfig(AppConfig):
    name = "asgi_user_agents.contrib.django"
    label = "asgi_user_agents"
```

Users add `"asgi_user_agents.contrib.django"` to `INSTALLED_APPS`. Django 3.2+ auto-detects the `AppConfig`; no `default_app_config` shim needed.

## Middleware

`middleware.py` — a single class supporting both sync and async `get_response`, detected at init via `asgiref.sync.iscoroutinefunction`. It sets `request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))` so parsing happens only if accessed (and not at all for cached/reused cases until touched).

```python
from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.utils.functional import SimpleLazyObject
from .utils import get_user_agent

class UserAgentMiddleware:
    async_capable = True
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response
        self._async = iscoroutinefunction(get_response)
        if self._async:
            markcoroutinefunction(self)

    def __call__(self, request):
        if self._async:
            return self.__acall__(request)
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))
        return self.get_response(request)

    async def __acall__(self, request):
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))
        return await self.get_response(request)
```

Install via `MIDDLEWARE = [..., "asgi_user_agents.contrib.django.UserAgentMiddleware"]`.

## Resolution (`utils.get_user_agent`)

`utils.py` — `get_user_agent(request)` implements the scope-first resolution and is the single source of `request.user_agent`. No caching in v1; it returns a `UADetails` directly. The three-branch ordering (reuse `scope["ua"]` → `UADetails(request.scope)` → synthesize from `request.headers`) lives here.

## Packaging

`pyproject.toml` adds:

```toml
[project.optional-dependencies]
django = ["django>=3.2"]
```

Install: `pip install asgi-user-agents[django]`. (`asgiref` arrives transitively with Django.)

## Error Handling

- Missing Django → standard `ImportError` from the `import` line.
- Missing/empty UA header → `UADetails` already tolerates it (`is_provided` is `False`, all `is_*` return `False`).
- No new exception paths.

## Testing

New file `tests/test_django_contrib.py` (additive; existing tests untouched). Uses Django's `SimpleTestCase`/`RequestFactory` configured via `settings.configure(...)`:

- **ASGI reuse:** scope carrying a `UADetails` under `"ua"` → `get_user_agent` returns that same instance.
- **ASGI no-middleware:** request with `scope` but no `"ua"` → builds a correct `UADetails`.
- **WSGI fallback:** `RequestFactory` request (no `scope`) with a `HTTP_USER_AGENT` header → correct `UADetails`.
- **Template filters:** render `{% load asgi_user_agents %}{{ request|is_mobile }}` etc. against the canonical `assets/test_middleware.json` fixture.

`hatch-test` env adds `django`.

## Documentation (README)

Add a "Django" subsection under "Framework integrations": `INSTALLED_APPS` + `MIDDLEWARE` setup, a view example (`request.user_agent.is_mobile`), and a template example. Note it reuses `scope["ua"]` under ASGI and falls back to header parsing under WSGI.

## Backward Compatibility

- All existing top-level exports untouched.
- Existing tests unmodified.
- No core files modified — the contrib is entirely additive.
```
