import re

from libaoc import SolutionBase


class Solution(SolutionBase):
    def parse_input(self) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
        stacks: list[list[str]] = [[] for _ in range(len(next(self.input())) // 4 + 1)]
        input_ = self.input()
        while "[" in (line := next(input_)):
            for i in range(0, len(line), 4):
                char = line[i + 1]
                if char != " ":
                    stacks[i // 4].insert(0, char)

        next(input_)  # skip empty line

        moves = []
        pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
        for line in input_:
            match = pattern.match(line)
            assert match is not None
            count, source, dest = map(int, match.group(1, 2, 3))
            moves.append((count, source - 1, dest - 1))

        return stacks, moves

    def part1(self) -> str:
        stacks, moves = self.parse_input()
        for count, source, dest in moves:
            for _ in range(count):
                stacks[dest].append(stacks[source].pop())
        return "".join(stack[-1] for stack in stacks)

    def part2(self) -> str:
        stacks, moves = self.parse_input()
        for count, source, dest in moves:
            stacks[dest].extend(stacks[source][-count:])
            for _ in range(count):
                stacks[source].pop()
        return "".join(stack[-1] for stack in stacks)


if __name__ == "__main__":
    Solution().run()
