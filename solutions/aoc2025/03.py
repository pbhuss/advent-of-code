from itertools import islice

from libaoc import SolutionBase


def max_idx(nums: list[int], start: int, stop: int) -> tuple[int, int]:
    max_val = nums[start]
    max_pos = start
    for cur_pos, cur_val in enumerate(islice(nums, start + 1, stop), start=start + 1):
        if cur_val > max_val:
            max_val = cur_val
            max_pos = cur_pos
    return max_val, max_pos


def joltage(nums: list[int], remaining: int, cur_pos: int = 0, cur_val: int = 0) -> int:
    remaining -= 1
    next_digit, next_pos = max_idx(nums, cur_pos, len(nums) - remaining)
    cur_val *= 10
    cur_val += next_digit
    if remaining == 0:
        return cur_val
    else:
        return joltage(nums, remaining, next_pos + 1, cur_val)


class Solution(SolutionBase):
    def solve(self, length: int) -> int:
        total = 0

        for line in self.input():
            vals = list(map(int, line))
            total += joltage(vals, length)

        return total

    def part1(self) -> int:
        return self.solve(2)

    def part2(self) -> int:
        return self.solve(12)


if __name__ == "__main__":
    Solution().run()
