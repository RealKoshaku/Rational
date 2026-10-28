from math import gcd
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class Rational:
    num: int = 0
    den: int = 1

    def __post_init__(self) -> None:
        for value in (self.num, self.den):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"num and den must be int, not {type(value).__name__}")
            if self.den == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            num, den = self.num, self.den

            sign_den: int = abs(den) // den
            g: int = gcd(num, den)

            object.__setattr__(self, "num", sign_den * num // g)
            object.__setattr__(self, "den", sign_den * den // g)

    def __hash__(self) -> int:
        if self.den == 1:
            return hash(self.num)
        return hash((self.num, self.den))

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Rational):
            return (self.num, self.den) == (value.num, value.den)
        if isinstance(value, bool):
            return NotImplemented
        if isinstance(value, int):
            return (self.num, self.den) == (value, 1)
        return NotImplemented

    def __add__(self, other: object) -> Rational:
        if isinstance(other, Rational):
            return Rational(self.num * other.den + self.den * other.num, self.den * other.den)
        elif isinstance(other, int):
            return self + Rational(other)
        return NotImplemented

    def __sub__(self, other: object) -> Rational:
        if isinstance(other, Rational):
            return self + (-other)
        elif isinstance(other, int):
            return self + (-Rational(other))
        return NotImplemented

    def __mul__(self, other) -> Rational:
        if not isinstance(other, Rational):
            return NotImplemented
        return Rational(self.num * other.num, self.den * other.den)

    def __truediv__(self, other) -> Rational:
        if not isinstance(other, Rational):
            return NotImplemented

        if other == Rational():
            raise ZeroDivisionError(f"cannot divide by {repr(other)}")

        return Rational(self.num * other.den, self.den * other.num)

    def __neg__(self):
        return Rational() - self

    def __str__(self) -> str:
        return f"{self.num} / {self.den}"

    def __repr__(self) -> str:
        return f"Rational({self.num}, {self.den})"