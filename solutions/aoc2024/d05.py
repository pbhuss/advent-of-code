from collections import defaultdict
from graphlib import TopologicalSorter

from libaoc import SolutionBase

OrderingDict = dict[str, set[str]]
Book = list[str]


class Solution(SolutionBase):
    def get_input(self) -> tuple[OrderingDict, list[Book]]:
        input_ = self.input()
        orderings: dict[str, set[str]] = defaultdict(set)
        while line := next(input_):
            before, after = line.split("|")
            orderings[before].add(after)

        books = [line.split(",") for line in input_]

        return orderings, books

    def part1(self) -> int:
        orderings, books = self.get_input()

        total = 0

        for book in books:
            seen: set[str] = set()
            valid = True
            for page in book:
                if orderings[page] & seen:
                    valid = False
                    break
                seen.add(page)
            if valid:
                total += int(book[len(book) // 2])

        return total

    def part2(self) -> int:
        orderings, books = self.get_input()

        total = 0

        for book in books:
            seen: set[str] = set()
            valid = True
            for page in book:
                if orderings[page] & seen:
                    valid = False
                    break
                seen.add(page)
            if not valid:
                # Need to filter keys to avoid cycles
                resolved_order = TopologicalSorter(
                    {k: v for k, v in orderings.items() if k in book}
                ).static_order()
                page_to_idx = {page: idx for idx, page in enumerate(resolved_order)}
                book.sort(key=lambda page: page_to_idx[page])
                total += int(book[len(book) // 2])

        return total


if __name__ == "__main__":
    Solution().run()
