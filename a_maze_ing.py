#!/usr/bin/env python3
import sys

from mazegen import MazeGenerator, maze_slover
from output import output_maze
from process_config import read_config_file, validate_config
from visualizer import run_menu


def build_maze(
        config: dict[str, int | str | bool | tuple[int, int]]
        ) -> MazeGenerator:

    assert isinstance(config["WIDTH"], int)
    assert isinstance(config["HEIGHT"], int)
    assert isinstance(config["PERFECT"], bool)
    assert isinstance(config["ENTRY"], tuple)
    assert isinstance(config["EXIT"], tuple)
    seed = config.get("SEED")
    assert isinstance(seed, None | int)

    return MazeGenerator(
        config["WIDTH"], config["HEIGHT"],
        config["ENTRY"], config["EXIT"],
        config["PERFECT"], seed,
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
        assert isinstance(config["OUTPUT_FILE"], str)
        path: str = maze_slover(maze)
        output_maze(maze, config["OUTPUT_FILE"], path)
    except (ValueError, OSError) as e:
        print(f"[ERROR] Could not write output file - {e}")
        sys.exit(1)

    try:
        run_menu(build_maze, config, maze)
    except ValueError as e:
        print(f"[ERROR] Could not generate maze: {e}")
    except (EOFError, KeyboardInterrupt):
        print("\nBye!")


if __name__ == "__main__":
    main()
