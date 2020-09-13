import dataclasses
from typing import Callable, Iterable, Tuple, TypeVar, Union

import numpy as np

from uncertainties.val import Val

T = TypeVar("T")
V = TypeVar("V")
Recursive = Iterable[Union[T, "Recursive"]]


def reduce_recursive(function: Callable[..., V], *iterables: Recursive[V]) -> Recursive[V]:
    return _reduce_recursive(function, iterables, [])


def _reduce_recursive(function: Callable[..., V], iterables: Recursive[V], result: Recursive[V]) -> Recursive[V]:
    for items in zip(*iterables):
        if any(isinstance(item, Iterable) for item in items):
            sub_result = []
            _reduce_recursive(function, items, sub_result)
        else:
            sub_result = function(*items)
        result.append(sub_result)
    return result


def to_val_array(values: np.ndarray, uncertainties: np.ndarray) -> np.ndarray:
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
    values = np.zeros(val_array.shape)
    uncertanties = np.zeros(val_array.shape)

    for ind in np.ndindex(val_array.shape):
        values[ind], uncertanties[ind] = dataclasses.astuple(val_array[ind])
    return values, uncertanties


def weighted_average(values: Iterable) -> Val:
    return Val(
        np.average([x.value for x in values], weights=[x.uncertainty ** -2 for x in values]),
        np.average([x.uncertainty for x in values], weights=[x.uncertainty ** -2 for x in values]),
    )
