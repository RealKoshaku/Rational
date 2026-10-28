import operator
from math import gcd

import pytest
from rational.rational import Rational


def R(num: int, den: int = 1) -> Rational:
    return Rational(num, den)


@pytest.mark.parametrize(
    "num, den, attendu_num, attendu_den",
    [
        (0, 1, 0, 1),
        (1, 1, 1, 1),
        (2, 2, 1, 1),
        (0, 6, 0, 1),
        (4, 6, 2, 3),
        (1, -2, -1, 2),
        (-1, -2, 1, 2),
        (-4, 6, -2, 3),
        (0, -5, 0, 1),
    ],
)
def test_rational_normalisation(num, den, attendu_num, attendu_den):
    r = Rational(num, den)
    assert (r.num, r.den) == (attendu_num, attendu_den)


def test_rational_valeurs_par_defaut():
    r = Rational()
    assert (r.num, r.den) == (0, 1)


@pytest.mark.parametrize("num", [0, 1, -3])
def test_rational_denominateur_nul(num):
    with pytest.raises(ZeroDivisionError):
        Rational(num, 0)


@pytest.mark.parametrize(
    "num, den, attendu",
    [
        (0, 1, "0 / 1"),
        (1, 1, "1 / 1"),
        (2, 2, "1 / 1"),
        (0, 6, "0 / 1"),
        (1, -2, "-1 / 2"),
    ],
)
def test_rational_to_str(num, den, attendu):
    assert str(Rational(num, den)) == attendu


@pytest.mark.parametrize(
    "num1, den1, num2, den2, attendu",
    [
        (1, 1, 2, 2, True),
        (1, 2, 2, 4, True),
        (1, 2, 1, 3, False),
        (2, 3, 2, 4, False),
        (7, 9, 9, 7, False),
        (1, -2, -1, 2, True),
        (0, 1, 0, 5, True),
        (1, 2, -1, 2, False),
    ],
)
def test_rational_equality(num1, den1, num2, den2, attendu):
    assert (Rational(num1, den1) == Rational(num2, den2)) is attendu


@pytest.mark.parametrize("autre", [1, 0.5, "1/2", None])
def test_rational_equality_autre_type(autre):
    assert (R(1, 2) == autre) is False


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 2), R(1, 3), R(5, 6)),
        (R(1, 2), R(1, 2), R(1)),
        (R(1, 2), R(-1, 2), R(0)),
        (R(-1, 3), R(-1, 6), R(-1, 2)),
        (R(0), R(2, 5), R(2, 5)),
    ],
)
def test_rational_add(a, b, attendu):
    assert a + b == attendu
    assert b + a == attendu  # commutativité


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 2), R(1, 3), R(1, 6)),
        (R(1, 3), R(1, 2), R(-1, 6)),
        (R(1, 2), R(1, 2), R(0)),
        (R(1, 2), R(-1, 2), R(1)),
        (R(2, 5), R(0), R(2, 5)),
    ],
)
def test_rational_sub(a, b, attendu):
    assert a - b == attendu


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 2), R(2, 3), R(1, 3)),
        (R(-1, 2), R(2, 3), R(-1, 3)),
        (R(-1, 2), R(-2, 3), R(1, 3)),
        (R(3, 4), R(0), R(0)),
        (R(3, 4), R(1), R(3, 4)),
    ],
)
def test_rational_mul(a, b, attendu):
    assert a * b == attendu
    assert b * a == attendu  # commutativité


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 2), R(1, 4), R(2)),
        (R(1, 2), R(-1, 4), R(-2)),
        (R(-1, 2), R(-1, 4), R(2)),
        (R(0), R(3, 5), R(0)),
        (R(3, 4), R(1), R(3, 4)),
    ],
)
def test_rational_truediv(a, b, attendu):
    assert a / b == attendu


def test_rational_truediv_par_zero():
    with pytest.raises(ZeroDivisionError):
        R(1, 2) / R(0)


@pytest.mark.parametrize(
    "resultat",
    [R(1, 2) + R(1, 3), R(1, 2) - R(1, 3), R(2, 4) * R(2, 4), R(1, 2) / R(-3, 6)],
)
def test_rational_resultat_normalise(resultat):
    assert resultat.den > 0
    assert gcd(resultat.num, resultat.den) == 1


@pytest.mark.parametrize(
    "operateur", [operator.add, operator.sub, operator.mul, operator.truediv]
)
@pytest.mark.parametrize("autre", [1, 0.5, "1/2", None])
def test_rational_operateur_autre_type(operateur, autre):
    with pytest.raises(TypeError):
        operateur(R(1, 2), autre)
