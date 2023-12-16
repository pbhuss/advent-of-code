import enum
from itertools import chain

from libaoc import SolutionBase


Coord = tuple[int, int]
Grid = list[list[str]]


class Direction(enum.Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


def move(coord: Coord, direction: Direction) -> Coord:
    x, y = coord
    x_move, y_move = direction.value
    return x + x_move, y + y_move


def in_bounds(coord: Coord, width: int, height: int) -> bool:
    x, y = coord
    if not 0 <= x < width:
        return False
    if not 0 <= y < height:
        return False
    return True


class Solution(SolutionBase):
    def get_grid(self) -> Grid:
        return [[pos for pos in line] for line in self.input()]

    def solve(self, grid: Grid, start: Coord, start_direction: Direction) -> int:
        energized = [[False for _ in row] for row in grid]
        height = len(grid)
        width = len(grid[0])
        seen = set()

        def beam(pos: Coord, direction: Direction) -> None:
            while in_bounds(pos, width, height):
                val = (pos, direction)
                if val in seen:
                    return
                seen.add(val)
                cur_x, cur_y = pos
                energized[cur_y][cur_x] = True
                match grid[cur_y][cur_x]:
                    case ".":
                        pass
                    case "-":
                        if direction in {Direction.NORTH, Direction.SOUTH}:
                            direction = Direction.EAST
                            beam(move(pos, Direction.WEST), Direction.WEST)
                    case "|":
                        if direction in {Direction.EAST, Direction.WEST}:
                            direction = Direction.NORTH
                            beam(move(pos, Direction.SOUTH), Direction.SOUTH)
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
                pos = move(pos, direction)

        beam(start, start_direction)
        return sum(sum(row) for row in energized)

    def part1(self) -> int:
        grid = self.get_grid()
        return self.solve(grid, (0, 0), Direction.EAST)

    def part2(self) -> int:
        grid = self.get_grid()
        height = len(grid)
        width = len(grid[0])
        south = [((x, 0), Direction.SOUTH) for x in range(width)]
        north = [((x, height - 1), Direction.NORTH) for x in range(width)]
        east = [((0, y), Direction.EAST) for y in range(height)]
        west = [((width - 1, y), Direction.WEST) for y in range(height)]
        return max(
            self.solve(grid, coord, direction)
            for coord, direction in chain(north, south, east, west)
        )


if __name__ == "__main__":
    Solution().run()
