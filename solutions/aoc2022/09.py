from typing import NewType

from libaoc import SolutionBase


Coord = NewType("Coord", tuple[int, int])


def get_tail_move(head: Coord, tail: Coord) -> Coord:
    x_diff = head[0] - tail[0]
    y_diff = head[1] - tail[1]
    if abs(x_diff) < 2 and abs(y_diff) < 2:
        return Coord((0, 0))
    return Coord((max(-1, min(1, x_diff)), max(-1, min(1, y_diff))))


def add_coords(*coords: Coord) -> Coord:
    return Coord(tuple(map(sum, zip(*coords))))


class Solution(SolutionBase):
    def solve(self, num_tails: int) -> int:
        head = Coord((0, 0))
        tails = [Coord((0, 0)) for _ in range(num_tails)]
        visited = {tails[-1]}
        moves = {
            "U": Coord((0, -1)),
            "D": Coord((0, 1)),
            "L": Coord((-1, 0)),
            "R": Coord((1, 0)),
        }
        for line in self.input():
            move, distance = line.split()
            head_move = moves[move]
            for _ in range(int(distance)):
                head = add_coords(head, head_move)
                cur_head = head
                for i, tail in enumerate(tails):
                    tail_move = get_tail_move(cur_head, tail)
                    cur_head = tails[i] = add_coords(tail, tail_move)
                visited.add(cur_head)
        return len(visited)

    def part1(self) -> int:
        return self.solve(1)

    def part2(self) -> int:
        return self.solve(9)


if __name__ == "__main__":
    Solution().run()