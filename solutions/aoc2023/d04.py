from collections import Counter

from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        total = 0
        for card, line in enumerate(self.input(), start=1):
            _, nums = line.split(": ")
            left, right = nums.split("|")
            winning = set(left.split())
            have = set(right.split())
            matches = len(have & winning)
            if matches:
                total += 2 ** (matches - 1)
        return total

    def part2(self) -> int:
        counts: Counter[int] = Counter()
        for card, line in enumerate(self.input(), start=1):
            _, nums = line.split(": ")
            left, right = nums.split("|")
            winning = set(left.split())
            have = set(right.split())
            matches = len(have & winning)
            counts[card] += 1
            for i in range(matches):
                counts[card + 1 + i] += counts[card]
        return sum(counts.values())


if __name__ == "__main__":
    Solution().run()
