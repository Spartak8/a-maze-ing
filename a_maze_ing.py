import sys
from parser import parse, validate


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: Invalid arguments")
        sys.exit(1)
    n_config = parse(sys.argv[1])
    config = validate(n_config)
    print(config)


if __name__ == "__main__":
    main()
