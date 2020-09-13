from numbers import Real
from typing import Tuple


def uncertainty_str(val: Real, dval: Real) -> str:
    """
    Returns a string that holds both a value and an uncertainty

    value: The value
    dvalue: The uncertainty
    """
    try:
        vpow = _get_pow(val)
    except ValueError:
        vpow = 1
    if -3 <= vpow <= 3:
        return "{} \u00b1 {}".format(*_uncertainty_str_decimal(val, dval))
    else:
        val *= 10 ** -vpow
        dval *= 10 ** -vpow
        return "({} \u00b1 {})e{}".format(*_uncertainty_str_decimal(val, dval), vpow)


def _uncertainty_str_decimal(val: Real, dval: Real) -> Tuple[str, str]:
    try:
        dpow = _get_pow(dval)
        if _sci_str(abs(round(dval, -dpow)))[0] == "1":
            dpow -= 1
        val = round(val, -dpow)
        dval = round(dval, -dpow)
        precision = max(-dpow, 0)
    except ValueError:
        return f"{val} \u00b1 {dval}"

    return _format(val, precision), _format(dval, precision)


def _sci_str(num: Real) -> str:
    return f"{num:e}"


def _get_pow(val: Real) -> int:
    string = _sci_str(val)
    start_index = string.index("e") + 1
    return int(string[start_index:])


def _format(value: Real, precision: int) -> str:
    return f"{{:.{precision}f}}".format(value)
