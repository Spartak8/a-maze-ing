import random
from maze import MazeGenerator


def show_menu(maze: MazeGenerator, config: dict) -> None:
    """Show interactive menu for maze control."""
    while True:
        maze.display()
        print("1. Re-generate maze")
        print("2. Show/Hide path")
        print("3. Change wall color")
        print("4. Quit")
        choice = input("Choice (1-4): ")

        if choice == "1":
            maze.reset(random.randint(0, 999999))
            maze.main_generator()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
