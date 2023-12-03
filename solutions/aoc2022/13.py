import json
import math
from functools import cmp_to_key
from itertools import batched
from itertools import zip_longest

from libaoc import SolutionBase


Item = int | list["Item"]


def check(left: Item, right: Item) -> bool | None:
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

    return None


def cmp(left: Item, right: Item) -> int:
    return -1 if check(left, right) else 1


class Solution(SolutionBase):
    def part1(self) -> int:
        result = 0
        for idx, lines in enumerate(batched(self.input(), 3), start=1):
            left = json.loads(lines[0])
            right = json.loads(lines[1])
            if check(left, right):
                result += idx
        return result

    def part2(self) -> int:
        dividers: Item = [[[2]], [[6]]]
        assert isinstance(dividers, list)
        rows: Item = dividers.copy()
        assert isinstance(rows, list)
        for line in self.input():
            if line != "":
                rows.append(json.loads(line))
        rows.sort(key=cmp_to_key(cmp))
        return math.prod(rows.index(divider) + 1 for divider in dividers)


if __name__ == "__main__":
    Solution().run()
