import dataclasses
import math
from numbers import Real
from typing import Union

import pytest

from uncertainties.var import Var


@pytest.mark.parametrize(
    "var1, var2, expected",
    (
        (Var(10, math.sqrt(7)), Var(5, math.sqrt(2)), Var(5, 3)),
        (Var(10, 3.21), 2, Var(8, 3.21)),
        (10, Var(5, 3.21), Var(5, 3.21)),
        (-5, Var(5, 3.21), Var(-10, 3.21)),
    ),
)
def test_subtraction(var1: Union[Real, Var], var2: Union[Real, Var], expected: Var):
    assert dataclasses.astuple(var1 - var2) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "var1, var2, expected",
    (
        (Var(10, math.sqrt(7)), Var(5, math.sqrt(2)), Var(15, 3)),
        (Var(10, 3.21), 2, Var(12, 3.21)),
        (10, Var(5, 3.21), Var(15, 3.21)),
        (-2, Var(5, 3.21), Var(3, 3.21)),
    ),
)
def test_addition(var1: Union[Real, Var], var2: Union[Real, Var], expected: Var):
    assert dataclasses.astuple(var1 + var2) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "var1, var2, expected",
    (
        (Var(10, 2), Var(5, 3), Var(50, math.sqrt((10 ** 2) * (3 ** 2) + (5 ** 2) * (2 ** 2)))),
        (Var(10, 3.21), 2, Var(20, math.sqrt((2 ** 2) * (3.21 ** 2)))),
        (10, Var(5, 3.21), Var(50, math.sqrt((10 ** 2) * (3.21 ** 2)))),
        (-2, Var(5, 3.21), Var(-10, math.sqrt((2 ** 2) * (3.21 ** 2)))),
    ),
)
def test_multiplication(var1: Union[Real, Var], var2: Union[Real, Var], expected: Var):
    assert dataclasses.astuple(var1 * var2) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "var1, var2, expected",
    (
        (Var(10, 2), Var(5, 3), Var(2, math.sqrt(3 ** 2 * ((10 ** 2) / (5 ** 4)) + (2 ** 2) / (5 ** 2)))),
        (Var(10, 2), 2, Var(5, math.sqrt(1))),
        (15, Var(3, 1), Var(5, math.sqrt((15 ** 2) / (3 ** 4)))),
    ),
)
def test_division(var1: Union[Real, Var], var2: Union[Real, Var], expected: Var):
    assert dataclasses.astuple(var1 / var2) == pytest.approx(dataclasses.astuple(expected))


def _power_uncertainty(a: Real, b: Real, x: Real, y: Real) -> Real:
    s = a ** (2 * x)
    first = (b ** 2) * ((s * x ** 2) / (a ** 2))
    second = (y ** 2) * (s * math.log(a) ** 2)
    return math.sqrt(first + second)


@pytest.mark.parametrize(
    "var, power, expected",
    (
        (Var(10, 3), Var(2, 1), Var(100, _power_uncertainty(10, 3, 2, 1))),
        (Var(10, 3), 2, Var(100, _power_uncertainty(10, 3, 2, 0))),
        (10, Var(2, 1), Var(100, _power_uncertainty(10, 0, 2, 1))),
    ),
)
def test_power(var: Union[Real, Var], power: Union[Real, Var], expected: Var):
    assert dataclasses.astuple(var ** power) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "var, expected",
    ((Var(10, 2), Var(math.log(10), math.sqrt((2 ** 2) / (10 ** 2)))),),
)
def test_log(var: Var, expected: Var):
    assert dataclasses.astuple(var.log()) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "var, expected",
    ((Var(10, 2), Var(math.sin(10), math.sqrt((2 ** 2) * (math.cos(10) ** 2)))),),
)
def test_sin(var: Var, expected: Var):
    assert dataclasses.astuple(var.sin()) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "var, expected",
    ((Var(16, 3), Var(4, _power_uncertainty(16, 3, 1 / 2, 0))),),
)
def test_sqrt(var: Var, expected: Var):
    assert dataclasses.astuple(var.sqrt()) == pytest.approx(dataclasses.astuple(expected))
