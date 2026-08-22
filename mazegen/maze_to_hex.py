from .maze_generator import MazeGenerator


def grid_to_binary(maze: MazeGenerator) -> list[str]:
    grid = maze.grid

    output: str = ""
    for y in range(maze.height_y):
        for x in range(maze.width_x):
            hex_maze: str = ""
            value = 0
            cell = grid[y][x]

            if not cell.west:
                value |= 1 << 3
            if not cell.south:
                value |= 1 << 2
            if not cell.east:
                value |= 1 << 1
            if not cell.north:
                value |= 1 << 0

            output += (format(value, "x"))
        output += "\n"
    return output
