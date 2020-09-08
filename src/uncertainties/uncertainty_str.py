def uncertainty_str(val, dval):
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


def _uncertainty_str_decimal(val, dval):
    try:
        dpow = _get_pow(dval)
        if _sci_str(abs(round(dval, -dpow)))[0] == "1":
            dpow -= 1
        val = round(val, -dpow)
        dval = round(dval, -dpow)
        precision = max(-dpow, 0)
    except ValueError:
        return f"{val} \u00b1 {dval}"

    return _try_format(val, precision), _try_format(dval, precision)


def _sci_str(num):
    return f"{num:e}"


def _get_pow(val):
    string = _sci_str(val)
    start_index = string.index("e") + 1
    return int(string[start_index:])


def _try_format(value, precision):
    try:
        fmt = "{:." + str(precision) + "f}"
        return fmt.format(value)
    except ValueError:
        return value


if __name__ == "__main__":
    print(uncertainty_str(321.8, 0.0324))
    print(uncertainty_str(321.856, 0.0324))
    print(uncertainty_str(321.856, 3.86))
    print(uncertainty_str(-321.856, 11.34))
    print(uncertainty_str(3.21856e-10, 3.24e-12))
    print(uncertainty_str(3.21856e10, 3.24e8))
    print(uncertainty_str(3.21856e10, 1.24e8))
    print(uncertainty_str(0.02094495456, 9.541774545e-05))
    print(uncertainty_str(0.02094495456, 9.341774545e-05))
    print(uncertainty_str(3559.8838983606497, 21.815841616631992))
