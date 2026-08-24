from mazegen import MazeGenerator
from mazegen import maze_to_hex


def output_maze(maze: MazeGenerator, file_name: str, path: str) -> None:
    with open(file_name, "w") as f:
        f.write(maze_to_hex(maze))
        f.write("\n")
        f.write(f"{maze.entry_pos[0]},{maze.entry_pos[1]}\n")
        f.write(f"{maze.exit_pos[0]},{maze.exit_pos[1]}\n")
        f.write(f"{path}\n")
