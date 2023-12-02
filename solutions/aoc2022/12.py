import math
from queue import PriorityQueue

from libaoc import SolutionBase


def neighbors(
    grid: dict[tuple[int, int], int], x: int, y: int
) -> list[tuple[int, int]]:
    return [
        (x + i, y + j)
        for i, j in [(0, -1), (0, 1), (1, 0), (-1, 0)]
        if (x + i, y + j) in grid and grid[(x + i, y + j)] - grid[(x, y)] <= 1
    ]


def neighbors_reverse(grid: dict[tuple[int, int], int], x: int, y: int):
    return [
        (x + i, y + j)
        for i, j in [(0, -1), (0, 1), (1, 0), (-1, 0)]
        if (x + i, y + j) in grid and grid[(x, y)] - grid[(x + i, y + j)] <= 1
    ]


# TODO: DRY this up
class Solution(SolutionBase):
    def part1(self) -> int:
        grid = {}
        start = None
        end = None
        for y, line in enumerate(self.input()):
            for x, val in enumerate(line):
                match val:
                    case "S":
                        start = (x, y)
                        val = "a"
                    case "E":
                        end = (x, y)
                        val = "z"
                grid[(x, y)] = ord(val) - ord("a")

        n_col, n_row = map(lambda x: x + 1, max(grid))

        dists = {}
        visited = set()
        dists[start] = 0

        queue = PriorityQueue()
        queue.put((0, start))
        for x in range(n_col):
            for y in range(n_row):
                pos = (x, y)
                if pos != start:
                    dists[pos] = math.inf

        while not queue.empty():
            dist, pos = queue.get()
            if pos == end:
                return dists[end]
            if pos in visited:
                continue
            visited.add(pos)
            for neighbor in neighbors(grid, *pos):
                alt_dist = dist + 1
                if alt_dist < dists[neighbor]:
                    dists[neighbor] = alt_dist
                    queue.put((alt_dist, neighbor))

        raise Exception("unreachable")

    def part2(self) -> int:
        grid = {}
        start = None
        ends = []
        for y, line in enumerate(self.input()):
            for x, val in enumerate(line):
                match val:
                    case "S":
                        ends.append((x, y))
                        val = "a"
                    case "E":
                        start = (x, y)
                        val = "z"
                    case "a":
                        ends.append((x, y))
                grid[(x, y)] = ord(val) - ord("a")

        n_col, n_row = map(lambda x: x + 1, max(grid))

        dists = {}
        visited = set()
        dists[start] = 0

        queue = PriorityQueue()
        queue.put((0, start))
        for x in range(n_col):
            for y in range(n_row):
                pos = (x, y)
                if pos != start:
                    dists[pos] = math.inf

        while not queue.empty():
            dist, pos = queue.get()
            if pos in visited:
                continue
            visited.add(pos)
            for neighbor in neighbors_reverse(grid, *pos):
                alt_dist = dist + 1
                if alt_dist < dists[neighbor]:
                    dists[neighbor] = alt_dist
                    queue.put((alt_dist, neighbor))

        return min(dists[end] for end in ends)


if __name__ == "__main__":
    Solution().run()
