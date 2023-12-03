import re

from tqdm import trange

from libaoc import SolutionBase


def must_match(pattern: re.Pattern[str], text: str) -> re.Match[str]:
    match = pattern.match(text)
    assert match is not None
    return match


class Solution(SolutionBase):
    def part1(self, y_check: int = 2000000) -> int:
        pattern = re.compile(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
        )
        x_no_beacon = set()
        x_beacon = set()

        for line in self.input():
            sensor_x, sensor_y, beacon_x, beacon_y = map(
                int, must_match(pattern, line).group(1, 2, 3, 4)
            )
            if beacon_y == y_check:
                x_beacon.add(beacon_x)
            beacon_dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            diff = beacon_dist - abs(sensor_y - y_check)
            for xi in range(sensor_x - diff, sensor_x + diff + 1):
                x_no_beacon.add(xi)

        return len(x_no_beacon - x_beacon)

    def part2(self, max_pos: int = 4000000) -> int:
        pattern = re.compile(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
        )
        min_pos = 0
        sensors = []
        for line in self.input():
            sensor_x, sensor_y, beacon_x, beacon_y = map(
                int, must_match(pattern, line).group(1, 2, 3, 4)
            )
            beacon_dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            sensors.append(((sensor_x, sensor_y), beacon_dist))

        for xi in trange(min_pos, max_pos + 1):
            yi = min_pos
            while yi <= max_pos:
                covered = False
                for (sensor_x, sensor_y), beacon_dist in sensors:
                    dist = abs(xi - sensor_x) + abs(yi - sensor_y)
                    if dist <= beacon_dist:
                        covered = True
                        yi += beacon_dist - dist
                        break
                if not covered:
                    return xi * max_pos + yi
                yi += 1
        raise Exception("unreachable")


if __name__ == "__main__":
    Solution().run()
