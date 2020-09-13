import numpy as np
import pytest

from tests.utilities import assert_approx, traverse
from uncertainties import utilities
from uncertainties.var import Var


@pytest.mark.parametrize(
    "values, uncertainties, expected",
    (
        (
            np.array([[1, 2], [3, 4]]),
            np.array([[0.1, 0.2], [0.3, 0.4]]),
            np.array([[Var(1.0, 0.1), Var(2, 0.2)], [Var(3, 0.3), Var(4.0, 0.4)]]),
        ),
    ),
)
def test_to_var_array(values: np.ndarray, uncertainties: np.ndarray, expected: np.ndarray):
    result = utilities.to_var_array(values, uncertainties)
    for ind in np.ndindex(result.shape):
        assert_approx(result[ind], expected[ind])


@pytest.mark.parametrize(
    "var_array, expected_values, expected_uncertainties",
    (
        (
            np.array([[Var(1.0, 0.1), Var(2, 0.2)], [Var(3, 0.3), Var(4.0, 0.4)]]),
            np.array([[1, 2], [3, 4]]),
            np.array([[0.1, 0.2], [0.3, 0.4]]),
        ),
    ),
)
def test_from_var_array(var_array: np.ndarray, expected_values: np.ndarray, expected_uncertainties: np.ndarray):
    values, uncertainties = utilities.from_var_array(var_array)
    assert values.shape == uncertainties.shape
    for ind in np.ndindex(var_array.shape):
        assert (values[ind], uncertainties[ind]) == pytest.approx((expected_values[ind], expected_uncertainties[ind]))


@pytest.mark.parametrize(
    "function, iterables, expected",
    (
        (
            lambda *items: sum(items),
            (
                [1, 2, 3, [4, 5, 6, [7, 8], 9], 10],
                [10, 20, 30, [40, 50, 60, [70, 80], 90], 100],
                [100, 200, 300, [400, 500, 600, [700, 800], 900], 1000],
            ),
            [111, 222, 333, [444, 555, 666, [777, 888], 999], 1110],
        ),
    ),
)
def test_reduce_recursive(function, iterables, expected):
    result = utilities.reduce_recursive(function, *iterables)
    for got, ex in zip(traverse(result), traverse(expected)):
        assert_approx(got, ex)


@pytest.mark.parametrize(
    "values, expected",
    (
        (
            # If all have same uncertainty this is just a simple average,
            (Var(5, 1), Var(6, 1), Var(7, 1), Var(4, 1), Var(4, 1)),
            Var(26 / 5, 1.0),
        ),
        (
            # Value with large uncertainty does not skew result
            (
                Var(1, 0.1),
                Var(3, 0.1),
                Var(2, 0.01),
                Var(100, 50),
                Var(3, 0.2),
            ),
            Var(2.002448821420095, 0.012226894387211954),
        ),
    ),
)
def test_weighted_average(values, expected):
    res = utilities.weighted_average(values)
    print(res.value, res.uncertainty)
    assert_approx(utilities.weighted_average(values), expected)
