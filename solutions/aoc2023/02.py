import re
from dataclasses import dataclass
from dataclasses import field

from libaoc import SolutionBase


@dataclass
class Color:
    name: str
    threshold: int
    pattern: re.Pattern[str] = field(init=False)

    def __post_init__(self) -> None:
        self.pattern = re.compile(rf"(\d+) {self.name}")


COLORS = [Color("red", 12), Color("green", 13), Color("blue", 14)]


class Solution(SolutionBase):
    def part1(self) -> int:
        total = 0
        for idx, line in enumerate(self.input(), start=1):
            if all(
                all(
                    int(count) <= color.threshold
                    for count in color.pattern.findall(line)
                )
                for color in COLORS
            ):
                total += idx

        return total

    def part2(self) -> int:
        total = 0
        for idx, line in enumerate(self.input(), start=1):
            power = 1
            for color in COLORS:
                power *= max(map(int, color.pattern.findall(line)))
            total += power

        return total


if __name__ == "__main__":
    Solution().run()
