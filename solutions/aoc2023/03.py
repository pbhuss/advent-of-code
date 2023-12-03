from collections.abc import Callable
from collections.abc import Collection
from collections.abc import Iterator

from libaoc import SolutionBase


Grid = list[list[str]]
Coord = tuple[int, int]


def surrounding(x: int, y: int, grid: Grid) -> Iterator[Coord]:
    height = len(grid)
    width = len(grid[0])
    for i in range(max(0, x - 1), min(width, x + 2)):
        for j in range(max(0, y - 1), min(height, y + 2)):
            if i != x or j != y:
                yield (i, j)


def get_number(i: int, j: int, grid: Grid) -> tuple[int, Coord]:
    width = len(grid[0])
    l_bound = r_bound = i
    while l_bound - 1 >= 0 and grid[j][l_bound - 1].isdigit():
        l_bound -= 1
    pos = (l_bound, j)
    while r_bound < width and grid[j][r_bound].isdigit():
        r_bound += 1
    return int("".join(grid[j][l_bound:r_bound])), pos


class Solution(SolutionBase):
    def solve(self, scorer: Callable[[Collection[int]], int]) -> int:
        total = 0
        grid = [[char for char in line] for line in self.input()]
        for y, col in enumerate(grid):
            for x, val in enumerate(col):
                if not val.isdigit() and val != ".":
                    numbers = {}
                    for i, j in surrounding(x, y, grid):
                        adj = grid[j][i]
                        if adj.isdigit():
                            num, pos = get_number(i, j, grid)
                            numbers[pos] = num
                    total += scorer(numbers.values())
        return total

    def part1(self) -> int:
        def scorer(values: Collection[int]) -> int:
            return sum(values)

        return self.solve(scorer)

    def part2(self) -> int:
        def scorer(values: Collection[int]) -> int:
            if len(values) == 2:
                a, b = values
                return a * b
            return 0

        return self.solve(scorer)


if __name__ == "__main__":
    Solution().run()
