from libaoc import SolutionBase


def draw_grid(source, walls, filled):
    min_x = min(x for x, _ in filled)
    max_x = max(x for x, _ in filled)
    max_y = max(y for _, y in filled)

    for y in range(max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            if (x, y) == source:
                char = "+"
            elif (x, y) in walls:
                char = "#"
            elif (x, y) in filled:
                char = "o"
            else:
                char = "."
            line.append(char)
        print("".join(line))
    print()


class Solution(SolutionBase):
    def part1(self, draw=False):
        walls = set()
        for line in self.input():
            points = line.split(" -> ")
            prev_x, prev_y = map(int, points[0].split(","))
            for cur_point in points[1:]:
                cur_x, cur_y = map(int, cur_point.split(","))
                if prev_x == cur_x:
                    for yi in range(min(prev_y, cur_y), max(prev_y, cur_y) + 1):
                        walls.add((cur_x, yi))
                else:
                    for xi in range(min(prev_x, cur_x), max(prev_x, cur_x) + 1):
                        walls.add((xi, cur_y))
                prev_x, prev_y = cur_x, cur_y

        source = (500, 0)
        count = 0
        max_y = max(y for _, y in walls)
        filled = walls.copy()

        if draw:
            draw_grid(source, walls, filled)

        while True:
            x, y = source
            while True:
                if (x, y + 1) not in filled:
                    y += 1
                elif (x - 1, y + 1) not in filled:
                    x -= 1
                    y += 1
                elif (x + 1, y + 1) not in filled:
                    x += 1
                    y += 1
                else:
                    filled.add((x, y))
                    count += 1
                    break

                if y > max_y:
                    if draw:
                        draw_grid(source, walls, filled)
                    return count

    def part2(self, draw=False):
        walls = set()
        for line in self.input():
            points = line.split(" -> ")
            prev_x, prev_y = map(int, points[0].split(","))
            for cur_point in points[1:]:
                cur_x, cur_y = map(int, cur_point.split(","))
                if prev_x == cur_x:
                    for yi in range(min(prev_y, cur_y), max(prev_y, cur_y) + 1):
                        walls.add((cur_x, yi))
                else:
                    for xi in range(min(prev_x, cur_x), max(prev_x, cur_x) + 1):
                        walls.add((xi, cur_y))
                prev_x, prev_y = cur_x, cur_y

        source = (500, 0)
        count = 0
        max_y = max(y for _, y in walls)
        for xi in range(500 - max_y - 10, 500 + max_y + 10):  # good enough
            walls.add((xi, max_y + 2))
        filled = walls.copy()

        if draw:
            draw_grid(source, walls, filled)

        while True:
            x, y = source
            while True:
                if (x, y + 1) not in filled:
                    y += 1
                elif (x - 1, y + 1) not in filled:
                    x -= 1
                    y += 1
                elif (x + 1, y + 1) not in filled:
                    x += 1
                    y += 1
                else:
                    filled.add((x, y))
                    count += 1
                    if (x, y) == source:
                        if draw:
                            draw_grid(source, walls, filled)
                        return count
                    break


if __name__ == "__main__":
    Solution().run()
