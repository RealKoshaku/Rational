from math import gcd


class Rational:
    def __init__(self, num: int = 0, den: int = 1) -> None:
        if den == 0:
            raise ZeroDivisionError("Cannot divide by zero.")

        gcd_value: int = gcd(num, den)
        sign_den: int = abs(den) // den  # Sign of denominator

        self.num: int = sign_den * num // gcd_value
        self.den: int = sign_den * den // gcd_value

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Rational):
            return NotImplemented
        return self.num * value.den == self.den * value.num

    def __add__(self, other: object) -> Rational:
        if not isinstance(other, Rational):
            return NotImplemented
        return Rational(self.num * other.den + self.den * other.num, self.den * other.den)

    def __sub__(self, other: object) -> Rational:
        if not isinstance(other, Rational):
            return NotImplemented
        return self + Rational(-other.num, other.den)

    def __mul__(self, other) -> Rational:
        if not isinstance(other, Rational):
            return NotImplemented
        return Rational(self.num * other.num, self.den * other.den)

    def __truediv__(self, other) -> Rational:
        if not isinstance(other, Rational):
            return NotImplemented
        return Rational(self.num * other.den, self.den * other.num)

    def __str__(self) -> str:
        return f"{self.num} / {self.den}"

    def __repr__(self) -> str:
        return f"Rational({self.num}, {self.den})"