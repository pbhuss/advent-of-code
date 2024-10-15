import re
from collections.abc import Callable
from collections.abc import Mapping
from typing import TypeVar

from libaoc import SolutionBase

Light = TypeVar("Light", int, bool)


class Solution(SolutionBase):
    def solve(
        self, instruction_to_op: Mapping[str, Callable[[Light], Light]], default: Light
    ) -> int:
        grid = [[default for _ in range(1000)] for _ in range(1000)]
        base_pattern = r"(\d+),(\d+) through (\d+),(\d+)"
        pattern_to_op = {
            re.compile(rf"{instruction} {base_pattern}"): op
            for instruction, op in instruction_to_op.items()
        }
        for instruction in self.input():
            for pattern, op in pattern_to_op.items():
                if match := pattern.match(instruction):
                    coords = match.groups()
                    selected_op = op
                    break

            x0, y0, x1, y1 = map(int, coords)

            for xi in range(min(x0, x1), max(x0, x1) + 1):
                for yi in range(min(y0, y1), max(y0, y1) + 1):
                    grid[yi][xi] = selected_op(grid[yi][xi])

        return sum(sum(row) for row in grid)

    def part1(self) -> int:
        def off(light: bool) -> bool:
            return False

        def on(light: bool) -> bool:
            return True

        def toggle(light: bool) -> bool:
            return not light

        instruction_to_op = {
            "turn off": off,
            "turn on": on,
            "toggle": toggle,
        }

        return self.solve(instruction_to_op, False)

    def part2(self) -> int:
        def off(light: int) -> int:
            return max(0, light - 1)

        def on(light: int) -> int:
            return light + 1

        def toggle(light: int) -> int:
            return light + 2

        instruction_to_op = {
            "turn off": off,
            "turn on": on,
            "toggle": toggle,
        }

        return self.solve(instruction_to_op, 0)


if __name__ == "__main__":
    Solution().run()
