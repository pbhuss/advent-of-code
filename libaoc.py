import abc
import pathlib
import sys
from collections.abc import Generator

import urllib3


def get_session_cookie() -> str:
    with open("session.txt") as fp:
        return fp.read().strip()


def get_data_file(year: int, day: int) -> pathlib.Path:
    data_dir = pathlib.Path(f"data/{year}/")
    data_dir.mkdir(parents=True, exist_ok=True)
    data_file = data_dir / f"{day:02d}.txt"
    if not data_file.exists():
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        resp = urllib3.request(
            method="GET",
            url=url,
            headers={
                "User-Agent": "https://github.com/pbhuss/advent-of-code",
                "Cookie": f"session={get_session_cookie()}",
            },
        )
        if 400 <= resp.status < 600:
            raise Exception(f"{url} returned {resp.status}: {resp.reason}")
        with data_file.open("wb") as fp:
            fp.write(resp.data)
    return data_file


class SolutionBase(abc.ABC):
    def __init__(self, example: bool = False) -> None:
        script_file = sys.modules[self.__module__].__file__
        assert script_file is not None
        script_path = pathlib.Path(script_file)
        *_, year_pt, _ = script_path.parts
        year = int(year_pt.lstrip("aoc"))
        day = int(script_path.stem)
        if example:
            self.data_file = pathlib.Path(f"example_data/{year}/{day:02d}.txt")
        else:
            self.data_file = get_data_file(year, day)

    def input(self, strip: bool = True) -> Generator[str, None, None]:
        with self.data_file.open() as fp:
            for line in fp:
                if strip:
                    yield line.rstrip("\n")
                else:
                    yield line

    def run(self) -> None:
        print(f"Part 1: \n{self.part1()}")
        print()
        print(f"Part 2: \n{self.part2()}")

    @abc.abstractmethod
    def part1(self) -> int | str:
        return ""

    @abc.abstractmethod
    def part2(self) -> int | str:
        return ""
