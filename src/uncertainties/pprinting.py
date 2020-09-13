import math
from typing import Union

import sympy as sp
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import parse_expr

from uncertainties.calculations import calculate, uncertainty
from uncertainties.var import Var

f = sp.symbols("f(...)")
df = sp.symbols("df(...)")


def pprint_uncertainty(expr: Union[str, Expr], *variables: str) -> None:
    if isinstance(expr, str):
        expr = parse_expr(expr)

    sp.pprint(sp.Eq(f, expr))
    sp.pprint(sp.Eq(df, uncertainty(expr, *variables)))


def pprint_calculation(expr: Union, **values):
    if isinstance(expr, str):
        expr = parse_expr(expr)

    result = calculate(expr, **values)

    sp.pprint(sp.Eq(f, expr))
    print("\t->", result.value)

    sp.pprint(sp.Eq(df, uncertainty(expr, *(key for key, value in values.items() if isinstance(value, Var)))))
    print("\t->", result.uncertainty)


def main():
    print("Just uncertainty")
    pprint_uncertainty(
        "x*y+z",
        "x",
        "y",
    )
    print()
    pprint_uncertainty(
        "x ** y",
        "y",
    )
    print()
    pprint_uncertainty("sin(x)", "x")
    print()

    print("Uncertainty calculation")
    pprint_calculation("log(x)", x=Var(1605, 53))
    print()
    pprint_calculation("x-log(300)", x=Var(math.log(1605), math.log(53)))
    print()
    pprint_calculation("x*y+z", x=Var(3, 0.1), y=Var(3, 3), z=4)
    print()
    pprint_calculation("x*y+z", x=Var(3, 0.1), y=Var(3, 3), z=4)
    print()


if __name__ == "__main__":
    main()
