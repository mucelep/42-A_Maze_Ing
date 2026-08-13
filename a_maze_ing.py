#!/usr/bin/env python3
import random


def read_config_file() -> dict[str, int | str | bool | tuple[int, int]]:
    config = {}
    with open("config.txt", "r") as file:
        for line in file:#satır satır tüm dosyayı geziyor
            line = line.strip()# strip sağdan soldan boslukları özel karakterleri siliyor \n gibi

            if not line or line.startswith("#"):#bos satır varsa o satırı atlıyor | stswith ise belli ztn yorum satırları icin
                continue

            if line.count("=") != 1:# 1 den fazla = var mı diye kontrol
                raise ValueError(
                    f"{line}: Invalid format use 'KEY=value'"
                )

            key, value = line.split("=")#= a göre splitliyip atıyor
            key = key.strip()# bastan sondan bosluk ve özel karakterleri sil
            value = value.strip()

            if key in config:# 2 kere yazılmıs mı kontrolü
                raise ValueError(f"Duplicate key: '{key}'")

            if key in ("WIDTH", "HEIGHT"):
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError(
                        f"{key} Must be integer"
                    )

            elif key in ("ENTRY", "EXIT"):
               try:
                    x, y = value.split(",")
                    value = (int(x), int(y))
               except ValueError:
                   raise ValueError(
                    f"{key} must be in the format x,y with integer coordinates"
                   )
                   
            elif key == "SEED":
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError(
                        f"{key} Must be integer"
                    )

            elif key == "PERFECT":
                if value == "True":
                    value = True
                elif value == "False":
                    value = False
                else:
                    raise ValueError("PERFECT must be True or False")

            elif key == "OUTPUT_FILE":
                pass

            else:
                raise ValueError(f"Unknown key: '{key}'")

            config[key] = value
    return config


def validate_config(config: dict[str, int | str | bool | tuple[int, int]]) -> None:
    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}

    for key in required_keys:# gerekli anahtarları gez
        if key not in config.keys():# her birini config içinde var mı diye kontrol et
            raise ValueError(f"Missing required key: '{key}'")

    if not config["WIDTH"] > 0:
        raise ValueError("WIDTH must be greater than '0'")

    if not config["HEIGHT"] > 0:
        raise ValueError("HEIGHT must be greater than '0'")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT cannot be equal")

    entry_x, entry_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]

    if not (0 <= entry_x < config["WIDTH"] and 0 <= entry_y < config["HEIGHT"]):
        raise ValueError(f"{config['ENTRY']} is outside the maze bounds")

    if not (0 <= exit_x < config["WIDTH"] and 0 <= exit_y < config["HEIGHT"]):
         raise ValueError(f"EXIT {config['EXIT']} is outside the maze bounds")


def main() -> None:
    try:
        config = read_config_file()
        validate_config(config)
    except ValueError as e:
        print(f"[ERROR] - {e}")
    



if __name__ == "__main__":
    main()