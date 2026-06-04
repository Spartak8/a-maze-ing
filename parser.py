import sys
import random


def parse(filepath: str) -> dict[str, str]:
    """Read config file and return dictionary of raw string values.

    Args:
        filepath: Path to the config file.

    Returns:
        Dictionary with raw string values.
    """
    config = {}
    try:
        with open(filepath) as f:
            for line in f:
                n_line = line.strip()
                if n_line.startswith('#'):
                    continue
                if not n_line:
                    continue
                s_line = n_line.split('=', 1)
                if len(s_line) != 2:
                    print(f"Error: invalid line '{n_line}'")
                    sys.exit(1)
                config[s_line[0].strip()] = s_line[1].strip()
            return config
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def validate(config: dict[str, str]) -> dict[str, object]:
    """Validate and convert raw config dictionary.

    Args:
        config: Raw dictionary from parse().

    Returns:
        Dictionary with validated and converted values.
    """
    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in required:
        if key not in config:
            print(f"Error: missing key '{key}'")
            sys.exit(1)
    if not config["OUTPUT_FILE"]:
        print("Error: OUTPUT_FILE cannot be empty")
        sys.exit(1)

    try:
        width = int(config["WIDTH"])
    except ValueError:
        print("Error: WIDTH must be a number")
        sys.exit(1)
    if width <= 0:
        print("Error: WIDTH must be positive")
        sys.exit(1)

    try:
        height = int(config["HEIGHT"])
    except ValueError:
        print("Error: HEIGHT must be a number")
        sys.exit(1)
    if height <= 0:
        print("Error: HEIGHT must be positive")
        sys.exit(1)

    entry = config["ENTRY"].split(',')
    if len(entry) != 2:
        print("Error: ENTRY must be two coordinates x,y")
        sys.exit(1)
    ex = config["EXIT"].split(',')
    if len(ex) != 2:
        print("Error: EXIT must be two coordinates x,y")
        sys.exit(1)

    try:
        n_entry = [int(x) for x in entry]
        result_en = tuple(n_entry)
    except ValueError:
        print("Error: Entry must be a number")
        sys.exit(1)

    try:
        n_ex = [int(x) for x in ex]
        result_ex = tuple(n_ex)
    except ValueError:
        print("Error: Exit must be a number")
        sys.exit(1)

    if config["PERFECT"] == "True":
        perfect = True
    elif config["PERFECT"] == "False":
        perfect = False
    else:
        print("Error: Perfect must be a bool")
        sys.exit(1)

    if result_en[0] < 0 or result_en[0] >= width:
        print("Error: ENTRY x is out of bounds")
        sys.exit(1)

    if result_en[1] < 0 or result_en[1] >= height:
        print("Error: ENTRY y is out of bounds")
        sys.exit(1)

    if result_ex[0] < 0 or result_ex[0] >= width:
        print("Error: EXIT x is out of bounds")
        sys.exit(1)

    if result_ex[1] < 0 or result_ex[1] >= height:
        print("Error: EXIT y is out of bounds")
        sys.exit(1)

    if result_en[0] == result_ex[0] and result_en[1] == result_ex[1]:
        print("Error: Exit and Entry are the same")
        sys.exit(1)

    if "SEED" in config:
        try:
            seed = int(config["SEED"])
        except ValueError:
            print("Error: SEED must be a number")
            sys.exit(1)
    else:
        seed = random.randint(0, 999999)
        print(f"No seed provided, using: {seed}")

    return {
        "width": width,
        "height": height,
        "entry": result_en,
        "exit": result_ex,
        "output_file": config["OUTPUT_FILE"],
        "perfect": perfect,
        "seed": seed
    }
