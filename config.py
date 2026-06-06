import random
from typing import TypedDict


class ConfigDict(TypedDict):
    """Store validated maze configuration values."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int


def parse(filepath: str) -> dict[str, str]:
    """Read raw key-value pairs from a config file."""
    config = {}
    with open(filepath) as f:
        for line in f:
            n_line = line.strip()
            if n_line.startswith('#'):
                continue
            if not n_line:
                continue
            s_line = n_line.split('=', 1)
            if len(s_line) != 2:
                raise ValueError(f"invalid line '{n_line}'")
            config[s_line[0].strip()] = s_line[1].strip()
        return config


def validate(config: dict[str, str]) -> ConfigDict:
    """Validate raw config values and convert them to Python types."""
    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in required:
        if key not in config:
            raise ValueError(f"missing key '{key}'")
    if not config["OUTPUT_FILE"]:
        raise ValueError("OUTPUT_FILE cannot be empty")

    try:
        width = int(config["WIDTH"])
    except ValueError:
        raise ValueError("WIDTH must be a number")
    if width <= 0:
        raise ValueError("WIDTH must be positive")

    try:
        height = int(config["HEIGHT"])
    except ValueError:
        raise ValueError("HEIGHT must be a number")
    if height <= 0:
        raise ValueError("HEIGHT must be positive")

    entry = config["ENTRY"].split(',')
    if len(entry) != 2:
        raise ValueError("ENTRY must be two coordinates x,y")
    ex = config["EXIT"].split(',')
    if len(ex) != 2:
        raise ValueError("EXIT must be two coordinates x,y")

    try:
        n_entry = [int(x) for x in entry]
        result_en = (n_entry[0], n_entry[1])
    except ValueError:
        raise ValueError("Entry must be a number")

    try:
        n_ex = [int(x) for x in ex]
        result_ex = (n_ex[0], n_ex[1])
    except ValueError:
        raise ValueError("Exit must be a number")

    if config["PERFECT"] == "True":
        perfect = True
    elif config["PERFECT"] == "False":
        perfect = False
    else:
        raise ValueError("Perfect must be a bool")

    if result_en[0] < 0 or result_en[0] >= width:
        raise ValueError("ENTRY x is out of bounds")

    if result_en[1] < 0 or result_en[1] >= height:
        raise ValueError("ENTRY y is out of bounds")

    if result_ex[0] < 0 or result_ex[0] >= width:
        raise ValueError("EXIT x is out of bounds")

    if result_ex[1] < 0 or result_ex[1] >= height:
        raise ValueError("EXIT y is out of bounds")

    if result_en[0] == result_ex[0] and result_en[1] == result_ex[1]:
        raise ValueError("Exit and Entry are the same")

    if "SEED" in config:
        try:
            seed = int(config["SEED"])
        except ValueError:
            raise ValueError("SEED must be a number")
    else:
        seed = random.randint(0, 999999)

    return {
        "width": width,
        "height": height,
        "entry": result_en,
        "exit": result_ex,
        "output_file": config["OUTPUT_FILE"],
        "perfect": perfect,
        "seed": seed
    }
