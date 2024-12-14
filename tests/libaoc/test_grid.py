import pytest

from libaoc.grid import Direction


@pytest.mark.parametrize(
    ("direction", "expected"),
    [
        (Direction.NORTH, (Direction.WEST, Direction.EAST)),
        (Direction.SOUTH, (Direction.WEST, Direction.EAST)),
        (Direction.EAST, (Direction.NORTH, Direction.SOUTH)),
        (Direction.WEST, (Direction.NORTH, Direction.SOUTH)),
    ],
)
def test_direction_adjacent(direction: Direction, expected: tuple[Direction]) -> None:
    assert sorted(direction.orthogonal) == sorted(expected)
