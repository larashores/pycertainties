import dataclasses
from typing import Callable, Iterable, List, Tuple, TypeVar, Union

import numpy as np

from uncertainties.val import Val

T = TypeVar("T")
V = TypeVar("V")
RecursiveIterable = Iterable[Union[T, "RecursiveIterable"]]  # type: ignore
RecursiveList = List[Union[T, "RecursiveList"]]  # type: ignore


def operate_recursive(function: Callable[..., V], *iterables: RecursiveIterable[V]) -> RecursiveList[V]:
    """
    Applies a function to matching scalers of a group of iterables of the same shape that containing either more
    iterables or scalers, and returns a list of the same shape containing either more list or the output of each
    invocation of "function".

    Example)
        operate_recursviely(
            lambda *items: sum(items),
            [1, 2, 3, [4, 5, 6, [7, 8], 9], 10],
            [10, 20, 30, [40, 50, 60, [70, 80], 90], 100],
            [100, 200, 300, [400, 500, 600, [700, 800], 900], 1000],
        ) ==  [111, 222, 333, [444, 555, 666, [777, 888], 999], 1110],

    """
    return _operate_recursive(function, iterables, [])


def _operate_recursive(
    function: Callable[..., V], iterables: RecursiveIterable[V], result: RecursiveList[V]
) -> RecursiveList[V]:
    """Private function performing the work of operate_recursive recursively"""
    for items in zip(*iterables):  # type: ignore
        if any(isinstance(item, Iterable) for item in items):  # pylint: disable=W1116
            sub_result = []  # type: ignore
            _operate_recursive(function, items, sub_result)
        else:
            sub_result = function(*items)  # type: ignore
        result.append(sub_result)
    return result


def to_val_array(values: np.ndarray, uncertainties: np.ndarray) -> np.ndarray:
    """
    Converts two numpy arrays of float/integer types and combines them into a single numpy array of Val types where the
    values are taken from the first array and the uncertainties are taken from the second array.

    Example:
        to_val_array(np.array([10, 100, 80]), np.array([.1, .15, .35]))
            == np.array([Val(10, 0.1), Val(100, 0.15), Val(80, 0.35)])
    """
    is_array = isinstance(uncertainties, np.ndarray)
    if is_array and values.shape != uncertainties.shape:
        raise ValueError("Values and uncertainties must have the same shape.")
    shape = values.shape
    val_array = np.zeros(values.shape, dtype=Val)
    for index in np.ndindex(shape):
        uncertainty_value = uncertainties[index] if is_array else uncertainties
        val_array[index] = Val(values[index], uncertainty_value)
    return val_array


def from_val_array(val_array: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Converts a numpy array of Val types to a tuple where both item are numpy arrays of float/integer types where the
    first consists of the array's values where the second consists of the array's uncertainties.

        from_val_array(np.array([Val(10, 0.1), Val(100, 0.15), Val(80, 0.35)]))
            == (np.array([10, 100, 80]), np.array([.1, .15, .35]))
    """
    values = np.zeros(val_array.shape)
    uncertanties = np.zeros(val_array.shape)

    for ind in np.ndindex(val_array.shape):
        values[ind], uncertanties[ind] = dataclasses.astuple(val_array[ind])
    return values, uncertanties


def weighted_average(values: Iterable[Val]) -> Val:
    """
    Calculates a weighted average of a group of values with uncertainties.

    The weights of avg(x ± y) are equal to 1/y^2.
    """
    return Val(
        np.average([x.value for x in values], weights=[x.uncertainty ** -2 for x in values]),
        np.average([x.uncertainty for x in values], weights=[x.uncertainty ** -2 for x in values]),
    )
