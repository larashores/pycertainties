from dataclasses import dataclass
from typing import Iterable, Union

import numpy as np

from uncertainties.strings import Real, uncertainty_str

IterableReal = Iterable[Union[Real, "IterableReal"]]  # type: ignore
RecursiveReal = Union[Real, IterableReal]  # type: ignore


@dataclass
class Val:
    """
    This class is number-like type that represents a value and associated uncertainty.

    Implements common mathmetical operators and a few mathmatics functions. Uses the following equation calulating
    uncertainties:
        δf(r_i) = √(Σ(df/dr_i^2*δr_i^2))

    Additionally, Val(a, b) comes with appropriate string conversions based on the relative and absolute values of
    a and b.

    Examples)
                                  Val(10, 4) - Val(4, 3) == Val(-10.0, 5.0)
                                       Val(63.5, 1) ** 3 == Val(256047.875, 12096.75)
                            Val(100, 2) + Val(50.5, 0.2) == Val(150.5, 2.009975124224178)
                                      Val(100, .1).sin() == Val(-0.5063656411097588, 0.08623188722876839)
                     Val(4.605170185988092, 0.001).log() == Val(4.605170185988092, 0.001)

                                  str(Val(321.8, .0324)) == "321.80 ± 0.03"
                                str(Val(321.856, .0324)) == "321.86 ± 0.03"
                                 str(Val(321.856, 3.86)) == "322 ± 4"
                               str(Val(-321.856, 11.34)) == "-322 ± 11"
                         str(Val(3.21856e-10, 3.24e-12)) == "(3.22 ± 0.03)e-10"
                            str(Val(3.21856e10, 3.24e8)) == "(3.22 ± 0.03)e10"
                            str(Val(3.21856e10, 1.24e8)) == "(3.219 ± 0.012)e10"
                str(Val(0.02094495456, 9.541774545e-05)) == "0.020945 ± 0.000095"
                str(Val(0.02094495456, 9.341774545e-05)) == "0.02094 ± 0.00009"
        str(Val(3559.8838983606497, 21.815841616631992)) == "3560 ± 20"

    """

    value: Real
    uncertainty: Real

    def __str__(self) -> str:
        return uncertainty_str(self.value, self.uncertainty)

    def __repr__(self) -> str:
        return f"Val({self.value}, {self.uncertainty})"

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
