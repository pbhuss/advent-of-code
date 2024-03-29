from itertools import chain

from libaoc import SolutionBase
from libaoc.grid import Coord
from libaoc.grid import Direction
from libaoc.grid import Grid
from libaoc.grid import in_bounds
from libaoc.grid import move


def score(grid: Grid[str], start: Coord, start_direction: Direction) -> int:
    energized = [[False for _ in row] for row in grid]
    seen = set()
    q = [(start, start_direction)]
    while q:
        val = (pos, direction) = q.pop()
        if not in_bounds(pos, grid) or val in seen:
            continue
        seen.add(val)
        x, y = pos
        energized[y][x] = True
        match grid[y][x]:
            case ".":
                pass
            case "-":
                if direction in {Direction.NORTH, Direction.SOUTH}:
                    direction = Direction.EAST
                    q.append((move(pos, Direction.WEST), Direction.WEST))
            case "|":
                if direction in {Direction.EAST, Direction.WEST}:
                    direction = Direction.NORTH
                    q.append((move(pos, Direction.SOUTH), Direction.SOUTH))
            case "/":
                match direction:
                    case Direction.NORTH:
                        direction = Direction.EAST
                    case Direction.EAST:
                        direction = Direction.NORTH
                    case Direction.WEST:
                        direction = Direction.SOUTH
                    case Direction.SOUTH:
                        direction = Direction.WEST
            case "\\":
                match direction:
                    case Direction.NORTH:
                        direction = Direction.WEST
                    case Direction.WEST:
                        direction = Direction.NORTH
                    case Direction.EAST:
                        direction = Direction.SOUTH
                    case Direction.SOUTH:
                        direction = Direction.EAST
        q.append((move(pos, direction), direction))

    return sum(sum(row) for row in energized)


class Solution(SolutionBase):
    def get_grid(self) -> Grid[str]:
        return [[pos for pos in line] for line in self.input()]

    def part1(self) -> int:
        grid = self.get_grid()
        return score(grid, (0, 0), Direction.EAST)

    def part2(self) -> int:
        grid = self.get_grid()
        height = len(grid)
        width = len(grid[0])
        south = (((x, 0), Direction.SOUTH) for x in range(width))
        north = (((x, height - 1), Direction.NORTH) for x in range(width))
        east = (((0, y), Direction.EAST) for y in range(height))
        west = (((width - 1, y), Direction.WEST) for y in range(height))
        return max(
            score(grid, coord, direction)
            for coord, direction in chain(north, south, east, west)
        )


if __name__ == "__main__":
    Solution().run()
