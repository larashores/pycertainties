# uncertainties

For all functions ![f\left( ;x_0,x_1,...,x_i\right)](https://latex.codecogs.com/svg.latex?f\left(&space;x_0,x_1,...,x_i\right)), where each value ![x_i](https://latex.codecogs.com/svg.latex?x_i) has an associated uncertainty ![\delta x_i](https://latex.codecogs.com/svg.latex?\delta&space;x_i), the uncertainty of the function ![\delta f](https://latex.codecogs.com/svg.latex?\delta&space;f), is equal to:

![\Large \delta f=\sqrt{\sum_{i}{\left(\frac{\partial f}{\partial x_i}\right)}^2(\delta x_i)^2}](https://latex.codecogs.com/svg.latex?&space;\delta&space;f=\sqrt{\sum_{i}{\left(\frac{\partial&space;f}{\partial&space;x_i}\right)}^2(\delta&space;x_i)^2})

This module contains various utilities for working determining, calculating, and working with values with uncertainties. All of the functions and types in the submodules below are also accesible directly from the `uncertainties` module.

## uncertainties.val

The `val` submodule provides a single type, `Val`, that can be used to store values that have an associated uncertainty, and perform calculations on those value as if they were any other number.

For example, the value 10.33 ± .12 is represented by `Val(10.33, 0.12)`. 


The `str` conversion returns a sensible representation of the `Val`.

    >>> Val(10.33, 0.12)
    10.33 ± 0.12
    >>> Val(3.21856e-10, 3.24e-12)
    (3.22 ± 0.03)e-10
    >>> Val(0.02094495456, 9.541774545e-05)
    0.020945 ± 0.000095

We can use the usual operators with `Val` types.

    >>> Val(10.33, 0.12) * 4
    41.3 ± 0.5
    >>> Val(41.32, 0.48) / 4
    10.33 ± 0.12
    >>> Val(10.33, 0.12) + Val(3, .5)
    13.3 ± 0.5
    >>> Val(10.33, 0.12) - Val(3, .5)
    7.3 ± 0.5
    >>> Val(10.33, 0.12) ** 2
    107 ± 2
    >>> Val(10.33, 0.12).sqrt()
    3.21 ± 0.02
    >>> Val(10.33, 0.12).sin()
    -0.79 ± 0.07
    >>> Val(10.33, 0.12).log()
    2.335 ± 0.012

## uncertainties.calculations

One possible concern with using `Val`s are accumulated round-off errors. Especially for computing uncertainties of more complex functions, the amount of intermediate steps can be signifigant, and the round-off errors add up.
If these errors are a concern, the `calculations.calculate(...)` function provides a way to first calculate the uncertainty equation of an equation symoblically (using `sympy` under the hood), and then calculate the value of that uncertainty equation as the last step.

For example:

    >>> calculate("x*y + z", x=Val(3, 0.1), y=Val(3, 1), z=4)
    13 ± 3
    >>> calculate("x*y + z", x=Val(3, 0.1), y=[Val(3, 1), [Val(5, 1)]], z=4)
    [13 ± 3, [19 ± 3]]
    >>> import numpy as np
    >>> calculate("x*y + z", x=Val(3, 0.1), y=numpy.array([Val(3, 1), Val(5, 1)]), z=4) 
    >>> calculate("x*y + z", x=Val(3, 0.1), y=np.array([Val(3, 1), Val(5, 1)]), z=4)

For a modest speed-up the first argument can also be a sympy expression so that the equation string only needs to be parsed once.

    >>> from sympy.parsing.sympy_parser import parse_expr
    >>> f = parse_expr("x*y + z")
    >>> calculate(f, x=Val(3, 0.1), y=[Val(3, 1), [Val(5, 1)]], z=4) 
    [13 ± 3, [19 ± 3]]

The uncertainty equation can also be determined without any values to calculate the final result. This expression can then be used in later calculations or converted to a sympy-parseable string or pretty string. This can be done by calling `calculations.uncertainty(expr, *variables)` where the variables are all symbols that have an associated uncertainty (equivalent to an uncertainty of 0).

    >>> df = uncertainty("x*y + z", "x", "y")
    >>> repr(df)
    sqrt(x**2*δy**2 + y**2*δx**2)
    >>> df
       _________________
      ╱  2   2    2   2
    ╲╱  x ⋅δy  + y ⋅δx

## uncertainties.pprinting

This submodule contains two functions that provide easy ways of visualizing results. The `pprinting.pprint_uncertainty(...)` function takes arguments of the same form as `calculations.uncertainty(...)`. It will pretty-print the original equation as well as its uncertainty equation.

    >>> pprint_uncertainty("x*y + z", "x", "y")
    f(...) = x⋅y + z
                 _________________
                ╱  2   2    2   2
    δf(...) = ╲╱  x ⋅δy  + y ⋅δx


 The `pprinting.pprint_calculation(...)` function  takes arguments of the same form as `calculations.calculate(...)`. It will pretty-print the original equation, its calculated result, the uncertainty equation, and its calculated result.

    >>> pprint_calculation("x*y + z", x=Val(3, 0.1), y=Val(3, 3), z=4)
    f(...) = x⋅y + z
            -> 13.0
                 _________________
                ╱  2   2    2   2
    δf(...) = ╲╱  x ⋅δy  + y ⋅δx
            -> 9.00499861188218

## uncertainties.strings

This submodule provides a single public function, `strings.uncertainty_str(...)` that will return a proper string representation of a value and its uncertainty. The expression `str(Val(x, y))` is equivilent to `uncertainty_str(x, y)`.

    >>> uncertainty_str(10.33, 0.12)
    10.33 ± 0.12
    >>> uncertainty_str(3.21856e-10, 3.24e-12)
    (3.22 ± 0.03)e-10
    >>> uncertainty_str(0.02094495456, 9.541774545e-05)
    0.020945 ± 0.000095

## uncertainties.utilities

This submodule provides a few useful functions for working with uncertainties in `numpy`.

The `utilities.to_val_array(...)` function converts two numpy arrays of int/float types to a single numpy array of `Val` type. The `utilities.from_val_arary(...)` function converts a single numpy array of type `Val` to two numpy arrays of int/float types.

    >>> to_val_array(np.array([10, 100, 80]), np.array([.1, .15, .35]))
    [Val(10, 0.1) Val(100, 0.15) Val(80, 0.35)]
    >>> from_val_array(np.array([Val(10, 0.1), Val(100, 0.15), Val(80, 0.35)]))
    ([ 10. 100.  80.], [0.1  0.15 0.35])

The `utilities.weighted_average(...)` function calculates a weighted average of a list of `Val` objects using `numpy`.

    >>> weighted_average([Val(5, .1), Val(100, 30), Val(10, 1), Val(15, .4)])
    5.63 ± 0.13`

Note that the large value of 100 does not appreciably contribute to the average.