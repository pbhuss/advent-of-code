from enum import StrEnum

from libaoc import SolutionBase


class Square(StrEnum):
    ROUND = "O"
    CUBE = "#"
    EMPTY = "."


Grid = list[list[Square]]


def slide_north(grid: Grid) -> Grid:
    width = len(grid[0])
    height = len(grid)
    for x in range(width):
        y = 0
        while y < height:
            if grid[y][x] == Square.EMPTY:
                for y2 in range(y + 1, height):
                    match grid[y2][x]:
                        case Square.CUBE:
                            break
                        case Square.ROUND:
                            grid[y][x] = Square.ROUND
                            grid[y2][x] = Square.EMPTY
                            break
            y += 1
    return grid


# TODO: repetitive
def slide_west(grid: Grid) -> Grid:
    width = len(grid[0])
    height = len(grid)
    for y in range(height):
        x = 0
        while x < width:
            if grid[y][x] == Square.EMPTY:
                for x2 in range(x + 1, width):
                    match grid[y][x2]:
                        case Square.CUBE:
                            break
                        case Square.ROUND:
                            grid[y][x] = Square.ROUND
                            grid[y][x2] = Square.EMPTY
                            break
            x += 1
    return grid


def slide_south(grid: Grid) -> Grid:
    width = len(grid[0])
    height = len(grid)
    for x in range(width):
        y = height - 1
        while y >= 0:
            if grid[y][x] == Square.EMPTY:
                for y2 in range(y - 1, -1, -1):
                    match grid[y2][x]:
                        case Square.CUBE:
                            break
                        case Square.ROUND:
                            grid[y][x] = Square.ROUND
                            grid[y2][x] = Square.EMPTY
                            break
            y -= 1
    return grid


def slide_east(grid: Grid) -> Grid:
    width = len(grid[0])
    height = len(grid)
    for y in range(height):
        x = width - 1
        while x >= 0:
            if grid[y][x] == Square.EMPTY:
                for x2 in range(x - 1, -1, -1):
                    match grid[y][x2]:
                        case Square.CUBE:
                            break
                        case Square.ROUND:
                            grid[y][x] = Square.ROUND
                            grid[y][x2] = Square.EMPTY
                            break
            x -= 1
    return grid


def cycle(grid: Grid) -> Grid:
    fns = (slide_north, slide_west, slide_south, slide_east)
    for fn in fns:
        grid = fn(grid)
    return grid


def hash_grid(grid: Grid) -> int:
    return hash("".join("".join(square.value for square in row) for row in grid))


def load(grid: Grid) -> int:
    height = len(grid)
    total = 0
    for i, row in enumerate(grid):
        for square in row:
            match square:
                case Square.ROUND:
                    total += height - i
    return total


class Solution(SolutionBase):
    def get_grid(self) -> Grid:
        grid = []
        for line in self.input():
            row = []
            for square in line:
                match square:
                    case "O":
                        row.append(Square.ROUND)
                    case "#":
                        row.append(Square.CUBE)
                    case ".":
                        row.append(Square.EMPTY)
            grid.append(row)
        return grid

    def part1(self) -> int:
        grid = self.get_grid()
        grid = slide_north(grid)
        return load(grid)

    def part2(self) -> int:
        grid = self.get_grid()
        hashes: list[int] = []
        loads = []
        i = 0
        while True:
            grid = cycle(grid)
            h = hash_grid(grid)
            if h in hashes:
                cycle_len = i - hashes.index(h)
                break
            hashes.append(h)
            loads.append(load(grid))
            i += 1
        return loads[-((1_000_000_000 - len(hashes)) % cycle_len)]


if __name__ == "__main__":
    Solution().run()
