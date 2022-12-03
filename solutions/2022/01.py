from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self):
        max_group = 0
        cur_group = 0
        for line in self.input():
            if line == "":
                max_group = max(max_group, cur_group)
                cur_group = 0
            else:
                cur_group += int(line)
        max_group = max(max_group, cur_group)

        return max_group

    def part2(self):
        groups = []
        cur_group = 0
        for line in self.input():
            if line == "":
                groups.append(cur_group)
                cur_group = 0
            else:
                cur_group += int(line)
        groups.append(cur_group)

        return sum(list(sorted(groups))[-3:])


if __name__ == "__main__":
    Solution().run()
