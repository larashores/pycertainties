from numbers import Real
from typing import Dict, Iterable, Union

import sympy as sp
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import parse_expr

from uncertainties import utilities as utils
from uncertainties.var import Var


def uncertainty(expr: Union[str, Expr], *variables: str) -> Expr:
    if isinstance(expr, str):
        expr = parse_expr(expr)

    return sp.sqrt(
        sum(
            sp.diff(expr, sym) ** 2 * sp.symbols("d" + sym.name) ** 2
            for sym in expr.free_symbols
            if sym.name in variables
        )
    )


def calculate(expr: Union[str, Expr], **values):
    if isinstance(expr, str):
        expr = parse_expr(expr)

    constants = {key: value for key, value in values.items() if not isinstance(value, Iterable)}
    iterables = {key: value for key, value in values.items() if isinstance(value, Iterable)}

    if any(iterables):
        return utils.reduce_recursive(
            lambda *items: _calculate(expr, **dict(zip(iterables.keys(), items)), **constants),
            *iterables.values(),
        )
    else:
        return _calculate(expr, **constants)


def _calculate(expr: Union[str, Expr], **values: Union[Var, Real]) -> Real:
    if isinstance(expr, str):
        expr = parse_expr(expr)

    uncertainty_expr = uncertainty(expr, *(key for key, value in values.items() if isinstance(value, Var)))
    to_sub = _create_subs_map(**values)
    result = Var(float(expr.subs(to_sub).evalf()), float(uncertainty_expr.subs(to_sub).evalf()))
    return result


def _create_subs_map(**values: Union[Var, Real]) -> Dict[str, Real]:
    to_sub = {}
    for sym, val in values.items():
        if isinstance(val, Var):
            to_sub[sym] = val.value
            to_sub["d" + sym] = val.uncertainty
        else:
            to_sub[sym] = val
    return to_sub
