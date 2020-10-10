from typing import Dict, Iterable, List, Union

import sympy as sp
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import parse_expr

from uncertainties import utilities as utils
from uncertainties.val import Real, Val

IterableValOrReal = Iterable[Union["Val", Real, "IterableValOrReal"]]  # type: ignore
ListValOrReal = List[Union["Val", Real, "ListValOrReal"]]  # type: ignore


def uncertainty(expr: Union[str, Expr], *variables: str) -> Expr:
    """
    Given either a string representation of an equation or sympy expression, and any number of 'variables', which
    represent values which have an associated uncertainty (vs cosntants, which have no uncertainty), returns a sympy
    expression representing the uncertainty of the equation.

    Example)
        repr(uncertainty("x*y + z", "x", "y")) == "sqrt(dx**2*y**2 + dy**2*x**2)"
    """
    if isinstance(expr, str):
        expr = parse_expr(expr)

    return sp.sqrt(
        sum(
            sp.diff(expr, sym) ** 2 * sp.symbols("δ" + sym.name) ** 2
            for sym in expr.free_symbols
            if sym.name in variables
        )
    )


def calculate(expr: Union[str, Expr], **values: Union["Val", Real, IterableValOrReal]) -> Union["Val", ListValOrReal]:
    """
    Given either a string representation of an equation or sympy expression, and keys corresponding to each symbol in
    the eqtn/expr mapped to values of the symbols, calculates and returns result of that equation.

    Each value may either be a:
        1) int/float
        2) A Val object
        3) An iterable of more iterables or Val objects

    All iterable values must be of the same shape. The return type depends on if there were any iterable values.
        1) If there were no iterable values
            - A single Val object with the result
        2) If there were any iterable values (all of the same shape)
            - A list of the same shape as the iterables with scalers of Val types

    Example)
        calculate("x*y + z", x=Val(3, 0.1), y=Val(3, 1), z=4) == Val(13.0, 3.0149626863362666)

        calculate("x*y + z", x=Val(3, 0.1), y=[Val(3, 1), [Val(5, 1)]], z=4)
            == [Val(13.0, 3.0149626863362666), [Val(19.0, 3.0413812651491092)]]
    """
    if isinstance(expr, str):
        expr = parse_expr(expr)

    # pylint: disable=W1116
    constants = {key: value for key, value in values.items() if not isinstance(value, Iterable)}
    iterables = {key: value for key, value in values.items() if isinstance(value, Iterable)}

    if any(iterables):
        return utils.operate_recursive(
            lambda *items: _calculate(expr, **dict(zip(iterables.keys(), items)), **constants),
            *iterables.values(),
        )
    else:
        return _calculate(expr, **constants)


def _calculate(expr: Union[str, Expr], **values: Union[Val, Real]) -> Val:
    """
    Performs the same calculations as _calculate(...); however, all values must either be int/floats or Val types.
    """
    if isinstance(expr, str):
        expr = parse_expr(expr)

    uncertainty_expr = uncertainty(expr, *(key for key, value in values.items() if isinstance(value, Val)))
    to_sub = _substitution_map(**values)
    return Val(float(expr.subs(to_sub).evalf()), float(uncertainty_expr.subs(to_sub).evalf()))


def _substitution_map(**values: Union[Val, Real]) -> Dict[str, Real]:
    """
    Given string keys mapping to int/float/Val values, creates a map where:
        1) If the value is an int/float
            - The key is mapped to the value
        2) If the value is a Val object
            - The key is mapped to Val.value
            - The string f"δ{key}" is mapped to Val.uncertainty
    """
    to_sub = {}
    for sym, val in values.items():
        if isinstance(val, Val):
            to_sub[sym] = val.value
            to_sub["δ" + sym] = val.uncertainty
        else:
            to_sub[sym] = val
    return to_sub
