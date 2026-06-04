import sys
from config import parse, validate
from maze import MazeGenerator


def main() -> None:
    """Main function to run the maze generator."""
    if len(sys.argv) != 2:
        print("Error: Invalid arguments. Usage: python3 a_maze_ing.py"
              "config.txt")
        sys.exit(1)

    try:
        n_config = parse(sys.argv[1])
        config = validate(n_config)
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    generator = MazeGenerator(
        width=config["width"],
        height=config["height"],
        seed=config["seed"],
        start=config["entry"],
        perfect=config["perfect"]
    )
    maze = generator.main_generator()
    generator.save_file(config["output_file"], config["exit"])


if __name__ == "__main__":
    main()
