from itertools import batched

from libaoc import SolutionBase
from libaoc.grid import Direction
from libaoc.grid import move

DIR_MAP = {
    "^": Direction.NORTH,
    "v": Direction.SOUTH,
    "<": Direction.WEST,
    ">": Direction.EAST,
}


class Solution(SolutionBase):
    def part1(self) -> int:
        moves = next(self.input())
        cur = (0, 0)
        seen = {cur}
        for m in moves:
            direction = DIR_MAP[m]
            cur = move(cur, direction)
            seen.add(cur)
        return len(seen)

    def part2(self) -> int:
        moves = next(self.input())
        cur1 = (0, 0)
        cur2 = (0, 0)
        seen = {cur1}
        for m1, m2 in batched(moves, 2):
            cur1 = move(cur1, DIR_MAP[m1])
            cur2 = move(cur2, DIR_MAP[m2])
            seen.add(cur1)
            seen.add(cur2)
        return len(seen)


if __name__ == "__main__":
    Solution().run()
