import math
from typing import Tuple

import pytest

from tests import utilities
from uncertainties import calculations
from uncertainties.var import Var


@pytest.mark.parametrize(
    "expr, variables, expected",
    (
        ("x*y+z", ("x", "y"), "sqrt(dx**2*y**2 + dy**2*x**2)"),
        ("x ** y", ("y"), "sqrt(dy**2*x**(2*y)*log(x)**2)"),
        ("sin(x)", ("x",), "sqrt(dx**2*cos(x)**2)"),
    ),
)
def test_uncertainty(expr: str, variables: Tuple[str], expected: str):
    assert str(calculations.uncertainty(expr, *variables)) == expected


@pytest.mark.parametrize(
    "expr, values, expected",
    (
        ("log(x)", {"x": Var(1605, 53)}, Var(math.log(1605), math.sqrt((53 ** 2) / (1605 ** 2)))),
        ("x-log(300)", {"x": Var(math.log(1605), math.log(53))}, Var(math.log(1605 / 300), math.log(53))),
        ("x*y+z", {"x": Var(3, 0.1), "y": Var(3, 3), "z": 4}, Var(13, math.sqrt(0.1 ** 2 * 3 ** 2 + 3 ** 2 * 3 ** 2))),
    ),
)
def test_calculate(expr, values, expected):
    utilities.assert_approx(calculations.calculate(expr, **values), expected)


@pytest.mark.parametrize(
    "expr, values, expected",
    (
        (
            "(2*A)/B",
            {
                "A": Var(3, 0.1),
                "B": [
                    1,
                    2,
                    Var(3, 0.3),
                    [4, Var(5, 0.5), [Var(6, 0.6)]],
                    [Var(7, 0.7), 8],
                ],
            },
            [
                Var(6, math.sqrt(4 * 0.1 ** 2 / 1 ** 2)),
                Var(3, math.sqrt(4 * 0.1 ** 2 / 2 ** 2)),
                Var(2, math.sqrt(4 * 3 ** 2 * 0.3 ** 2 / 3 ** 4 + 4 * 0.1 ** 2 / 3 ** 2)),
                [
                    Var(3 / 2, math.sqrt(4 * 0.1 ** 2 / 4 ** 2)),
                    Var(6 / 5, math.sqrt(4 * 3 ** 2 * 0.5 ** 2 / 5 ** 4 + 4 * 0.1 ** 2 / 5 ** 2)),
                    [Var(1, math.sqrt(4 * 3 ** 2 * 0.6 ** 2 / 6 ** 4 + 4 * 0.1 ** 2 / 6 ** 2))],
                ],
                [
                    Var(6 / 7, math.sqrt(4 * 3 ** 2 * 0.7 ** 2 / 7 ** 4 + 4 * 0.1 ** 2 / 7 ** 2)),
                    Var(3 / 4, math.sqrt(4 * 0.1 ** 2 / 8 ** 2)),
                ],
            ],
        ),
    ),
)
def test_calculate_list(expr, values, expected):
    result = calculations.calculate(expr, **values)

    for got, ex in zip(utilities.traverse(result), utilities.traverse(expected)):
        utilities.assert_approx(got, ex)
