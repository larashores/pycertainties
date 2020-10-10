from typing import Tuple, Union

Real = Union[int, float]


def uncertainty_str(val: Real, dval: Real) -> str:
    """
    Given a value and its uncertainty, returns an appropriate string representation based on the relative and absolute
    values of the value and its uncertainty.

    Examples)
                                  Val(10, 4) - Val(4, 3) == Val(-10.0, 5.0)
                                       Val(63.5, 1) ** 3 == Val(256047.875, 12096.75)
                            Val(100, 2) + Val(50.5, 0.2) == Val(150.5, 2.009975124224178)
                                      Val(100, .1).sin() == Val(-0.5063656411097588, 0.08623188722876839)
                     Val(4.605170185988092, 0.001).log() == Val(4.605170185988092, 0.001)

                                  str(Val(321.8, .0324)) == "321.80 ± 0.03"
                                str(Val(321.856, .0324)) == "321.86 ± 0.03"
                                 str(Val(321.856, 3.86)) == "322 ± 4"
                               str(Val(-321.856, 11.34)) == "-322 ± 11"
                         str(Val(3.21856e-10, 3.24e-12)) == "(3.22 ± 0.03)e-10"
                            str(Val(3.21856e10, 3.24e8)) == "(3.22 ± 0.03)e10"
                            str(Val(3.21856e10, 1.24e8)) == "(3.219 ± 0.012)e10"
                str(Val(0.02094495456, 9.541774545e-05)) == "0.020945 ± 0.000095"
                str(Val(0.02094495456, 9.341774545e-05)) == "0.02094 ± 0.00009"
        str(Val(3559.8838983606497, 21.815841616631992)) == "3560 ± 20"
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
    """
    Private function used to calculate the non-exponential part of a string representation of a value and its
    uncertainty.
    """
    dpow = _get_pow(dval)
    if f"{abs(round(dval, -dpow)):e}"[0] == "1":
        dpow -= 1
    val = round(val, -dpow)
    dval = round(dval, -dpow)
    precision = max(-dpow, 0)

    return _format(val, precision), _format(dval, precision)


def _get_pow(val: Real) -> int:
    """Returns the power of a numbers exponential representation"""
    string = f"{val:e}"
    start_index = string.index("e") + 1
    return int(string[start_index:])


def _format(value: Real, precision: int) -> str:
    """Returns a string representation of value to the specified precision"""
    return f"{{:.{precision}f}}".format(value)
