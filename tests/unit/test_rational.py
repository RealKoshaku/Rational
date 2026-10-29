import math
import operator
from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

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


# --- Comparaisons avec des int ------------------------------------------------


@pytest.mark.parametrize(
    "a, n",
    [
        (R(1, 2), 1),
        (R(-1, 2), 0),
        (R(-3, 2), -1),
        (R(0), 1),
        (R(-1, 100), 0),
        (R(7, 2), 4),
        (R(-7, 2), -3),
        (R(10**20, 3), 10**20),
        (R(-5), -4),
    ],
)
def test_comparaisons_rational_inferieur_a_int(a, n):
    # a < n, avec l'int à droite puis à gauche (opérateur réfléchi)
    assert a < n
    assert a <= n
    assert not a > n
    assert not a >= n
    assert a != n
    assert n > a
    assert n >= a
    assert not n < a
    assert not n <= a
    assert n != a


@pytest.mark.parametrize(
    "a, n",
    [
        (R(3, 2), 1),
        (R(1, 100), 0),
        (R(1, 2), -1),
        (R(-1, 2), -1),
        (R(9, 2), 4),
        (R(-5, 2), -3),
        (R(10**20 + 1, 3), 10**19),
        (R(5), 4),
    ],
)
def test_comparaisons_rational_superieur_a_int(a, n):
    assert a > n
    assert a >= n
    assert not a < n
    assert not a <= n
    assert a != n
    assert n < a
    assert n <= a
    assert not n > a
    assert not n >= a
    assert n != a


@pytest.mark.parametrize(
    "a, n",
    [
        (R(2), 2),
        (R(0), 0),
        (R(-3), -3),
        (R(6, 3), 2),
        (R(0, -4), 0),
        (R(10**20), 10**20),
    ],
)
def test_comparaisons_rational_egal_a_int(a, n):
    assert a == n
    assert n == a
    assert a <= n
    assert a >= n
    assert n <= a
    assert n >= a
    assert not a < n
    assert not a > n
    assert not n < a
    assert not n > a


@pytest.mark.parametrize("a", [R(1, 2), R(-1, 2), R(0), R(7, 3), R(-7, 3), R(4)])
@pytest.mark.parametrize("n", [-3, -1, 0, 1, 2, 4])
def test_trichotomie_int(a, n):
    assert (a < n) + (a == n) + (a > n) == 1
    assert (a < n) == (a < R(n))
    assert (a <= n) == (a <= R(n))
    assert (a > n) == (a > R(n))
    assert (a >= n) == (a >= R(n))
    assert (n < a) == (R(n) < a)
    assert (n >= a) == (R(n) >= a)


@pytest.mark.parametrize("a", [R(7, 2), R(-7, 2), R(1, 3), R(-1, 3)])
def test_encadrement_par_entiers(a):
    # floor(a) <= a < floor(a) + 1
    plancher = a.num // a.den
    assert plancher <= a < plancher + 1


def test_tri_et_extremes_melanges():
    valeurs = [R(1, 2), 0, R(-1, 2), 1, -1, R(3, 2)]
    assert sorted(valeurs) == [-1, R(-1, 2), 0, R(1, 2), 1, R(3, 2)]
    assert min(valeurs) == -1
    assert max(valeurs) == R(3, 2)


@pytest.mark.parametrize("op", [operator.lt, operator.le, operator.gt, operator.ge])
@pytest.mark.parametrize("autre", [True, False])
def test_comparaison_bool_refusee(op, autre):
    with pytest.raises(TypeError):
        op(R(1, 2), autre)
    with pytest.raises(TypeError):
        op(autre, R(1, 2))


@pytest.mark.parametrize("op", [operator.lt, operator.le, operator.gt, operator.ge])
@pytest.mark.parametrize("autre", AUTRES_TYPES)
def test_comparaison_inverse_autre_type(op, autre):
    with pytest.raises(TypeError):
        op(autre, R(1, 2))


@pytest.mark.parametrize("methode", ["__lt__", "__le__", "__gt__", "__ge__"])
@pytest.mark.parametrize("autre", AUTRES_TYPES + [True, False])
def test_methode_comparaison_retourne_not_implemented(methode, autre):
    assert getattr(R(1, 2), methode)(autre) is NotImplemented


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


# --- Arithmétique avec des int (Rational à gauche) --------------------------


@pytest.mark.parametrize(
    "a, n, attendu",
    [
        (R(1, 2), 1, (3, 2)),
        (R(1, 2), -1, (-1, 2)),
        (R(1, 2), 0, (1, 2)),
        (R(-3, 4), 2, (5, 4)),
        (R(1, 2), -3, (-5, 2)),
        (R(1, 2), 5, (11, 2)),
        (R(1, 2), 2, (5, 2)),
        (R(-1, 2), 1, (1, 2)),  # résultat réduit
    ],
)
def test_add_int(a, n, attendu):
    assert paire(a + n) == attendu
    assert a + n == a + R(n)


@pytest.mark.parametrize(
    "a, n, attendu",
    [
        (R(1, 2), 1, (-1, 2)),
        (R(1, 2), -1, (3, 2)),
        (R(1, 2), 0, (1, 2)),
        (R(3, 4), 2, (-5, 4)),
        (R(5, 2), 2, (1, 2)),
        (R(1, 2), 3, (-5, 2)),
    ],
)
def test_sub_int(a, n, attendu):
    assert paire(a - n) == attendu
    assert a - n == a - R(n)


@pytest.mark.parametrize(
    "a, n, attendu",
    [
        (R(1, 2), 2, (1, 1)),
        (R(1, 2), 3, (3, 2)),
        (R(2, 3), 3, (2, 1)),
        (R(2, 3), 6, (4, 1)),
        (R(-1, 2), 3, (-3, 2)),
        (R(1, 2), -4, (-2, 1)),
        (R(3, 4), 0, (0, 1)),
        (R(3, 4), 1, (3, 4)),
        (R(4, 9), 3, (4, 3)),  # simplification croisée
    ],
)
def test_mul_int(a, n, attendu):
    assert paire(a * n) == attendu
    assert a * n == a * R(n)


@pytest.mark.parametrize(
    "a, n, attendu",
    [
        (R(1, 2), 2, (1, 4)),
        (R(1, 2), -2, (-1, 4)),
        (R(-1, 2), -2, (1, 4)),
        (R(3, 4), 1, (3, 4)),
        (R(4, 3), 2, (2, 3)),  # résultat réduit
        (R(0), 5, (0, 1)),
        (R(3, 4), 3, (1, 4)),
    ],
)
def test_truediv_int(a, n, attendu):
    assert paire(a / n) == attendu
    assert a / n == a / R(n)


@pytest.mark.parametrize("a", [R(1, 2), R(0), R(-3, 4)])
def test_truediv_par_int_zero(a):
    with pytest.raises(ZeroDivisionError):
        a / 0


@pytest.mark.parametrize(
    "op",
    [operator.add, operator.sub, operator.mul, operator.truediv],
)
@pytest.mark.parametrize("autre", [True, False])
def test_operateur_bool_refuse(op, autre):
    with pytest.raises(TypeError):
        op(R(1, 2), autre)


@pytest.mark.parametrize("a", [R(1, 2), R(-3, 4), R(0)])
@pytest.mark.parametrize("n", [-3, 0, 2])
def test_proprietes_algebriques_int(a, n):
    assert (a + n) - n == a
    assert (a - n) + n == a
    if n != 0:
        assert (a * n) / n == a
        assert (a / n) * n == a


# --- Opérateurs inverses (int à gauche) -----------------------------------


@pytest.mark.parametrize(
    "n, a, attendu",
    [
        (1, R(1, 2), (3, 2)),
        (-1, R(1, 2), (-1, 2)),
        (0, R(1, 2), (1, 2)),
        (2, R(-3, 4), (5, 4)),
        (1, R(-1, 2), (1, 2)),
        (-3, R(1, 2), (-5, 2)),
        (2, R(1, 2), (5, 2)),
        (1, R(-1, 1), (0, 1)),  # résultat nul normalisé
        (10**20, R(1, 3), (3 * 10**20 + 1, 3)),
    ],
)
def test_radd(n, a, attendu):
    assert paire(n + a) == attendu
    assert n + a == R(n) + a
    assert n + a == a + n  # commutativité


@pytest.mark.parametrize(
    "n, a, attendu",
    [
        (1, R(1, 2), (1, 2)),
        (0, R(1, 2), (-1, 2)),
        (-1, R(1, 2), (-3, 2)),
        (2, R(-3, 4), (11, 4)),
        (2, R(5, 2), (-1, 2)),
        (1, R(1, 1), (0, 1)),
        (3, R(0), (3, 1)),
        (0, R(0), (0, 1)),
        (1, R(2, 4), (1, 2)),
    ],
)
def test_rsub(n, a, attendu):
    assert paire(n - a) == attendu
    assert n - a == R(n) - a
    assert (n - a) + a == n


@pytest.mark.parametrize(
    "n, a, attendu",
    [
        (2, R(1, 2), (1, 1)),
        (3, R(1, 2), (3, 2)),
        (3, R(2, 3), (2, 1)),
        (6, R(2, 3), (4, 1)),
        (3, R(-1, 2), (-3, 2)),
        (-4, R(1, 2), (-2, 1)),
        (-4, R(-1, 2), (2, 1)),
        (0, R(3, 4), (0, 1)),
        (1, R(3, 4), (3, 4)),
        (3, R(4, 9), (4, 3)),
    ],
)
def test_rmul(n, a, attendu):
    assert paire(n * a) == attendu
    assert n * a == R(n) * a
    assert n * a == a * n  # commutativité


@pytest.mark.parametrize(
    "n, a, attendu",
    [
        (1, R(1, 2), (2, 1)),
        (1, R(2, 3), (3, 2)),
        (2, R(1, 2), (4, 1)),
        (2, R(-1, 2), (-4, 1)),
        (-2, R(-1, 2), (4, 1)),
        (-2, R(1, 2), (-4, 1)),
        (0, R(3, 5), (0, 1)),
        (3, R(3, 4), (4, 1)),
        (4, R(6, 1), (2, 3)),  # résultat réduit
        (1, R(-3, 1), (-1, 3)),  # signe porté par le numérateur
        (5, R(1, 1), (5, 1)),
    ],
)
def test_rtruediv(n, a, attendu):
    assert paire(n / a) == attendu
    assert n / a == R(n) / a


@pytest.mark.parametrize("n", [-5, 0, 1, 7])
def test_rtruediv_par_zero(n):
    with pytest.raises(ZeroDivisionError):
        n / R(0)


@pytest.mark.parametrize("n", [-5, 0, 1, 7])
@pytest.mark.parametrize("a", [R(1, 2), R(-3, 4), R(5, 1)])
def test_inverses_coherents_avec_directs(n, a):
    assert n + a == a + n
    assert n * a == a * n
    assert n - a == R(n) - a
    assert (n - a) + a == n
    assert (n - a) + (a - n) == 0


@pytest.mark.parametrize("n", [-5, 1, 7])
@pytest.mark.parametrize("a", [R(1, 2), R(-3, 4), R(5, 1)])
def test_rtruediv_inverse_de_truediv(n, a):
    assert (n / a) * a == n
    assert n / a == R(n) / a
    assert (n / a) * (a / n) == R(1)


@pytest.mark.parametrize(
    "op",
    [operator.add, operator.sub, operator.mul, operator.truediv],
)
@pytest.mark.parametrize("autre", [True, False])
def test_operateur_inverse_bool_refuse(op, autre):
    with pytest.raises(TypeError):
        op(autre, R(1, 2))


@pytest.mark.parametrize(
    "op",
    [operator.add, operator.sub, operator.mul, operator.truediv],
)
@pytest.mark.parametrize("autre", AUTRES_TYPES)
def test_operateur_inverse_autre_type(op, autre):
    with pytest.raises(TypeError):
        op(autre, R(1, 2))


@pytest.mark.parametrize(
    "methode", ["__radd__", "__rsub__", "__rmul__", "__rtruediv__"]
)
@pytest.mark.parametrize("autre", AUTRES_TYPES + [True, False])
def test_methode_inverse_retourne_not_implemented(methode, autre):
    assert getattr(R(1, 2), methode)(autre) is NotImplemented


def test_operateurs_augmentes_avec_int():
    r = R(1, 2)
    r += 1
    assert paire(r) == (3, 2)
    r -= 2
    assert paire(r) == (-1, 2)
    r *= -4
    assert paire(r) == (2, 1)
    r /= 4
    assert paire(r) == (1, 2)


def test_operateurs_augmentes_int_gauche():
    n = 1
    n += R(1, 2)
    assert paire(n) == (3, 2)
    n = 3
    n -= R(1, 2)
    assert paire(n) == (5, 2)
    n = 3
    n *= R(1, 2)
    assert paire(n) == (3, 2)
    n = 3
    n /= R(1, 2)
    assert paire(n) == (6, 1)


# --- Puissance ------------------------------------------------------------


@pytest.mark.parametrize(
    "a, n, attendu",
    [
        (R(1, 2), 0, (1, 1)),
        (R(1, 2), 1, (1, 2)),
        (R(1, 2), 2, (1, 4)),
        (R(2, 3), 3, (8, 27)),
        (R(-1, 2), 2, (1, 4)),
        (R(-1, 2), 3, (-1, 8)),
        (R(3), 4, (81, 1)),
        (R(0), 3, (0, 1)),
        (R(0), 0, (1, 1)),  # 0**0 == 1, comme pour int
        (R(1), 100, (1, 1)),
        (R(-1), 101, (-1, 1)),
        (R(-1), 100, (1, 1)),
        (R(2, 4), 2, (1, 4)),  # base non réduite à l'origine
        (R(10, 3), 20, (10**20, 3**20)),
    ],
)
def test_pow_positif(a, n, attendu):
    assert paire(a**n) == attendu


@pytest.mark.parametrize(
    "a, n, attendu",
    [
        (R(1, 2), -1, (2, 1)),
        (R(1, 2), -2, (4, 1)),
        (R(2, 3), -3, (27, 8)),
        (R(-1, 2), -1, (-2, 1)),
        (R(-1, 2), -2, (4, 1)),
        (R(-1, 2), -3, (-8, 1)),
        (R(3), -2, (1, 9)),
        (R(-3), -3, (-1, 27)),  # signe porté par le numérateur
        (R(1), -5, (1, 1)),
        (R(-1), -5, (-1, 1)),
        (R(6, 4), -2, (4, 9)),
    ],
)
def test_pow_negatif(a, n, attendu):
    assert paire(a**n) == attendu


@pytest.mark.parametrize("n", [-1, -2, -10])
def test_pow_zero_exposant_negatif(n):
    with pytest.raises(ZeroDivisionError):
        R(0) ** n


@pytest.mark.parametrize("a", [R(1, 2), R(-2, 3), R(5), R(-7, 4)])
@pytest.mark.parametrize("n", [-3, -1, 0, 1, 2, 5])
def test_pow_proprietes(a, n):
    assert a**n * a**-n == R(1)
    assert a ** (n + 1) == a**n * a
    assert a**-n == R(1) / a**n
    assert (a**n) ** 2 == a ** (2 * n)
    assert a**n == pow(a, n)


@pytest.mark.parametrize("a, b", [(R(1, 2), R(2, 3)), (R(-3, 4), R(5, 2))])
@pytest.mark.parametrize("n", [-2, 0, 3])
def test_pow_distributif_sur_produit(a, b, n):
    assert (a * b) ** n == a**n * b**n


@pytest.mark.parametrize("a", [R(1, 2), R(-3, 4), R(0), R(5)])
def test_pow_cas_simples(a):
    assert a**0 == R(1)
    assert a**1 == a
    assert a**2 == a * a


def test_pow_retourne_normalise_et_hashable():
    r = R(2, 4) ** 3
    assert paire(r) == (1, 8)
    assert hash(R(2) ** 3) == hash(8)


@pytest.mark.parametrize("autre", [True, False])
def test_pow_exposant_bool_refuse(autre):
    with pytest.raises(TypeError):
        R(1, 2) ** autre


@pytest.mark.parametrize("autre", [0.5, 2.0, "2", None, R(2)])
def test_pow_exposant_autre_type(autre):
    with pytest.raises(TypeError):
        R(1, 2) ** autre


@pytest.mark.parametrize("autre", [0.5, "2", None, True, R(2)])
def test_pow_methode_retourne_not_implemented(autre):
    assert R(1, 2).__pow__(autre) is NotImplemented


def test_pow_base_int_non_supportee():
    # pas de __rpow__ : int ** Rational n'a pas de sens pour un exposant rationnel
    with pytest.raises(TypeError):
        2 ** R(1, 2)


# --- Négation, valeur absolue, booléen ------------------------------------


@pytest.mark.parametrize(
    "a, attendu",
    [
        (R(1, 2), (-1, 2)),
        (R(-1, 2), (1, 2)),
        (R(0), (0, 1)),
        (R(3), (-3, 1)),
        (R(-3), (3, 1)),
        (R(2, -4), (1, 2)),
        (R(-6, -4), (-3, 2)),
        (R(10**20, 3), (-(10**20), 3)),
    ],
)
def test_neg(a, attendu):
    assert paire(-a) == attendu


@pytest.mark.parametrize("a", [R(1, 2), R(-3, 4), R(0), R(5)])
def test_neg_proprietes(a):
    assert -(-a) == a  # noqa: B002
    assert a + (-a) == R(0)
    assert a - a == a + (-a)
    assert -a == R(0) - a
    assert -a == a * -1
    assert -a == -1 * a


def test_neg_zero_reste_normalise():
    assert paire(-R(0)) == (0, 1)
    assert hash(-R(0)) == hash(R(0)) == hash(0)


def test_neg_retourne_nouvelle_instance():
    a = R(1, 2)
    b = -a
    assert b is not a
    assert paire(a) == (1, 2)


@pytest.mark.parametrize(
    "a, attendu",
    [
        (R(1, 2), (1, 2)),
        (R(-1, 2), (1, 2)),
        (R(0), (0, 1)),
        (R(7), (7, 1)),
        (R(-7), (7, 1)),
        (R(-4, 6), (2, 3)),
        (R(4, -6), (2, 3)),
        (R(-4, -6), (2, 3)),
        (R(-(10**20), 3), (10**20, 3)),
    ],
)
def test_abs(a, attendu):
    assert paire(abs(a)) == attendu


@pytest.mark.parametrize("a", [R(1, 2), R(-3, 4), R(0), R(-5), R(5)])
def test_abs_proprietes(a):
    assert abs(a) >= R(0)
    assert abs(a) == abs(-a)
    assert abs(abs(a)) == abs(a)
    assert abs(a) in (a, -a)
    assert (abs(a) == R(0)) is (a == R(0))


@pytest.mark.parametrize(
    "a, b", [(R(1, 2), R(-1, 3)), (R(-2, 3), R(-5, 7)), (R(0), R(3, 4))]
)
def test_abs_multiplicatif_et_inegalite_triangulaire(a, b):
    assert abs(a * b) == abs(a) * abs(b)
    assert abs(a + b) <= abs(a) + abs(b)


@pytest.mark.parametrize(
    "a, attendu",
    [
        (R(0), False),
        (R(0, 5), False),
        (R(0, -5), False),
        (R(1), True),
        (R(-1), True),
        (R(1, 2), True),
        (R(-1, 2), True),
        (R(1, 10**20), True),
    ],
)
def test_bool(a, attendu):
    assert bool(a) is attendu


def test_bool_dans_conditions():
    assert not R(0)
    assert R(1, 2)
    assert (R(1, 2) and "vrai") == "vrai"
    assert (R(0) or "defaut") == "defaut"
    assert [r for r in (R(0), R(1, 2), R(-1), R(0, 3)) if r] == [R(1, 2), R(-1)]


@pytest.mark.parametrize("a", [R(1, 2), R(-3, 4), R(5)])
def test_bool_coherent_avec_neg_et_abs(a):
    assert bool(-a) is bool(a)
    assert bool(abs(a)) is bool(a)
    assert bool(a - a) is False


# --- Construction depuis un float -----------------------------------------


def fraction(r: Rational) -> Fraction:
    """Équivalent exact de la bibliothèque standard, pour comparer."""
    return Fraction(r.num, r.den)


@pytest.mark.parametrize(
    "x, attendu",
    [
        (0.0, (0, 1)),
        (-0.0, (0, 1)),
        (1.0, (1, 1)),
        (-1.0, (-1, 1)),
        (0.5, (1, 2)),
        (-0.5, (-1, 2)),
        (0.25, (1, 4)),
        (0.75, (3, 4)),
        (2.5, (5, 2)),
        (-3.125, (-25, 8)),
        (1e10, (10**10, 1)),
        (2.0**-10, (1, 1024)),
        (2.0**60, (2**60, 1)),
    ],
)
def test_from_float_exact(x, attendu):
    assert paire(Rational.from_float(x)) == attendu


@pytest.mark.parametrize(
    "x, attendu",
    [
        # un float non représentable exactement garde sa valeur binaire réelle
        (0.1, (3602879701896397, 36028797018963968)),
        (0.2, (3602879701896397, 18014398509481984)),
        (1 / 3, (6004799503160661, 18014398509481984)),
    ],
)
def test_from_float_valeur_binaire_exacte(x, attendu):
    assert paire(Rational.from_float(x)) == attendu


def test_from_float_n_est_pas_la_decimale_ecrite():
    assert Rational.from_float(0.1) != Rational(1, 10)
    assert Rational.from_float(0.1) + Rational.from_float(0.2) != Rational.from_float(
        0.3
    )


@pytest.mark.parametrize("x", [0.0, 0.5, -0.5, 0.1, 1 / 3, 123456.789, -1e-300, 1e300])
def test_from_float_aller_retour(x):
    r = Rational.from_float(x)
    assert r.num / r.den == x
    assert float(fraction(r)) == x
    assert fraction(r) == Fraction(x)


@pytest.mark.parametrize("x", [0.5, -0.5, 0.1, 3.75, -1e-5, 1e15])
def test_from_float_normalise(x):
    r = Rational.from_float(x)
    assert r.den > 0
    assert math.gcd(r.num, r.den) == 1


@pytest.mark.parametrize("x", [2.0, -7.0, 0.0, 1e10])
def test_from_float_entier_egal_a_int(x):
    r = Rational.from_float(x)
    assert r.den == 1
    assert r == int(x)
    assert hash(r) == hash(int(x))


@pytest.mark.parametrize("x, y", [(0.5, 0.25), (-0.5, 0.75), (0.1, 0.2)])
def test_from_float_conserve_l_ordre_et_l_arithmetique(x, y):
    a, b = Rational.from_float(x), Rational.from_float(y)
    assert (a < b) is (x < y)
    assert (a > b) is (x > y)
    assert fraction(a + b) == Fraction(x) + Fraction(y)
    assert fraction(a * b) == Fraction(x) * Fraction(y)


def test_from_float_retourne_un_rational():
    assert isinstance(Rational.from_float(0.5), Rational)


def test_from_float_appelable_depuis_une_instance():
    assert Rational(1, 3).from_float(0.5) == Rational(1, 2)


@pytest.mark.parametrize("x", [float("inf"), float("-inf")])
def test_from_float_infini(x):
    with pytest.raises(OverflowError):
        Rational.from_float(x)


def test_from_float_nan():
    with pytest.raises(ValueError):
        Rational.from_float(float("nan"))


@given(st.floats(allow_nan=False, allow_infinity=False))
def test_from_float_propriete_hypothesis(x):
    r = Rational.from_float(x)
    assert fraction(r) == Fraction(x)
    assert r.num / r.den == x
    assert r.den > 0
    assert math.gcd(r.num, r.den) == 1


# --- Conversion en float --------------------------------------------------


@pytest.mark.parametrize(
    ("r", "attendu"),
    [
        (R(1, 2), 0.5),
        (R(-3, 4), -0.75),
        (R(0), 0.0),
        (R(5), 5.0),
        (R(-7), -7.0),
        (R(1, 3), 1 / 3),
        (R(2, 3), 2 / 3),
        (R(1, 10), 0.1),
        (R(22, 7), 22 / 7),
    ],
)
def test_float(r, attendu):
    assert float(r) == attendu


def test_float_retourne_un_float():
    assert type(float(R(1, 2))) is float
    assert type(float(R(3))) is float


def test_float_zero_signe():
    assert math.copysign(1, float(R(0))) == 1.0


@pytest.mark.parametrize("x", [0.5, 0.1, -3.125, 1e-300, 1e300, 2**-1074, 0.0])
def test_float_aller_retour(x):
    assert float(Rational.from_float(x)) == x


def test_float_arrondi_correct_pour_grands_entiers():
    # num et den dépassent la plage d'un float, mais le quotient est correct
    assert float(R(10**400, 3 * 10**400)) == 1 / 3
    assert float(R(10**400 + 1, 10**400)) == 1.0


def test_float_trop_grand():
    with pytest.raises(OverflowError):
        float(R(10**400))


def test_float_tres_petit_donne_zero():
    assert float(R(1, 10**400)) == 0.0


def test_float_conserve_l_ordre():
    assert float(R(1, 3)) < float(R(1, 2)) < float(R(2, 3))


def test_float_coherent_avec_fraction():
    r = R(-355, 113)
    assert float(r) == float(fraction(r))


@given(st.floats(allow_nan=False, allow_infinity=False))
def test_float_aller_retour_hypothesis(x):
    assert float(Rational.from_float(x)) == x


# --- Conversion en int ----------------------------------------------------


@pytest.mark.parametrize(
    ("r", "attendu"),
    [
        (R(0), 0),
        (R(5), 5),
        (R(-5), -5),
        (R(1, 2), 0),
        (R(-1, 2), 0),
        (R(1, 3), 0),
        (R(7, 2), 3),
        (R(-7, 2), -3),
        (R(9, 4), 2),
        (R(-9, 4), -2),
        (R(99, 100), 0),
        (R(-99, 100), 0),
        (R(101, 100), 1),
        (R(-101, 100), -1),
        (R(10**30 + 1, 10), 10**29),
        (R(-(10**30) - 1, 10), -(10**29)),
    ],
)
def test_int(r, attendu):
    assert int(r) == attendu


def test_int_retourne_un_int():
    assert type(int(R(7, 2))) is int
    assert type(int(R(3))) is int
    assert type(int(R(0))) is int


def test_int_tronque_vers_zero_et_non_vers_moins_infini():
    assert int(R(-7, 2)) == -3
    assert int(R(-7, 2)) == math.trunc(-3.5)
    assert int(R(-7, 2)) != math.floor(-3.5)


def test_int_aller_retour():
    for n in [0, 1, -1, 42, -42, 10**30]:
        assert int(R(n)) == n


def test_int_coherent_avec_float():
    for r in [R(7, 2), R(-7, 2), R(1, 3), R(-1, 3), R(22, 7)]:
        assert int(r) == int(float(r))


@pytest.mark.parametrize("r", [R(7, 2), R(-7, 2), R(1, 3), R(5), R(0)])
def test_int_est_proche_de_la_valeur(r):
    assert abs(r) - abs(int(r)) >= 0
    assert abs(r) - abs(int(r)) < 1


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


rationnels = st.builds(
    Rational,
    st.integers(),
    st.integers().filter(lambda d: d != 0),
)


@given(rationnels, rationnels)
def test_add_commutatif(a, b):
    assert a + b == b + a


@given(rationnels)
def test_sub_same(a):
    assert a - a == 0


@given(rationnels, rationnels)
def test_mul_commutatif(a, b):
    assert a * b == b * a


@given(rationnels, rationnels, rationnels)
def test_distributivity(a, b, c):
    assert a * (b + c) == a * b + a * c


@given(rationnels, rationnels)
def test_add_normalized(a, b):
    r = a + b
    assert math.gcd(r.num, r.den) == 1
    assert r.den > 0


@given(rationnels)
def test_float_propriete_hypothesis(r):
    assert float(r) == float(fraction(r))


@given(rationnels)
def test_int_propriete_hypothesis(r):
    assert int(r) == int(fraction(r))
    assert int(r) == math.trunc(fraction(r))
    assert 0 <= abs(r) - abs(int(r)) < 1
