import abc
import pathlib
import sys
from collections.abc import Generator

import requests


def get_session_cookie() -> str:
    with open("session.txt") as fp:
        return fp.read().strip()


def get_data_file(year: int, day: int) -> pathlib.Path:
    data_dir = pathlib.Path(f"data/{year}/")
    data_dir.mkdir(parents=True, exist_ok=True)
    data_file = data_dir / f"{day:02d}.txt"
    if not data_file.exists():
        resp = requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input",
            cookies={"session": get_session_cookie()},
            headers={"User-Agent": "https://github.com/pbhuss/advent-of-code"},
        )
        resp.raise_for_status()
        with data_file.open("w") as fp:
            fp.write(resp.text)
    return data_file


class SolutionBase(abc.ABC):
    def __init__(self) -> None:
        script_path = pathlib.Path(sys.modules[self.__module__].__file__)
        *_, year_pt, _ = script_path.parts
        year = int(year_pt)
        day = int(script_path.stem)
        self.data_file = get_data_file(year, day)

    def input(
        self, strip: bool = True, newline: str | None = None
    ) -> Generator[str, None, None]:
        with self.data_file.open(newline=newline) as fp:
            for line in fp:
                if strip:
                    yield line.strip()
                else:
                    yield line

    def run(self) -> None:
        print(f"Part 1: {self.part1()}")
        print(f"Part 2: {self.part2()}")

    @abc.abstractmethod
    def part1(self):
        return ""

    @abc.abstractmethod
    def part2(self):
        return ""
