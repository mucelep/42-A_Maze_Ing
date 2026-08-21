from .maze_generator import MazeGenerator


def grid_to_binary(maze: MazeGenerator) -> list[str]:
    grid = maze.grid
    hex_list: list[str] = []

    for y in range(maze.height_y):
        for x in range(maze.width_x):
            
            hex_maze: str = ""
            cell = grid[y][x]
            if not cell.north:
                hex_maze += "0"
            else:
                hex_maze += "1"
            if not cell.east:
                hex_maze += "0"
            else:
                hex_maze += "1"
            if not cell.south:
                hex_maze += "0"
            else:
                hex_maze += "1"
            if not cell.west:
                hex_maze += "0"
            else:
                hex_maze += "1"
            hex_list.append(hex_maze)
    
    return hex_list
