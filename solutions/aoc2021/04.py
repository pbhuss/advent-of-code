from collections import defaultdict

from more_itertools import chunked

from libaoc import SolutionBase


def check_board(board_state: list[list[bool]]) -> bool:
    for i in range(5):
        if all(board_state[i][j] for j in range(5)) or all(
            board_state[j][i] for j in range(5)
        ):
            return True
    return False


def sum_unrevealed(board: list[list[int]], board_state: list[list[bool]]) -> int:
    return sum(
        val
        for row, row_state in zip(board, board_state)
        for val, val_state in zip(row, row_state)
        if not val_state
    )


class Solution(SolutionBase):
    def get_boards(
        self,
    ) -> tuple[
        list[int],
        list[list[list[int]]],
        list[list[list[bool]]],
        dict[int, list[tuple[int, int, int]]],
    ]:
        # TODO: fix typing
        input_ = self.input()
        calls = list(map(int, next(input_).split(",")))

        # Skip blank line
        next(input_)

        num_to_pos = defaultdict(list)
        boards = []
        for i, board_lines in enumerate(
            chunked(input_, 6)
        ):  # 5 board lines + 1 separator line
            board = []
            for j, line in enumerate(board_lines[:5]):
                row = []
                for k, num in enumerate(line.split()):
                    num = int(num)
                    num_to_pos[num].append((i, j, k))
                    row.append(num)
                board.append(row)
            boards.append(board)

        board_states = [[[False for _ in range(5)] for _ in range(5)] for _ in boards]

        return calls, boards, board_states, num_to_pos

    def part1(self) -> int:
        calls, boards, board_states, num_to_pos = self.get_boards()

        for call in calls:
            for i, j, k in num_to_pos[call]:
                board_states[i][j][k] = True
            for board, board_state in zip(boards, board_states):
                if check_board(board_state):
                    return call * sum_unrevealed(board, board_state)
        raise Exception("unreachable")

    def part2(self) -> int:
        calls, boards, board_states, num_to_pos = self.get_boards()
        final = False
        final_board: list[list[int]] | None = None
        final_board_state: list[list[bool]] | None = None
        for call in calls:
            for i, j, k in num_to_pos[call]:
                board_states[i][j][k] = True
            if final:
                assert final_board is not None
                assert final_board_state is not None
                if check_board(final_board_state):
                    return call * sum_unrevealed(final_board, final_board_state)
            else:
                unsolved = []
                for board, board_state in zip(boards, board_states):
                    if not check_board(board_state):
                        unsolved.append((board, board_state))
                if len(unsolved) == 1:
                    final = True
                    ((final_board, final_board_state),) = unsolved
        raise Exception("unreachable")


if __name__ == "__main__":
    Solution().run()
