# Imports
import sys
import numpy as np
sys.path.append("src")
from automata import run
from rules import rules
from starters import *

# Execution
if __name__ == "__main__":
    run(
        cells = random_cells(100, 100, p_life=0.5),
        rules = rules["Conway's Life"],
        boundaries = "periodic",
        nsteps = 100,
        print_steps = True,
        live_view = True
    )
    