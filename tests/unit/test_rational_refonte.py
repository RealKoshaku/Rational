import operator

import pytest
from rational.rational import Rational


def R(num: int, den: int = 1) -> Rational:
    return Rational(num, den)


def paire(r: Rational) -> tuple[int, int]:
    """(num, den) : contrairement à ==, vérifie aussi la normalisation."""
    return r.num, r.den


AUTRES_TYPES = [0.5, "1/2", None]


# --- Construction ---------------------------------------------------------


@pytest.mark.parametrize(
    "num, den, attendu",
    [
        (0, 1, (0, 1)),
        (1, 1, (1, 1)),
        (2, 2, (1, 1)),
        (0, 6, (0, 1)),
        (4, 6, (2, 3)),
        (1, -2, (-1, 2)),
        (-1, -2, (1, 2)),
        (-4, 6, (-2, 3)),
        (0, -5, (0, 1)),
        (6, 3, (2, 1)),
    ],
)
def test_normalisation(num, den, attendu):
    assert paire(Rational(num, den)) == attendu


def test_valeurs_par_defaut():
    assert paire(Rational()) == (0, 1)


def test_denominateur_par_defaut():
    assert paire(Rational(3)) == (3, 1)


@pytest.mark.parametrize("num", [0, 1, -3])
def test_denominateur_nul(num):
    with pytest.raises(ZeroDivisionError):
        Rational(num, 0)


@pytest.mark.parametrize(
    "num, den", [(1.5, 2), (1, 2.0), ("1", 2), (1, None), (True, 1), (1, False)]
)
def test_type_invalide(num, den):
    with pytest.raises(TypeError):
        Rational(num, den)


def test_immuable():
    r = R(1, 2)
    with pytest.raises(AttributeError):
        r.num = 5
    with pytest.raises(AttributeError):
        r.den = 5


# --- Représentation -------------------------------------------------------


@pytest.mark.parametrize(
    "num, den, attendu",
    [
        (0, 1, "0 / 1"),
        (1, 1, "1 / 1"),
        (2, 2, "1 / 1"),
        (0, 6, "0 / 1"),
        (1, -2, "-1 / 2"),
        (1, 2, "1 / 2"),
    ],
)
def test_str(num, den, attendu):
    assert str(Rational(num, den)) == attendu


@pytest.mark.parametrize(
    "num, den, attendu",
    [(1, 2, "Rational(1, 2)"), (2, 4, "Rational(1, 2)"), (-1, -3, "Rational(1, 3)")],
)
def test_repr(num, den, attendu):
    assert repr(Rational(num, den)) == attendu


# --- Égalité et hachage ---------------------------------------------------


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 1), R(2, 2), True),
        (R(1, 2), R(2, 4), True),
        (R(1, -2), R(-1, 2), True),
        (R(0, 1), R(0, 5), True),
        (R(1, 2), R(1, 3), False),
        (R(2, 3), R(2, 4), False),
        (R(7, 9), R(9, 7), False),
        (R(1, 2), R(-1, 2), False),
    ],
)
def test_egalite_rationnels(a, b, attendu):
    assert (a == b) is attendu
    assert (a != b) is (not attendu)


def test_egalite_int():
    assert R(2, 1) == 2
    assert 2 == R(2, 1)
    assert R(1, 2) != 1


@pytest.mark.parametrize("autre", AUTRES_TYPES + [True])
def test_egalite_autre_type(autre):
    assert R(1, 2) != autre


@pytest.mark.parametrize("autre", [True, False])
def test_egalite_bool_jamais_egal(autre):
    assert R(int(autre)) != autre


def test_hash_rationnels_egaux():
    assert hash(R(1, 2)) == hash(R(2, 4))
    assert len({R(1, 2), R(2, 4)}) == 1


def test_hash_coherent_avec_int():
    assert hash(R(2, 1)) == hash(2)
    assert R(2, 1) in {2: "x"}


# --- Comparaisons ---------------------------------------------------------


@pytest.mark.parametrize(
    "petit, grand",
    [
        (R(1, 3), R(1, 2)),
        (R(-1, 2), R(1, 3)),
        (R(-1, 2), R(-1, 3)),
        (R(0), R(1, 100)),
        (R(-1, 100), R(0)),
    ],
)
def test_comparaisons_strictes(petit, grand):
    assert petit < grand
    assert petit <= grand
    assert grand > petit
    assert grand >= petit
    assert not grand < petit
    assert not grand <= petit
    assert not petit > grand
    assert not petit >= grand


@pytest.mark.parametrize("a", [R(1, 2), R(0), R(-3, 4)])
def test_comparaisons_egaux(a):
    b = Rational(a.num * 2, a.den * 2)
    assert a <= b
    assert a >= b
    assert not a < b
    assert not a > b


@pytest.mark.parametrize(
    "a, b",
    [(R(1, 2), R(1, 3)), (R(1, 2), R(1, 2)), (R(-1, 2), R(1, 3))],
)
def test_trichotomie(a, b):
    assert (a < b) + (a == b) + (a > b) == 1


def test_tri():
    valeurs = [R(1, 2), R(-1, 2), R(0), R(1, 3), R(-2, 3)]
    assert sorted(valeurs) == [R(-2, 3), R(-1, 2), R(0), R(1, 3), R(1, 2)]


# --- Arithmétique ---------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 2), R(1, 3), (5, 6)),
        (R(1, 2), R(1, 2), (1, 1)),
        (R(1, 2), R(-1, 2), (0, 1)),
        (R(-1, 3), R(-1, 6), (-1, 2)),
        (R(0), R(2, 5), (2, 5)),
    ],
)
def test_add(a, b, attendu):
    assert paire(a + b) == attendu
    assert paire(b + a) == attendu


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 2), R(1, 3), (1, 6)),
        (R(1, 3), R(1, 2), (-1, 6)),
        (R(1, 2), R(1, 2), (0, 1)),
        (R(1, 2), R(-1, 2), (1, 1)),
        (R(2, 5), R(0), (2, 5)),
    ],
)
def test_sub(a, b, attendu):
    assert paire(a - b) == attendu


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 2), R(2, 3), (1, 3)),
        (R(2, 3), R(3, 4), (1, 2)),
        (R(-1, 2), R(2, 3), (-1, 3)),
        (R(-1, 2), R(-2, 3), (1, 3)),
        (R(3, 4), R(0), (0, 1)),
        (R(3, 4), R(1), (3, 4)),
    ],
)
def test_mul(a, b, attendu):
    assert paire(a * b) == attendu
    assert paire(b * a) == attendu


@pytest.mark.parametrize(
    "a, b, attendu",
    [
        (R(1, 2), R(1, 4), (2, 1)),
        (R(1, 2), R(-1, 4), (-2, 1)),
        (R(-1, 2), R(-1, 4), (2, 1)),
        (R(0), R(3, 5), (0, 1)),
        (R(3, 4), R(1), (3, 4)),
    ],
)
def test_truediv(a, b, attendu):
    assert paire(a / b) == attendu


@pytest.mark.parametrize("a", [R(1, 2), R(0), R(-3, 4)])
def test_truediv_par_zero(a):
    with pytest.raises(ZeroDivisionError):
        a / R(0)


@pytest.mark.parametrize(
    "a, b", [(R(1, 2), R(1, 3)), (R(-2, 3), R(5, 7)), (R(3, 4), R(-3, 4))]
)
def test_proprietes_algebriques(a, b):
    assert (a + b) - b == a
    assert (a - b) + b == a
    assert a - a == R(0)
    assert a * R(1) == a
    if b != R(0):
        assert (a * b) / b == a
        assert (a / b) * b == a


# --- Types non supportés --------------------------------------------------


@pytest.mark.parametrize(
    "op",
    [
        operator.add,
        operator.sub,
        operator.mul,
        operator.truediv,
        operator.lt,
        operator.le,
        operator.gt,
        operator.ge,
    ],
)
@pytest.mark.parametrize("autre", AUTRES_TYPES)
def test_operateur_autre_type(op, autre):
    with pytest.raises(TypeError):
        op(R(1, 2), autre)
