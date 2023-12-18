from __future__ import annotations

import enum
from collections.abc import Iterator
from functools import total_ordering
from typing import TypeVar

T = TypeVar("T")
Coord = tuple[int, int]
Grid = list[list[T]]


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


def move(coord: Coord, direction: Direction) -> Coord:
    x, y = coord
    x_move, y_move = direction.value
    return x + x_move, y + y_move


def in_bounds(coord: Coord, grid: Grid[T]) -> bool:
    height = len(grid)
    width = len(grid[0])
    x, y = coord
    return 0 <= x < width and 0 <= y < height


def surrounding(
    coord: Coord, grid: Grid[T], include_self: bool = False
) -> Iterator[Coord]:
    height = len(grid)
    width = len(grid[0])
    x, y = coord
    for xi in range(max(0, x - 1), min(width, x + 2)):
        for yi in range(max(0, y - 1), min(height, y + 2)):
            if include_self or (xi, yi) != coord:
                yield xi, yi
