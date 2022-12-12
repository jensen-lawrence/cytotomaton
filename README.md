# cytomaton
`cytomaton` is an implementation of many life-like cellular automata, including Conway's Game of Life. To run a celluler automaton, use the `run` function. In general, executing

```python
run(
  cells, rules, boundaries, nsteps, print_steps=True, live_view=True,
  data_output="./data.out", anim_output="./anim.mp4", dpi=100, fps=10
)
```

will run an automaton with initial configuration `cells` subjected to the rules defined by `rules` and the boundary conditions defined by `boundaries` for `nsteps` iterations. `print_steps` controls whether the state of the automaton is printed each step and `live_view` control whether a live animation of the cells is displayed as the automaton runs. `data_output` provides the path and file name where the automaton state at each step is saved. `anim_output` provides the path and file name where the animation of the automaton is saved, with `dpi` and `fps` controlling the resolution and fps of the animation, respectively.

`cells` is any numpy.ndarray of 0s and 1s specified by the user, but numerous templates, as well as a function that generates a random array of cells, are provided in `src/starters.py`.

`rules` is a dictionary of the form `{"S": (...), "B": (...)}`, where the `"S"` tuple indicates how many cells must surround a given cell for it to survive in the next step, and the `"B"` tuple indicates how many cells must surround an empty space for it to become alive in the next step. Any such dictionary can be used, but many rule sets are pre-defined in `src/rules.py`. 

`boundaries` is a string that can either be `"periodic"` or `"solid"`. In the case of `"periodic"`, the boundaries of the automaton are treated as if they "wrap around", i.e. a cell on the rightmost side of the domain is counted among the neighbours of a cell on the leftmost side of the domain (same for the top and bottom). This means that any space has eight neighbouring spaces, regardless of the cell's location. In the case of `"solid"`, the boundaries of the automaton are treated as solid, i.e. a cells on opposite sides of the domain do not influence each other. This means that spaces on the interior of the automaton domain have eight neighbouring spaces, but spaces on the boundaries of the automaton have four (corners) or five (edges) neighbouring spaces.

For example, running
```python
from automata import run
from rules import rules
from starters import random_cells

run(
    cells = random_cells(100, 100, p_life=0.5),
    rules = rules["Conway's Life"],
    boundaries = "periodic",
    nsteps = 100,
    print_steps = True,
    live_view = True,
    data_output = "./conway.out"
  )
```

will initialize an automaton with a 100x100 domain with periodic boundaries, where 50% of the spaces initially contain cells. The automaton is then evolved for 100 steps according to the classic rules of Conway's Game of Life. The state of the automaton is printed and animated at each step. The automaton data is saved to `./conway.out`, but an animation is not produced.
