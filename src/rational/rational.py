from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True, slots=True)
class Rational:
    num: int = 0
    den: int = 1

    def __post_init__(self) -> None:
        for value in (self.num, self.den):
            if isinstance(value, bool) or not isinstance(value, int):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(f"num and den must be int, not {type(value).__name__}")
        if self.den == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        num, den = self.num, self.den

        sign_den: int = abs(den) // den
        g: int = gcd(num, den)

        object.__setattr__(self, "num", sign_den * num // g)
        object.__setattr__(self, "den", sign_den * den // g)

    @classmethod
    def from_float(cls, x: float):
        (num, den) = x.as_integer_ratio()
        return cls(num, den)

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

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Rational):
            return self.num * other.den < self.den * other.num
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, int):
            return self.num < self.den * other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, Rational):
            return self.num * other.den <= self.den * other.num
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, int):
            return self.num <= self.den * other
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Rational):
            return self.num * other.den > self.den * other.num
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, int):
            return self.num > self.den * other
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Rational):
            return self.num * other.den >= self.den * other.num
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, int):
            return self.num >= self.den * other
        return NotImplemented

    def __add__(self, other: object) -> Rational:
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, int):
            return Rational(self.num + self.den * other, self.den)
        if not isinstance(other, Rational):
            return NotImplemented

        return Rational(
            self.num * other.den + self.den * other.num, self.den * other.den
        )

    def __sub__(self, other: object) -> Rational:
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, int):
            return Rational(self.num - self.den * other, self.den)
        if not isinstance(other, Rational):
            return NotImplemented

        return Rational(
            self.num * other.den - self.den * other.num, self.den * other.den
        )

    def __mul__(self, other: object) -> Rational:
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, int):
            return Rational(self.num * other, self.den)
        if not isinstance(other, Rational):
            return NotImplemented

        return Rational(self.num * other.num, self.den * other.den)

    def __truediv__(self, other: object) -> Rational:
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return Rational(self.num, self.den * other)
        if not isinstance(other, Rational):
            return NotImplemented

        if other == Rational():
            raise ZeroDivisionError(f"Cannot divide by {other!r}")

        return Rational(self.num * other.den, self.den * other.num)

    def __radd__(self, other: object) -> Rational:
        if isinstance(other, bool) or not isinstance(other, int):
            return NotImplemented
        return self + other

    def __rsub__(self, other: object) -> Rational:
        if isinstance(other, bool) or not isinstance(other, int):
            return NotImplemented
        return Rational(self.den * other - self.num, self.den)

    def __rmul__(self, other: object) -> Rational:
        if isinstance(other, bool) or not isinstance(other, int):
            return NotImplemented
        return self * other

    def __rtruediv__(self, other: object):
        if isinstance(other, bool) or not isinstance(other, int):
            return NotImplemented
        if self == Rational():
            raise ZeroDivisionError(f"Cannot divide by {self!r}")
        return Rational(other * self.den, self.num)

    def __pow__(self, power: object) -> Rational:
        if isinstance(power, bool) or not isinstance(power, int):
            return NotImplemented
        if power >= 0:
            return Rational(pow(self.num, power), pow(self.den, power))
        if self.num == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return Rational(pow(self.den, -power), pow(self.num, -power))

    def __neg__(self) -> Rational:
        return Rational(-self.num, self.den)

    def __abs__(self) -> Rational:
        return self if self >= Rational() else -self

    def __bool__(self) -> bool:
        return self != Rational()

    def __str__(self) -> str:
        return f"{self.num} / {self.den}"

    def __repr__(self) -> str:
        return f"Rational({self.num}, {self.den})"
