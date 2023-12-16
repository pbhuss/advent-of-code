from libaoc import SolutionBase


def hash_value(s: str) -> int:
    result = 0
    for char in s:
        result += ord(char)
        result *= 17
        result %= 256
    return result


class Solution(SolutionBase):
    def part1(self) -> int:
        sequence = next(self.input())
        return sum(hash_value(step) for step in sequence.split(","))

    def part2(self) -> int:
        sequence = next(self.input())
        label_boxes: list[list[str]] = [[] for _ in range(256)]
        lens_boxes: list[list[str]] = [[] for _ in range(256)]
        for step in sequence.split(","):
            label, sign, focal_len = step.partition("=")
            label, _, _ = label.partition("-")
            h = hash_value(label)
            label_box = label_boxes[h]
            lens_box = lens_boxes[h]
            if sign:
                if label in label_box:
                    idx = label_box.index(label)
                    lens_box[idx] = focal_len
                else:
                    label_box.append(label)
                    lens_box.append(focal_len)
            else:
                if label in label_box:
                    idx = label_box.index(label)
                    label_box.pop(idx)
                    lens_box.pop(idx)

        return sum(
            box_num * slot_num * int(focal_len)
            for box_num, lens_box in enumerate(lens_boxes, start=1)
            for slot_num, focal_len in enumerate(lens_box, start=1)
        )


if __name__ == "__main__":
    Solution(False).run()
