import math
import re
from queue import PriorityQueue
from typing import NamedTuple

from libaoc import SolutionBase


class State(NamedTuple):

    current_position: str
    time_remaining: int
    valves_closed: frozenset[str]


class TwoState(NamedTuple):

    current_positions: frozenset[str]
    time_remaining: int
    valves_closed: frozenset[str]


def heuristic(state: State, valve_to_rate: dict[str, int]) -> int:
    total = 0
    for i, valve in enumerate(
        sorted(state.valves_closed, key=lambda k: valve_to_rate[k], reverse=True),
        start=1,
    ):
        total += (2 * i - 1) * valve_to_rate[valve]
    return total


def heuristic_two(state: TwoState, valve_to_rate: dict[str, int]) -> int:
    total = 0
    for i, valve in enumerate(
        sorted(state.valves_closed, key=lambda k: valve_to_rate[k], reverse=True)
    ):
        total += (2 * (i // 2) + 1) * valve_to_rate[valve]
    return total


class Solution(SolutionBase):
    def part1(self):
        valve_pattern = re.compile(r"[A-Z]{2}")
        rate_pattern = re.compile(r"\d+")
        valve_to_rate = {}
        valve_to_adjacents = {}

        for line in self.input():
            valve, *adj_valves = valve_pattern.findall(line)
            flow_rate = int(rate_pattern.search(line).group(0))
            if flow_rate > 0:
                valve_to_rate[valve] = flow_rate
            valve_to_adjacents[valve] = set(adj_valves)

        starting_state = State("AA", 30, frozenset(valve_to_rate))

        # A* Search
        open_set = PriorityQueue()
        came_from = {}
        g_score = {starting_state: 0}
        f_score = {starting_state: heuristic(starting_state, valve_to_rate)}
        open_set.put((f_score[starting_state], starting_state))

        while not open_set.empty():
            cur_score: int
            cur_state: State
            cur_score, cur_state = open_set.get()

            if not cur_state.valves_closed or cur_state.time_remaining == 0:
                pressure_released = 0
                path = [cur_state]
                while cur_state in came_from:
                    cur_state = came_from[cur_state]
                    path.append(cur_state)
                path.reverse()
                cur_closed = path[0].valves_closed
                for state in path[1:]:
                    opened = cur_closed - state.valves_closed
                    if opened:
                        cur_closed = state.valves_closed
                        pressure_released += (
                            valve_to_rate[next(iter(opened))] * state.time_remaining
                        )
                return pressure_released

            new_states = []

            if cur_state.current_position in cur_state.valves_closed:
                new_states.append(
                    State(
                        cur_state.current_position,
                        cur_state.time_remaining - 1,
                        frozenset(
                            cur_state.valves_closed - {cur_state.current_position}
                        ),
                    )
                )
            for adj_valve in valve_to_adjacents[cur_state.current_position]:
                new_states.append(
                    State(
                        adj_valve,
                        cur_state.time_remaining - 1,
                        cur_state.valves_closed,
                    )
                )

            for new_state in new_states:
                tentative_g_score = g_score[cur_state] + sum(
                    valve_to_rate[v] for v in cur_state.valves_closed
                )
                if tentative_g_score < g_score.get(new_state, math.inf):
                    came_from[new_state] = cur_state
                    g_score[new_state] = tentative_g_score
                    f_score[new_state] = tentative_g_score + heuristic(
                        new_state, valve_to_rate
                    )
                    open_set.put((f_score[new_state], new_state))
        raise Exception("unreachable")

    def part2(self):
        valve_pattern = re.compile(r"[A-Z]{2}")
        rate_pattern = re.compile(r"\d+")
        valve_to_rate = {}
        valve_to_adjacents = {}

        for line in self.input():
            valve, *adj_valves = valve_pattern.findall(line)
            flow_rate = int(rate_pattern.search(line).group(0))
            if flow_rate > 0:
                valve_to_rate[valve] = flow_rate
            valve_to_adjacents[valve] = set(adj_valves)

        starting_state = TwoState(frozenset({"AA"}), 26, frozenset(valve_to_rate))

        # A* Search
        open_set = PriorityQueue()
        came_from = {}
        g_score = {starting_state: 0}
        f_score = {starting_state: heuristic_two(starting_state, valve_to_rate)}
        open_set.put((f_score[starting_state], starting_state))

        while not open_set.empty():
            cur_score: int
            cur_state: TwoState
            cur_score, cur_state = open_set.get()

            if not cur_state.valves_closed or cur_state.time_remaining == 0:
                pressure_released = 0
                path = [cur_state]
                while cur_state in came_from:
                    cur_state = came_from[cur_state]
                    path.append(cur_state)
                path.reverse()
                cur_closed = path[0].valves_closed
                for state in path[1:]:
                    for opened in cur_closed - state.valves_closed:
                        pressure_released += (
                            valve_to_rate[opened] * state.time_remaining
                        )
                    cur_closed = state.valves_closed
                return pressure_released

            new_states = []

            if len(cur_state.current_positions) == 1:
                cur_pos = next(iter(cur_state.current_positions))
                if cur_pos in cur_state.valves_closed:
                    for adj_valve in valve_to_adjacents[cur_pos]:
                        new_states.append(
                            TwoState(
                                frozenset({cur_pos, adj_valve}),
                                cur_state.time_remaining - 1,
                                frozenset(cur_state.valves_closed - {cur_pos}),
                            )
                        )
                for a1 in valve_to_adjacents[cur_pos]:
                    for a2 in valve_to_adjacents[cur_pos]:
                        new_states.append(
                            TwoState(
                                frozenset({a1, a2}),
                                cur_state.time_remaining - 1,
                                cur_state.valves_closed,
                            )
                        )
            else:
                pos_1, pos_2 = cur_state.current_positions
                if pos_1 in cur_state.valves_closed:
                    if pos_2 in cur_state.valves_closed:
                        new_states.append(
                            TwoState(
                                cur_state.current_positions,
                                cur_state.time_remaining - 1,
                                cur_state.valves_closed - {pos_1, pos_2},
                            )
                        )
                    for a2 in valve_to_adjacents[pos_2]:
                        new_states.append(
                            TwoState(
                                frozenset({pos_1, a2}),
                                cur_state.time_remaining - 1,
                                cur_state.valves_closed - {pos_1},
                            )
                        )
                if pos_2 in cur_state.valves_closed:
                    for a1 in valve_to_adjacents[pos_1]:
                        new_states.append(
                            TwoState(
                                frozenset({a1, pos_2}),
                                cur_state.time_remaining - 1,
                                cur_state.valves_closed - {pos_2},
                            )
                        )
                for a1 in valve_to_adjacents[pos_1]:
                    for a2 in valve_to_adjacents[pos_2]:
                        new_states.append(
                            TwoState(
                                frozenset({a1, a2}),
                                cur_state.time_remaining - 1,
                                cur_state.valves_closed,
                            )
                        )

            for new_state in new_states:
                tentative_g_score = g_score[cur_state] + sum(
                    valve_to_rate[v] for v in cur_state.valves_closed
                )
                if tentative_g_score < g_score.get(new_state, math.inf):
                    came_from[new_state] = cur_state
                    g_score[new_state] = tentative_g_score
                    f_score[new_state] = tentative_g_score + heuristic_two(
                        new_state, valve_to_rate
                    )
                    open_set.put((f_score[new_state], new_state))
        raise Exception("unreachable")


if __name__ == "__main__":
    Solution().run()
