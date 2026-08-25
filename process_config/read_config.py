def read_config_file(filename: str) -> dict[str, int | str
                                            | bool | tuple[int, int]]:
    """Read and parse the maze configuration file."""
    config = {}

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.count("=") != 1:
                    raise ValueError(
                        f"{line}: Invalid format use 'KEY=value'"
                    )

                key, value = line.split("=")
                key = key.strip()
                value = value.strip()

                if key in config:
                    raise ValueError(f"Duplicate key: '{key}'")

                parsed_value: int | str | bool | tuple[int, int]

                if key in ("WIDTH", "HEIGHT"):
                    try:
                        parsed_value = int(value)
                    except ValueError:
                        raise ValueError(
                            f"{key} Must be integer"
                        )

                elif key in ("ENTRY", "EXIT"):
                    try:
                        x, y = value.split(",")
                        parsed_value = (int(x), int(y))
                    except ValueError:
                        raise ValueError(
                            f"{key} must be in the format "
                            "x,y with integer coordinates"
                        )

                elif key == "SEED":
                    try:
                        parsed_value = int(value)
                    except ValueError:
                        raise ValueError(
                            f"{key} Must be integer"
                        )

                elif key == "PERFECT":
                    if value == "True":
                        parsed_value = True
                    elif value == "False":
                        parsed_value = False
                    else:
                        raise ValueError("PERFECT must be True or False")

                elif key == "OUTPUT_FILE":
                    parsed_value = value

                else:
                    raise ValueError(f"Unknown key: '{key}'")

                config[key] = parsed_value
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: '{filename}'")
    return config
