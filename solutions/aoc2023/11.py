from itertools import combinations

from libaoc import SolutionBase


def get_expansion_map(seen: set[int], multiplier: int) -> dict[int, int]:
    result = {}
    prev = 0
    expansion = 0
    for cur in sorted(seen):
        expansion += (cur - prev) * (multiplier - 1)
        result[cur] = expansion
        prev = cur + 1
    return result


class Solution(SolutionBase):
    def solve(self, multiplier: int):
        x_seen = set()
        y_seen = set()
        galaxies = []
        for y, line in enumerate(self.input()):
            for x, c in enumerate(line):
                if c == "#":
                    x_seen.add(x)
                    y_seen.add(y)
                    galaxies.append((x, y))
        x_expansion = get_expansion_map(x_seen, multiplier)
        y_expansion = get_expansion_map(y_seen, multiplier)
        expanded_galaxies = [
            (x + x_expansion[x], y + y_expansion[y]) for x, y in galaxies
        ]
        total = 0
        for (x1, y1), (x2, y2) in combinations(expanded_galaxies, 2):
            total += abs(x1 - x2) + abs(y1 - y2)
        return total

    def part1(self) -> int:
        return self.solve(2)

    def part2(self) -> int:
        return self.solve(1_000_000)


if __name__ == "__main__":
    Solution().run()
