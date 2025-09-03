from __future__ import annotations

import enum
from collections.abc import Iterator
from functools import total_ordering
from typing import TypeVar

T = TypeVar("T")

type Coord = tuple[int, int]
type Grid[T] = list[list[T]]


@total_ordering
class Direction(enum.Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTHWEST = (-1, -1)
    NORTHEAST = (1, -1)
    SOUTHWEST = (-1, 1)
    SOUTHEAST = (1, 1)

    @property
    def opposite(self) -> Direction:
        x, y = self.value
        return Direction((-x, -y))

    @property
    def orthogonal(self) -> tuple[Direction, Direction]:
        x, y = self.value
        if x == 0:
            return Direction((1, 0)), Direction((-1, 0))
        elif y == 0:
            return Direction((0, 1)), Direction((0, -1))
        else:
            return Direction((x, -y)), Direction((-x, y))

    def __lt__(self, other: Direction) -> bool:
        return self.value < other.value

    @classmethod
    def cardinal(cls) -> set[Direction]:
        return {cls.NORTH, cls.SOUTH, cls.EAST, cls.WEST}


def move(coord: Coord, direction: Direction, n: int = 1) -> Coord:
    x, y = coord
    x_move, y_move = direction.value
    return x + x_move * n, y + y_move * n


def move_get[T](grid: Grid[T], coord: Coord, direction: Direction, n: int = 1) -> T:
    x, y = move(coord, direction, n)
    return grid[y][x]


def in_bounds[T](coord: Coord, grid: Grid[T]) -> bool:
    height = len(grid)
    width = len(grid[0])
    x, y = coord
    return 0 <= x < width and 0 <= y < height


def surrounding[T](
    coord: Coord, grid: Grid[T], include_self: bool = False
) -> Iterator[Coord]:
    height = len(grid)
    width = len(grid[0])
    x, y = coord
    for xi in range(max(0, x - 1), min(width, x + 2)):
        for yi in range(max(0, y - 1), min(height, y + 2)):
            if include_self or (xi, yi) != coord:
                yield xi, yi


def line[T](grid: Grid[T], start: Coord, direction: Direction, length: int) -> list[T]:
    if not in_bounds(start, grid):
        raise ValueError("Start of line is not in bounds")
    end = move(start, direction, length - 1)
    if not in_bounds(end, grid):
        raise ValueError("End of line is not in bounds")
    result = []
    cur = x, y = start
    for i in range(length):
        result.append(grid[y][x])
        cur = x, y = move(cur, direction)
    return result
