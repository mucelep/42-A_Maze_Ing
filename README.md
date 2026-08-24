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

## Installation

The project requires Python 3.10 or later.

Clone the repository and create a virtual environment:

    git clone [REPOSITORY_URL]
    cd [REPOSITORY_NAME]
    python3 -m venv .venv
    source .venv/bin/activate

Install the dependencies:

    make install

## Usage

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

Additional parameters:

    [TODO: ADD IF APPLICABLE]

## Maze Generation

### Algorithm

We use **[ALGORITHM NAME]** to generate the maze.

The algorithm works by:

1. [SHORT DESCRIPTION]
2. [SHORT DESCRIPTION]
3. [SHORT DESCRIPTION]

### Why This Algorithm?

We chose `[ALGORITHM NAME]` because:

- [REASON]
- [REASON]
- [REASON]

It provides the properties required by the project while being suitable for random
and reproducible maze generation.

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

Example:

    [MAZE DATA]

    0,0
    19,14
    EESSENNE...

## Visualization

The generated maze is displayed using **[ASCII / GRAPHICAL INTERFACE]**.

The visualization shows:

- Maze walls
- Entry and exit
- The `42` pattern
- The shortest path

### Controls

| Key | Action |
|---|---|
| `[KEY]` | Regenerate maze |
| `[KEY]` | Show/hide solution |
| `[KEY]` | Change wall colour |
| `[KEY]` | Exit |

[TODO: Replace with the actual controls.]

## Path Finding

The program calculates a shortest path from the entry to the exit using
**[BFS / ALGORITHM]**.

The algorithm only allows movement through open neighbouring cells and returns
the result using `N`, `E`, `S` and `W`.

## Reusable Maze Generator

The maze-generation logic is separated into a reusable module.

The main class is `MazeGenerator`.

Example usage:

    from mazegen import MazeGenerator

    generator = MazeGenerator(
        width=20,
        height=15,
        seed=42
    )

    generator.generate()

    maze = generator.get_maze()
    solution = generator.get_solution()

[TODO: Adapt this example to the actual API.]

The generator allows users to:

- Define maze dimensions
- Set a seed
- Choose generation options
- Generate a maze
- Access the generated maze
- Access a solution

The reusable module is packaged as:

    mazegen-[VERSION]-py3-none-any.whl

The repository contains everything required to rebuild the package.

## Project Structure

    .
    ├── a_maze_ing.py
    ├── config.txt
    ├── Makefile
    ├── README.md
    ├── LICENSE.md
    ├── requirements.txt
    ├── pyproject.toml
    ├── mazegen/
    │   ├── __init__.py
    │   └── [generator files]
    ├── [visualization files]
    └── tests/

[TODO: Update this to match the final project structure.]

## Team & Project Management

| Member | Role |
|---|---|
| [NAME] | [ROLE] |
| [NAME] | [ROLE] |

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

[TODO: Briefly explain how your actual plan evolved.]

### What Worked Well

- [POINT]
- [POINT]

### What Could Be Improved

- [POINT]
- [POINT]

## Tools

We used:

- Python 3.10+
- Git
- [IDE / EDITOR]
- flake8
- mypy
- [OTHER TOOLS]

## AI Usage

AI tools were used as a development and learning aid.

They were used for:

- Understanding maze-generation algorithms
- Discussing implementation approaches
- Debugging errors
- Suggesting test cases
- Reviewing documentation
- Explaining Python concepts

All generated suggestions were reviewed and tested by the team before being used.

## Resources

- A-Maze-ing Project Subject
- Python Documentation: https://docs.python.org/3/
- [Maze Algorithm Reference]
- [Path Finding Reference]
- flake8 Documentation: https://flake8.pycqa.org/
- mypy Documentation: https://mypy.readthedocs.io/
- [Other resources used]

## License

The reusable maze generator is distributed under the license specified in
`LICENSE.md`.

The selected license permits reuse and distribution of the generator.

## Authors

**[NAME]** — [LOGIN]

**[NAME]** — [LOGIN]

42 School