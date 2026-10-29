# Rational

[![CI](https://github.com/RealKoshaku/Rational/actions/workflows/ci.yml/badge.svg)](https://github.com/RealKoshaku/Rational/actions/workflows/ci.yml)

A small learning project: an immutable `Rational` (fraction) class in Python, with exact arithmetic, comparisons and `int` interoperability.

## Requirements

- Python 3.14 (see `.python-version`; `pyproject.toml` requires `>=3.14.7`)
- [uv](https://docs.astral.sh/uv/)

## Installation

```sh
git clone git@github.com:RealKoshaku/Rational.git
cd Rational
uv sync
```

`uv sync` also installs the `dev` dependency group (`pytest`, `pytest-cov`, `hypothesis`, `ruff`, `pyright`).

## Usage

```python
from rational import Rational

a = Rational(1, 2)
b = Rational(1, 3)

a + b  # Rational(5, 6)
a * 3  # Rational(3, 2)
1 - a  # Rational(1, 2)
2 / Rational(3, 4)  # Rational(8, 3)
Rational(2, 3) ** -2  # Rational(9, 4)

str(Rational(2, 4))  # '1 / 2'
```

### Normalization

Instances are always stored in lowest terms, with a positive denominator and the sign carried by the numerator:

```python
Rational(2, 4)  # Rational(1, 2)
Rational(1, -2)  # Rational(-1, 2)
Rational(0, 5)  # Rational(0, 1)
Rational(3)  # Rational(3, 1)  (the denominator defaults to 1)
```

- A zero denominator raises `ZeroDivisionError`.
- `num` and `den` must be `int`; anything else (including `bool`) raises `TypeError`.
- Instances are immutable (`@dataclass(frozen=True, slots=True)`).

### Supported operations

| Category | Operators |
| --- | --- |
| Arithmetic | `+`, `-`, `*`, `/` between `Rational`s, and with an `int` on either side |
| Power | `**` with an `int` exponent (negative included; `0 ** -n` raises `ZeroDivisionError`) |
| Unary | `-x`, `abs(x)`, `bool(x)` (false only for zero) |
| Comparison | `==`, `!=`, `<`, `<=`, `>`, `>=` between `Rational`s, and with an `int` on either side |
| Hashing | `hash(Rational(n))` equals `hash(n)`, so equal values behave the same in sets and dict keys |

```python
Rational(4, 2) == 2  # True
Rational(1, 2) < 1  # True
sorted([Rational(1, 2), 0, Rational(-1, 3)])  # [Rational(-1, 3), 0, Rational(1, 2)]
```

Unsupported operand types (`float`, `str`, `None`, ...) and `bool` return `NotImplemented`, so Python raises `TypeError` for arithmetic, `**` and ordering comparisons (`<`, `<=`, `>`, `>=`). `==` and `!=` simply return `False` / `True` for those types. Division by a zero `Rational` or by `0` raises `ZeroDivisionError`.

## Development

```sh
uv run pytest                                            # run all tests
uv run pytest tests/unit/test_rational.py::test_str      # run a single test
uv run pytest --cov=rational --cov-report=term-missing   # run tests with coverage (currently 100%)
uv run ruff check                                        # lint (currently passes with no errors)
uv run ruff format                                       # format the code (currently already formatted)
uv run pyright                                           # type-check src/ in strict mode (currently passes)
```

Tests use `pytest` (with `@pytest.mark.parametrize`) and `hypothesis` for property-based checks; `pytest-cov` measures coverage of `src/rational`. `ruff` is used both as a linter and as a formatter (the repository has no `[tool.ruff]` configuration yet, so default formatting applies). `pyright` type-checks `src/` only, in `strict` mode (see `[tool.pyright]` in `pyproject.toml`); the tests are not type-checked. See [`ROADMAP.md`](ROADMAP.md) for planned work.

## Project layout

```text
src/rational/rational.py   the Rational class
src/rational/__init__.py   re-exports Rational
tests/unit/                pytest test suite
ROADMAP.md                 checklist of planned and finished work
```
