from libaoc import SolutionBase


class Solution(SolutionBase):
    def part1(self):
        match_score = {
            ("A", "X"): 3,
            ("A", "Y"): 6,
            ("A", "Z"): 0,
            ("B", "X"): 0,
            ("B", "Y"): 3,
            ("B", "Z"): 6,
            ("C", "X"): 6,
            ("C", "Y"): 0,
            ("C", "Z"): 3,
        }

        play_score = {
            "X": 1,
            "Y": 2,
            "Z": 3,
        }

        score = 0

        for row in self.input():
            a, b = row.strip().split(" ")
            score += match_score[(a, b)]
            score += play_score[b]

        return score

    def part2(self):
        play_score = {
            ("A", "X"): 3,
            ("A", "Y"): 1,
            ("A", "Z"): 2,
            ("B", "X"): 1,
            ("B", "Y"): 2,
            ("B", "Z"): 3,
            ("C", "X"): 2,
            ("C", "Y"): 3,
            ("C", "Z"): 1,
        }

        match_score = {
            "X": 0,
            "Y": 3,
            "Z": 6,
        }

        score = 0

        for row in self.input():
            a, b = row.strip().split(" ")
            score += play_score[(a, b)]
            score += match_score[b]

        return score


if __name__ == "__main__":
    Solution().run()
