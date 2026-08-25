*This project has been created as part of the 42 curriculum by mucelep, bakumcu.*

# A-Maze-ing

## Description

A-Maze-ing is a Python project that generates, solves and visually represents mazes.

The program reads a configuration file, generates a random maze, finds a path between
the entry and exit, saves the maze using the required hexadecimal format and displays
the result.

The project also contains a reusable maze generator module that can be packaged and
used independently in another Python project.

### Main Features

- Random maze generation
- Reproducible generation using a seed
- Perfect and non-perfect maze modes
- Maze validation
- Shortest path calculation
- Required `42` pattern
- Hexadecimal output format
- Visual maze representation
- Reusable `MazeGenerator` module

## Instructions

### Installation

The project requires Python 3.10 or later.

Clone the repository and create a virtual environment:

    git clone [REPOSITORY_URL]
    cd [REPOSITORY_NAME]
    python3 -m venv .venv
    source .venv/bin/activate

Install the dependencies:

    make install

### Usage

Run the project with:

    make run

or directly:

    python3 a_maze_ing.py config.txt

A different configuration file can be provided:

    python3 a_maze_ing.py [CONFIG_FILE]

### Makefile

| Command | Description |
|---|---|
| `make install` | Install dependencies |
| `make run` | Run the project |
| `make debug` | Run using the Python debugger |
| `make clean` | Remove temporary files |
| `make lint` | Run flake8 and mypy |

## Configuration

The program uses a `KEY=VALUE` configuration file.

Example:

    WIDTH=20
    HEIGHT=15
    ENTRY=0,0
    EXIT=19,14
    OUTPUT_FILE=maze.txt
    PERFECT=False
    SEED=42

### Parameters

| Parameter | Description |
|---|---|
| `WIDTH` | Maze width |
| `HEIGHT` | Maze height |
| `ENTRY` | Entry cell coordinates |
| `EXIT` | Exit cell coordinates |
| `OUTPUT_FILE` | Generated maze output file |
| `PERFECT` | Enables or disables perfect maze generation |
| `SEED` | Seed used for reproducible generation |

No additional configuration keys are currently supported beyond the ones listed above.

## Maze Generation

### Algorithm

We use a **recursive backtracker** (randomized iterative depth-first search) to carve
the base maze, then a **braiding pass** to turn it into a playable board when
`PERFECT=False`.

The algorithm works by:

1. Starting from the entry cell, push it onto a stack and mark it visited.
2. While the stack is not empty, look at the cell on top of the stack. If it has an
   unvisited neighbour (and that neighbour isn't part of the reserved `42` pattern),
   knock down the wall between them, mark the neighbour visited and push it.
3. If the current cell has no unvisited neighbour, pop it off the stack and backtrack.

This always produces a **perfect maze**: every cell reachable, exactly one path
between any two cells, no loops.

When `PERFECT=False`, we then:

- Randomly remove a batch of the remaining interior walls to create loops, rejecting
  any removal that would open up a 3x3 (or larger) empty area.
- Force the four corners and the centre cell open, as required for the Pac-Man-style
  board.
- Run a braiding pass that removes one wall from each dead end (again rejecting moves
  that create a 3x3 open area) until at most two dead ends remain.

### Why This Algorithm?

We chose the recursive backtracker because:

- It is simple to implement iteratively with an explicit stack, so it can't blow the
  recursion limit on large mazes.
- It naturally produces a perfect maze (single path, full connectivity) in one pass,
  which is exactly what `PERFECT=True` requires.
- Driving `random.choice`/`random.shuffle` from a single seeded `random.seed(seed)`
  call makes the whole generation deterministic and reproducible.
- Starting from a perfect maze and selectively re-opening walls (braiding) is a
  straightforward way to reach the `PERFECT=False` requirements (loops, rare dead
  ends, no 3x3 open areas) without a second, unrelated algorithm.

## Maze Modes

### Perfect Maze

When `PERFECT=True`, the maze contains exactly one path between the entry and exit
and does not contain loops.

### Non-Perfect Maze

When `PERFECT=False`, the maze is designed as a playable board. It remains fully
connected, contains multiple routes and avoids excessive dead ends.

## Output Format

Each maze cell is represented by one hexadecimal character.

The four bits represent the walls:

| Bit | Direction |
|---|---|
| `0` | North |
| `1` | East |
| `2` | South |
| `3` | West |

A set bit represents a wall.

The output contains:

1. The maze grid
2. An empty line
3. Entry coordinates
4. Exit coordinates
5. The shortest path

The shortest path uses `N`, `E`, `S` and `W`.

Example (4x2 maze):

    913955
    ac2a91

    3,5
    25,20
    EESSENNE...

## Visualization

The generated maze is displayed as **ANSI-coloured ASCII art in the terminal**
(each cell rendered as a 2x2 block of coloured spaces).

The visualization shows:

- Maze walls
- Entry (purple) and exit (red)
- The `42` pattern (grey)
- The shortest path, when toggled on (blue)

### Controls

The program shows a numbered menu after each render:

| Choice | Action |
|---|---|
| `1` | Re-generate a new maze (same config, new random layout) |
| `2` | Show / hide the shortest path |
| `3` | Rotate the wall colour (white → gold → sky blue → mint green) |
| `4` | Quit |

## Path Finding

The program calculates a shortest path from the entry to the exit using a
**breadth-first search (BFS)**.

Starting from the entry cell, it explores neighbouring cells in FIFO order, only
through walls that are open, and records for each visited cell which direction it
was reached from. Once the exit is dequeued, the path is rebuilt by walking these
"came from" links back to the entry and reversed, giving the result as a string of
`N`, `E`, `S` and `W` moves. BFS guarantees the shortest path because it expands
cells in order of distance from the entry.

## Reusable Maze Generator

The maze-generation logic is separated into a standalone package, `mazegen/`, with
no dependency on the CLI, config parser or visualizer — it can be imported and used
on its own in any Python project.

The main class is `MazeGenerator`. Generation happens immediately when the object is
constructed (there is no separate `generate()` call).

Example usage:

    from mazegen import MazeGenerator, maze_slover, maze_to_hex

    generator = MazeGenerator(
        width=20,
        height=15,
        entry_pos=(0, 0),
        exit_pos=(19, 14),
        perfect=True,
        seed=42,
    )

    # the maze is already generated at this point

Passing custom parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | `int` | required | number of columns |
| `height` | `int` | required | number of rows |
| `entry_pos` | `tuple[int, int]` | `(0, 0)` | entry cell coordinates |
| `exit_pos` | `tuple[int, int] \| None` | `(width - 1, height - 1)` | exit cell coordinates |
| `perfect` | `bool` | `True` | single-path maze vs. playable board with loops |
| `seed` | `int \| None` | `None` | seed for `random`, for reproducible output |

Accessing the generated structure:

    # grid[y][x] is a Cell with .north / .east / .south / .west booleans
    # (True = wall closed, False = wall open / passage)
    cell = generator.grid[0][0]

    # hexadecimal wall-encoding of the whole grid, one row per line
    hex_maze = maze_to_hex(generator)

Accessing a solution:

    # shortest entry -> exit path as a string of "N"/"E"/"S"/"W" moves
    solution = maze_slover(generator)

The generator allows users to:

- Define maze dimensions, entry and exit cells
- Set a seed for reproducible generation
- Choose perfect vs. playable-board generation
- Access the generated cell grid directly
- Get the shortest solution path and the hexadecimal encoding via helper functions

The reusable module is packaged as `mazegen-1.0.0-py3-none-any.whl` (and the
equivalent `mazegen-1.0.0.tar.gz` sdist), both at the repository root.

The package is built from `pyproject.toml` at the repository root, which only
declares the `mazegen/` directory — the CLI, config parser and visualizer are
not part of it. To rebuild it from source:

    pip install build
    python3 -m build
    cp dist/mazegen-1.0.0-py3-none-any.whl dist/mazegen-1.0.0.tar.gz .

To install and use it in another project:

    pip install mazegen-1.0.0-py3-none-any.whl

## Project Structure

    .
    ├── a_maze_ing.py         # entry point, wires config -> generator -> output -> visualizer
    ├── config.txt             # default configuration file
    ├── output.py               # writes the hex grid + entry/exit/path to OUTPUT_FILE
    ├── Makefile
    ├── README.md
    ├── LICENSE.md
    ├── .gitignore
    ├── pyproject.toml           # build config for the mazegen package
    ├── mazegen-1.0.0-py3-none-any.whl  # built package (see Reusable Maze Generator)
    ├── mazegen-1.0.0.tar.gz            # built package (sdist)
    ├── mazegen/                # reusable, standalone package
    │   ├── __init__.py          # package usage docs live in this module's docstring
    │   ├── cell.py              # Cell dataclass (north/east/south/west walls)
    │   ├── maze_generator.py    # MazeGenerator class (recursive backtracker + braiding)
    │   ├── maze_slover.py       # maze_slover(): BFS shortest path
    │   └── maze_to_hex.py       # maze_to_hex(): hexadecimal wall encoding
    ├── process_config/         # config file parsing and validation
    │   ├── __init__.py
    │   ├── read_config.py
    │   └── validate_config.py
    └── visualizer/              # terminal ASCII rendering + interactive menu
        ├── __init__.py
        └── visualizer.py

`maze_analyzer.py` (the 42-provided output checker used to verify the
"42" pattern, wall coherence and the no-dead-end bonus) is not part of this
repository -- it's supplied separately by the subject and run against
`OUTPUT_FILE` after generation, e.g. `python3 maze_analyzer.py maze.txt
--max-dead-ends 0`.

## Team & Project Management

| Member | Role |
|---|---|
| Muhammed Ömer Celep (mucelep) | Config parsing, validation & MazeGenerator, PERFECT/NON-PERFECT generation & maze solver, reusable package, etc... |
| Batuhan Fatih Kumcu (bakumcu) | Visualizer, output generation, testing, readme, license, makefile |

### Planning

We initially divided the project into several parts:

- Maze generation
- Configuration parsing
- Path finding
- Output generation
- Visualization
- Testing
- Reusable package

The work was divided between team members and integrated progressively.

Firstly, grid generation and the algorithm for the maze was created. Afterwards, reading through the config file was implemented and later on we started working on a visualizer. After creating a basic sketch and understanding what needed to be done, we once again worked on generation and hex-encoding. After making sure everything was done we finished the visualizer and the interactive menu. We then started working on new checks to make sure every case worked well, and lastly we made the remaining files that were needed in this project.

### What Worked Well

- The planning and sharing of different parts of the project, making a solid teamwork balance that fits well for both our calendars.
- The development cycle of giving each other feedback on what to change/improve, and going back to those parts to make sure that everything was working well.

### What Could Be Improved

- The communication between two members on what to do was, at times, too limiting and it definitely made the project progress slower than it should have.
- Since this project is between two team members, when one person develops something it can cause something else to break. So when making commits and adding comments for other people to look at, we both needed to be more thorough in our explanations and clearer on what a given block of code meant, since it slowed progress when the code broke more than it should have and we had to fix it every time.

## Tools

We used:

- Python 3.10+
- Git
- VS code
- flake8
- mypy
- build (PyPA build) + hatchling
- maze_analyzer.py

## Resources

- A-Maze-ing Project Subject (42 curriculum)
- Python Documentation: https://docs.python.org/3/
- Maze generation algorithms overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Recursive backtracker walkthrough: https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
- Breadth-first search: https://en.wikipedia.org/wiki/Breadth-first_search
- Python Packaging User Guide (building the `mazegen` wheel): https://packaging.python.org/

### AI Usage

AI tools were used as a development and learning aid.

They were used for:

- Understanding maze-generation algorithms
- Discussing implementation approaches
- Debugging errors
- Suggesting test cases
- Reviewing documentation
- Explaining Python concepts
- Making a better formatted and readable README file

All generated suggestions were reviewed and tested by the team before being used.

## License

The reusable maze generator is distributed under the license specified in
`LICENSE.md`.

The selected license permits reuse and distribution of the generator.

## Authors

**Muhammed Ömer Celep** — mucelep

**Batuhan Fatih Kumcu** — bakumcu

42 School