import re

from libaoc import SolutionBase

DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


class Solution(SolutionBase):
    def part1(self) -> int:
        pattern = re.compile(r"\d")
        total = 0
        for line in self.input():
            matches = pattern.findall(line)
            total += int(matches[0] + matches[-1])
        return total

    def part2(self) -> int:
        pattern = re.compile(
            rf"(?=(\d|{'|'.join(DIGITS)}))"
        )  # positive lookahead for match overlaps
        total = 0
        for line in self.input():
            matches = pattern.findall(line)
            first = DIGITS.get(matches[0], matches[0])
            last = DIGITS.get(matches[-1], matches[-1])
            num = int(first + last)
            assert 11 <= num <= 99
            total += num
        return total


if __name__ == "__main__":
    Solution().run()
