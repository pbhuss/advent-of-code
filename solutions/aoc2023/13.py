from libaoc import SolutionBase


Pattern = list[str]

flip = {"#": ".", ".": "#"}


def rotate_pattern(pattern: Pattern) -> Pattern:
    x = ["".join(line[i] for line in pattern) for i in range(len(pattern[0]))]
    return x


def find_reflections(pattern: Pattern) -> list[int]:
    reflections = []
    pattern_len = len(pattern)
    for split in range(1, pattern_len):
        if all(
            pattern[split - offset - 1] == pattern[split + offset]
            for offset in range(min(split, pattern_len - split))
        ):
            reflections.append(split)
    return reflections


def scores(pattern: Pattern) -> set[int]:
    result = set(map(lambda x: 100 * x, find_reflections(pattern)))
    result.update(find_reflections(rotate_pattern(pattern)))
    return result


def find_flip(pattern: Pattern) -> int:
    old_scores = scores(pattern)
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            old_str = pattern[i]
            pattern[i] = f"{old_str[:j]}{flip[old_str[j]]}{old_str[j + 1:]}"
            new_scores = scores(pattern)
            diff = new_scores - old_scores
            if diff:
                (new_score,) = diff
                return new_score
            pattern[i] = old_str
    raise Exception("unreachable")


class Solution(SolutionBase):
    def get_patterns(self) -> list[Pattern]:
        patterns = []
        pattern: Pattern = []
        for line in self.input():
            if line == "":
                patterns.append(pattern)
                pattern = []
            else:
                pattern.append(line)
        patterns.append(pattern)
        return patterns

    def part1(self) -> int:
        return sum(next(iter(scores(pattern))) for pattern in self.get_patterns())

    def part2(self) -> int:
        return sum(find_flip(pattern) for pattern in self.get_patterns())


if __name__ == "__main__":
    Solution().run()
