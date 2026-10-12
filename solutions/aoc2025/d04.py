from libaoc import SolutionBase
from libaoc.grid import Grid
from libaoc.grid import surrounding


def init_counts(grid: Grid[str]) -> Grid[int]:
    counts = [[0 for _ in grid[0]] for _ in grid]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "@":
                for xi, yi in surrounding((x, y), grid):
                    counts[yi][xi] += 1
    return counts


class Solution(SolutionBase):
    def part1(self) -> int:
        grid = [list(line) for line in self.input()]
        counts = init_counts(grid)
        return sum(
            1
            for y in range(len(grid))
            for x in range(len(grid[0]))
            if grid[y][x] == "@" and counts[y][x] < 4
        )

    def part2(self) -> int:
        grid = [list(line) for line in self.input()]
        counts = init_counts(grid)
        total = 0
        queue = set()
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == "@" and counts[y][x] < 4:
                    queue.add((x, y))
        while len(queue) != 0:
            coord = queue.pop()
            total += 1

            for xi, yi in surrounding(coord, grid):
                counts[yi][xi] -= 1
                if grid[yi][xi] == "@" and counts[yi][xi] == 3:
                    queue.add((xi, yi))
        return total


if __name__ == "__main__":
    Solution().run()
