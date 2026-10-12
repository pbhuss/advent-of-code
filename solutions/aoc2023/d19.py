from __future__ import annotations

import math
from collections.abc import Iterator
from copy import copy
from dataclasses import dataclass
from dataclasses import field
from enum import StrEnum

from libaoc import SolutionBase


class Category(StrEnum):
    X = "x"
    M = "m"
    A = "a"
    S = "s"


class Operator(StrEnum):
    LESS_THAN = "<"
    GREATER_THAN = ">"


class FinalState(StrEnum):
    ACCEPT = "A"
    REJECT = "R"


@dataclass
class Node:
    name: str
    cat: Category
    op: Operator
    val: int
    success: str
    failure: str = field(init=False)

    def __repr__(self) -> str:
        return f"{self.name} ({self.cat}{self.op}{self.val}) -> [{self.success}, {self.failure}]"


class Bounds:
    def __init__(self) -> None:
        self._bounds = {cat: (1, 4000) for cat in Category}
        self.broken = False

    def constrain(self, node: Node, success: bool) -> Bounds:
        x_min, x_max = self._bounds[node.cat]
        match node.op:
            case ">":
                if success:
                    x_min = max(x_min, node.val + 1)
                else:
                    x_max = min(x_max, node.val)
            case "<":
                if success:
                    x_max = min(x_max, node.val - 1)
                else:
                    x_min = max(x_min, node.val)
        new_ = copy(self)
        new_._bounds[node.cat] = (x_min, x_max)
        if x_min > x_max:
            new_.broken = True
        return new_

    def contains(self, **kwargs: int) -> bool:
        if not set(kwargs) == set(Category):
            raise ValueError(f"Invalid arguments: {kwargs}")
        return not self.broken and all(
            self._bounds[cat][0] <= kwargs[cat] <= self._bounds[cat][1]
            for cat in Category
        )

    def size(self) -> int:
        return math.prod(x_max - x_min + 1 for x_min, x_max in self._bounds.values())

    def __copy__(self) -> Bounds:
        new_ = Bounds()
        new_._bounds = self._bounds.copy()
        new_.broken = self.broken
        return new_


STARTING_NODE = "in"


def all_bounds(
    nodes: dict[str, Node | FinalState], node: Node | FinalState, bounds: Bounds
) -> Iterator[Bounds]:
    if bounds.broken:
        return
    if isinstance(node, FinalState):
        if node == FinalState.ACCEPT:
            yield bounds
        else:
            return
    else:
        yield from all_bounds(nodes, nodes[node.success], bounds.constrain(node, True))
        yield from all_bounds(nodes, nodes[node.failure], bounds.constrain(node, False))


class Solution(SolutionBase):
    def build_dag(self) -> dict[str, Node | FinalState]:
        with open(self.data_file) as fp:
            data = fp.read()

        instructions_str, _ = data.split("\n\n")

        nodes: dict[str, Node | FinalState] = {
            FinalState.ACCEPT.value: FinalState.ACCEPT,
            FinalState.REJECT.value: FinalState.REJECT,
        }

        for instruction in instructions_str.split("\n"):
            name, _, workflow = instruction.partition("{")
            workflow = workflow[:-1]
            *states, final_state = workflow.split(",")
            cur_node = None
            for i, state in enumerate(states):
                check, _, result = state.partition(":")
                if ">" in check:
                    cat, symbol, count = check.partition(">")
                else:
                    cat, symbol, count = check.partition("<")
                if i > 0:
                    assert isinstance(cur_node, Node)
                    name = f"{name}[{i}]"
                    cur_node.failure = name
                cur_node = Node(
                    name, Category(cat), Operator(symbol), int(count), result
                )
                nodes[name] = cur_node
            assert isinstance(cur_node, Node)
            cur_node.failure = final_state
        return nodes

    def part1(self) -> int:
        nodes = self.build_dag()
        bounds = list(all_bounds(nodes, nodes[STARTING_NODE], Bounds()))

        with open(self.data_file) as fp:
            data = fp.read()

        _, parts_str = data.split("\n\n")

        total = 0
        for part in parts_str.strip().split("\n"):
            obj = {}
            part = part[1:-1]
            for entry in part.split(","):
                cat, _, val = entry.partition("=")
                obj[cat] = int(val)
            for bound in bounds:
                if bound.contains(**obj):
                    total += sum(obj.values())
                    break
        return total

    def part2(self) -> int:
        nodes = self.build_dag()
        return sum(
            bound.size() for bound in all_bounds(nodes, nodes[STARTING_NODE], Bounds())
        )


if __name__ == "__main__":
    Solution().run()
