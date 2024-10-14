import hashlib

from libaoc import SolutionBase


class Solution(SolutionBase):
    def find(self, start: str) -> int:
        key = next(self.input())
        i = 1
        while True:
            if hashlib.md5(f"{key}{i}".encode()).hexdigest().startswith(start):
                return i
            i += 1

    def part1(self) -> int:
        return self.find("00000")

    def part2(self) -> int:
        return self.find("000000")


if __name__ == "__main__":
    Solution().run()
