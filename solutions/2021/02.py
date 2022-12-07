from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self):
        horizontal = 0
        depth = 0
        for line in self.input():
            match line.split(" "):
                case "up", n:
                    depth -= int(n)
                case "down", n:
                    depth += int(n)
                case "forward", n:
                    horizontal += int(n)
        return horizontal * depth

    def part2(self):
        horizontal = 0
        depth = 0
        aim = 0
        for line in self.input():
            match line.split(" "):
                case "down", n:
                    aim += int(n)
                case "up", n:
                    aim -= int(n)
                case "forward", n:
                    n = int(n)
                    horizontal += n
                    depth += aim * n
        return horizontal * depth


if __name__ == "__main__":
    Solution().run()
