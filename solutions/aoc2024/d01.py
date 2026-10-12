from collections import Counter

from libaoc import SolutionBase


class Solution(SolutionBase):
    def get_lists(self) -> tuple[list[int], list[int]]:
        rows = (map(int, line.split()) for line in self.input())
        a, b = map(list, zip(*rows))
        return a, b

    def part1(self) -> int:
        a, b = self.get_lists()
        a.sort()
        b.sort()
        return sum(abs(bx - ax) for ax, bx in zip(a, b))

    def part2(self) -> int:
        a, b = self.get_lists()
        a_counts = Counter(a)
        b_counts = Counter(b)
        return sum(x * a_count * b_counts[x] for x, a_count in a_counts.items())


if __name__ == "__main__":
    Solution().run()
