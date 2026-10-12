from libaoc import grid
from libaoc import SolutionBase
from libaoc.grid import Direction


class Solution(SolutionBase):
    def part1(self) -> int:
        word_search = [list(line) for line in self.input()]
        height = len(word_search)
        width = len(word_search[0])
        total = 0
        for yi in range(height):
            for xi in range(width):
                for direction in grid.Direction:
                    try:
                        line = grid.line(word_search, (xi, yi), direction, 4)
                        if "".join(line) == "XMAS":
                            total += 1
                    except ValueError:
                        continue
        return total

    def part2(self) -> int:
        word_search = [list(line) for line in self.input()]
        height = len(word_search)
        width = len(word_search[0])
        line1 = (Direction.NORTHWEST, Direction.SOUTHEAST)
        line2 = (Direction.NORTHEAST, Direction.SOUTHWEST)
        total = 0
        target = {"M", "S"}
        for yi in range(1, height - 1):
            for xi in range(1, width - 1):
                if word_search[yi][xi] == "A":
                    pos = (xi, yi)
                    diag1 = {grid.move_get(word_search, pos, d) for d in line1}
                    diag2 = {grid.move_get(word_search, pos, d) for d in line2}
                    if diag1 == target and diag2 == target:
                        total += 1
        return total


if __name__ == "__main__":
    Solution().run()
