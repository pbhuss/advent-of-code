from itertools import pairwise

import networkx as nx

from libaoc import SolutionBase


EDGES = {
    "|": ((0, -1), (0, 1)),
    "-": ((-1, 0), (1, 0)),
    "L": ((0, -1), (1, 0)),
    "J": ((0, -1), (-1, 0)),
    "7": ((0, 1), (-1, 0)),
    "F": ((0, 1), (1, 0)),
    ".": (),
    "S": ((1, 0), (-1, 0), (0, -1), (0, 1)),
}

Coord = tuple[int, int]


def expand(x: int, y: int) -> Coord:
    return (2 * x + 1, 2 * y + 1)


class Solution(SolutionBase):
    def build_graph(self) -> tuple[nx.Graph, Coord]:
        g = nx.Graph()
        partial_edges: set[tuple[Coord, Coord]] = set()
        for y, line in enumerate(self.input()):
            for x, char in enumerate(line):
                g.add_node((x, y))
                if char == "S":
                    start = (x, y)
                for offset in EDGES[char]:
                    u = (x, y)
                    v = (x + offset[0], y + offset[1])
                    u, v = sorted((u, v))
                    edge = (u, v)
                    if edge in partial_edges:
                        partial_edges.remove(edge)
                        g.add_edge(u, v)
                    else:
                        partial_edges.add(edge)
        return g, start

    def part1(self) -> int:
        g, start = self.build_graph()

        dest, _ = g[start]
        g.remove_edge(start, dest)
        path = nx.shortest_path(g, start, dest)

        return len(path) // 2

    def part2(self, verbose: bool = False) -> int:
        g, start = self.build_graph()
        dest, _ = g[start]
        g.remove_edge(start, dest)
        path = [*nx.shortest_path(g, start, dest), start]
        new_path = set()
        for (x1, y1), (x2, y2) in pairwise(path):
            new_path.add(expand(x1, y1))
            mx, my = expand(min(x1, x2), min(y1, y2))
            if x1 == x2:
                new_path.add((mx, my + 1))
            else:
                new_path.add((mx + 1, my))
        new_path = set(new_path)
        max_x, max_y = max(g.nodes)
        width, height = expand(max_x + 1, max_y + 1)
        new_g = nx.Graph()
        for x in range(width):
            for y in range(height):
                u = (x, y)
                if u not in new_path:
                    for offset in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                        v = (x + offset[0], y + offset[1])
                        if v not in new_path:
                            new_g.add_edge(u, v)
        connected = nx.node_connected_component(new_g, (0, 0))
        total = 0
        for x in range(width):
            for y in range(height):
                if (x, y) in new_path:
                    if verbose:
                        print("o", end="")
                elif (x, y) in connected:
                    if verbose:
                        print(".", end="")
                else:
                    if verbose:
                        print("*", end="")
                    if x % 2 == 1 and y % 2 == 1:
                        total += 1
            if verbose:
                print()
        return total


if __name__ == "__main__":
    Solution(False).run()
