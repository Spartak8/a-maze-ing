import random

from maze import MazeGenerator


def path_to_coords(solution: str, start: tuple[int, int]) -> set[tuple[int, int]]:
    x, y = start
    coords = {(x, y)}

    for move in solution:
        if move == "N":
            y -= 1
        elif move == "E":
            x += 1
        elif move == "S":
            y += 1
        elif move == "W":
            x -= 1
        coords.add((x, y))

    return coords


def show_menu(maze: MazeGenerator, config: dict, road: str) -> None:
    """Show interactive menu for maze control."""
    colors = ["\033[0m", "\033[31m", "\033[33m", "\033[34m", "\033[36m"]
    color_idx = 0
    show_path = False

    while True:
        road = maze.solve_maze(maze.maze, config["entry"], config["exit"])
        maze.save_file(config["output_file"], config["exit"], road)
        if show_path:
            solution = maze.solve_maze(
                maze.maze,
                start=config["entry"],
                end=config["exit"],
            )
            path_coords = path_to_coords(solution, config["entry"])
        else:
            path_coords = set()

        maze.display(
            wall_color=colors[color_idx],
            path_coords=path_coords,
            end_pos=config["exit"],
        )

        print("1. Re-generate maze")
        print("2. Show/Hide path")
        print("3. Change wall color")
        print("4. Quit")
        choice = input("Choice (1-4): ").strip()

        if choice == "1":
            maze.reset(random.randint(0, 999999))
            maze.main_generator()
            show_path = False

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            color_idx = (color_idx + 1) % len(colors)

        elif choice == "4":
            print("Quitting program")
            break

        else:
            print("Invalid choice. Please try again.")
