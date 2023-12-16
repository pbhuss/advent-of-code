from functools import cache

from libaoc import SolutionBase


@cache
def consume(pattern: str, counts: tuple[int, ...], pos: int, ate: bool) -> int:
    if len(counts) == 0:
        return int("#" not in pattern[pos:])
    if ate:
        if pattern[pos] == "#":
            return 0
        return consume(pattern, counts, pos + 1, False)
    if len(pattern) - sum(counts) - pos - len(counts) + 1 < 0:
        return 0
    cur_count = counts[0]
    other_counts = tuple(counts[1:])
    match pattern[pos]:
        case ".":
            return consume(pattern, counts, pos + 1, False)
        case "#":
            if "." in pattern[pos : pos + cur_count]:
                return 0
            return consume(pattern, other_counts, pos + cur_count, True)
        case "?":
            total = 0
            if "." not in pattern[pos : pos + cur_count]:
                total += consume(pattern, other_counts, pos + cur_count, True)
            total += consume(pattern, counts, pos + 1, False)
            return total
        case _:
            raise Exception("unreachable")


class Solution(SolutionBase):
    def solve(self, n: int) -> int:
        total = 0
        for line in self.input():
            pattern, str_counts = line.split()
            counts = tuple(map(int, str_counts.split(","))) * n
            pattern = "?".join(pattern for _ in range(n))
            total += consume(pattern, counts, 0, False)
        return total

    def part1(self) -> int:
        return self.solve(1)

    def part2(self) -> int:
        return self.solve(5)


if __name__ == "__main__":
    Solution().run()
