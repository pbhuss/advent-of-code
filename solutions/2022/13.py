import json
import math
from functools import cmp_to_key
from itertools import zip_longest

from more_itertools import chunked

from libaoc import SolutionBase


def check(left: int | list, right: int | list) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left > right:
            return False
        elif left == right:
            return None
        else:
            return True

    if isinstance(left, int):
        left = [left]

    if isinstance(right, int):
        right = [right]

    for left_mem, right_mem in zip_longest(left, right):
        if left_mem is None:
            return True
        if right_mem is None:
            return False
        sub = check(left_mem, right_mem)
        if isinstance(sub, bool):
            return sub


class Solution(SolutionBase):
    def part1(self):
        result = 0
        for idx, lines in enumerate(chunked(self.input(), 3), start=1):
            left = json.loads(lines[0])
            right = json.loads(lines[1])
            if check(left, right):
                result += idx
        return result

    def part2(self):
        dividers = [[[2]], [[6]]]
        rows = dividers.copy()
        for line in self.input():
            if line != "":
                rows.append(json.loads(line))
        rows.sort(key=cmp_to_key(lambda left, right: -1 if check(left, right) else 1))
        return math.prod(rows.index(divider) + 1 for divider in dividers)


if __name__ == "__main__":
    Solution().run()
