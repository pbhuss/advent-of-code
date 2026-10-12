import math

from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        total = 0
        for present in self.input():
            length, width, height = list(map(int, present.split("x")))
            sides = (length * width, length * height, width * height)
            total += 2 * sum(sides) + min(sides)
        return total

    def part2(self) -> int:
        total = 0
        for present in self.input():
            dimensions = sorted(map(int, present.split("x")))
            total += 2 * sum(dimensions[:2]) + math.prod(dimensions)
        return total


if __name__ == "__main__":
    Solution().run()
