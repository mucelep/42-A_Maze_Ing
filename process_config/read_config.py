def read_config_file(filename: str) -> dict[str, int | str | bool | tuple[int, int]]:
    config = {}

    try: 
        with open(filename, "r") as file:
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
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: '{filename}'")
    return config