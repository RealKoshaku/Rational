# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Small learning project: a `Rational` (fraction) class in Python, managed with `uv` (build backend `uv_build`, src layout). Pinned to Python 3.14 via `.python-version` (`pyproject.toml` requires `>=3.13`). `pytest` is declared in `[project].dependencies` (not a dev group).

## Commands

- `uv sync` — create/refresh `.venv`
- `uv run rational` — run the `rational` console script (currently `main()` in `src/rational/__init__.py`, still the "Hello" stub)
- `uv run pytest` — run all tests (config in `[tool.pytest.ini_options]`: `testpaths=["tests"]`, `pythonpath=["src"]`, `--import-mode=importlib`)
- `uv run pytest tests/unit/test_rational.py::test_rational_equality` — run a single test
- No linter or formatter is configured.

## Architecture

- `src/rational/rational.py` holds the `Rational` class; `src/rational/__init__.py` is only the entry-point stub and does not re-export `Rational` (import it from `rational.rational`).
- Invariant: instances are always normalized in `__init__` — reduced by `gcd` and with a positive denominator (the sign lives in `num`). Zero denominator raises `ZeroDivisionError`. Operators build results through the constructor so they stay normalized.
- Binary operators (`__eq__`, `__add__`, `__sub__`, `__mul__`, `__truediv__`) only accept `Rational` and return `NotImplemented` otherwise. `__sub__` is implemented as add of the negation.
- `__truediv__` does not guard against a zero numerator in `other` explicitly; it relies on the constructor raising `ZeroDivisionError`.

## Tests

- Tests live in `tests/unit/test_rational.py` and use `@pytest.mark.parametrize` with a French `attendu` (expected) parameter. Covered: normalization (gcd, sign), `ZeroDivisionError`, `__str__` (format `"num / den"`), `__eq__`, `+ - * /` (including normalized results) and `TypeError` for unsupported operand types. A small `R(num, den)` helper builds instances in parametrized cases.

## Conventions

- Code is type-annotated (`num: int`, return types) — the newer operators are still partially missing annotations.
- The user speaks French; reply in French.
- Keep `claude_history.md` (repo root) updated: after each modification, commit or file creation in the repo, append a dated line at the bottom.
