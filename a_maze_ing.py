#!/usr/bin/env python3
from process_config import read_config_file
from process_config import validate_config


def main() -> None:
    try:
        config = read_config_file()
        validate_config(config)
    except ValueError as e:
        print(f"[ERROR] - {e}")


if __name__ == "__main__":
    main()