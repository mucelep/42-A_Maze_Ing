def validate_config(config: dict[str, int | str |
                    bool | tuple[int, int]]) -> None:
    """Validate the maze configuration and raise errors for invalid values."""
    required_keys = {"WIDTH", "HEIGHT", "ENTRY",
                     "EXIT", "OUTPUT_FILE", "PERFECT"}

    assert isinstance(config["WIDTH"], int)
    assert isinstance(config["HEIGHT"], int)
    assert isinstance(config["ENTRY"], tuple)
    assert isinstance(config["EXIT"], tuple)

    for key in required_keys:
        if key not in config.keys():
            raise ValueError(f"Missing required key: '{key}'")

    if not config["WIDTH"] > 0:
        raise ValueError("WIDTH must be greater than '0'")

    if not config["HEIGHT"] > 0:
        raise ValueError("HEIGHT must be greater than '0'")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT cannot be equal")

    entry_x, entry_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]

    if not (0 <= entry_x < config["WIDTH"] and
            0 <= entry_y < config["HEIGHT"]):
        raise ValueError(f"{config['ENTRY']} is outside the maze bounds")

    if not (0 <= exit_x < config["WIDTH"] and 0 <= exit_y < config["HEIGHT"]):
        raise ValueError(f"EXIT {config['EXIT']} is outside the maze bounds")
