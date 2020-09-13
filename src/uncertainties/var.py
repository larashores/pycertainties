from dataclasses import dataclass
from numbers import Real

import numpy as np

from uncertainties.strings import uncertainty_str


@dataclass
class Var:
    value: Real
    uncertainty: Real

    def __str__(self) -> str:
        return uncertainty_str(self.value, self.uncertainty)

    def __repr__(self) -> str:
        return f"({self})"

    def __format__(self, format_spec: str) -> str:
        return str(self)

    def __mul__(self, other: "Var") -> "Var":
        if isinstance(other, Real):
            return Var(self.value * other, self.uncertainty * abs(other))
        elif isinstance(other, Var):
            return Var(
                self.value * other.value,
                np.sqrt((self.value ** 2) * (other.uncertainty ** 2) + (other.value ** 2) * (self.uncertainty ** 2)),
            )

    def __rmul__(self, other: "Var") -> "Var":
        return self.__mul__(other)

    def __truediv__(self, other: "Var") -> "Var":
        if isinstance(other, Real):
            return Var(self.value / other, self.uncertainty / abs(other))
        elif isinstance(other, Var):
            return Var(
                self.value / other.value,
                np.sqrt(
                    (other.uncertainty ** 2) * (self.value ** 2 / other.value ** 4)
                    + (self.uncertainty ** 2 / other.value ** 2)
                ),
            )

    def __rtruediv__(self, other: "Var") -> "Var":
        return Var(other, 0) / self

    def __sub__(self, other: "Var") -> "Var":
        if isinstance(other, Real):
            return Var(self.value - other, self.uncertainty)
        elif isinstance(other, Var):
            return Var(self.value - other.value, np.sqrt(self.uncertainty ** 2 + other.uncertainty ** 2))

    def __rsub__(self, other: "Var") -> "Var":
        return Var(other, 0) - self

    def __add__(self, other: "Var") -> "Var":
        if isinstance(other, Real):
            return Var(self.value + other, self.uncertainty)
        elif isinstance(other, Var):
            return Var(self.value + other.value, np.sqrt(self.uncertainty ** 2 + other.uncertainty ** 2))

    def __radd__(self, other: "Var") -> "Var":
        return self.__add__(other)

    def __neg__(self: "Var") -> "Var":
        return Var(-self.value, self.uncertainty)

    def __pow__(self, power: "Var") -> "Var":
        if isinstance(power, Real):
            square = self.value ** (2 * power)
            return Var(
                self.value ** power, np.sqrt((self.uncertainty ** 2) * ((square * power ** 2) / (self.value ** 2)))
            )
        elif isinstance(power, Var):
            square = self.value ** (2 * power.value)
            first = (self.uncertainty ** 2) * ((square * power.value ** 2) / (self.value ** 2))
            second = (power.uncertainty ** 2) * (square * np.log(self.value) ** 2)
            return Var(self.value ** power.value, np.sqrt(first + second))

    def __rpow__(self, other: "Var") -> "Var":
        return Var(other, 0) ** self

    def log(self) -> "Var":
        return Var(np.log(self.value), np.sqrt((self.uncertainty ** 2) / (self.value ** 2)))

    def sin(self) -> "Var":
        return Var(np.sin(self.value), np.sqrt((self.uncertainty ** 2) * (np.cos(self.value) ** 2)))

    def sqrt(self) -> "Var":
        return self ** (1 / 2)
