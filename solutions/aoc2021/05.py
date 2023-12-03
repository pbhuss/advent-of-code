import re
from collections import Counter

from libaoc import SolutionBase


class Solution(SolutionBase):
    def solve(self, diagonal: bool) -> int:
        points_pattern = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")
        counts: Counter[tuple[int, int]] = Counter()
        for line in self.input():
            match = points_pattern.search(line)
            assert match is not None
            x1, y1, x2, y2 = map(int, match.groups())
            if x1 == x2:
                for yi in range(min(y1, y2), max(y1, y2) + 1):
                    counts[(x1, yi)] += 1
            elif y1 == y2:
                for xi in range(min(x1, x2), max(x1, x2) + 1):
                    counts[(xi, y1)] += 1
            elif diagonal and abs(x1 - x2) == abs(y1 - y2):
                x_step = 1 if x2 > x1 else -1
                y_step = 1 if y2 > y1 else -1
                for i in range(0, abs(x2 - x1) + 1):
                    counts[(x1 + x_step * i, y1 + y_step * i)] += 1

        return sum(1 for count in counts.values() if count > 1)

    def part1(self) -> int:
        return self.solve(diagonal=False)

    def part2(self) -> int:
        return self.solve(diagonal=True)


if __name__ == "__main__":
    Solution().run()
