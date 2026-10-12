import operator
from functools import reduce
from itertools import batched

from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        total = 0
        for line in self.input():
            (c,) = set(line[: len(line) // 2]) & set(line[len(line) // 2 :])
            if c.islower():
                total += ord(c) - ord("a") + 1
            else:
                total += ord(c) - ord("A") + 27
        return total

    def part2(self) -> int:
        total = 0
        for rows in batched(self.input(), 3):
            (c,) = reduce(operator.and_, map(set, rows))
            if c.islower():
                total += ord(c) - ord("a") + 1
            else:
                total += ord(c) - ord("A") + 27
        return total


if __name__ == "__main__":
    Solution().run()
