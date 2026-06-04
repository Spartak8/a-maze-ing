import random


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: int,
        start: tuple[int, int],
    ) -> None:
        self.width = width
        self.height = height
        self.start = start
        self.mij = random.Random(seed)
        self.maze = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

    def main_generator(self):
        self.visited[self.start[1]][self.start[0]] = True
        self.x = self.start[0]
        self.y = self.start[1]
        trace = [(self.x, self.y)]

        def check_possible(x: int, y: int) -> list[int]:
            possible = []
            if y > 0 and self.visited[y - 1][x] == False:
                possible.append(0)
            if x < self.width - 1 and self.visited[y][x + 1] == False:
                possible.append(1)
            if y < self.height - 1 and self.visited[y + 1][x] == False:
                possible.append(2)
            if x > 0 and self.visited[y][x - 1] == False:
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
        return self.maze
