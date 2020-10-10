from typing import Union

import sympy as sp
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import parse_expr

from uncertainties.calculations import Real, calculate, uncertainty
from uncertainties.val import Val

f = sp.symbols("f(...)")
df = sp.symbols("δf(...)")


def pprint_uncertainty(expr: Union[str, Expr], *variables: str) -> None:
    """
    Given either a string representation of an equation or sympy expression, and any number of 'variables', which
    represent values which have an associated uncertainty (vs cosntants, which have no uncertainty), pretty-prints the
    equation and the uncertainty of the result of the equation.

    Example)
        pprint_uncertainty("x*y + z", "x", "y") ->
            f(...) = x⋅y + z
                        _________________
                        ╱   2  2     2  2
            δf(...) = ╲╱  dx ⋅y  + dy ⋅x
    """
    if isinstance(expr, str):
        expr = parse_expr(expr)

    sp.pprint(sp.Eq(f, expr))
    sp.pprint(sp.Eq(df, uncertainty(expr, *variables)))


def pprint_calculation(expr: Union[str, Expr], **values: Union["Val", Real]) -> None:
    """
    Given either a string representation of an equation or sympy expression, and the values of all symbols in the
    equation, pretty-prints the equation, the result, the uncertainty equation of the equaltion, and its result.

    Each value may be an int/float or a Val type.

    Example)
        pprint_calculation("x*y + z", x=Val(3, 0.1), y=Val(3, 3), z=4) ->
            f(...) = x⋅y + z
            -> 13.0
                        _________________
                        ╱   2  2     2  2
            δf(...) = ╲╱  dx ⋅y  + dy ⋅x
                -> 9.00499861188218
    """
    if isinstance(expr, str):
        expr = parse_expr(expr)

    result = calculate(expr, **values)

    sp.pprint(sp.Eq(f, expr))
    print("\t->", result.value)  # type: ignore

    sp.pprint(sp.Eq(df, uncertainty(expr, *(key for key, value in values.items() if isinstance(value, Val)))))
    print("\t->", result.uncertainty)  # type: ignore
