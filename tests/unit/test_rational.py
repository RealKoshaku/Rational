import operator
from math import gcd

import pytest
from rational.rational import Rational


def R(num: int, den: int = 1) -> Rational:
    return Rational(num, den)


def paire(r: Rational) -> tuple[int, int]:
    """(num, den) : contrairement à ==, vérifie aussi la normalisation."""
    return r.num, r.den


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

def test_eq_int():
    assert R(2, 1) == 2
    assert 2 == R(2, 1)
def test_hash_int():
    assert R(2, 1) in {2: "x"}

def test_hash_rationnels_egaux():
    assert hash(R(1, 2)) == hash(R(2, 4))
    assert len({R(1, 2), R(2, 4)}) == 1

def test_lt():
    assert R(1, 3) < R(1, 2)

def test_lt_negatifs():
    assert R(-1, 2) < R(1, 3)
    assert R(-1, 2) < R(-1, 3)
    assert not R(1, 2) < R(1, 2)

def test_le():
    assert R(1, 3) <= R(1, 2)
    assert R(1, 2) <= R(1, 2)
    assert not R(1, 2) <= R(1, 3)

def test_gt():
    assert R(1, 2) > R(1, 3)
    assert not R(1, 2) > R(1, 2)
    assert not R(1, 3) > R(1, 2)

def test_ge():
    assert R(1, 2) >= R(1, 3)
    assert R(1, 2) >= R(1, 2)
    assert not R(1, 3) >= R(1, 2)

def test_coherence_comparaisons():
    paires = [
        (R(1, 2), R(1, 3)),
        (R(1, 2), R(1, 2)),
        (R(-1, 2), R(1, 3)),
    ]
    for a, b in paires:
        assert (a < b) + (a == b) + (a > b) == 1
        assert (a <= b) == (a < b or a == b)
        assert (a >= b) == (a > b or a == b)

def test_add():
    assert R(1, 2) + R(1, 3) == R(5, 6)

def test_sub():
    assert R(1, 2) - R(1, 3) == R(1, 6)

def test_mul():
    assert R(2, 3) * R(3, 4) == R(1, 2)

def test_truediv():
    assert R(1, 2) / R(1, 4) == R(2, 1)

def test_truediv_par_zero():
    with pytest.raises(ZeroDivisionError):
        R(1, 2) / R(0)

def test_str():
    assert str(R(1, 2)) == "1 / 2"

def test_immuable():
    r = R(1, 2)
    with pytest.raises(AttributeError):
        r.num = 5

@pytest.mark.parametrize("num, den", [(1.5, 2), (1, 2.0), ("1", 2), (True, 1)])
def test_type_invalide(num, den):
    with pytest.raises(TypeError):
        Rational(num, den)

@pytest.mark.parametrize("autre", [0.5, "1/2", None, True])
def test_eq_autre_type(autre):
    assert R(1, 2) != autre

import operator

@pytest.mark.parametrize(
    "op",
    [operator.add, operator.sub, operator.mul, operator.truediv,
     operator.lt, operator.le, operator.gt, operator.ge],
)
@pytest.mark.parametrize("autre", [0.5, "1/2", None])
def test_operateur_autre_type(op, autre):
    with pytest.raises(TypeError):
        op(R(1, 2), autre)