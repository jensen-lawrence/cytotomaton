# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import njit
from time import time, sleep
from typing import Callable

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

@njit
def periodic_neighbours(cells: np.ndarray, nrows: int, ncols: int,
                        row: int, col: int) -> int:
    """
    Determines the number of neighbours a cell has in a domain with
    periodic boundary conditions.

    Parameters
    ----------
    cells : numpy.ndarray
        The array of cells.
    nrows : int
        The number of rows of cells in the array.
    ncols : int
        The number of columns of cells in the array.
    row : int
        The row index of the cell of interest.
    col : int
        The column index of the cell of interest.

    Returns
    -------
    int
        The number of neighbours the cell has.
    """
    N, S = (row + 1) % nrows, row - 1
    E, W = (col + 1) % ncols, col - 1
    n = cells[S,col] + cells[N,col] + cells[row,W] + cells[row,E]\
      + cells[S,W] + cells[S,E] + cells[N,W] + cells[N,E]
    return n


@njit
def solid_neighbours(cells: np.ndarray, nrows: int, ncols: int,
                     row: int, col: int) -> int:
    """
    Determines the number of neighbours a cell has in a domain with
    solid boundary conditions.

    Parameters
    ----------
    cells : numpy.ndarray
        The array of cells.
    nrows : int
        The number of rows of cells in the array.
    ncols : int
        The number of columns of cells in the array.
    row : int
        The row index of the cell of interest.
    col : int
        The column index of the cell of interest.

    Returns
    -------
    int
        The number of neighbours the cell has.
    """
    rowlow, rowhigh = max(0, row - 1), min(nrows, row + 2)
    collow, colhigh = max(0, col - 1), min(ncols, col + 2)
    n = int(np.sum(cells[rowlow:rowhigh,collow:colhigh]) - cells[row,col])
    return n


@njit
def update_cells(cells: np.ndarray, nrows: int, ncols: int,
                 survival: tuple[int], birth: tuple[int],
                 neighbours_func: Callable) -> np.ndarray:
    """
    Updates the cells in an array according to the automaton rules and the
    boundary conditions.

    Parameters
    ----------
    cells : numpy.ndarray
        The array of cells.
    nrows : int
        The number of rows of cells in the array.
    ncols : int
        The number of columns of cells in the array.
    survival : tuple[int]
        The number(s) of cells a cell can be surrounded by to survive
        in the next step.
    birth : tuple[int]
        The number(s) of cells an empty space must be surrounded by
        to become alive in the next step.

    Returns
    -------
    numpy.ndarray
        The array of updated cells.
    """
    # Initialize array for updated cells
    updated_cells = np.zeros_like(cells)

    # Iterate over rows and columns to update cells
    for row in range(nrows):
        for col in range(ncols):
            cell = cells[row,col]
            n = neighbours_func(cells, nrows, ncols, row, col)
            if (cell and n in survival) or (not cell and n in birth):
                updated_cells[row,col] = 1

    return updated_cells


def animate(nsteps: int, nrows: int, ncols: int, data_output: str,
            anim_output: str, dpi: int, fps: int) -> None:
    """
    Animates the results of an automaton using the data from the
    saved output file.

    Parameters
    ----------
    nsteps : int
        The number of steps taken by the automaton.
    nrows : int
        The number of rows of cells in the array.
    ncols : int
        The number of columns of cells in the array.
    data_output : str
        The path and file name where the output data is saved.
    anim_output : str
        The path and file name where the animation will be saved.
    dpi : int
        The resolution of the animation.
    fps : int
        The fps of the animation.

    Returns
    -------
    None
    """
    # Determine file type of animation
    file_type = anim_output.split(".")[-1]

    # Load results from output file
    data = np.loadtxt(data_output)
    steps = []
    for i in range(nsteps):
        steps.append(data[i*nrows:(i+1)*nrows,:])
    steps = np.array(steps)

    # Generate animation
    fig, ax = plt.subplots(figsize=((ncols/nrows)*8,8), tight_layout=True)

    def update(i):
        ax.clear()
        ax.imshow(steps[i], cmap="inferno")
        ax.set_axis_off()

    anim = FuncAnimation(fig, update, frames=np.arange(0, nsteps),
                         interval=50, blit=True, cache_frame_data=False)

    # Save animation
    writer = "ffmpeg" if file_type == "mp4" else "pillow"
    anim.save(anim_output, dpi=dpi, fps=fps, writer=writer)
    plt.close()

# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------

def run(cells: np.ndarray, rules: dict[str, tuple[int]], boundaries: str,
        nsteps: int, print_steps: bool = True, live_view: bool = False,
        data_output: str = None, anim_output: str = None,
        dpi: int = 100, fps: int = 10) -> None:
    """
    Runs an automaton with the given initial cell configuration with specified
    rules and boundary conditions for a given number of step.

    Parameters
    ----------
    cells : numpy.ndarray
        The array of the initial state of the cells.
    rules : dict[str, tuple[int]]
        A dictionary of the form {"S": (...), "B": (...)} that contains the
        rules governing survival and birth. Any cell surrounded by a number
        of cells found in S will survive in the next step; any empty space
        surrounded by a number of cells found in B will become alive in the
        next step.
    boundaries : str
        A string that determines the boundary conditions imposed on the
        automaton. If "periodic", the boundaries are periodic (i.e. the
        top/bottom and left/right edges wrap around to each other). If
        "solid", the boundaries are solid.
    nsteps : int
        The number of steps the automaton will take.
    print_steps : bool, optional
        If True, the array of cells will be printed at each time step.
        True by default.
    live_view : bool, optional
        If True, an animation showing the evolution of the cells will be
        displayed while the automaton runs. False by default.
    data_output : str, optional
        Path and file name where the cell configurations from each step
        will be saved. If no path is provided, the data is not saved.
        None by default.
    anim_output : str, optional
        Path and file name where an animation showing the evolution of
        the cells will be saved. For the animation to be generated and
        saved, data_output must also be specified. If no path is provided,
        the animation is not created. None by default.
    dpi : int, optional
        The resolution of the saved animation. 100 by default.
    fps : int, optional
        The fps of the saved animation. 10 by default.

    Returns
    -------
    None
    """
    # Grid size
    nrows, ncols = cells.shape

    # Survival and birth rules
    survival = rules["S"]
    birth = rules["B"]
    
    # Boundary conditions
    if boundaries == "periodic":
        neighbours_func = periodic_neighbours
    elif boundaries == "solid":
        neighbours_func = solid_neighbours

    # Compile Numba on easy input
    update_cells(np.zeros((3,3)), 3, 3, survival, birth, neighbours_func)

    # Start automaton
    print("Running automaton...")
    t0 = time()

    # Initial conditions
    if print_steps:
        print("Step 1")
        print(cells, "\n")

    if live_view:
        fig, ax = plt.subplots(figsize=((ncols/nrows)*8,8), tight_layout=True)
        im = ax.imshow(cells, cmap="inferno")
        ax.set_axis_off()
        plt.show(block=False)

    if data_output is not None:
        with open(data_output, "w") as f:
            np.savetxt(f, cells, fmt="%i", footer=" ")

    # Loop through time and evolve automaton
    for i in range(2, nsteps + 1):
        cells = update_cells(cells, nrows, ncols, survival, birth, neighbours_func)

        if print_steps:
            print(f"Step {i}")
            print(cells, "\n")

        if live_view:
            sleep(0.1)
            im.set_array(cells)
            fig.canvas.draw()
            fig.canvas.flush_events()

        if data_output is not None:
            with open(data_output, "a") as f:
                np.savetxt(f, cells, fmt="%i", footer=" ")

    # Print time summary
    tf = time() - t0 
    print(f"Automaton run in {tf//60} min {round(tf%60,3)} sec")
    sleep(1)
    plt.close()

    # Save data
    if data_output is not None:
        print(f"Data saved to {data_output}\n")
    
    # Generate and save animation
    if anim_output is not None:
        print("Animating results...")
        t0 = time()
        animate(nsteps, nrows, ncols, data_output, anim_output, dpi, fps)
        tf = time() - t0 
        print(f"Rendering completed in {tf//60} min {round(tf%60,3)} sec")
        print(f"Animation saved to {anim_output}")
