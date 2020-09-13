import dataclasses
import math
from numbers import Real
from typing import Union

import pytest

from uncertainties.val import Val


@pytest.mark.parametrize(
    "val1, val2, expected",
    (
        (Val(10, math.sqrt(7)), Val(5, math.sqrt(2)), Val(5, 3)),
        (Val(10, 3.21), 2, Val(8, 3.21)),
        (10, Val(5, 3.21), Val(5, 3.21)),
        (-5, Val(5, 3.21), Val(-10, 3.21)),
    ),
)
def test_subtraction(val1: Union[Real, Val], val2: Union[Real, Val], expected: Val):
    assert dataclasses.astuple(val1 - val2) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "val1, val2, expected",
    (
        (Val(10, math.sqrt(7)), Val(5, math.sqrt(2)), Val(15, 3)),
        (Val(10, 3.21), 2, Val(12, 3.21)),
        (10, Val(5, 3.21), Val(15, 3.21)),
        (-2, Val(5, 3.21), Val(3, 3.21)),
    ),
)
def test_addition(val1: Union[Real, Val], val2: Union[Real, Val], expected: Val):
    assert dataclasses.astuple(val1 + val2) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "val1, val2, expected",
    (
        (Val(10, 2), Val(5, 3), Val(50, math.sqrt((10 ** 2) * (3 ** 2) + (5 ** 2) * (2 ** 2)))),
        (Val(10, 3.21), 2, Val(20, math.sqrt((2 ** 2) * (3.21 ** 2)))),
        (10, Val(5, 3.21), Val(50, math.sqrt((10 ** 2) * (3.21 ** 2)))),
        (-2, Val(5, 3.21), Val(-10, math.sqrt((2 ** 2) * (3.21 ** 2)))),
    ),
)
def test_multiplication(val1: Union[Real, Val], val2: Union[Real, Val], expected: Val):
    assert dataclasses.astuple(val1 * val2) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "val1, val2, expected",
    (
        (Val(10, 2), Val(5, 3), Val(2, math.sqrt(3 ** 2 * ((10 ** 2) / (5 ** 4)) + (2 ** 2) / (5 ** 2)))),
        (Val(10, 2), 2, Val(5, math.sqrt(1))),
        (15, Val(3, 1), Val(5, math.sqrt((15 ** 2) / (3 ** 4)))),
    ),
)
def test_division(val1: Union[Real, Val], val2: Union[Real, Val], expected: Val):
    assert dataclasses.astuple(val1 / val2) == pytest.approx(dataclasses.astuple(expected))


def _power_uncertainty(a: Real, b: Real, x: Real, y: Real) -> Real:
    s = a ** (2 * x)
    first = (b ** 2) * ((s * x ** 2) / (a ** 2))
    second = (y ** 2) * (s * math.log(a) ** 2)
    return math.sqrt(first + second)


@pytest.mark.parametrize(
    "val, power, expected",
    (
        (Val(10, 3), Val(2, 1), Val(100, _power_uncertainty(10, 3, 2, 1))),
        (Val(10, 3), 2, Val(100, _power_uncertainty(10, 3, 2, 0))),
        (10, Val(2, 1), Val(100, _power_uncertainty(10, 0, 2, 1))),
    ),
)
def test_power(val: Union[Real, Val], power: Union[Real, Val], expected: Val):
    assert dataclasses.astuple(val ** power) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "val, expected",
    ((Val(10, 2), Val(math.log(10), math.sqrt((2 ** 2) / (10 ** 2)))),),
)
def test_log(val: Val, expected: Val):
    assert dataclasses.astuple(val.log()) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "val, expected",
    ((Val(10, 2), Val(math.sin(10), math.sqrt((2 ** 2) * (math.cos(10) ** 2)))),),
)
def test_sin(val: Val, expected: Val):
    assert dataclasses.astuple(val.sin()) == pytest.approx(dataclasses.astuple(expected))


@pytest.mark.parametrize(
    "val, expected",
    ((Val(16, 3), Val(4, _power_uncertainty(16, 3, 1 / 2, 0))),),
)
def test_sqrt(val: Val, expected: Val):
    assert dataclasses.astuple(val.sqrt()) == pytest.approx(dataclasses.astuple(expected))
