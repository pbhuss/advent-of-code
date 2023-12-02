from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        result = 0
        cycle = 0
        value = 1
        for line in self.input():
            cycle += 1
            if cycle % 40 == 20:
                result += cycle * value
            if line != "noop":
                cycle += 1
                if cycle % 40 == 20:
                    result += cycle * value
                value += int(line.split()[1])
            if cycle >= 220:
                break
        return result

    def part2(self) -> str:
        rows = []
        cycle = 0
        value = 1
        row = []
        for line in self.input():
            for i in range(2):
                if i == 1 and line == "noop":
                    break
                if abs(value - cycle % 40) > 1:
                    row.append(".")
                else:
                    row.append("#")
                cycle += 1
                if i == 1:
                    value += int(line.split()[1])
                if cycle % 40 == 0:
                    rows.append("".join(row))
                    row = []
        return "\n".join(rows)


if __name__ == "__main__":
    Solution().run()
