from dataclasses import dataclass
from numbers import Real

import numpy as np

from uncertainties.strings import uncertainty_str


@dataclass
class Val:
    value: Real
    uncertainty: Real

    def __str__(self) -> str:
        return uncertainty_str(self.value, self.uncertainty)

    def __repr__(self) -> str:
        return f"({self})"

    def __format__(self, format_spec: str) -> str:
        return str(self)

    def __mul__(self, other: "Val") -> "Val":
        if isinstance(other, Real):
            return Val(self.value * other, self.uncertainty * abs(other))
        elif isinstance(other, Val):
            return Val(
                self.value * other.value,
                np.sqrt((self.value ** 2) * (other.uncertainty ** 2) + (other.value ** 2) * (self.uncertainty ** 2)),
            )

    def __rmul__(self, other: "Val") -> "Val":
        return self.__mul__(other)

    def __truediv__(self, other: "Val") -> "Val":
        if isinstance(other, Real):
            return Val(self.value / other, self.uncertainty / abs(other))
        elif isinstance(other, Val):
            return Val(
                self.value / other.value,
                np.sqrt(
                    (other.uncertainty ** 2) * (self.value ** 2 / other.value ** 4)
                    + (self.uncertainty ** 2 / other.value ** 2)
                ),
            )

    def __rtruediv__(self, other: "Val") -> "Val":
        return Val(other, 0) / self

    def __sub__(self, other: "Val") -> "Val":
        if isinstance(other, Real):
            return Val(self.value - other, self.uncertainty)
        elif isinstance(other, Val):
            return Val(self.value - other.value, np.sqrt(self.uncertainty ** 2 + other.uncertainty ** 2))

    def __rsub__(self, other: "Val") -> "Val":
        return Val(other, 0) - self

    def __add__(self, other: "Val") -> "Val":
        if isinstance(other, Real):
            return Val(self.value + other, self.uncertainty)
        elif isinstance(other, Val):
            return Val(self.value + other.value, np.sqrt(self.uncertainty ** 2 + other.uncertainty ** 2))

    def __radd__(self, other: "Val") -> "Val":
        return self.__add__(other)

    def __neg__(self: "Val") -> "Val":
        return Val(-self.value, self.uncertainty)

    def __pow__(self, power: "Val") -> "Val":
        if isinstance(power, Real):
            square = self.value ** (2 * power)
            return Val(
                self.value ** power, np.sqrt((self.uncertainty ** 2) * ((square * power ** 2) / (self.value ** 2)))
            )
        elif isinstance(power, Val):
            square = self.value ** (2 * power.value)
            first = (self.uncertainty ** 2) * ((square * power.value ** 2) / (self.value ** 2))
            second = (power.uncertainty ** 2) * (square * np.log(self.value) ** 2)
            return Val(self.value ** power.value, np.sqrt(first + second))

    def __rpow__(self, other: "Val") -> "Val":
        return Val(other, 0) ** self

    def log(self) -> "Val":
        return Val(np.log(self.value), np.sqrt((self.uncertainty ** 2) / (self.value ** 2)))

    def sin(self) -> "Val":
        return Val(np.sin(self.value), np.sqrt((self.uncertainty ** 2) * (np.cos(self.value) ** 2)))

    def sqrt(self) -> "Val":
        return self ** (1 / 2)
