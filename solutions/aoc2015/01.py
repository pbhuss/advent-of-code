from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        instruction = next(self.input())
        return instruction.count("(") - instruction.count(")")

    def part2(self) -> int:
        instruction = next(self.input())
        cur_floor = 0
        for i, char in enumerate(instruction, start=1):
            match char:
                case "(":
                    cur_floor += 1
                case ")":
                    cur_floor -= 1
            if cur_floor == -1:
                return i
        raise Exception("not reachable")


if __name__ == "__main__":
    Solution().run()
