from __future__ import annotations

from collections import deque
from functools import cached_property

from libaoc import SolutionBase


class Directory:
    def __init__(self, parent: Directory | None) -> None:
        self.directories: dict[str, Directory] = {}
        self.size = 0
        self.parent = parent

    @cached_property
    def full_size(self) -> int:
        return self.size + sum(
            directory.full_size for directory in self.directories.values()
        )

    def sum_below(self, n: int) -> int:
        sub = sum(directory.sum_below(n) for directory in self.directories.values())
        return sub + (0 if self.full_size > n else self.full_size)


class Solution(SolutionBase):
    def get_tree(self) -> Directory:
        root = Directory(None)
        cur_dir = root
        lines = deque(self.input())
        while len(lines) > 0:
            _, cmd, *args = lines.popleft().split(" ")
            if cmd == "ls":
                # in case we `ls` twice in the same directory
                cur_dir.size = 0
                while len(lines) > 0:
                    line = lines.popleft()
                    parts = line.split(" ")
                    if parts[0] == "$":
                        lines.appendleft(line)
                        break
                    if parts[0] != "dir":
                        cur_dir.size += int(parts[0])
            elif cmd == "cd":
                (target,) = args
                if target == "/":
                    cur_dir = root
                elif target == "..":
                    parent_directory = cur_dir.parent
                    assert parent_directory is not None
                    cur_dir = parent_directory
                else:
                    cur_dir = cur_dir.directories.setdefault(target, Directory(cur_dir))
        return root

    def part1(self) -> int:
        return self.get_tree().sum_below(100000)

    def part2(self) -> int:
        total = 70000000
        required = 30000000
        tree = self.get_tree()
        free = total - tree.full_size
        sizes = []

        def add_sizes(directory: Directory) -> None:
            sizes.append(directory.full_size)
            for subdir in directory.directories.values():
                add_sizes(subdir)

        add_sizes(tree)

        for size in sorted(sizes):
            if size + free >= required:
                return size

        raise Exception("unreachable")


if __name__ == "__main__":
    Solution().run()
