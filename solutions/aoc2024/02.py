from collections.abc import Iterable
from itertools import pairwise

from libaoc import SolutionBase


def same_polarity(n: Iterable[int]) -> bool:
    return len(set(x > 0 for x in n)) == 1


def all_between(n: Iterable[int], a: int, b: int) -> bool:
    return all(a <= abs(x) <= b for x in n)


class Solution(SolutionBase):
    def solve(self, with_removal: bool) -> int:
        total = 0
        for line in self.input():
            nums = list(map(int, line.split()))
            diffs = [x - y for x, y in pairwise(nums)]
            if same_polarity(diffs) and all_between(diffs, 1, 3):
                total += 1
                continue

            if with_removal:
                for i, x in enumerate(nums):
                    nums.pop(i)
                    diffs = [x - y for x, y in pairwise(nums)]
                    if same_polarity(diffs) and all_between(diffs, 1, 3):
                        total += 1
                        break
                    nums.insert(i, x)
        return total

    def part1(self) -> int:
        return self.solve(with_removal=False)

    def part2(self) -> int:
        return self.solve(with_removal=True)


if __name__ == "__main__":
    Solution().run()
