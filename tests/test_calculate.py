import math
from typing import Dict, Tuple

import pytest

from tests import utilities
from uncertainties import calculations
from uncertainties.calculations import IterableValOrReal
from uncertainties.val import Val


@pytest.mark.parametrize(
    "expr, variables, expected",
    (
        ("x*y+z", ("x", "y"), "sqrt(x**2*δy**2 + y**2*δx**2)"),
        ("x ** y", ("y"), "sqrt(x**(2*y)*δy**2*log(x)**2)"),
        ("sin(x)", ("x",), "sqrt(δx**2*cos(x)**2)"),
    ),
)
def test_uncertainty(expr: str, variables: Tuple[str], expected: str):
    """Tests that the string representations of calculated uncertainty equations represent the correct equations"""
    assert str(calculations.uncertainty(expr, *variables)) == expected


@pytest.mark.parametrize(
    "expr, values, expected",
    (
        ("log(x)", {"x": Val(1605, 53)}, Val(math.log(1605), math.sqrt((53 ** 2) / (1605 ** 2)))),
        ("x-log(300)", {"x": Val(math.log(1605), math.log(53))}, Val(math.log(1605 / 300), math.log(53))),
        ("x*y+z", {"x": Val(3, 0.1), "y": Val(3, 3), "z": 4}, Val(13, math.sqrt(0.1 ** 2 * 3 ** 2 + 3 ** 2 * 3 ** 2))),
    ),
)
def test_calculate(expr: str, values: Dict[str, Val], expected: Val):
    """Tests that calculate works correctly with non-iterable values"""
    utilities.assert_approx(calculations.calculate(expr, **values), expected)  # type: ignore


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
def test_calculate_list(expr: str, values: Dict[str, IterableValOrReal], expected: IterableValOrReal):
    """
    Tests that the calculate function returns lists of the correct shape and values when calculating equation with
    iterable values.
    """
    result = calculations.calculate(expr, **values)

    for got, ex in zip(utilities.traverse(result), utilities.traverse(expected)):  # type: ignore
        utilities.assert_approx(got, ex)
