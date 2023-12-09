import math
import re
from itertools import cycle

from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        input_ = self.input()
        order = next(input_)
        next(input_)
        result = 0
        pattern = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")
        graph = {}
        for line in input_:
            match = pattern.match(line)
            assert match is not None
            a, b, c = match.groups()
            graph[a] = (b, c)

        cur = "AAA"
        for step in cycle(order):
            if step == "L":
                cur = graph[cur][0]
            else:
                cur = graph[cur][1]
            result += 1
            if cur == "ZZZ":
                return result
        raise Exception("not reachable")

    def part2(self) -> int:
        input_ = self.input()
        order = next(input_)
        next(input_)
        pattern = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")
        graph = {}
        for line in input_:
            match = pattern.match(line)
            assert match is not None
            a, b, c = match.groups()
            graph[a] = (b, c)

        curs = tuple(x for x in graph if x[-1] == "A")
        scores = []
        for cur in curs:
            result = 0
            for step in cycle(order):
                if step == "L":
                    cur = graph[cur][0]
                else:
                    cur = graph[cur][1]
                result += 1
                if cur[-1] == "Z":
                    scores.append(result)
                    break
        return math.lcm(*scores)


if __name__ == "__main__":
    Solution(False).run()
