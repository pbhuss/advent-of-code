import logging
import math
import operator
import re
from collections.abc import Callable
from functools import partial
from itertools import batched
from typing import NamedTuple

from libaoc import SolutionBase

logging.basicConfig(level=logging.ERROR, format="%(message)s")
logger = logging.getLogger(__name__)


class Monkey(NamedTuple):
    items: list[int]
    operation: Callable[[int], int]
    divisor: int
    true_idx: int
    false_idx: int


def square(x: int) -> int:
    return x**2


def must_search(pattern: re.Pattern[str], text: str) -> re.Match[str]:
    match = pattern.search(text)
    assert match is not None
    return match


class Solution(SolutionBase):
    def solve(self, num_rounds: int, divide: bool) -> int:
        monkeys = []
        num_pattern = re.compile(r"\d+")
        operation_re = re.compile(r"([+*]) (old|[0-9]+)")
        for lines in batched(self.input(), 7):
            items = list(map(int, num_pattern.findall(lines[1])))
            operation_match = operation_re.search(lines[2])
            assert operation_match is not None
            op_str, op_right = operation_match.groups((2, 3))
            op = operator.add if op_str == "+" else operator.mul
            if op_right == "old":
                operation = square
            else:
                assert isinstance(op_right, str)
                operation = partial(op, int(op_right))
            divisor, true_idx, false_idx = map(
                int, (must_search(num_pattern, line).group(0) for line in lines[3:6])
            )
            monkeys.append(
                Monkey(
                    items=items,
                    operation=operation,
                    divisor=divisor,
                    true_idx=true_idx,
                    false_idx=false_idx,
                )
            )

        modulo = math.prod(monkey.divisor for monkey in monkeys)
        inspect_counts = [0 for _ in monkeys]

        for _ in range(num_rounds):
            for i, monkey in enumerate(monkeys):
                logging.info(f"Monkey {i}")
                inspect_counts[i] += len(monkey.items)
                for item in monkey.items:
                    logging.info(
                        f"  Monkey inspects an item with a worry value of {item}."
                    )
                    item = monkey.operation(item)
                    if divide:
                        item //= 3
                    else:
                        item %= modulo
                    logging.info(f"    Worry level is modified to {item}.")
                    if item % monkey.divisor == 0:
                        logging.info(
                            f"    Current worry is divisible by {monkey.divisor}."
                        )
                        logging.info(
                            f"    Item with worry level {item} is thrown to monkey {monkey.true_idx}."
                        )
                        monkeys[monkey.true_idx].items.append(item)
                    else:
                        logging.info(
                            f"    Current worry is not divisible by {monkey.divisor}."
                        )
                        logging.info(
                            f"    Item with worry level {item} is thrown to monkey {monkey.false_idx}."
                        )
                        monkeys[monkey.false_idx].items.append(item)
                monkey.items.clear()

        for i, inspect_count in enumerate(inspect_counts):
            logging.info(f"Monkey {i} inspected items {inspect_count} times.")

        inspect_counts.sort()
        return inspect_counts[-1] * inspect_counts[-2]

    def part1(self) -> int:
        return self.solve(num_rounds=20, divide=True)

    def part2(self) -> int:
        return self.solve(num_rounds=10000, divide=False)


if __name__ == "__main__":
    Solution().run()
