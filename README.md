*This project has been created as part of the 42 curriculum by skhachat, armelkon.*

# A-Maze-ing

## Description

A-Maze-ing is a procedural maze generator and solver written in Python. The program reads a configuration file, generates a random maze using the **Recursive Backtracker** algorithm, finds the shortest path from entry to exit using **BFS**, and displays the result in the terminal with an interactive menu. The maze always contains a hidden **"42"** pattern drawn from fully closed cells.

The generation logic is packaged as a reusable pip-installable module (`mazegen-amazeing`).

---

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
make install
```

### Running

```bash
make run
# or directly:
python3 a_maze_ing.py config.txt
```

### Debug mode

```bash
make debug
```

### Lint

```bash
make lint
make lint-strict  # optional, stricter mypy
```

### Clean

```bash
make clean
```

---

## Configuration File Format

The config file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are comments and are ignored. Empty lines are also ignored.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells (positive integer) | `WIDTH=20` |
| `HEIGHT` | Maze height in cells (positive integer) | `HEIGHT=20` |
| `ENTRY` | Entry coordinates `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze? (`True` or `False`) | `PERFECT=True` |
| `SEED` | Optional seed for reproducibility | `SEED=42` |

**Example config.txt:**
```
# A-Maze-ing default config
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

If `SEED` is not provided, a random seed is generated automatically.

---

## Output File Format

The output file contains one hexadecimal character per cell, where each hex digit encodes which walls are closed (bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West). Cells are stored row by row. After an empty line, the entry coordinates, exit coordinates, and shortest path (as a string of `N`, `E`, `S`, `W` letters) are written.

```
9F5A...
...
(empty line)
0,0
19,14
SSEENEEW...
```

---

## Maze Generation Algorithm

The maze is generated using the **Recursive Backtracker** (iterative DFS with a stack), which guarantees a perfect maze (exactly one path between any two cells).

**Steps:**
1. Start from the entry cell, mark it as visited.
2. Look at unvisited neighbours. Pick one randomly, knock down the wall between them, move there.
3. If no unvisited neighbours — backtrack using the stack.
4. Repeat until all cells are visited.

**Why this algorithm?**
- Produces long, winding corridors — visually appealing mazes.
- Guarantees full connectivity (perfect maze) by construction.
- Simple to implement with a stack instead of recursion.
- Easy to make reproducible with a seed.

For imperfect mazes (`PERFECT=False`), about 5% of walls are randomly removed after generation to create loops.

---

## Visual Representation

The maze is displayed in the terminal using ASCII characters (`+`, `-`, `|`). The **"42" pattern** is highlighted in green. The solution path is highlighted in blue.

### Interactive Menu

```
1. Re-generate maze   — generate a new maze with a random seed
2. Show/Hide path     — toggle the BFS shortest path display
3. Change wall color  — cycle through wall colors
4. Quit               — exit the program
```

---

## Reusable Module

The maze generation logic is packaged as `mazegen-amazeing` and can be installed via pip:

```bash
pip install mazegen-amazeing-1.0.0-py3-none-any.whl
```

### Basic Usage

```python
from maze import MazeGenerator

# Create generator
gen = MazeGenerator(width=20, height=15, seed=42, start=(0, 0), perfect=True)

# Generate maze
grid = gen.main_generator()

# Find shortest path
path = gen.solve_maze(grid, start=(0, 0), end=(19, 14))
print(path)  # e.g. "SSEENEEW..."

# Save to file
gen.save_file("maze.txt", end=(19, 14), road=path)

# Display in terminal
gen.display()
```

### Custom Parameters

```python
# Different size and seed
gen = MazeGenerator(width=30, height=20, seed=12345, start=(0, 0), perfect=False)

# Reset with new seed (for re-generation)
gen.reset(new_seed=99999)
gen.main_generator()
```

### Accessing the Maze Structure

```python
# maze.maze — 2D list of integers (hex wall values)
grid = gen.maze  # list[list[int]]

# maze.blocked_cells — set of coordinates forming the "42" pattern
pattern = gen.blocked_cells  # set[tuple[int, int]]

# solve_maze — returns path as string of N/E/S/W letters
path = gen.solve_maze(grid, start=(0, 0), end=(19, 14))
```

### Building the Package

```bash
pip install build
python -m build
# Output: dist/mazegen_amazeing-1.0.0-py3-none-any.whl
```

---

## Team and Project Management

### Roles

| Member | Responsibilities |
|--------|-----------------|
| **skhachat** | Config parser (`config.py`), input validation, interactive menu (`show.py`), visual display, testing, pip packaging, Makefile, `.gitignore`, README, output file format |
| **armelkon** | Maze generator (`maze.py`), BFS solver, "42" pattern, border enforcement, connectivity check, imperfect maze logic, main entry point (`a_maze_ing.py`) |

### Planning and Evolution

We started by splitting the project into two independent parts: the generator core (armelkon) and the interface/config layer (skhachat). This allowed parallel development without blocking each other.

Initially we planned to use the MiniLibX graphical library, but switched to terminal ASCII rendering early on — it was faster to implement, easier to debug, and worked across all platforms.

The main challenge was integrating the "42" pattern with the maze generation algorithm. The solution was to pre-mark pattern cells as `visited=True` before running the backtracker, so the algorithm naturally routes around them.

### What Worked Well

- Clear separation of responsibilities between team members
- Early decision to use terminal rendering instead of MLX saved significant time
- Using `raise ValueError` in the core modules and catching everything in `main()` made error handling clean and centralized

### What Could Be Improved

- The "42" pattern is always centered — a configurable position would be better
- No animation during generation (bonus feature we didn't have time for)
- Windows PowerShell has partial ANSI support — some color features work better on Linux/macOS terminals

### Tools Used

- VS Code with Python extension
- mypy and flake8 for static analysis and style
- Git for version control and collaboration
- Claude AI (claude.ai) — used for explaining concepts (BFS, bitwise operations, ANSI color codes), reviewing code logic, and helping structure the README. All generated content was reviewed, tested, and understood before inclusion.

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation — Think Labyrinth](http://www.astrolog.org/labyrnth/algrithm.htm)
- [BFS shortest path — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python bitwise operators](https://wiki.python.org/moin/BitwiseOperators)
- [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

**AI usage:** Claude (claude.ai) was used throughout the project to explain concepts (bitwise operations, BFS algorithm, ANSI color codes, Python packaging), review code for bugs, and help draft this README. All AI-generated explanations and suggestions were verified, tested, and fully understood by both team members before being used.
