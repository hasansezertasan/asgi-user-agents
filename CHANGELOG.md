# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

* Nothing yet.

## [0.3.0] - 2026-06-08

### What's Changed

* 🔧 Add codespell hook for spell checking and check-jsonschema for GitHub action validation by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/18
* Bump codecov/codecov-action from 4.0.1 to 4.4.1 by @dependabot[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/21
* Remove duplicate `__version__` tag alongside with `__all__` tag from `__init__.py` and implement relative imports. by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/19
* Add `user-agent` keyword to PyPI configuration by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/20
* Bump `ruff` from 0.4.5 to 0.4.7 by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/23
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/22
* Update `ruff` configuration: remove defaults and extend rules by `ALL`. by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/24
* Configure Renovate by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/27
* Bump codecov/codecov-action from 4.4.1 to 4.5.0 by @dependabot[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/26
* Update codecov/codecov-action action to v4.6.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/28
* ci(publishing): replacing the previous publish workflow with cd workflow, migrating to trusted host publishing by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/33
* Update dependency codespell to v2.4.1 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/29
* Update dependency fastapi to >=0.116.1, <0.117.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/31
* chore(gitignore): use more generic gitignore by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/34
* refactor(ASGITransport): pass application to AsyncClient through ASGITransport by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/35
* Update dependency httpx to >=0.28.1, <0.29.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/32
* deps(ruff): bump `ruff` from 0.4.5 to 0.12.5 by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/38
* chore(dependabot): remove by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/39
* feat(uv): project can be used with uv and cd.yml now uses uv to publish to pypi by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/42
* feat(ci): add GitHub Actions workflow to lint pull request titles for Conventional Commits compliance by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/45
* chore(pre-commit): update pr title format by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/46
* chore(deps): update dependency ruff to v0.12.6 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/37
* chore(deps): update codecov/codecov-action action to v5 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/41
* chore(deps): update dependency ruff to v0.12.7 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/47
* ci(codecov): migrate to v5 by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/48
* chore(cd): rename environment to 'publish' and update artifact attachment step description by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/49
* chore(docs): update docstrings for user-agent data retrieval in FastAPI, Litestar, Quart, and Starlette tests by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/50
* chore(deps): update dependency ruff to v0.12.8 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/52
* chore(deps): update dependency uvicorn to >=0.35.0,<0.36.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/40
* chore(deps): update actions/checkout action to v5 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/53
* chore(deps): update amannn/action-semantic-pull-request action to v6 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/54
* chore(deps): update codecov/codecov-action action to v5.5.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/56
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/51
* chore(deps): update dependency ruff to v0.12.10 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/55
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/57
* chore(deps): update dependency ruff to v0.12.11 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/58
* chore(deps): update python docker tag to v3.14 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/65
* chore(deps): update actions/checkout action to v6 - autoclosed by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/67
* chore(deps): update astral-sh/setup-uv action to v7 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/66
* chore(deps): update actions/setup-python action to v6 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/60
* chore(deps): update codecov/codecov-action action to v5.5.2 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/61
* chore(deps): update dependency pre-commit to v4 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/44
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/59
* chore(deps): update dependency ruff to v0.15.2 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/62
* chore(deps): update dependency fastapi to >=0.129.0,<0.130.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/64
* chore(deps): update dependency uvicorn to >=0.41.0,<0.42.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/63
* refactor: preserve pre-populated UA scope entries in middleware by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/68
* refactor: avoid parsing missing user-agent headers by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/69
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/71
* chore(deps): update dependency uvicorn to >=0.42.0,<0.43.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/75
* chore(deps): update marocchino/sticky-pull-request-comment action to v3 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/74
* chore(deps): update dependency ruff to v0.15.6 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/72
* chore(deps): update dependency fastapi to >=0.135.1,<0.136.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/70
* chore(deps): update dependency codespell to v2.4.2 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/73
* chore(deps): update dependency ruff to v0.15.7 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/77
* chore(deps): update codecov/codecov-action action to v5.5.3 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/76
* chore(deps): update dependency ruff to v0.15.8 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/81
* chore(deps): update codecov/codecov-action action to v6 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/80
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/78
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/82
* chore(deps): update dependency ruff to v0.15.10 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/83
* chore(deps): update dependency uvicorn to >=0.44.0,<0.45.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/84
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/85
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/86
* chore(deps): update dependency ruff to v0.15.11 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/89
* chore(deps): update dependency fastapi to >=0.136.0,<0.137.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/87
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/91
* chore(deps): update dependency uvicorn to >=0.45.0,<0.46.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/92
* chore(deps): update dependency pre-commit to >=4.6.0,<4.7.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/93
* chore(deps): update astral-sh/setup-uv action to v8 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/88
* chore(deps): update dependency ruff to v0.15.12 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/95
* chore(deps): update dependency uvicorn to >=0.46.0,<0.47.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/94
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/96
* chore(deps): update dependency parametrize_from_file to v0.21.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/97
* chore(deps): [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/98
* chore(deps): update dependency ruff to v0.15.13 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/99
* chore(deps): update dependency uvicorn to >=0.47.0,<0.48.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/100
* chore(deps): update codecov/codecov-action action to v6.0.1 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/101
* chore(deps): update dependency uvicorn to >=0.48.0,<0.49.0 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/103
* chore(deps): update dependency ruff to v0.15.15 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/102
* chore: drop Python 3.8/3.9 support, add 3.14 by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/110
* feat: add contrib integrations for Litestar and FastAPI by @hasansezertasan in https://github.com/hasansezertasan/asgi-user-agents/pull/109
* chore(deps): update dependency ruff to v0.15.16 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/106
* chore(deps): update python docker tag to v3.14 by @renovate[bot] in https://github.com/hasansezertasan/asgi-user-agents/pull/111

### New Contributors

* @dependabot[bot] made their first contribution in https://github.com/hasansezertasan/asgi-user-agents/pull/21
* @pre-commit-ci[bot] made their first contribution in https://github.com/hasansezertasan/asgi-user-agents/pull/22
* @renovate[bot] made their first contribution in https://github.com/hasansezertasan/asgi-user-agents/pull/27

**Full Changelog**: https://github.com/hasansezertasan/asgi-user-agents/compare/0.2.0...0.3.0

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
