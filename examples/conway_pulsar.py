import sys
sys.path.append("../src")
from automata import run
from rules import rules
from starters import pulsar

run(
    cells = pulsar,
    rules = rules["Conway's Life"],
    boundaries = "periodic",
    nsteps = 16,
    print_steps = True,
    live_view = True,
    data_output = "./conway_pulsar.out",
    anim_output = "./conway_pulsar.gif",
    fps = 4
)
