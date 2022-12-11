import logging
import operator
import re
from collections.abc import Callable
from dataclasses import dataclass

from more_itertools import chunked

from libaoc import SolutionBase


logging.basicConfig(level=logging.ERROR, format="%(message)s")
logger = logging.getLogger(__name__)


@dataclass
class Monkey:

    items: list[int]
    op: Callable[[int, int], int]
    op_right: str
    divisor: int
    true_idx: int
    false_idx: int
    inspect_count: int = 0

    def update(self, item: int, divide: bool, modulo: int = 0) -> int:
        if self.op_right == "old":
            val = self.op(item, item)
        else:
            val = self.op(item, int(self.op_right))
        if divide:
            val //= 3
        else:
            val %= modulo
        return val


class Solution(SolutionBase):
    def solve(self, num_rounds: int, divide: bool) -> int:
        monkeys = []
        num_pattern = re.compile(r"\d+")
        operation_re = re.compile(r"([+*]) (old|[0-9]+)")
        for lines in chunked(self.input(), 7):
            items = list(map(int, num_pattern.findall(lines[1])))
            op_str, op_right = operation_re.search(lines[2]).groups((2, 3))
            op = operator.add if op_str == "+" else operator.mul

            divisor, true_idx, false_idx = map(
                int, (num_pattern.search(line).group(0) for line in lines[3:6])
            )
            monkeys.append(
                Monkey(
                    items=items,
                    op=op,
                    op_right=op_right,
                    divisor=divisor,
                    true_idx=true_idx,
                    false_idx=false_idx,
                )
            )

        modulo = 1
        for monkey in monkeys:
            modulo *= monkey.divisor

        for round in range(num_rounds):
            for i, monkey in enumerate(monkeys):
                logging.info(f"Monkey {i}")
                monkey.inspect_count += len(monkey.items)
                for item in monkey.items:
                    logging.info(
                        f"  Monkey inspects an item with a worry value of {item}."
                    )
                    item = monkey.update(item, divide, modulo)
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
                monkey.items = []

        for i, monkey in enumerate(monkeys):
            logging.info(f"Monkey {i} inspected items {monkey.inspect_count} times.")

        top_counts = sorted(monkey.inspect_count for monkey in monkeys)[-2:]
        return top_counts[0] * top_counts[1]

    def part1(self):
        return self.solve(num_rounds=20, divide=True)

    def part2(self):
        return self.solve(num_rounds=10000, divide=False)


if __name__ == "__main__":
    Solution().run()
