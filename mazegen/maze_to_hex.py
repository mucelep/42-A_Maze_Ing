from .maze_generator import MazeGenerator


def maze_to_hex(maze: MazeGenerator) -> str:
    grid = maze.grid

    output: str = ""
    for y in range(maze.height_y):
        for x in range(maze.width_x):
            value = 0
            cell = grid[y][x]

            if cell.west:
                value |= 1 << 3
            if cell.south:
                value |= 1 << 2
            if cell.east:
                value |= 1 << 1
            if cell.north:
                value |= 1 << 0

            output += (format(value, "x"))
        output += "\n"
    return output
