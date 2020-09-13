import math
from typing import Tuple

import pytest

from tests import utilities
from uncertainties import calculations
from uncertainties.val import Val


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
        ("log(x)", {"x": Val(1605, 53)}, Val(math.log(1605), math.sqrt((53 ** 2) / (1605 ** 2)))),
        ("x-log(300)", {"x": Val(math.log(1605), math.log(53))}, Val(math.log(1605 / 300), math.log(53))),
        ("x*y+z", {"x": Val(3, 0.1), "y": Val(3, 3), "z": 4}, Val(13, math.sqrt(0.1 ** 2 * 3 ** 2 + 3 ** 2 * 3 ** 2))),
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
                "A": Val(3, 0.1),
                "B": [
                    1,
                    2,
                    Val(3, 0.3),
                    [4, Val(5, 0.5), [Val(6, 0.6)]],
                    [Val(7, 0.7), 8],
                ],
            },
            [
                Val(6, math.sqrt(4 * 0.1 ** 2 / 1 ** 2)),
                Val(3, math.sqrt(4 * 0.1 ** 2 / 2 ** 2)),
                Val(2, math.sqrt(4 * 3 ** 2 * 0.3 ** 2 / 3 ** 4 + 4 * 0.1 ** 2 / 3 ** 2)),
                [
                    Val(3 / 2, math.sqrt(4 * 0.1 ** 2 / 4 ** 2)),
                    Val(6 / 5, math.sqrt(4 * 3 ** 2 * 0.5 ** 2 / 5 ** 4 + 4 * 0.1 ** 2 / 5 ** 2)),
                    [Val(1, math.sqrt(4 * 3 ** 2 * 0.6 ** 2 / 6 ** 4 + 4 * 0.1 ** 2 / 6 ** 2))],
                ],
                [
                    Val(6 / 7, math.sqrt(4 * 3 ** 2 * 0.7 ** 2 / 7 ** 4 + 4 * 0.1 ** 2 / 7 ** 2)),
                    Val(3 / 4, math.sqrt(4 * 0.1 ** 2 / 8 ** 2)),
                ],
            ],
        ),
    ),
)
def test_calculate_list(expr, values, expected):
    result = calculations.calculate(expr, **values)

    for got, ex in zip(utilities.traverse(result), utilities.traverse(expected)):
        utilities.assert_approx(got, ex)
