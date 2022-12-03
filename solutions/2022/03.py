from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self):
        total = 0
        for line in self.input():
            c = list(set(line[: len(line) // 2]) & set(line[len(line) // 2 :]))[0]
            if c.islower():
                total += ord(c) - ord("a") + 1
            else:
                total += ord(c) - ord("A") + 27
        return total

    def part2(self):
        total = 0
        buf = []
        for line in self.input():
            buf.append(line.strip())
            if len(buf) == 3:
                c = list(set(buf[0]) & set(buf[1]) & set(buf[2]))[0]
                if c.islower():
                    total += ord(c) - ord("a") + 1
                else:
                    total += ord(c) - ord("A") + 27
                buf = []
        return total


if __name__ == "__main__":
    Solution().run()
