import operator
from collections.abc import Callable

from libaoc import SolutionBase


def reduce_value(lines: list[str], op: Callable) -> str:
    i = 0
    while len(lines) > 1:
        a0 = [line for line in lines if line[i] == "0"]
        a1 = [line for line in lines if line[i] == "1"]
        lines = a1 if op(len(a1), len(a0)) else a0
        i += 1
    return lines[0]


class Solution(SolutionBase):
    def part1(self):
        counts = [0] * len(next(self.input()))
        for line in self.input():
            for i, char in enumerate(line):
                if char == "1":
                    counts[i] += 1
                else:
                    counts[i] -= 1
        a = "".join("0" if count > 0 else "1" for count in counts)
        b = "".join("1" if count > 0 else "0" for count in counts)
        return int(a, base=2) * int(b, base=2)

    def part2(self):
        lines = list(self.input())

        a = reduce_value(lines, operator.ge)
        b = reduce_value(lines, operator.lt)

        return int(a, base=2) * int(b, base=2)


if __name__ == "__main__":
    Solution().run()
