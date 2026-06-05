import random
from maze import MazeGenerator


def show_menu(maze: MazeGenerator, config: dict) -> None:
    """Show interactive menu for maze control."""
    colors = ["\033[0m", "\033[31m", "\033[33m", "\033[34m", "\033[36m"]
    color_idx = 0
    show_path = False

    while True:
        path_mock = set()

        maze.display(
            wall_color=colors[color_idx],
            path_coords=path_mock if show_path else set(),
            end_pos=config["exit"]
        )

        if show_path:
            print("[INFO] Путь включен (ожидает алгоритма напарника)\n")

        print("1. Re-generate maze")
        print("2. Show/Hide path")
        print("3. Change wall color")
        print("4. Quit")
        choice = input("Choice (1-4): ").strip()

        if choice == "1":
            maze.reset(random.randint(0, 999999))
            maze.main_generator()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_idx = (color_idx + 1) % len(colors)
        elif choice == "4":
            print("Quitting program")
            break
        else:
            print("Invalid choice. Please try again.")
