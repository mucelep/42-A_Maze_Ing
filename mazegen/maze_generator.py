import random
from .cell import Cell


class MazeGenerator:
    """Generate a maze using a randomized depth-first search algorithm."""
    _DIRECTIONS = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }

    def __init__(self, width: int, height: int,
                 entry_pos: tuple[int, int] = (0, 0),
                 exit_pos: tuple[int, int] | None = None,
                 perfect: bool = True, seed: int | None = None):

        self.width_x = width
        self.height_y = height
        self.seed = seed
        self.entry_pos = entry_pos
        if exit_pos is not None:
            self.exit_pos = exit_pos
        else:
            self.exit_pos = (width - 1, height - 1)

        if seed is not None:
            random.seed(seed)

        self.grid = self._create_grid()
        self.locked_cells = self._compute_42_pattern()

        if (
            self.entry_pos in self.locked_cells
            or self.exit_pos in self.locked_cells
        ):
            raise ValueError("ENTRY/EXIT cannot be inside the '42' pattern")

        if perfect:
            self._generate_maze()
        else:
            self._generate_maze()
            self._perfect_false()

    def _create_grid(self) -> list[list[Cell]]:
        """Create and return a grid filled with Cell objects."""
        grid = []

        for y in range(self.height_y):
            row = []

            for x in range(self.width_x):
                cell = Cell()
                row.append(cell)
            grid.append(row)

        return grid

    def _generate_maze(self) -> None:
        """Generate the maze using depth-first search with backtracking."""
        start_x, start_y = self.entry_pos
        visited: set[tuple[int, int]] = set()
        stack:   list[tuple[int, int]]

        visited.add((start_x, start_y))
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack[-1]

            neighbors = self._get_unvisited_neighbors(x, y, visited)

            if neighbors:
                new_x, new_y, direction = random.choice(neighbors)
                self._remove_wall(x, y, new_x, new_y, direction)

                visited.add((new_x, new_y))
                stack.append((new_x, new_y))
            else:
                stack.pop()

    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: set[tuple[int, int]]
            ) -> list[tuple[int, int, str]]:
        """Return valid unvisited neighboring cells."""
        neighbors: list[tuple[int, int, str]] = []

        for direction, (dx, dy) in self._DIRECTIONS.items():
            new_x = x + dx
            new_y = y + dy

            if not (0 <= new_x < self.width_x and 0 <= new_y < self.height_y):
                continue

            if (new_x, new_y) in visited:
                continue

            if (new_x, new_y) in self.locked_cells:
                continue

            neighbors.append((new_x, new_y, direction))

        return neighbors

    def _remove_wall(self, x: int, y: int, new_x: int,
                     new_y: int, direction: str) -> None:
        """Remove the wall between two adjacent cells."""
        current_cell: Cell = self.grid[y][x]
        neighbor_cell: Cell = self.grid[new_y][new_x]

        if direction == "N":
            current_cell.north = False
            neighbor_cell.south = False
        elif direction == "S":
            current_cell.south = False
            neighbor_cell.north = False
        elif direction == "E":
            current_cell.east = False
            neighbor_cell.west = False
        elif direction == "W":
            current_cell.west = False
            neighbor_cell.east = False

    def _add_wall(self, x: int, y: int, new_x: int,
                  new_y: int, direction: str) -> None:
        """Add a wall between two adjacent cells."""
        current_cell: Cell = self.grid[y][x]
        neighbor_cell: Cell = self.grid[new_y][new_x]

        if direction == "N":
            current_cell.north = True
            neighbor_cell.south = True
        elif direction == "S":
            current_cell.south = True
            neighbor_cell.north = True
        elif direction == "E":
            current_cell.east = True
            neighbor_cell.west = True
        elif direction == "W":
            current_cell.west = True
            neighbor_cell.east = True

    def _perfect_false(self) -> None:
        """Add loops and open areas for a non-perfect maze."""
        closed = self._get_closed_neighbors()
        random.shuffle(closed)

        max_loops = max(2, int(len(closed) * 0.20))
        min_loops = 2
        success_count = 0

        for x, y, new_x, new_y, direction in closed:
            if success_count >= max_loops:
                break

            self._remove_wall(x, y, new_x, new_y, direction)

            if self._has_open_3x3(x, y):
                self._add_wall(x, y, new_x, new_y, direction)
            else:
                success_count += 1

        if success_count < min_loops:
            raise ValueError(
                "Could not open enough loops for PERFECT=False; "
                "maze may be too small or too constrained"
            )

        self._FBI_open_the_corner()
        self._open_center()
        self._braid_dead_ends()

    def _get_closed_neighbors(self) -> list[tuple[int, int, int, int, str]]:
        """Return neighboring cell pairs separated by a wall."""
        closed: list[tuple[int, int, int, int, str]] = []

        for y in range(self.height_y):
            for x in range(self.width_x):
                cell = self.grid[y][x]

                if (x, y) in self.locked_cells:
                    continue

                if x + 1 < self.width_x and cell.east:
                    if (x + 1, y) not in self.locked_cells:
                        closed.append((x, y, x + 1, y, "E"))

                if y + 1 < self.height_y and cell.south:
                    if (x, y + 1) not in self.locked_cells:
                        closed.append((x, y, x, y + 1, "S"))

        return closed

    def _FBI_open_the_corner(self) -> None:
        """Open passages around the four corners of the maze."""
        if self.width_x > 1:
            self._remove_wall(0, 0, 1, 0, "E")
            self._remove_wall(0, 0, 0, 1, "S")

            self._remove_wall(
                self.width_x - 1, 0,
                self.width_x - 2, 0, "W"
            )
            self._remove_wall(
                self.width_x - 1, 0,
                self.width_x - 1, 1, "S"
            )

            self._remove_wall(
                0, self.height_y - 1,
                0, self.height_y - 2, "N"
            )
            self._remove_wall(
                0, self.height_y - 1,
                1, self.height_y - 1, "E"
            )

            self._remove_wall(
                self.width_x - 1, self.height_y - 1,
                self.width_x - 2, self.height_y - 1, "W"
            )

            self._remove_wall(
                self.width_x - 1, self.height_y - 1,
                self.width_x - 1, self.height_y - 2, "N"
            )

    def _compute_42_pattern(self) -> set[tuple[int, int]]:
        """Calculate the cells occupied by the '42' pattern."""
        _DIGIT_4 = {
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4),
        }
        _DIGIT_2 = {
            (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2),
            (0, 3), (0, 4), (1, 4), (2, 4),
        }

        digit_width = 3
        gap = 1
        pattern_width = digit_width * 2 + gap
        pattern_height = 5
        center_x = self.width_x // 2
        center_y = self.height_y // 2
        start_x = center_x - pattern_width // 2
        start_y = center_y - pattern_height // 2

        locked_cells: set[tuple[int, int]] = set()

        if pattern_width > self.width_x or pattern_height > self.height_y:
            print("Maze is too small to fit the '42' pattern")
            return locked_cells

        for cx, cy in _DIGIT_4:
            real_x = start_x + cx
            real_y = start_y + cy
            locked_cells.add((real_x, real_y))
        for cx, cy in _DIGIT_2:
            real_x = start_x + digit_width + gap + cx
            real_y = start_y + cy
            locked_cells.add((real_x, real_y))

        return locked_cells

    def _open_center(self) -> None:
        """Open passages through the center of the maze."""
        center_x = self.width_x // 2
        center_y = self.height_y // 2

        self._remove_wall(center_x, center_y, center_x, center_y + 1, "S")
        self._remove_wall(center_x, center_y, center_x, center_y - 1, "N")

    def _has_open_3x3(self, x: int, y: int) -> bool:
        """Check whether an open 3x3 area exists near a cell."""
        x_starts = (x - 2, x - 1, x)
        y_starts = (y - 2, y - 1, y)

        for start_y in y_starts:
            for start_x in x_starts:

                is_open = True
                if start_x < 0 or start_x + 2 >= self.width_x:
                    continue
                if start_y < 0 or start_y + 2 >= self.height_y:
                    continue

                for row in range(start_y, start_y + 3):
                    for col in range(start_x, start_x + 2):
                        if self.grid[row][col].east:
                            is_open = False
                            break
                    if not is_open:
                        break
                if not is_open:
                    continue

                for row in range(start_y, start_y + 2):
                    for col in range(start_x, start_x + 3):
                        if self.grid[row][col].south:
                            is_open = False
                            break
                    if not is_open:
                        break

                if is_open:
                    return True
        return False

    _WALL_ATTR = {"N": "north", "E": "east", "S": "south", "W": "west"}

    def _degree(self, x: int, y: int) -> int:
        """Return the number of open passages connected to a cell."""
        cell = self.grid[y][x]
        return sum(
            not getattr(cell, attr) for attr in self._WALL_ATTR.values()
        )

    def _get_dead_ends(self) -> list[tuple[int, int]]:
        """Return all non-locked cells that have only one open passage."""
        return [
            (x, y)
            for y in range(self.height_y)
            for x in range(self.width_x)
            if (x, y) not in self.locked_cells and self._degree(x, y) == 1
        ]

    def _braid_dead_ends(
        self, max_remaining: int = 2, max_passes: int = 10
    ) -> None:
        """Reduce dead ends by opening additional passages."""
        for _ in range(max_passes):
            dead_ends = self._get_dead_ends()
            if len(dead_ends) <= max_remaining:
                return

            random.shuffle(dead_ends)
            progress = False

            for x, y in dead_ends:
                candidates: list[tuple[int, int, str]] = []
                for direction, (dx, dy) in self._DIRECTIONS.items():
                    new_x, new_y = x + dx, y + dy

                    in_bounds = (
                        0 <= new_x < self.width_x
                        and 0 <= new_y < self.height_y
                    )
                    if not in_bounds:
                        continue
                    if (new_x, new_y) in self.locked_cells:
                        continue
                    wall_attr = self._WALL_ATTR[direction]
                    if not getattr(self.grid[y][x], wall_attr):
                        continue  # already open, not the dead end's escape

                    candidates.append((new_x, new_y, direction))

                random.shuffle(candidates)

                for new_x, new_y, direction in candidates:
                    self._remove_wall(x, y, new_x, new_y, direction)

                    if self._has_open_3x3(x, y):
                        self._add_wall(x, y, new_x, new_y, direction)
                        continue

                    progress = True
                    break

            if not progress:
                return
