#!/usr/bin/env python3
# from mazegen import MazeGenerator


# def print_maze_ascii(gen: MazeGenerator) -> None:
#     """Labirenti terminale basar - '42' desenindeki kilitli hücreleri '#' ile,
#     normal koridorları boşluk ile gösterir.
#     """
#     width, height = gen.width_x, gen.height_y

#     print("+" + "---+" * width)

#     for y in range(height):
#         # hücre içi + doğu duvarları
#         line = "|"
#         for x in range(width):
#             cell = gen.grid[y][x]
#             line += "###" if (x, y) in gen.locked_cells else "   "
#             line += "|" if cell.east else " "
#         print(line)

#         # güney duvarları
#         line = "+"
#         for x in range(width):
#             cell = gen.grid[y][x]
#             line += "---" if cell.south else "   "
#             line += "+"
#         print(line)

# if __name__ == "__main__":
#     try:
#         gen = MazeGenerator(width=20, height=15, perfect=True)
#         print("=== PERFECT=True (20x15, seed=1) ===\n")
#         print_maze_ascii(gen)

#         print("\n\n=== PERFECT=False (20x15, seed=1) ===\n")
#         gen2 = MazeGenerator(width=20, height=15, perfect=False)
#         print_maze_ascii(gen2)
#     except (ValueError, FileNotFoundError) as e:
#         print(f"[ERROR] {e}")
        


from output import output_maze
from process_config import read_config_file
from process_config import validate_config
from mazegen import MazeGenerator, maze_slover
import sys
from visualizer import run_menu

#!/usr/bin/env python3
import sys

from output import output_maze
from process_config import read_config_file, validate_config
from mazegen import MazeGenerator, maze_slover
from visualizer import run_menu


def build_maze(config: dict) -> MazeGenerator:
    return MazeGenerator(
        config["WIDTH"], config["HEIGHT"],
        config["ENTRY"], config["EXIT"],
        config["PERFECT"], config.get("SEED"),
    )


def main() -> None:
    if len(sys.argv) != 2:
        print("[ERROR] Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    try:
        config = read_config_file(sys.argv[1])
        validate_config(config)
        maze = build_maze(config)
    except (ValueError, FileNotFoundError) as e:
        print(f"[ERROR] - {e}")
        sys.exit(1)

    try:
        path: str = maze_slover(maze)
        output_maze(maze, config["OUTPUT_FILE"], path)
    except (ValueError, OSError) as e:
        print(f"[ERROR] Could not write output file - {e}")
        sys.exit(1)

    try:
        run_menu(build_maze, config)
    except ValueError as e:
        print(f"[ERROR] Could not generate maze: {e}")
    except (EOFError, KeyboardInterrupt):
        print("\nBye!")


if __name__ == "__main__":
    main()

