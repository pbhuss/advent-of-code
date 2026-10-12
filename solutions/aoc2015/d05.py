from collections.abc import Iterable
from itertools import pairwise

from libaoc import SolutionBase

"""
A nice string is one with all of the following properties:
  - It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
  - It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
  - It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
"""

VOWELS = "aeiou"
DENY_STRS = ("ab", "cd", "pq", "xy")


def num_vowels(s: str) -> int:
    return sum(s.count(v) for v in VOWELS)


def has_repeat(s: str) -> bool:
    return any(c1 == c2 for c1, c2 in pairwise(s))


def contains_any_substr(s: str, substrs: Iterable[str]) -> bool:
    return any(substr in s for substr in substrs)


def has_repeating_pair(s: str) -> bool:
    return any(s[i : i + 2] in s[i + 2 :] for i in range(len(s) - 3))


def has_repeating_off_by_one(s: str) -> bool:
    return any(s[i] == s[i + 2] for i in range(len(s) - 2))


class Solution(SolutionBase):
    def part1(self) -> int:
        return sum(
            1
            for s in self.input()
            if num_vowels(s) >= 3
            and has_repeat(s)
            and not contains_any_substr(s, DENY_STRS)
        )

    def part2(self) -> int:
        return sum(
            1
            for s in self.input()
            if has_repeating_pair(s) and has_repeating_off_by_one(s)
        )


if __name__ == "__main__":
    Solution().run()
