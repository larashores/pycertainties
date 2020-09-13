from numbers import Real

import pytest

from uncertainties.strings import uncertainty_str


@pytest.mark.parametrize(
    "value, uncertainty, result",
    (
        (321.8, 0.0324, "321.80 ± 0.03"),
        (321.856, 0.0324, "321.86 ± 0.03"),
        (321.856, 3.86, "322 ± 4"),
        (-321.856, 11.34, "-322 ± 11"),
        (-32.1856, 1.134, "-32.2 ± 1.1"),
        (3.21856e-10, 3.24e-12, "(3.22 ± 0.03)e-10"),
        (3.21856e10, 3.24e8, "(3.22 ± 0.03)e10"),
        (3.21856e10, 1.24e8, "(3.219 ± 0.012)e10"),
        (0.02094495456, 9.541774545e-05, "0.020945 ± 0.000095"),
        (0.02094495456, 9.341774545e-05, "0.02094 ± 0.00009"),
        (3559.8838983606497, 21.815841616631992, "3560 ± 20"),
    ),
)
def test_uncertainty_str(value: Real, uncertainty: Real, result: str):
    assert uncertainty_str(value, uncertainty) == result
