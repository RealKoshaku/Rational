# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Small learning project: a `Rational` (fraction) class in Python, managed with `uv` (build backend `uv_build`, src layout). Pinned to Python 3.14 via `.python-version` (`pyproject.toml` requires `>=3.13`). No runtime dependencies.

## Commands

- `uv sync` — create/refresh `.venv`
- `uv run rational` — run the `rational` console script (currently `main()` in `src/rational/__init__.py`, still the "Hello" stub)
- No tests, linter or formatter are configured yet. If pytest is added, run a single test with `uv run pytest path/to/test.py::test_name`.

## Architecture

- `src/rational/rational.py` holds the `Rational` class; `src/rational/__init__.py` is only the entry-point stub and does not re-export `Rational` (import it from `rational.rational`).
- Invariant: instances are always normalized in `__init__` — reduced by `gcd` and with a positive denominator (the sign lives in `num`). Zero denominator raises `ZeroDivisionError`. Operators build results through the constructor so they stay normalized.
- Binary operators (`__eq__`, `__add__`, `__sub__`, `__mul__`, `__truediv__`) only accept `Rational` and return `NotImplemented` otherwise. `__sub__` is implemented as add of the negation.
- `__truediv__` does not guard against a zero numerator in `other` explicitly; it relies on the constructor raising `ZeroDivisionError`.

## Conventions

- Code is type-annotated (`num: int`, return types) — the newer operators are still partially missing annotations.
- The user speaks French; reply in French.
- Keep `claude_history.md` (repo root) updated: after each modification, commit or file creation in the repo, append a dated line at the bottom.
