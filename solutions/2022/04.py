from libaoc import SolutionBase


def get_pairs(line):
    return (tuple(map(int, seg.split("-"))) for seg in line.split(","))


class Solution(SolutionBase):
    def part1(self):
        count = 0
        for line in self.input():
            (a1, a2), (b1, b2) = get_pairs(line)
            if (a1 <= b1 and a2 >= b2) or (a1 >= b1 and a2 <= b2):
                count += 1
        return count

    def part2(self):
        count = 0
        for line in self.input():
            (a1, a2), (b1, b2) = get_pairs(line)
            if (b1 <= a1 <= b2) or (a1 <= b1 <= a2):
                count += 1
        return count


if __name__ == "__main__":
    Solution().run()
