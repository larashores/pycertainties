from typing import Union

import sympy as sp
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import parse_expr

from uncertainties.calculations import RecursiveValOrReal, calculate, uncertainty
from uncertainties.val import Val

f = sp.symbols("f(...)")
df = sp.symbols("df(...)")


def pprint_uncertainty(expr: Union[str, Expr], *variables: str) -> None:
    if isinstance(expr, str):
        expr = parse_expr(expr)

    sp.pprint(sp.Eq(f, expr))
    sp.pprint(sp.Eq(df, uncertainty(expr, *variables)))


def pprint_calculation(expr: Union[str, Expr], **values: RecursiveValOrReal) -> None:
    if isinstance(expr, str):
        expr = parse_expr(expr)

    result = calculate(expr, **values)

    sp.pprint(sp.Eq(f, expr))
    print("\t->", result.value)

    sp.pprint(sp.Eq(df, uncertainty(expr, *(key for key, value in values.items() if isinstance(value, Val)))))
    print("\t->", result.uncertainty)
