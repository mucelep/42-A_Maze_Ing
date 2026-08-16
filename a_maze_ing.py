#!/usr/bin/env python3
from process_config import read_config_file
from process_config import validate_config
from mazegen import MazeGenerator


def main() -> None:
    try:
        config = read_config_file()
        validate_config(config)
    except ValueError as e:
        print(f"[ERROR] - {e}")
    maze = MazeGenerator(
        config["WIDTH"],
        config["HEIGHT"],
        config["PERFECT"],
        config["SEED"]
    )
    
if __name__ == "__main__":
    main()