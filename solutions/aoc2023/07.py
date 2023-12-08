from collections import Counter
from collections.abc import Callable

from libaoc import SolutionBase

ALL_CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def rank(hand: str, wild_jacks: bool) -> tuple[int, tuple[int, ...]]:
    counter = Counter(hand)

    card_list = ALL_CARDS

    if wild_jacks:
        if "J" in counter:
            j_count = counter.pop("J")
            if j_count == 5:
                counter["J"] = 5
            else:
                counter[counter.most_common(1)[0][0]] += j_count

        card_list = card_list.copy()
        card_list.remove("J")
        card_list.insert(0, "J")

    tie_break = tuple(card_list.index(c) for c in hand)

    if max(counter.values()) == 5:
        ranking = 6
    elif max(counter.values()) == 4:
        ranking = 5
    elif sorted(counter.values()) == [2, 3]:
        ranking = 4
    elif max(counter.values()) == 3:
        ranking = 3
    elif sum(1 for v in counter.values() if v == 2) == 2:
        ranking = 2
    elif max(counter.values()) == 2:
        ranking = 1
    else:
        ranking = 0

    return ranking, tie_break


class Solution(SolutionBase):
    def solve(
        self,
        ranker: Callable[[str, bool], tuple[int, tuple[int, ...]]],
        wild_jacks: bool,
    ) -> int:
        input_ = self.input()
        result = 0
        all = []
        for line in input_:
            cards, bet = line.split()
            all.append((cards, int(bet)))

        all.sort(key=lambda cb: ranker(cb[0], wild_jacks))
        for idx, cb in enumerate(all, start=1):
            result += idx * cb[1]
        return result

    def part1(self) -> int:
        return self.solve(rank, False)

    def part2(self) -> int:
        return self.solve(rank, True)


if __name__ == "__main__":
    Solution(False).run()
