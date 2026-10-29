# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Small learning project: a `Rational` (fraction) class in Python, managed with `uv` (build backend `uv_build`, src layout). Pinned to Python 3.14 via `.python-version` (`pyproject.toml` requires `>=3.14.7`). Runtime dependencies are empty; `pytest`, `pytest-cov`, `hypothesis`, `ruff` and `pyright` live in the `dev` dependency group (installed by `uv sync`). `ROADMAP.md` holds the checkbox roadmap — tick items there as they are done.

## Commands

- `uv sync` — create/refresh `.venv`
- `uv run pytest` — run all tests (config in `[tool.pytest.ini_options]`: `testpaths=["tests"]`, `pythonpath=["src"]`, `--import-mode=importlib`)
- `uv run pytest tests/unit/test_rational.py::test_str` — run a single test
- `uv run pytest --cov=rational --cov-report=term-missing` — tests with coverage (currently 100%)
- `uv run ruff check` — lint; currently passes. There is no `[tool.ruff]` section in the repo, so the enabled rules come from outside it. `uv run ruff format` is the formatter (default settings; `--check` to verify); `uv run pyright` type-checks `src/` only, in `strict` mode (`[tool.pyright]`; tests are excluded) and currently passes.
- There is no console script anymore: `main()` was removed from `src/rational/__init__.py` and `[project.scripts]` from `pyproject.toml`.

## Architecture

- `src/rational/rational.py` holds the `Rational` class; `src/rational/__init__.py` only re-exports it (`from rational import Rational as Rational`).
- `Rational` is a `@dataclass(frozen=True, slots=True)` with fields `num`/`den`. Normalization happens in `__post_init__` (reduced by `gcd`, positive denominator, sign in `num`) and writes back with `object.__setattr__` because the instance is frozen. Zero denominator raises `ZeroDivisionError`; non-`int` (and `bool`) fields should raise `TypeError`. Operators build results through the constructor so they stay normalized.
- `__eq__` and `__hash__` are hand-written (not the dataclass ones): equality compares normalized `(num, den)` and also accepts `int` (but not `bool`); the hash of an integer-valued `Rational` equals `hash(int)` to stay consistent with that equality.
- `__add__`/`__sub__`/`__mul__`/`__truediv__` and the comparisons (`<`, `<=`, `>`, `>=`) accept `Rational` and `int` (not `bool`) and return `NotImplemented` for other types, so Python raises `TypeError` (`==`/`!=` fall back to `False`/`True`). Results are built through the constructor.
- Reflected operators `__radd__`/`__rsub__`/`__rmul__`/`__rtruediv__` accept `int` only (so `2 < Rational` works via the reflected comparison). `__pow__` takes an `int` exponent, negatives included (`Rational(0) ** -n` raises `ZeroDivisionError`); there is no `__rpow__`. Also `__neg__`, `__abs__` and `__bool__` (false only for zero).
- `__truediv__`/`__rtruediv__` raise `ZeroDivisionError` explicitly for a zero divisor (`int` 0 or zero `Rational`).

## Tests

- All tests live in `tests/unit/test_rational.py`, grouped by `# --- section ---` comments, and use `@pytest.mark.parametrize` with a French `attendu` (expected) parameter. Helpers: `R(num, den)` builds instances; `paire(r)` returns `(num, den)` — use it instead of `==` on results when you want to check normalization too; `AUTRES_TYPES = [0.5, "1/2", None]` lists unsupported operand types (`int` and `bool` are tested separately).
- Covered: normalization, errors, `__str__`/`__repr__`, `==`/hash, comparisons and arithmetic with `Rational` and `int` on either side, reflected operators, `__pow__`, `__neg__`/`__abs__`/`__bool__`, and `NotImplemented`/`TypeError` for unsupported types. A final section uses `hypothesis` (`@given(rationnels, ...)`) for properties such as commutativity, distributivity and normalization.

## Conventions

- Code is type-annotated; only `__rtruediv__` still lacks a return type. Keep `uv run ruff check` and `uv run pyright` clean and the code formatted with `uv run ruff format`.
- The user speaks French; reply in French.
- Keep `claude_history.md` (repo root) updated: after each modification, commit or file creation in the repo, append a dated line at the bottom.
