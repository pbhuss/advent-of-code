from libaoc import SolutionBase


class Solution(SolutionBase):
    def result(self, size: int):
        line = next(self.input())
        for i in range(len(line) - (size - 1)):
            if len(set(line[i : i + size])) == size:
                return i + size

    def part1(self):
        return self.result(4)

    def part2(self):
        return self.result(14)


if __name__ == "__main__":
    Solution().run()
