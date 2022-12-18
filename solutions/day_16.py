import re
import functools
import itertools
from typing import Iterable
from dataclasses import dataclass
import numpy as np

import aoc_helper

ValveSet = frozenset[str]

# use immutable state to allow easy memoization by functools.cache
@dataclass(frozen=True)
class State:
    current_valve: str
    remaining_time: int
    valves_opened: ValveSet = frozenset()


class ValveNetwork:
    def __init__(self, raw: str):
        self._valves = {}
        self._edges = {}
        pattern = r"Valve (\w+) has flow rate=(\d+).*to valves? (.+)"
        for name, rate, neighbour_valves in re.findall(pattern, raw):
            self._valves[name] = int(rate)
            self._edges[name] = frozenset(neighbour_valves.split(", "))
        self.dist: dict[tuple[str, str], int] = self.calc_all_distances()

    def neighbour_valves(self, valve_name: str) -> ValveSet:
        return self._edges[valve_name]

    def calc_all_distances(self) -> dict[tuple[str, str], int]:
        n = len(self.valves)
        arr = np.full(shape=(n, n), fill_value=n + 1)

        for valve in range(n):
            arr[valve, valve] = 0

        for (a, b) in itertools.combinations(list(range(n)), 2):
            if self.valves[b] in self.neighbour_valves(self.valves[a]):
                arr[a, b] = 1
                arr[b, a] = 1

        for (k, i, j) in itertools.product(list(range(n)), repeat=3):
            arr[i, j] = min(arr[i, j], arr[i, k] + arr[k, j])

        dist = {
            (self.valves[x], self.valves[y]): arr[x, y]
            for x in range(n)
            for y in range(n)
        }
        return dist

    def flow_rate(self, valve_name: str) -> int:
        return self._valves[valve_name]

    @property
    def valves(self) -> list[str]:
        return list(self._valves)

    @property
    def useful_valves(self) -> ValveSet:
        return frozenset([valve for valve in self.valves if self.flow_rate(valve) > 0])

    @functools.cache
    def untapped_valves(self, valves_opened: ValveSet) -> dict[str, int]:
        return {
            valve: self.flow_rate(valve)
            for valve in self.useful_valves.difference(valves_opened)
        }

    def possible_choices(self, state) -> Iterable[int]:
        current_valve = state.current_valve
        remaining_time = state.remaining_time
        valves_opened = state.valves_opened

        for target_valve, flow_rate in self.untapped_valves(valves_opened).items():
            distance = self.dist[(current_valve, target_valve)]
            if remaining_time <= distance + 1:
                # skip if no benefit trying open that valve
                continue
            newly_released = flow_rate * (remaining_time - distance - 1)
            new_state = State(
                current_valve=target_valve,
                remaining_time=remaining_time - distance - 1,
                valves_opened=valves_opened.union([target_valve]),
            )
            yield newly_released + self.maximized_release(state=new_state)

        # if no way to open a new valve in remaining time, return 0
        yield 0

    @functools.cache
    def maximized_release(self, state: State):
        possible_choices = self.possible_choices(state=state)

        return max(possible_choices)

    @functools.cache
    def explore_all_solutions(self, state: State) -> dict[ValveSet, int]:
        # less efficient then maximized_release, but is necessary to find sub-optimal solution for part two
        current_valve = state.current_valve
        remaining_time = state.remaining_time
        valves_opened = state.valves_opened

        # add current route to memo
        combined_solution = {valves_opened: 0}

        for target_valve, flow_rate in self.untapped_valves(valves_opened).items():
            distance = self.dist[(current_valve, target_valve)]
            if remaining_time < distance + 1:
                continue
            newly_released = flow_rate * (remaining_time - distance - 1)

            new_state = State(
                current_valve=target_valve,
                remaining_time=remaining_time - distance - 1,
                valves_opened=valves_opened.union([target_valve]),
            )
            recur_solutions = self.explore_all_solutions(state=new_state)
            for key in recur_solutions:
                # fill in the value to memo here, so that function signature don't need to keep track of release got already.
                combined_solution[key] = max(
                    recur_solutions[key] + newly_released, combined_solution.get(key, 0)
                )

        return combined_solution


def parse_raw(raw: str) -> ValveNetwork:
    return ValveNetwork(raw)


def part_one(network: ValveNetwork) -> int:
    initial_state = State(current_valve="AA", remaining_time=30)
    return network.maximized_release(initial_state)


def part_two(network: ValveNetwork) -> int:
    initial_state = State(current_valve="AA", remaining_time=26)
    all_solutions = network.explore_all_solutions(state=initial_state)

    all_disjointed_routes = (
        (set_a, set_b)
        for set_a, set_b in itertools.combinations(all_solutions, r=2)
        if set(set_a).isdisjoint(set(set_b))
    )
    max_combined_score = max(
        all_solutions[set_a] + all_solutions[set_b]
        for set_a, set_b in all_disjointed_routes
    )

    return max_combined_score


if __name__ == "__main__":

    day = 16

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
