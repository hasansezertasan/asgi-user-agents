# Contrib Integrations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `asgi_user_agents.contrib.litestar` (UAPlugin) and `asgi_user_agents.contrib.fastapi` (UADep, install_ua, etc.) per the approved spec at `docs/superpowers/specs/2026-06-08-contrib-integrations-design.md`.

**Architecture:** Two parallel framework-specific subpackages under a new `contrib/` namespace. Both expose two flavors of DI — the project's `UADetails` wrapper and the raw `user_agents.UserAgent`. FastAPI also exposes an idempotent `install_ua(app)` helper for adding the existing `UAMiddleware`. No changes to existing top-level APIs.

**Tech Stack:** Python 3.8+, `user-agents`, Litestar 2.x (extra), FastAPI 0.110+ (extra), Starlette (transitive), `typing_extensions` (for `Annotated` on 3.8), pytest + httpx for tests, hatch for env management.

---

## File Structure

**Create:**
- `src/asgi_user_agents/contrib/__init__.py` — empty namespace marker
- `src/asgi_user_agents/contrib/litestar/__init__.py` — re-exports
- `src/asgi_user_agents/contrib/litestar/plugin.py` — `UAPlugin`, `provide_ua`, `provide_user_agent`
- `src/asgi_user_agents/contrib/fastapi/__init__.py` — re-exports
- `src/asgi_user_agents/contrib/fastapi/dependencies.py` — `get_ua`, `get_user_agent`, `UADep`, `UserAgentDep`, `install_ua`
- `tests/test_litestar_plugin.py` — DI behavior + non-clobber
- `tests/test_fastapi_contrib.py` — DI behavior + `install_ua` idempotency

**Modify:**
- `pyproject.toml` — add `[project.optional-dependencies]` with `litestar` and `fastapi` extras; add `typing_extensions` to core deps
- `README.md` — add "Framework integrations" section

**Untouched:**
- `src/asgi_user_agents/__init__.py`, `middleware.py`, `datastructures.py`, `requests.py`, `_types.py`
- Existing tests (`test_fastapi.py`, `test_litestar.py`, `test_starlette.py`, `test_quart.py`, `test_datastructures.py`)

---

## Task 1: Bootstrap contrib namespace + packaging

**Files:**
- Create: `src/asgi_user_agents/contrib/__init__.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Create empty contrib namespace**

Create `src/asgi_user_agents/contrib/__init__.py` with content:

```python
"""Framework-specific integration subpackages.

Each subpackage requires its framework as an optional extra:
- `pip install asgi-user-agents[litestar]`
- `pip install asgi-user-agents[fastapi]`
"""
```

- [ ] **Step 2: Add extras and typing_extensions to pyproject.toml**

In `pyproject.toml`, change the `dependencies` line under `[project]` from:

```toml
dependencies = ["user-agents"]
```

to:

```toml
dependencies = ["user-agents", "typing_extensions>=4.0.0"]

[project.optional-dependencies]
litestar = ["litestar>=2.0.0,<3.0.0"]
fastapi = ["fastapi>=0.110.0,<1.0.0"]
```

Place the `[project.optional-dependencies]` block immediately after the `dependencies = [...]` line and before the blank line preceding `[project.urls]`.

- [ ] **Step 3: Verify package still imports**

Run: `hatch run python -c "import asgi_user_agents; print(asgi_user_agents.UAMiddleware)"`
Expected: prints `<class 'asgi_user_agents.middleware.UAMiddleware'>` (no errors)

- [ ] **Step 4: Verify contrib namespace imports**

Run: `hatch run python -c "import asgi_user_agents.contrib"`
Expected: no output, no error

- [ ] **Step 5: Commit**

```bash
git add src/asgi_user_agents/contrib/__init__.py pyproject.toml
git commit -m "feat(contrib): bootstrap contrib namespace and per-framework extras"
```

---

## Task 2: Litestar plugin — failing test

**Files:**
- Test: `tests/test_litestar_plugin.py`

- [ ] **Step 1: Write the failing test file**

Create `tests/test_litestar_plugin.py`:

```python
"""Tests for the Litestar contrib plugin."""

from __future__ import annotations

from typing import Any, Dict

import parametrize_from_file as pff
import pytest
from httpx import ASGITransport, AsyncClient
from litestar import Litestar, get
from litestar.di import Provide
from user_agents.parsers import UserAgent

from asgi_user_agents import UADetails
from asgi_user_agents.contrib.litestar import UAPlugin


@get("/")
async def index(ua: UADetails, user_agent: UserAgent) -> Dict[str, Any]:
    """Return user-agent data via injected dependencies."""
    assert isinstance(ua, UADetails)
    assert isinstance(user_agent, UserAgent)
    return {
        "ua_string": ua.ua_string,
        "os": ua.os,
        "os.family": ua.os.family,
        "os.version": ua.os.version,
        "os.version_string": ua.os.version_string,
        "browser": ua.browser,
        "browser.family": ua.ua.browser.family,
        "browser.version": ua.ua.browser.version,
        "browser.version_string": ua.ua.browser.version_string,
        "device": ua.device,
        "device.family": ua.device.family,
        "device.brand": ua.device.brand,
        "device.model": ua.device.model,
        "is_provided": ua.is_provided,
        "is_tablet": ua.is_tablet,
        "is_mobile": ua.is_mobile,
        "is_touch_capable": ua.is_touch_capable,
        "is_pc": ua.is_pc,
        "is_bot": ua.is_bot,
        "is_email_client": ua.is_email_client,
        "raw_family": user_agent.browser.family,
    }


app = Litestar(route_handlers=[index], plugins=[UAPlugin()])


@pytest.mark.asyncio
@pff.parametrize(path="assets/test_middleware.json")
async def test_user_agent_data(ua_string: str, response_data: dict) -> None:
    """Test that both injected dependencies produce the expected data."""
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver"
    ) as client:
        response = await client.get("/", headers={"User-Agent": ua_string})
        data = response.json()
        assert data["ua_string"] == response_data["ua_string"]
        assert data["os.family"] == response_data["os.family"]
        assert data["browser.family"] == response_data["browser.family"]
        assert data["device.family"] == response_data["device.family"]
        assert data["is_bot"] is response_data["is_bot"]
        assert data["is_mobile"] is response_data["is_mobile"]
        assert data["raw_family"] == response_data["browser.family"]


@pytest.mark.asyncio
async def test_plugin_does_not_clobber_existing_dependencies() -> None:
    """If `ua` is already registered, the plugin must not overwrite it."""

    async def custom_ua() -> str:
        return "custom"

    @get("/custom")
    async def handler(ua: str) -> Dict[str, str]:
        return {"ua": ua}

    local_app = Litestar(
        route_handlers=[handler],
        dependencies={"ua": Provide(custom_ua, sync_to_thread=False)},
        plugins=[UAPlugin()],
    )

    async with AsyncClient(
        transport=ASGITransport(local_app), base_url="http://testserver"
    ) as client:
        response = await client.get("/custom")
        assert response.json() == {"ua": "custom"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `hatch test tests/test_litestar_plugin.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'asgi_user_agents.contrib.litestar'`

---

## Task 3: Litestar plugin — implementation

**Files:**
- Create: `src/asgi_user_agents/contrib/litestar/__init__.py`
- Create: `src/asgi_user_agents/contrib/litestar/plugin.py`

- [ ] **Step 1: Create plugin.py**

Create `src/asgi_user_agents/contrib/litestar/plugin.py`:

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
    """Provide a `UADetails` instance built from the current request scope."""
    return UADetails(request.scope)


def provide_user_agent(request: Request) -> UserAgent:
    """Provide a raw `user_agents.UserAgent` for the current request."""
    return UserAgent(request.headers.get("user-agent", ""))


class UAPlugin(InitPluginProtocol):
    """Register `ua: UADetails` and `user_agent: UserAgent` as Litestar dependencies."""

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Register UA dependencies without clobbering user-provided ones."""
        app_config.dependencies.setdefault(
            "ua", Provide(provide_ua, sync_to_thread=False)
        )
        app_config.dependencies.setdefault(
            "user_agent", Provide(provide_user_agent, sync_to_thread=False)
        )
        return app_config
```

- [ ] **Step 2: Create __init__.py with re-exports**

Create `src/asgi_user_agents/contrib/litestar/__init__.py`:

```python
"""Litestar integration for asgi-user-agents."""

from asgi_user_agents.contrib.litestar.plugin import (
    UAPlugin as UAPlugin,
    provide_ua as provide_ua,
    provide_user_agent as provide_user_agent,
)
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `hatch test tests/test_litestar_plugin.py -v`
Expected: both tests PASS (parametrized cases for `test_user_agent_data` plus `test_plugin_does_not_clobber_existing_dependencies`)

- [ ] **Step 4: Run existing Litestar test to confirm no regression**

Run: `hatch test tests/test_litestar.py -v`
Expected: all parametrized cases PASS

- [ ] **Step 5: Commit**

```bash
git add src/asgi_user_agents/contrib/litestar tests/test_litestar_plugin.py
git commit -m "feat(contrib): add Litestar UAPlugin with ua/user_agent DI"
```

---

## Task 4: FastAPI contrib — failing test

**Files:**
- Test: `tests/test_fastapi_contrib.py`

- [ ] **Step 1: Write the failing test file**

Create `tests/test_fastapi_contrib.py`:

```python
"""Tests for the FastAPI contrib dependencies."""

from __future__ import annotations

from typing import Any, Dict

import parametrize_from_file as pff
import pytest
from fastapi.applications import FastAPI
from httpx import ASGITransport, AsyncClient
from starlette.responses import JSONResponse, Response

from asgi_user_agents import UADetails, UAMiddleware
from asgi_user_agents.contrib.fastapi import (
    UADep,
    UserAgentDep,
    get_ua,
    get_user_agent,
    install_ua,
)


app = install_ua(FastAPI())


@app.get("/")
async def index(ua: UADep, user_agent: UserAgentDep) -> Response:
    """Return user-agent data via injected dependencies."""
    assert isinstance(ua, UADetails)
    data: Dict[str, Any] = {
        "ua_string": ua.ua_string,
        "os.family": ua.os.family,
        "browser.family": ua.browser.family,
        "device.family": ua.device.family,
        "is_provided": ua.is_provided,
        "is_mobile": ua.is_mobile,
        "is_bot": ua.is_bot,
        "raw_family": user_agent.browser.family,
    }
    return JSONResponse(data)


@pytest.mark.asyncio
@pff.parametrize(path="assets/test_middleware.json")
async def test_user_agent_data(ua_string: str, response_data: dict) -> None:
    """Test that both injected dependencies match the expected data."""
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver"
    ) as client:
        response = await client.get("/", headers={"User-Agent": ua_string})
        data = response.json()
        assert data["ua_string"] == response_data["ua_string"]
        assert data["os.family"] == response_data["os.family"]
        assert data["browser.family"] == response_data["browser.family"]
        assert data["device.family"] == response_data["device.family"]
        assert data["is_bot"] is response_data["is_bot"]
        assert data["is_mobile"] is response_data["is_mobile"]
        assert data["raw_family"] == response_data["browser.family"]


def test_install_ua_is_idempotent() -> None:
    """Calling install_ua twice must result in exactly one UAMiddleware entry."""
    fresh = FastAPI()
    install_ua(fresh)
    install_ua(fresh)
    ua_entries = [m for m in fresh.user_middleware if m.cls is UAMiddleware]
    assert len(ua_entries) == 1


def test_install_ua_returns_app() -> None:
    """install_ua must return the app for chaining."""
    fresh = FastAPI()
    assert install_ua(fresh) is fresh


def test_plain_dependency_functions_exist() -> None:
    """get_ua and get_user_agent must be importable and callable."""
    assert callable(get_ua)
    assert callable(get_user_agent)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `hatch test tests/test_fastapi_contrib.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'asgi_user_agents.contrib.fastapi'`

---

## Task 5: FastAPI contrib — implementation

**Files:**
- Create: `src/asgi_user_agents/contrib/fastapi/__init__.py`
- Create: `src/asgi_user_agents/contrib/fastapi/dependencies.py`

- [ ] **Step 1: Create dependencies.py**

Create `src/asgi_user_agents/contrib/fastapi/dependencies.py`:

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
    """Install `UAMiddleware` on `app` if not already installed. Returns the app."""
    if not any(m.cls is UAMiddleware for m in app.user_middleware):
        app.add_middleware(UAMiddleware)
    return app
```

- [ ] **Step 2: Create __init__.py with re-exports**

Create `src/asgi_user_agents/contrib/fastapi/__init__.py`:

```python
"""FastAPI integration for asgi-user-agents."""

from asgi_user_agents.contrib.fastapi.dependencies import (
    UADep as UADep,
    UserAgentDep as UserAgentDep,
    get_ua as get_ua,
    get_user_agent as get_user_agent,
    install_ua as install_ua,
)
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `hatch test tests/test_fastapi_contrib.py -v`
Expected: all tests PASS (parametrized `test_user_agent_data`, `test_install_ua_is_idempotent`, `test_install_ua_returns_app`, `test_plain_dependency_functions_exist`)

- [ ] **Step 4: Run existing FastAPI test to confirm no regression**

Run: `hatch test tests/test_fastapi.py -v`
Expected: all parametrized cases PASS

- [ ] **Step 5: Commit**

```bash
git add src/asgi_user_agents/contrib/fastapi tests/test_fastapi_contrib.py
git commit -m "feat(contrib): add FastAPI deps and install_ua helper"
```

---

## Task 6: Full test sweep + lint + types

**Files:** (no edits — verification only)

- [ ] **Step 1: Run the full test suite**

Run: `hatch test -v`
Expected: every test passes (existing + 2 new test files). No failures, no errors.

- [ ] **Step 2: Run linting**

Run: `hatch run types:style`
Expected: no errors. If `ruff` flags new code, fix the specific complaints in-place (do NOT silence lints with `# noqa` unless the existing codebase does so for the same rule).

- [ ] **Step 3: Run formatting**

Run: `hatch run types:format`
Expected: no changes, or only auto-applied formatting. If files were reformatted, stage them.

- [ ] **Step 4: Run type checking**

Run: `hatch run types:typing`
Expected: `Success: no issues found` across `src/` and `tests/`.

- [ ] **Step 5: Commit any lint/format/type fixups (only if needed)**

If steps 2–4 produced any code changes:

```bash
git add -u
git commit -m "style(contrib): apply lint/format fixes"
```

If no changes, skip this commit.

---

## Task 7: Update README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read the existing Usage section to find insertion point**

Run: `grep -n "^## " README.md`
Identify the line number where `## Usage` ends (i.e., the line of the next `## ` heading after Usage). The new section is inserted before that next heading.

- [ ] **Step 2: Insert the Framework integrations section**

Insert the following block immediately before the heading that follows `## Usage`:

````markdown
## Framework integrations

For Litestar and FastAPI, optional `contrib` subpackages provide
framework-idiomatic access. The core `UAMiddleware` still works for any
ASGI framework — `contrib` is additive convenience.

Install with the relevant extra:

```bash
pip install asgi-user-agents[litestar]
pip install asgi-user-agents[fastapi]
```

### Litestar

Use `UAPlugin` to inject `ua: UADetails` and `user_agent: UserAgent`
into route handlers. No middleware needed.

```python
from litestar import Litestar, get

from asgi_user_agents import UADetails
from asgi_user_agents.contrib.litestar import UAPlugin


@get("/")
async def index(ua: UADetails) -> dict:
    return {"is_bot": ua.is_bot, "browser": ua.browser.family}


app = Litestar(route_handlers=[index], plugins=[UAPlugin()])
```

If you already registered a dependency named `ua` or `user_agent`,
`UAPlugin` will not overwrite it.

### FastAPI

Use `install_ua(app)` plus the prebuilt `UADep` / `UserAgentDep`
annotated dependencies.

```python
from fastapi import FastAPI

from asgi_user_agents.contrib.fastapi import UADep, install_ua

app = install_ua(FastAPI())


@app.get("/")
async def index(ua: UADep) -> dict:
    return {"is_bot": ua.is_bot, "browser": ua.browser.family}
```

`install_ua` is idempotent. The plain dependency functions `get_ua`
and `get_user_agent` are also exported if you prefer to wire them
yourself.

````

- [ ] **Step 3: Verify the README renders correctly**

Run: `grep -c "Framework integrations" README.md`
Expected: `1`

- [ ] **Step 4: Update the table of contents if one exists**

Run: `grep -n "Framework integrations" README.md`

If the README has a `<!-- toc -->` block (it does, per the existing structure), regenerate or hand-edit so the TOC includes the new section. To hand-edit: in the `<!-- toc -->`/`<!-- tocstop -->` block, add the lines:

```markdown
- [Framework integrations](#framework-integrations)
  - [Litestar](#litestar)
  - [FastAPI](#fastapi)
```

Insert these alphabetically/logically — right after `- [Usage](#usage)` and before the next existing item.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: document contrib integrations for Litestar and FastAPI"
```

---

## Self-Review Results

**Spec coverage check:**
- Layout (`contrib/`, two subpackages, empty namespace) → Task 1, Task 3, Task 5 ✓
- Packaging (extras, no `[all]`, typing_extensions) → Task 1 ✓
- Litestar `UAPlugin`, `provide_ua`, `provide_user_agent`, `setdefault`, `sync_to_thread=False` → Task 3 ✓
- Non-clobber behavior → Task 2 (test), Task 3 (impl) ✓
- FastAPI `get_ua`, `get_user_agent`, `UADep`, `UserAgentDep`, `install_ua` → Task 4, Task 5 ✓
- `install_ua` idempotency + returns app → Task 4 (tests), Task 5 (impl) ✓
- Top-level API untouched → enforced by file structure; verified implicitly by running existing tests in Task 3 step 4 and Task 5 step 4 ✓
- README docs → Task 7 ✓
- Test coverage reuses `assets/test_middleware.json` → Task 2, Task 4 ✓

**Placeholder scan:** No "TBD", no vague "handle edge cases", every step has runnable code or commands.

**Type consistency:** `UAPlugin`, `provide_ua`/`provide_user_agent`, `get_ua`/`get_user_agent`, `UADep`/`UserAgentDep`, `install_ua` — names and signatures match across tasks and the spec.
