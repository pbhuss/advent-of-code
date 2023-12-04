from collections import Counter

from libaoc import SolutionBase


def triangular(n: int) -> int:
    return n * (n + 1) // 2


class Solution(SolutionBase):
    def part1(self) -> int:
        positions = sorted(map(int, next(self.input()).split(",")))
        median = positions[len(positions) // 2]
        return sum(
            abs(pos - median) * count for pos, count in Counter(positions).items()
        )

    def part2(self) -> int:
        positions = sorted(map(int, next(self.input()).split(",")))
        pos_counts = Counter(positions)
        return min(
            sum(
                triangular(abs(pos - align_pos)) * count
                for pos, count in pos_counts.items()
            )
            for align_pos in range(min(pos_counts), max(pos_counts) + 1)
        )


if __name__ == "__main__":
    Solution().run()
