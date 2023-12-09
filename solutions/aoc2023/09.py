from itertools import pairwise

from libaoc import SolutionBase


def get_seqs(line: str) -> list[tuple[int, ...]]:
    seqs = [tuple(map(int, line.split()))]
    while not all(v == 0 for v in seqs[-1]):
        seq = tuple(j - i for i, j in pairwise(seqs[-1]))
        seqs.append(seq)
    return seqs


class Solution(SolutionBase):
    def part1(self) -> int:
        total = 0
        for line in self.input():
            seqs = get_seqs(line)
            last = 0
            while seqs:
                last += seqs.pop()[-1]
            total += last
        return total

    def part2(self) -> int:
        total = 0
        for line in self.input():
            seqs = get_seqs(line)
            first = 0
            while seqs:
                first = seqs.pop()[0] - first
            total += first
        return total


if __name__ == "__main__":
    Solution().run()
