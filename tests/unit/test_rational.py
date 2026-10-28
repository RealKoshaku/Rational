import pytest
from rational.rational import Rational


@pytest.mark.parametrize(
    "num, den, attendu",
    [
        (0,1,"0 / 1"),
        (1,1,"1 / 1"),
        (2,2,"1 / 1"),
        (0, 6, "0 / 1")
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
        (7, 9, 9, 7, False)
    ],
)

def test_rational_equality(num1, den1, num2, den2, attendu):
    assert (Rational(num1, den1) == Rational(num2, den2)) is attendu
