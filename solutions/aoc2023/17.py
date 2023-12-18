from __future__ import annotations

import heapq
from collections.abc import Callable
from collections.abc import Iterable
from dataclasses import dataclass

from libaoc import SolutionBase
from libaoc.grid import Coord
from libaoc.grid import Direction
from libaoc.grid import Grid
from libaoc.grid import in_bounds
from libaoc.grid import move


@dataclass(frozen=True, order=True)
class State:
    x: int
    y: int
    direction: Direction
    count: int

    def move(self, direction: Direction) -> State:
        new_x, new_y = move((self.x, self.y), direction)
        if direction == self.direction:
            new_count = self.count + 1
        else:
            new_count = 1
        return State(new_x, new_y, direction, new_count)

    @property
    def coord(self) -> Coord:
        return (self.x, self.y)


AdjacencyFn = Callable[[Grid[int], State], Iterable[State]]


def adjacent_part1(grid: Grid[int], state: State) -> tuple[State, ...]:
    return tuple(
        filter(
            lambda new_state: in_bounds(new_state.coord, grid) and new_state.count <= 3,
            (
                state.move(direction)
                for direction in (state.direction,) + state.direction.adjacent
            ),
        )
    )


def adjacent_part2(grid: Grid[int], state: State) -> tuple[State, ...]:
    if state.count == 0:
        valid_directions = tuple(Direction)
    elif state.count < 4:
        valid_directions = (state.direction,)
    elif state.count < 10:
        valid_directions = (state.direction,) + state.direction.adjacent
    else:
        valid_directions = state.direction.adjacent
    return tuple(
        filter(
            lambda new_state: in_bounds(new_state.coord, grid),
            (state.move(direction) for direction in valid_directions),
        )
    )


def dijkstra(
    grid: Grid[int],
    start_state: State,
    adjacency_fn: AdjacencyFn,
    min_stop: int,
    verbose: bool = False,
) -> int:
    costs = {start_state: 0}

    from_map = {}

    pq = [(0, start_state)]
    while len(pq) > 0:
        cur_cost, cur_state = heapq.heappop(pq)
        if cur_cost > costs[cur_state]:
            continue
        for neighbor in adjacency_fn(grid, cur_state):
            cost = cur_cost + grid[neighbor.y][neighbor.x]
            if neighbor not in costs or cost < costs[neighbor]:
                from_map[neighbor] = cur_state
                costs[neighbor] = cost
                heapq.heappush(pq, (cost, neighbor))

    height = len(grid)
    width = len(grid[0])

    min_cost, r = min(
        (cost, state)
        for state, cost in costs.items()
        if state.x == width - 1 and state.y == height - 1 and state.count >= min_stop
    )

    if verbose:
        path = [r]
        while r != start_state:
            r = from_map[r]
            path.append(r)
        path.reverse()
        for p in path:
            print(p, costs[p])
    return min_cost


class Solution(SolutionBase):
    def __init__(self, verbose: bool = False, example: bool = False) -> None:
        super().__init__(example=example)
        self.verbose = verbose

    def get_grid(self) -> Grid[int]:
        return [[int(v) for v in row] for row in self.input()]

    def solve(self, adjacency_fn: AdjacencyFn, min_stop: int) -> int:
        grid = self.get_grid()
        initial_state = State(0, 0, Direction.SOUTH, 0)
        return dijkstra(
            grid, initial_state, adjacency_fn, min_stop, verbose=self.verbose
        )

    def part1(self) -> int:
        return self.solve(adjacent_part1, 0)

    def part2(self) -> int:
        return self.solve(adjacent_part2, 4)


if __name__ == "__main__":
    Solution(verbose=False, example=False).run()
