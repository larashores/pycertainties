import collections
from dataclasses import dataclass
from numbers import Real

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from uncertainty_str import uncertainty_str

f = sp.symbols("f(...)")
df = sp.symbols("df(...)")
sp.init_printing(wrap_line=False)


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
            return Var(self.value ** power, np.sqrt(first + second))

    def __rpow__(self, other: "Var") -> "Var":
        return Var(other, 0) ** self

    def log(self) -> "Var":
        return Var(np.log(self.value), np.sqrt((self.uncertainty ** 2) / (self.value ** 2)))

    def sin(self) -> "Var":
        return Var(np.sin(self.value), np.sqrt((self.uncertainty ** 2) * (np.cos(self.value) ** 2)))

    def sqrt(self) -> "Var":
        return self ** (1 / 2)


def uncertainty(expr, variables, print_res=True):
    """
    Calculates an uncertainty in an expression without needing explicit values

    expr: A sympy expression or a string that it can parse (eg 2*x+yz)
    variables : A list of strings that may have uncertainty(eg ('x', 'y'))
    print_res: Whether to print out visual function
    """
    if type(expr) == str:
        expr = parse_expr(expr)
    squares = []
    for sym in expr.free_symbols:
        if sym.name not in variables:
            continue
        val = sp.diff(expr, sym) ** 2 * sp.symbols("d" + sym.name) ** 2
        squares.append(val)
    new_expr = 0
    for square in squares:
        new_expr += square
    new_expr = sp.sqrt(new_expr)

    #  Printing
    if print_res:
        sp.pprint(sp.Eq(f, expr))
        sp.pprint(sp.Eq(df, new_expr))
        print("")

    return new_expr


def create_subs_map(values):
    to_sub = {}
    for sym, val in values.items():
        if isinstance(val, Var):
            to_sub[sym] = val.value
            to_sub["d" + sym] = val.uncertainty
        else:
            to_sub[sym] = val
    return to_sub


def calc(expr, print_res=False, **values):
    """
    Calculates an expression with an uncertainty and returns the result

    expr: A sympy expression or a string that it can parse (eg 2*x+yz)
    print_res: Whether to print out visual function
    values: Each variable can be given a value and the uncertainy can be
        given a value by adding d to the front (eg x=2, dx=.02, y=3)
    """
    if type(expr) == str:
        expr = parse_expr(expr)
    variables = {
        sym.name: values[sym.name]
        for sym in expr.free_symbols
        if sym.name in values and isinstance(values[sym.name], Var)
    }
    uncertainty_expr = uncertainty(expr, variables, False)
    to_sub = create_subs_map(values)
    result = Var(float(expr.subs(to_sub).evalf()), float(uncertainty_expr.subs(to_sub).evalf()))

    #  Printing
    if print_res:
        sp.pprint(sp.Eq(f, expr))
        print("\t->", result.value)
        sp.pprint(sp.Eq(df, uncertainty_expr))
        print("\t->", result.uncertainty)
        print("")

    return result


def calc_array(expr, **values):
    """
    Calculates an expression with an uncertainty and returns the result. any of the inputs can be an array
    If there are array's they must all be the same shape, and the output will be array's of that shape. Each index of
    the resultant array will use the same index from the input arrays

    expr: A sympy expression or a string that it can parse (eg 2*x+yz)
    values: Each variable can be given a value and the uncertainy can be
        given a value by adding d to the front (eg x=[1, 2, 3, 4], dx=[.1, .2, .3, .4], y=3)
    """
    arrays = {}
    values_for_calc = {}
    shape = None
    for key, val in values.items():
        if isinstance(val, np.ndarray):
            arrays[key] = val
            if shape is None:
                shape = val.shape
            elif val.shape != shape:
                raise ValueError("All arrays must be of the same length")
        else:
            values_for_calc[key] = values[key]

    values = np.zeros(shape, dtype=object)
    for index in np.ndindex(shape):
        for key, array in arrays.items():
            values_for_calc[key] = array[index]
        values[index] = calc(expr, **values_for_calc)
    return values


def var_array(values, uncertainties):
    is_array = isinstance(uncertainties, np.ndarray)
    if is_array and values.shape != uncertainties.shape:
        raise ValueError("Values and uncertainties must have the same shape.")
    shape = values.shape
    vars = np.zeros(values.shape, dtype=Var)
    for index in np.ndindex(shape):
        uncertainty = uncertainties[index] if is_array else uncertainties
        vars[index] = Var(values[index], uncertainty)
    return vars


def from_var_array(var_array):
    return np.array([var.value for var in var_array]), np.array([var.uncertainty for var in var_array])


def average(values):
    return Var(
        np.average([x.value for x in values], weights=[x.uncertainty ** -2 for x in values]),
        np.average([x.uncertainty for x in values], weights=[x.uncertainty ** -2 for x in values]),
    )


if __name__ == "__main__":
    print("Just uncertainty")
    uncertainty("x*y+z", ["x", "y"], True)
    uncertainty("x ** y", ["y"], True)
    uncertainty("sin(x)", ["x"], True)

    print("Uncertainty calculation")
    print(calc("log(x)", x=Var(1605, 53)))
    print(calc("x-log(300)", x=Var(np.log(1605), np.log(53))))
    print(calc("x*y+z", x=Var(3, 0.1), y=Var(3, 3), z=4))
    print(calc("x*y+z", x=Var(3, 0.1), y=Var(3, 3), z=4))  # False makes it not print the result
    print()

    print("With array")
    array = np.array([[1, 2], [3, 4]])
    print(calc_array("(2*A)/B", A=Var(3, 0.1), B=var_array(array, array * 0.1)))
    print(calc_array("log(x)", x=np.array([Var(1605, 53)])))
    #
    # print('\nWith list')
    # lst = [[1, 2, 3, [4, 5, 6]], [7, 8]]
    # lst2 = [[.1, .2, .3, [.4, .5, .6]], [.7, .8]]
    # val, dval = calc_list('(2*A)/B', A=3, dA=.1, B=lst, dB=lst2)
    # print(val)
    # print(dval)
    #
    print("\nAverage")
    vals = var_array(np.array([1, 3, 4, 5, 6]), 0.1)
    print(average(vals))

    print("\nSubtraction")
    var = Var(3, 1)
    print(var - 1)
    print(4 - var)
