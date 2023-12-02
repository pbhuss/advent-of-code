from collections import deque

from libaoc import SolutionBase


class Solution(SolutionBase):
    def result(self, size: int) -> int:
        line = next(self.input())
        window: deque[str] = deque(maxlen=size)
        for i, char in enumerate(line, start=1):
            window.append(char)
            if len(window) == size and len(set(window)) == size:
                return i
        raise Exception("unreachable")

    def part1(self) -> int:
        return self.result(4)

    def part2(self) -> int:
        return self.result(14)


if __name__ == "__main__":
    Solution().run()
