import pkgutil
import re
from importlib import import_module
from types import ModuleType

import pytest

import solutions


def load_solution_modules() -> dict[str, ModuleType]:
    module_map = {}
    pattern = re.compile(r"(\d{4})\.(\d{2})")
    for _, modname, is_pkg in pkgutil.walk_packages(
        solutions.__path__, f"{solutions.__name__}."
    ):
        if is_pkg:
            continue
        match = pattern.search(modname)
        if match is None:
            raise Exception(f"invalid module {modname}")
        problem = f"{match.group(1)}-{match.group(2)}"
        module_map[problem] = import_module(modname)
    return module_map


def pytest_addoption(parser: pytest.Parser) -> None:
    solution_modules = load_solution_modules()
    parser.addoption(
        "--solutions",
        action="store",
        nargs="*",
        choices=solution_modules,
        default=solution_modules,
        help="solution numbers to test (default: all)",
    )


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    metafunc.parametrize("problem", metafunc.config.option.solutions)


@pytest.fixture(scope="session")
def solution_modules() -> dict[str, ModuleType]:
    return load_solution_modules()
