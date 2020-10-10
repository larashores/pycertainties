from typing import Generator, Iterable, Union

import pytest

from pycertainties.calculations import IterableValOrReal
from pycertainties.val import Real, Val


def assert_approx(got: Union[Val, Real], expected: Union[Val, Real]) -> None:
    """
    Asserts that two Vals/ints/floats are approximately equal to each other (to account for floating-point errors)
    """
    got_value, got_uncertainty = (got.value, got.uncertainty) if isinstance(got, Val) else (got, 0)
    ex_value, ex_uncertainty = (expected.value, expected.uncertainty) if isinstance(expected, Val) else (expected, 0)
    assert (got_value, got_uncertainty) == pytest.approx((ex_value, ex_uncertainty))


def traverse(items: IterableValOrReal) -> Generator[Union[Val, Real], None, None]:
    """Generator that traverses an iterable of more iterables or scalars, generating each scalar"""
    for item in items:
        if isinstance(item, Iterable):  # pylint: disable=W1116
            for value in traverse(item):
                yield value
        else:
            yield item
