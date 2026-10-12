import re

from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        pat = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
        total = 0
        for line in self.input():
            for match in pat.finditer(line):
                a, b = map(int, match.groups())
                total += a * b
        return total

    def part2(self) -> int:
        pat = re.compile(r"mul\(([0-9]+),([0-9]+)\)|(do\(\))|(don't\(\))")
        total = 0
        enabled = True
        for line in self.input():
            for match in pat.finditer(line):
                a, b, do, dont = match.groups()
                if do:
                    enabled = True
                elif dont:
                    enabled = False
                elif enabled:
                    total += int(a) * int(b)
        return total


if __name__ == "__main__":
    Solution().run()
