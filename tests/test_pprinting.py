import math

import pytest

from uncertainties import pprinting
from uncertainties.var import Var

EXPECTED_UNCERTAINTY_1 = """
f(...) = x⋅y + z
             _________________
            ╱   2  2     2  2 
df(...) = ╲╱  dx ⋅y  + dy ⋅x  
"""

EXPECTED_UNCERTAINTY_2 = """
          y
f(...) = x 
             __________________
            ╱   2  2⋅y    2    
df(...) = ╲╱  dy ⋅x   ⋅log (x) 
"""

EXPECTED_UNCERTAINTY_3 = """
f(...) = sin(x)
             _____________
            ╱   2    2    
df(...) = ╲╱  dx ⋅cos (x) 
"""

EXPECTED_CALCULATION_1 = """
f(...) = log(x)
	-> 7.380879035564116
                _____
               ╱   2 
              ╱  dx  
df(...) =    ╱   ─── 
            ╱      2 
          ╲╱      x  
	-> 0.03302180685358255
"""

EXPECTED_CALCULATION_2 = """
f(...) = x - log(300)
	-> 1.6770965609079151
             _____
            ╱   2 
df(...) = ╲╱  dx  
	-> 3.970291913552122
"""

EXPECTED_CALCULATION_3 = """
f(...) = x⋅y + z
	-> 13.0
             _________________
            ╱   2  2     2  2 
df(...) = ╲╱  dx ⋅y  + dy ⋅x  
	-> 9.00499861188218
"""


@pytest.mark.parametrize(
    "expr, variables, expected",
    (
        ("x*y+z", ("x", "y"), EXPECTED_UNCERTAINTY_1),
        ("x ** y", ("y",), EXPECTED_UNCERTAINTY_2),
        ("sin(x)", ("x",), EXPECTED_UNCERTAINTY_3),
    ),
)
def test_pprint_uncertainty(expr, variables, expected, capsys):
    pprinting.pprint_uncertainty(expr, *variables)
    out, _ = capsys.readouterr()
    assert out == expected.lstrip("\n")


@pytest.mark.parametrize(
    "expr, values, expected",
    (
        ("log(x)", {"x": Var(1605, 53)}, EXPECTED_CALCULATION_1),
        ("x-log(300)", {"x": Var(math.log(1605), math.log(53))}, EXPECTED_CALCULATION_2),
        ("x*y+z", {"x": Var(3, 0.1), "y": Var(3, 3), "z": 4}, EXPECTED_CALCULATION_3),
    ),
)
def test_(expr, values, expected, capsys):
    pprinting.pprint_calculation(expr, **values)
    out, _ = capsys.readouterr()
    assert out == expected.lstrip("\n")
