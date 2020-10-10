import numpy as np
import sympy as sp

from pycertainties.calculations import calculate, uncertainty
from pycertainties.pprinting import pprint_calculation, pprint_uncertainty
from pycertainties.strings import uncertainty_str
from pycertainties.utilities import from_val_array, to_val_array, weighted_average
from pycertainties.val import Val

# Setup numpy so that arrays of Vals print prettily
np.set_printoptions(
    formatter={
        "object": (
            lambda obj: (
                (s if "e" in (s := str(obj)) else f"({s})")
                if isinstance(obj, Val)
                else np.get_printoptions().formatter.get("object", repr)
            )
        )
    }
)
sp.init_printing(wrap_line=False)
