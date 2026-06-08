# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

* Nothing yet.

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

### Dependencies

* ⬆️ Bump `ruff` from `0.4.5` → `0.15.16`. ([#23](https://github.com/hasansezertasan/asgi-user-agents/pull/23), [#38](https://github.com/hasansezertasan/asgi-user-agents/pull/38), [#37](https://github.com/hasansezertasan/asgi-user-agents/pull/37), [#47](https://github.com/hasansezertasan/asgi-user-agents/pull/47), [#52](https://github.com/hasansezertasan/asgi-user-agents/pull/52), [#55](https://github.com/hasansezertasan/asgi-user-agents/pull/55), [#58](https://github.com/hasansezertasan/asgi-user-agents/pull/58), [#62](https://github.com/hasansezertasan/asgi-user-agents/pull/62), [#72](https://github.com/hasansezertasan/asgi-user-agents/pull/72), [#77](https://github.com/hasansezertasan/asgi-user-agents/pull/77), [#81](https://github.com/hasansezertasan/asgi-user-agents/pull/81), [#83](https://github.com/hasansezertasan/asgi-user-agents/pull/83), [#89](https://github.com/hasansezertasan/asgi-user-agents/pull/89), [#95](https://github.com/hasansezertasan/asgi-user-agents/pull/95), [#99](https://github.com/hasansezertasan/asgi-user-agents/pull/99), [#102](https://github.com/hasansezertasan/asgi-user-agents/pull/102), [#106](https://github.com/hasansezertasan/asgi-user-agents/pull/106))
* ⬆️ Bump `uvicorn` constraint through `>=0.48.0,<0.49.0`. ([#40](https://github.com/hasansezertasan/asgi-user-agents/pull/40), [#63](https://github.com/hasansezertasan/asgi-user-agents/pull/63), [#75](https://github.com/hasansezertasan/asgi-user-agents/pull/75), [#84](https://github.com/hasansezertasan/asgi-user-agents/pull/84), [#92](https://github.com/hasansezertasan/asgi-user-agents/pull/92), [#94](https://github.com/hasansezertasan/asgi-user-agents/pull/94), [#100](https://github.com/hasansezertasan/asgi-user-agents/pull/100), [#103](https://github.com/hasansezertasan/asgi-user-agents/pull/103))
* ⬆️ Bump `fastapi` constraint through `>=0.136.0,<0.137.0`. ([#31](https://github.com/hasansezertasan/asgi-user-agents/pull/31), [#64](https://github.com/hasansezertasan/asgi-user-agents/pull/64), [#70](https://github.com/hasansezertasan/asgi-user-agents/pull/70), [#87](https://github.com/hasansezertasan/asgi-user-agents/pull/87))
* ⬆️ Bump `httpx` to `>=0.28.1,<0.29.0`. ([#32](https://github.com/hasansezertasan/asgi-user-agents/pull/32))
* ⬆️ Bump `codespell` to `v2.4.2`. ([#29](https://github.com/hasansezertasan/asgi-user-agents/pull/29), [#73](https://github.com/hasansezertasan/asgi-user-agents/pull/73))
* ⬆️ Bump `parametrize_from_file` to `v0.21.0`. ([#97](https://github.com/hasansezertasan/asgi-user-agents/pull/97))
* ⬆️ Bump `pre-commit` to `>=4.6.0,<4.7.0` and routine `pre-commit.ci` autoupdates. ([#44](https://github.com/hasansezertasan/asgi-user-agents/pull/44), [#93](https://github.com/hasansezertasan/asgi-user-agents/pull/93), [#22](https://github.com/hasansezertasan/asgi-user-agents/pull/22), [#51](https://github.com/hasansezertasan/asgi-user-agents/pull/51), [#57](https://github.com/hasansezertasan/asgi-user-agents/pull/57), [#59](https://github.com/hasansezertasan/asgi-user-agents/pull/59), [#71](https://github.com/hasansezertasan/asgi-user-agents/pull/71), [#78](https://github.com/hasansezertasan/asgi-user-agents/pull/78), [#82](https://github.com/hasansezertasan/asgi-user-agents/pull/82), [#85](https://github.com/hasansezertasan/asgi-user-agents/pull/85), [#86](https://github.com/hasansezertasan/asgi-user-agents/pull/86), [#91](https://github.com/hasansezertasan/asgi-user-agents/pull/91), [#96](https://github.com/hasansezertasan/asgi-user-agents/pull/96), [#98](https://github.com/hasansezertasan/asgi-user-agents/pull/98))
* ⬆️ Bump `codecov/codecov-action` to `v6.0.1`. ([#21](https://github.com/hasansezertasan/asgi-user-agents/pull/21), [#26](https://github.com/hasansezertasan/asgi-user-agents/pull/26), [#28](https://github.com/hasansezertasan/asgi-user-agents/pull/28), [#41](https://github.com/hasansezertasan/asgi-user-agents/pull/41), [#56](https://github.com/hasansezertasan/asgi-user-agents/pull/56), [#61](https://github.com/hasansezertasan/asgi-user-agents/pull/61), [#76](https://github.com/hasansezertasan/asgi-user-agents/pull/76), [#80](https://github.com/hasansezertasan/asgi-user-agents/pull/80), [#101](https://github.com/hasansezertasan/asgi-user-agents/pull/101))
* ⬆️ Bump `actions/checkout` to `v6`, `actions/setup-python` to `v6`, `astral-sh/setup-uv` to `v8`. ([#53](https://github.com/hasansezertasan/asgi-user-agents/pull/53), [#60](https://github.com/hasansezertasan/asgi-user-agents/pull/60), [#66](https://github.com/hasansezertasan/asgi-user-agents/pull/66), [#67](https://github.com/hasansezertasan/asgi-user-agents/pull/67), [#88](https://github.com/hasansezertasan/asgi-user-agents/pull/88))
* ⬆️ Bump `amannn/action-semantic-pull-request` to `v6` and `marocchino/sticky-pull-request-comment` to `v3`. ([#54](https://github.com/hasansezertasan/asgi-user-agents/pull/54), [#74](https://github.com/hasansezertasan/asgi-user-agents/pull/74))
* ⬆️ Bump `python` Docker tag to `3.14`. ([#65](https://github.com/hasansezertasan/asgi-user-agents/pull/65), [#111](https://github.com/hasansezertasan/asgi-user-agents/pull/111))

### New Contributors

* [@dependabot\[bot\]](https://github.com/apps/dependabot) made their first contribution in [#21](https://github.com/hasansezertasan/asgi-user-agents/pull/21)
* [@pre-commit-ci\[bot\]](https://github.com/apps/pre-commit-ci) made their first contribution in [#22](https://github.com/hasansezertasan/asgi-user-agents/pull/22)
* [@renovate\[bot\]](https://github.com/apps/renovate) made their first contribution in [#27](https://github.com/hasansezertasan/asgi-user-agents/pull/27)

**Full Changelog**: <https://github.com/hasansezertasan/asgi-user-agents/compare/0.2.0...0.3.0>

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
