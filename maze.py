import random


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: int,
        start: tuple[int, int],
        perfect: bool,
    ) -> None:
        self.width = width
        self.height = height
        self.start = start
        self.perfect = perfect
        self.reset(seed)

    def reset(self, new_seed: int) -> None:
        self.seed = new_seed
        self.mij = random.Random(new_seed)
        self.maze = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.visited = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]
        self.blocked_cells: set[tuple[int, int]] = set()

    def add_42_pattern(self) -> None:
        pattern = [
            "10010111",
            "10010001",
            "11110111",
            "00110100",
            "00110111",
        ]

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        if start_x < 0 or start_y < 0:
            print("Error: maze is too small for 42 pattern")
            return

        for row in range(pattern_height):
            for col in range(pattern_width):
                if pattern[row][col] == "1":
                    x = start_x + col
                    y = start_y + row

                    if (x, y) == self.start:
                        continue

                    self.maze[y][x] = 15
                    self.visited[y][x] = True
                    self.blocked_cells.add((x, y))

    def enforce_border_walls(self) -> None:
        for x in range(self.width):
            self.maze[0][x] |= 1
            self.maze[self.height - 1][x] |= 4

        for y in range(self.height):
            self.maze[y][0] |= 8
            self.maze[y][self.width - 1] |= 2

    def check_connectivity(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.blocked_cells and not self.visited[y][x]:
                    raise ValueError("Maze is not fully connected")

    def make_imperfect(self) -> None:
        for _ in range((self.width * self.height) // 20):
            x = self.mij.randrange(self.width)
            y = self.mij.randrange(self.height)

            if (x, y) in self.blocked_cells:
                continue

            possible = []

            if (
                y > 0 and (x, y - 1) not in self.blocked_cells
                and self.maze[y][x] & 1
            ):
                possible.append(0)
            if (
                x < self.width - 1
                and (x + 1, y) not in self.blocked_cells
                and self.maze[y][x] & (1 << 1)
            ):
                possible.append(1)
            if (
                y < self.height - 1
                and (x, y + 1) not in self.blocked_cells
                and self.maze[y][x] & (1 << 2)
            ):
                possible.append(2)
            if (
                x > 0
                and (x - 1, y) not in self.blocked_cells
                and self.maze[y][x] & (1 << 3)
            ):
                possible.append(3)

            if not possible:
                continue

            direction = self.mij.choice(possible)

            if direction == 0:
                self.maze[y][x] &= ~1
                self.maze[y - 1][x] &= ~(1 << 2)
            elif direction == 1:
                self.maze[y][x] &= ~(1 << 1)
                self.maze[y][x + 1] &= ~(1 << 3)
            elif direction == 2:
                self.maze[y][x] &= ~(1 << 2)
                self.maze[y + 1][x] &= ~(1 << 0)
            elif direction == 3:
                self.maze[y][x] &= ~(1 << 3)
                self.maze[y][x - 1] &= ~(1 << 1)

    def main_generator(self) -> list[list[int]]:
        if not (
            0 <= self.start[0] < self.width
            and 0 <= self.start[1] < self.height
        ):
            raise ValueError("Start position is outside the maze")

        self.add_42_pattern()

        self.visited[self.start[1]][self.start[0]] = True
        self.x = self.start[0]
        self.y = self.start[1]
        trace = [(self.x, self.y)]

        def check_possible(x: int, y: int) -> list[int]:
            possible = []
            if y > 0 and not self.visited[y - 1][x]:
                possible.append(0)
            if x < self.width - 1 and not self.visited[y][x + 1]:
                possible.append(1)
            if y < self.height - 1 and not self.visited[y + 1][x]:
                possible.append(2)
            if x > 0 and not self.visited[y][x - 1]:
                possible.append(3)
            return possible

        def moves(direction: int) -> None:
            nx, ny = self.x, self.y

            if direction == 0:
                self.maze[ny][nx] = self.maze[ny][nx] & ~1
                ny -= 1
                self.maze[ny][nx] = self.maze[ny][nx] & ~(1 << 2)
            elif direction == 1:
                self.maze[ny][nx] = self.maze[ny][nx] & ~(1 << 1)
                nx += 1
                self.maze[ny][nx] = self.maze[ny][nx] & ~(1 << 3)
            elif direction == 2:
                self.maze[ny][nx] = self.maze[ny][nx] & ~(1 << 2)
                ny += 1
                self.maze[ny][nx] = self.maze[ny][nx] & ~(1 << 0)
            elif direction == 3:
                self.maze[ny][nx] = self.maze[ny][nx] & ~(1 << 3)
                nx -= 1
                self.maze[ny][nx] = self.maze[ny][nx] & ~(1 << 1)

            self.visited[ny][nx] = True
            trace.append((nx, ny))

        while trace:
            self.x, self.y = trace[-1]
            possible = check_possible(self.x, self.y)

            if possible:
                direction = self.mij.choice(possible)
                moves(direction)
            else:
                trace.pop()

        self.check_connectivity()
        self.enforce_border_walls()

        if not self.perfect:
            self.make_imperfect()
            self.enforce_border_walls()

        return self.maze

    def solve_maze(
        self,
        maze: list[list[int]],
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> str:
        height = len(maze)
        width = len(maze[0])

        queue = [start]
        head = 0
        visited = {start}
        parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

        while head < len(queue):
            x, y = queue[head]
            head += 1

            if (x, y) == end:
                break

            if y > 0 and not (maze[y][x] & 1):
                next_cell = (x, y - 1)
                if next_cell not in visited:
                    visited.add(next_cell)
                    parent[next_cell] = ((x, y), "N")
                    queue.append(next_cell)

            if x < width - 1 and not (maze[y][x] & (1 << 1)):
                next_cell = (x + 1, y)
                if next_cell not in visited:
                    visited.add(next_cell)
                    parent[next_cell] = ((x, y), "E")
                    queue.append(next_cell)

            if y < height - 1 and not (maze[y][x] & (1 << 2)):
                next_cell = (x, y + 1)
                if next_cell not in visited:
                    visited.add(next_cell)
                    parent[next_cell] = ((x, y), "S")
                    queue.append(next_cell)

            if x > 0 and not (maze[y][x] & (1 << 3)):
                next_cell = (x - 1, y)
                if next_cell not in visited:
                    visited.add(next_cell)
                    parent[next_cell] = ((x, y), "W")
                    queue.append(next_cell)

        if end not in visited:
            raise ValueError("No path from entry to exit")

        path = []
        current = end

        while current != start:
            previous, move = parent[current]
            path.append(move)
            current = previous
        path.reverse()
        return "".join(path)

    def save_file(
        self, filename: str, end: tuple[int, int], road: str
    ) -> None:
        with open(filename, "w") as f:
            for row in self.maze:
                hex_row = "".join(f"{cell:X}" for cell in row)
                f.write(hex_row + "\n")
            f.write("\n")
            f.write(f"{self.start[0]},{self.start[1]}\n")
            f.write(f"{end[0]},{end[1]}\n")
            f.write(f"{road}\n")

    def display(
        self,
        wall_color: str = "",
        path_coords: set[tuple[int, int]] | None = None,
        end_pos: tuple[int, int] | None = None,
    ) -> None:
        """Классическая визуализация +---+, которая идеально работает в PS."""
        if path_coords is None:
            path_coords = set()
        if end_pos is None:
            end_pos = (self.width - 1, self.height - 1)

        print("\n=== A-Maze-ing ===")
        reset = "\033[0m"

        if not wall_color:
            wall_color = reset

        for y in range(self.height):
            top_line = ""
            mid_line = ""
            for x in range(self.width):
                cell = self.maze[y][x]

                top_line += "+---" if cell & 1 else "+   "
                west_wall = "|" if cell & 8 else " "
                if (x, y) in self.blocked_cells:
                    mid_line += f"{west_wall}\033[42m   {reset}{wall_color}"
                elif (x, y) in path_coords:
                    mid_line += f"{west_wall}\033[44m   {reset}{wall_color}"
                elif (x, y) == self.start:
                    # магента = вход
                    mid_line += f"{west_wall}\033[45m   {reset}{wall_color}"
                elif (x, y) == end_pos:
                    mid_line += f"{west_wall}\033[41m   {reset}{wall_color}"
                else:
                    mid_line += f"{west_wall}   "
            print(f"{wall_color}{top_line}+{reset}")
            east_wall = "|" if self.maze[y][-1] & 2 else " "
            print(f"{wall_color}{mid_line}{east_wall}{reset}")
        bottom_line = ""
        for x in range(self.width):
            bottom_line += "+---" if self.maze[-1][x] & 4 else "+   "
        print(f"{wall_color}{bottom_line}+{reset}")
        print("==================\n")
