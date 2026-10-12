from collections import Counter

from libaoc import SolutionBase


class Solution(SolutionBase):
    def solve(self, days: int) -> int:
        initial_values = map(int, next(self.input()).split(","))
        counts = Counter(initial_values)
        for _ in range(days):
            new_counts: Counter[int] = Counter()
            for timer, count in counts.items():
                if timer == 0:
                    new_counts[6] += count
                    new_counts[8] += count
                else:
                    new_counts[timer - 1] += count
            counts = new_counts
        return sum(counts.values())

    def part1(self) -> int:
        return self.solve(80)

    def part2(self) -> int:
        return self.solve(256)


if __name__ == "__main__":
    Solution().run()
