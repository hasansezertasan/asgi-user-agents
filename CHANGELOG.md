# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

### Added

* ✨ Add `contrib` integration for Django: a sync/async `UserAgentMiddleware` attaching a lazy `request.user_agent`, the `{% load asgi_user_agents %}` template filters (`is_mobile`, `is_pc`, `is_tablet`, `is_bot`, `is_touch_capable`), and a `[django]` extra. Reuses `scope["ua"]` under ASGI and falls back to header parsing under WSGI.

## [0.3.0] - 2026-06-08

### Added

* ✨ Add `contrib` integrations for Litestar and FastAPI. by [@hasansezertasan](https://github.com/hasansezertasan) in [#109](https://github.com/hasansezertasan/asgi-user-agents/pull/109)
* ✨ Project can be used with `uv`; `cd.yml` uses `uv` to publish to PyPI. by [@hasansezertasan](https://github.com/hasansezertasan) in [#42](https://github.com/hasansezertasan/asgi-user-agents/pull/42)
* ✨ Add GitHub Actions workflow to lint pull request titles for Conventional Commits compliance. by [@hasansezertasan](https://github.com/hasansezertasan) in [#45](https://github.com/hasansezertasan/asgi-user-agents/pull/45)
* Add `user-agent` keyword to PyPI configuration. by [@hasansezertasan](https://github.com/hasansezertasan) in [#20](https://github.com/hasansezertasan/asgi-user-agents/pull/20)

### Changed

* 💥 Drop Python 3.8 and 3.9 support; add Python 3.14. by [@hasansezertasan](https://github.com/hasansezertasan) in [#110](https://github.com/hasansezertasan/asgi-user-agents/pull/110)
* Remove duplicate `__version__` and `__all__` tags from `__init__.py`; implement relative imports. by [@hasansezertasan](https://github.com/hasansezertasan) in [#19](https://github.com/hasansezertasan/asgi-user-agents/pull/19)

### Fixed

* 🐛 Preserve pre-populated UA scope entries in middleware. by [@hasansezertasan](https://github.com/hasansezertasan) in [#68](https://github.com/hasansezertasan/asgi-user-agents/pull/68)
* 🐛 Avoid parsing missing `user-agent` headers. by [@hasansezertasan](https://github.com/hasansezertasan) in [#69](https://github.com/hasansezertasan/asgi-user-agents/pull/69)
* ♻️ Pass application to `AsyncClient` through `ASGITransport` in tests. by [@hasansezertasan](https://github.com/hasansezertasan) in [#35](https://github.com/hasansezertasan/asgi-user-agents/pull/35)

### Internal

* 🔧 Add `codespell` hook for spell checking and `check-jsonschema` for GitHub Actions validation. by [@hasansezertasan](https://github.com/hasansezertasan) in [#18](https://github.com/hasansezertasan/asgi-user-agents/pull/18)
* 🔧 Update `ruff` configuration: remove defaults and extend rules by `ALL`. by [@hasansezertasan](https://github.com/hasansezertasan) in [#24](https://github.com/hasansezertasan/asgi-user-agents/pull/24)
* 🔧 Configure Renovate; remove Dependabot. by [@renovate\[bot\]](https://github.com/apps/renovate) in [#27](https://github.com/hasansezertasan/asgi-user-agents/pull/27) and by [@hasansezertasan](https://github.com/hasansezertasan) in [#39](https://github.com/hasansezertasan/asgi-user-agents/pull/39)
* 🔧 Replace previous publish workflow with `cd` workflow; migrate to PyPI Trusted Publishing. by [@hasansezertasan](https://github.com/hasansezertasan) in [#33](https://github.com/hasansezertasan/asgi-user-agents/pull/33)
* 🔧 Use a more generic `.gitignore`. by [@hasansezertasan](https://github.com/hasansezertasan) in [#34](https://github.com/hasansezertasan/asgi-user-agents/pull/34)
* 🔧 Update PR title format. by [@hasansezertasan](https://github.com/hasansezertasan) in [#46](https://github.com/hasansezertasan/asgi-user-agents/pull/46)
* 🔧 Migrate Codecov to v5. by [@hasansezertasan](https://github.com/hasansezertasan) in [#48](https://github.com/hasansezertasan/asgi-user-agents/pull/48)
* 🔧 Rename CD environment to `publish` and update artifact attachment step description. by [@hasansezertasan](https://github.com/hasansezertasan) in [#49](https://github.com/hasansezertasan/asgi-user-agents/pull/49)
* 📝 Update docstrings for user-agent data retrieval in FastAPI, Litestar, Quart, and Starlette tests. by [@hasansezertasan](https://github.com/hasansezertasan) in [#50](https://github.com/hasansezertasan/asgi-user-agents/pull/50)

## [0.2.0] - 2024-05-26

### Internal

* 🔧 Update CI workflow, by adding `codecov/codecov-action`. by [@hasansezertasan](https://github.com/hasansezertasan) in [#13](https://github.com/hasansezertasan/asgi-user-agents/pull/13)
* 🔧 Update CI workflow, by adding `Run Coverage` step. by [@hasansezertasan](https://github.com/hasansezertasan) in [#14](https://github.com/hasansezertasan/asgi-user-agents/pull/14)
* 🔧 Update CI workflow, by adding `files: .coverage` configuration to `Upload coverage reports to Codecov` step so the action can properly upload the coverage report. by [@hasansezertasan](https://github.com/hasansezertasan) in [#15](https://github.com/hasansezertasan/asgi-user-agents/pull/15)

### Changed

* Bump `Development Status` classifier from `1 - Planning` to `3 - Alpha`. by [@hasansezertasan](https://github.com/hasansezertasan) in [#16](https://github.com/hasansezertasan/asgi-user-agents/pull/16)
* Release 0.2.0 by [@hasansezertasan](https://github.com/hasansezertasan) in [#17](https://github.com/hasansezertasan/asgi-user-agents/pull/17)

## [0.1.0] - 2024-05-26

* Initial release.

### Added

* CI/CD Pipelines added. by [@hasansezertasan](https://github.com/hasansezertasan) in [#1](https://github.com/hasansezertasan/asgi-user-agents/pull/1)
* Update branch names on CI/CD Pipelines. by [@hasansezertasan](https://github.com/hasansezertasan) in [#2](https://github.com/hasansezertasan/asgi-user-agents/pull/2)
* Add `Scope`, `Message`, `Receive`, `Send`, and `ASGIApp` types from `starlette.types` for type hinting. by [@hasansezertasan](https://github.com/hasansezertasan) in [#3](https://github.com/hasansezertasan/asgi-user-agents/pull/3)
* Add `UADetails` data structure that provides information about the user agent extracted from the request headers. by [@hasansezertasan](https://github.com/hasansezertasan) in [#4](https://github.com/hasansezertasan/asgi-user-agents/pull/4)
* Add `UARequest` that facilitates type hinting `request.scope["ua"]` in Starlette-based frameworks. by [@hasansezertasan](https://github.com/hasansezertasan) in [#5](https://github.com/hasansezertasan/asgi-user-agents/pull/5)
* Add `UAMiddleware` that automatically adds an `UADetails` instance as `scope["ua"]`. by [@hasansezertasan](https://github.com/hasansezertasan) in [#6](https://github.com/hasansezertasan/asgi-user-agents/pull/6)
* Add `py.typed` file to indicate that the package supports type hinting. by [@hasansezertasan](https://github.com/hasansezertasan) in [#7](https://github.com/hasansezertasan/asgi-user-agents/pull/7)
* Add `__init__.py` and `__about__.py` files to the `src/asgi_user_agents` directory to make it a package. by [@hasansezertasan](https://github.com/hasansezertasan) in [#8](https://github.com/hasansezertasan/asgi-user-agents/pull/8)
* Add tests for the `UADetails`, `UARequest`, and `UAMiddleware` classes with over 90% coverage. by [@hasansezertasan](https://github.com/hasansezertasan) in [#9](https://github.com/hasansezertasan/asgi-user-agents/pull/9)
* Add `README.md` with usage instructions, development guide, and simple API reference. by [@hasansezertasan](https://github.com/hasansezertasan) in [#10](https://github.com/hasansezertasan/asgi-user-agents/pull/10)
* Add `CHANGELOG.md` to document the changes in the project. by [@hasansezertasan](https://github.com/hasansezertasan) in [#11](https://github.com/hasansezertasan/asgi-user-agents/pull/11)
* Update `CHANGELOG.md` to include the changes in the project. by [@hasansezertasan](https://github.com/hasansezertasan) in [#12](https://github.com/hasansezertasan/asgi-user-agents/pull/12)

<!-- Links -->
[keep a changelog]: https://keepachangelog.com/en/1.1.0/
[semantic versioning]: https://semver.org

<!-- Versions -->
[unreleased]: https://github.com/hasansezertasan/asgi-user-agents/compare/0.3.0...HEAD
[0.3.0]: https://github.com/hasansezertasan/asgi-user-agents/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/hasansezertasan/asgi-user-agents/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/hasansezertasan/asgi-user-agents/releases/tag/0.1.0
