import math

from libaoc import SolutionBase


class Solution(SolutionBase):
    def solve(self, *, click_mode: bool) -> int:
        zeroes = 0
        cur = 50
        for line in self.input():
            direction = line[0]
            value = int(line[1:])
            prev_zero = cur == 0
            match direction:
                case "L":
                    cur -= value
                case "R":
                    cur += value
                case _:
                    raise ValueError(direction)
            if click_mode:
                if cur <= 0:
                    zeroes += abs(math.ceil(cur / 100)) + (0 if prev_zero else 1)
                elif cur >= 100:
                    zeroes += math.floor(cur / 100)
            cur %= 100
            if not click_mode and cur == 0:
                zeroes += 1
        return zeroes

    def part1(self) -> int:
        return self.solve(click_mode=False)

    def part2(self) -> int:
        return self.solve(click_mode=True)


if __name__ == "__main__":
    Solution().run()
