from __future__ import annotations

import enum
import heapq
from collections.abc import Callable
from collections.abc import Iterable
from dataclasses import dataclass
from functools import total_ordering

from libaoc import SolutionBase


Grid = list[list[int]]


@total_ordering
class Direction(enum.Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    @property
    def opposite(self) -> Direction:
        match self:
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.WEST:
                return Direction.EAST

    @property
    def adjacent(self) -> tuple[Direction, Direction]:
        a1, a2 = set(Direction) - {self, self.opposite}
        return a1, a2

    def __lt__(self, other: Direction) -> bool:
        return self.value < other.value


@dataclass(frozen=True, order=True)
class State:
    x: int
    y: int
    direction: Direction
    count: int

    def move(self, direction: Direction) -> State:
        x_offset, y_offset = direction.value
        new_x = self.x + x_offset
        new_y = self.y + y_offset
        if direction == self.direction:
            new_count = self.count + 1
        else:
            new_count = 1
        return State(new_x, new_y, direction, new_count)


def in_bounds(grid: Grid, state: State) -> bool:
    height = len(grid)
    width = len(grid[0])
    return 0 <= state.x < width and 0 <= state.y < height


AdjacencyFn = Callable[[Grid, State], Iterable[State]]


def adjacent_part1(grid: Grid, state: State) -> tuple[State, ...]:
    return tuple(
        filter(
            lambda new_state: in_bounds(grid, new_state) and new_state.count <= 3,
            (
                state.move(direction)
                for direction in (state.direction,) + state.direction.adjacent
            ),
        )
    )


def adjacent_part2(grid: Grid, state: State) -> tuple[State, ...]:
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
            lambda new_state: in_bounds(grid, new_state),
            (state.move(direction) for direction in valid_directions),
        )
    )


def dijkstra(
    grid: Grid,
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

    def get_grid(self) -> Grid:
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
