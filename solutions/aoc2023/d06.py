from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        input_ = self.input()
        times = list(map(int, next(input_).split(":")[1].split()))
        distances = list(map(int, next(input_).split(":")[1].split()))
        product = 1
        for time, distance in zip(times, distances):
            total = 0
            for i in range(time):
                if i * (time - i) > distance:
                    total += 1
            product *= total
        return product

    def part2(self) -> int:
        input_ = self.input()
        time = int("".join(next(input_).split(":")[1].split()))
        distance = int("".join(next(input_).split(":")[1].split()))
        total = 0
        for i in range(time):
            if i * (time - i) > distance:
                total += 1
        return total


if __name__ == "__main__":
    Solution(False).run()
