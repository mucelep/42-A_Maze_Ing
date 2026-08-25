"""mazegen - reusable maze generator and solver.

Standalone package extracted from the A-Maze-ing 42 project. It has no
dependency on that project's CLI, config parser or visualizer, and only
depends on the Python standard library.

Basic usage::

    from mazegen import MazeGenerator, maze_slover, maze_to_hex

    generator = MazeGenerator(
        width=20,
        height=15,
        entry_pos=(0, 0),
        exit_pos=(19, 14),
        perfect=True,
        seed=42,
    )
    # the maze is already generated at this point -- there is no
    # separate generate() call

Custom parameters: ``width``/``height`` set the maze size in cells,
``entry_pos``/``exit_pos`` are (x, y) cell coordinates (``exit_pos``
defaults to the bottom-right corner), ``perfect=True`` guarantees a
single path between entry and exit (``perfect=False`` instead produces
a playable board with loops, open corners/centre and no dead ends), and
the optional ``seed`` makes generation reproducible via ``random``.

Accessing the generated structure::

    # grid[y][x] is a Cell with .north / .east / .south / .west booleans
    # (True = wall closed, False = wall open / passage)
    cell = generator.grid[0][0]

    # hexadecimal wall-encoding of the whole grid, one row per line
    # (bit 0=North, 1=East, 2=South, 3=West; set bit = closed wall)
    hex_maze = maze_to_hex(generator)

Accessing a solution::

    # shortest entry -> exit path as a string of "N"/"E"/"S"/"W" moves
    solution = maze_slover(generator)
"""

from .maze_generator import MazeGenerator
from .maze_slover import maze_slover
from .maze_to_hex import maze_to_hex

__all__ = [
    "MazeGenerator",
    "maze_slover",
    "maze_to_hex",
]
