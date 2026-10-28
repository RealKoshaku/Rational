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
