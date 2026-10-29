# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Small learning project: a `Rational` (fraction) class in Python, managed with `uv` (build backend `uv_build`, src layout). Pinned to Python 3.14 via `.python-version` (`pyproject.toml` requires `>=3.14.7`). `pytest` is pinned (`==9.2.0`) in `[project].dependencies` (not a dev group). `ROADMAP.md` holds the checkbox roadmap — tick items there as they are done.

## Commands

- `uv sync` — create/refresh `.venv`
- `uv run rational` — run the `rational` console script (currently `main()` in `src/rational/__init__.py`, still the "Hello" stub)
- `uv run pytest` — run all tests (config in `[tool.pytest.ini_options]`: `testpaths=["tests"]`, `pythonpath=["src"]`, `--import-mode=importlib`)
- `uv run pytest tests/unit/test_rational.py::test_rational_equality` — run a single test
- No linter or formatter is configured.

## Architecture

- `src/rational/rational.py` holds the `Rational` class; `src/rational/__init__.py` re-exports `Rational` (`from rational import Rational` works) and also holds the `main()` entry-point stub.
- `Rational` is a `@dataclass(frozen=True, slots=True)` with fields `num`/`den`. Normalization happens in `__post_init__` (reduced by `gcd`, positive denominator, sign in `num`) and writes back with `object.__setattr__` because the instance is frozen. Zero denominator raises `ZeroDivisionError`; non-`int` (and `bool`) fields should raise `TypeError`. Operators build results through the constructor so they stay normalized.
- `__eq__` and `__hash__` are hand-written (not the dataclass ones): equality compares normalized `(num, den)` and also accepts `int` (but not `bool`); the hash of an integer-valued `Rational` equals `hash(int)` to stay consistent with that equality.
- `__add__`/`__sub__`/`__mul__`/`__truediv__` accept `Rational` and `int` (not `bool`) and return `NotImplemented` for other types. Each computes its result directly and builds it through the constructor. No reflected operators (`__radd__`, …), `__neg__`, `__abs__`, `__bool__` or `__pow__` yet (see `ROADMAP.md`).
- `__truediv__` raises `ZeroDivisionError` explicitly for an `int` 0 and for a zero `Rational`. Comparisons (`<`, `<=`, `>`, `>=`) only accept `Rational`.
- `rational.py` still has a stray unused `from ast import Raise` import.

## Tests

- Tests live in `tests/unit/test_rational.py` (and a rewrite in progress, `tests/unit/test_rational.py`) and use `@pytest.mark.parametrize` with a French `attendu` (expected) parameter. Helpers: `R(num, den)` builds instances; `paire(r)` returns `(num, den)` — use it instead of `==` on results when you want to check normalization too. Covered: normalization, `ZeroDivisionError`, `__str__` (format `"num / den"`), `__eq__`, `+ - * /` and `TypeError` for unsupported operand types.
- The "unsupported type" tests use `int` as an unsupported operand; this conflicts with `int` support in `__add__`/`__sub__`/`__mul__`/`__truediv__`/`__eq__` and needs updating as `int` interop grows (see `ROADMAP.md` section 3).

## Conventions

- Code is type-annotated (`num: int`, return types) — `__mul__`/`__truediv__` still take an unannotated `other`, and the comparison methods lack return types.
- The user speaks French; reply in French.
- Keep `claude_history.md` (repo root) updated: after each modification, commit or file creation in the repo, append a dated line at the bottom.
