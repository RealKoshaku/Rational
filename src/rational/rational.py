from math import gcd


class Rational:
    def __init__(self, num: int, den: int) -> None:
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
