from collections import defaultdict

from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self):
        total = 0
        cur = None
        for line in self.input():
            new = int(line)
            if cur is not None and new > cur:
                total += 1
            cur = new
        return total

    def part2(self):
        sums = defaultdict(int)
        for i, row in enumerate(self.input()):
            value = int(row)
            for j in range(0, 3):
                sums[i - j] += value

        cur = sums[0]
        total = 0
        for i in range(1, max(sums) + 1):
            new = sums[i]
            if new > cur:
                total += 1
            cur = new
        return total


if __name__ == "__main__":
    Solution().run()
