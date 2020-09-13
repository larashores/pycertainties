from dataclasses import dataclass
from typing import Iterable, Union

import numpy as np

from uncertainties.strings import Real, uncertainty_str

IterableReal = Iterable[Union[Real, "IterableReal"]]
RecursiveReal = Union[Real, IterableReal]


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

    def __mul__(self, other: Union["Val", Real]) -> "Val":
        if isinstance(other, Val):
            return Val(
                self.value * other.value,
                np.sqrt((self.value ** 2) * (other.uncertainty ** 2) + (other.value ** 2) * (self.uncertainty ** 2)),
            )
        else:
            return Val(self.value * other, self.uncertainty * abs(other))

    def __rmul__(self, other: Real) -> "Val":
        return self.__mul__(other)

    def __truediv__(self, other: Union["Val", Real]) -> "Val":
        if isinstance(other, Val):
            return Val(
                self.value / other.value,
                np.sqrt(
                    (other.uncertainty ** 2) * (self.value ** 2 / other.value ** 4)
                    + (self.uncertainty ** 2 / other.value ** 2)
                ),
            )
        else:
            return Val(self.value / other, self.uncertainty / abs(other))

    def __rtruediv__(self, other: Real) -> "Val":
        return Val(other, 0) / self

    def __sub__(self, other: Union["Val", Real]) -> "Val":
        if isinstance(other, Val):
            return Val(self.value - other.value, np.sqrt(self.uncertainty ** 2 + other.uncertainty ** 2))
        else:
            return Val(self.value - other, self.uncertainty)

    def __rsub__(self, other: Real) -> "Val":
        return Val(other, 0) - self

    def __add__(self, other: Union["Val", Real]) -> "Val":
        if isinstance(other, Val):
            return Val(self.value + other.value, np.sqrt(self.uncertainty ** 2 + other.uncertainty ** 2))
        else:
            return Val(self.value + other, self.uncertainty)

    def __radd__(self, other: "Val") -> "Val":
        return self.__add__(other)

    def __neg__(self: "Val") -> "Val":
        return Val(-self.value, self.uncertainty)

    def __pow__(self, power: Union["Val", Real]) -> "Val":
        if isinstance(power, Val):
            square = self.value ** (2 * power.value)
            first = (self.uncertainty ** 2) * ((square * power.value ** 2) / (self.value ** 2))
            second = (power.uncertainty ** 2) * (square * np.log(self.value) ** 2)
            return Val(self.value ** power.value, np.sqrt(first + second))
        else:
            square = self.value ** (2 * power)
            return Val(
                self.value ** power, np.sqrt((self.uncertainty ** 2) * ((square * power ** 2) / (self.value ** 2)))
            )

    def __rpow__(self, other: Real) -> "Val":
        return Val(other, 0) ** self

    def log(self) -> "Val":
        return Val(np.log(self.value), np.sqrt((self.uncertainty ** 2) / (self.value ** 2)))

    def sin(self) -> "Val":
        return Val(np.sin(self.value), np.sqrt((self.uncertainty ** 2) * (np.cos(self.value) ** 2)))

    def sqrt(self) -> "Val":
        return self ** (1 / 2)
