import re
import functools
from typing import Iterable

import aoc_helper


class ValveNetwork:
    def __init__(self, raw: str):
        self._valves = {}
        self._connections = {}
        pattern = r"Valve (\w+) has flow rate=(\d+).*to valves? (.+)"
        for name, rate, neighbour_valves in re.findall(pattern, raw):
            self._valves[name] = int(rate)
            self._connections[name] = frozenset(neighbour_valves.split(", "))

    def neighbour_valves(self, valve_name: str) -> frozenset[str]:
        return self._connections[valve_name]

    def flow_rate(self, valve_name: str) -> int:
        return self._valves[valve_name]

    @property
    def valves(self) -> list[str]:
        return list(self._valves)

    @functools.cache
    def current_flow_rate(self, valves_opened: frozenset[str]) -> int:
        return sum(self.flow_rate(valve_name) for valve_name in valves_opened)

    def possible_choices(
        self,
        current_valve: str,
        valves_opened: frozenset[set],
        remaining_time: int,
    ) -> Iterable[int]:
        # do nothing
        yield self.total_pressure_released(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )
        # open the current valve
        if current_valve not in valves_opened and self.flow_rate(current_valve) > 0:
            yield self.total_pressure_released(
                current_valve=current_valve,
                valves_opened=valves_opened.union([current_valve]),
                remaining_time=remaining_time,
            )
        # go to a neighbour value
        for neighbour in self.neighbour_valves(current_valve):
            yield self.total_pressure_released(
                current_valve=neighbour,
                valves_opened=valves_opened,
                remaining_time=remaining_time,
            )

    @functools.cache
    def total_pressure_released(
        self,
        current_valve: str,
        valves_opened: frozenset[set],
        remaining_time: int,
    ) -> int:
        if remaining_time == 0:
            return 0

        release_for_this_minute = self.current_flow_rate(valves_opened)

        if remaining_time == 1:
            return release_for_this_minute

        best_choice = max(
            self.possible_choices(
                current_valve=current_valve,
                valves_opened=valves_opened,
                remaining_time=remaining_time - 1,
            )
        )

        return best_choice + release_for_this_minute


def parse_raw(raw: str) -> ValveNetwork:
    return ValveNetwork(raw)


def part_one(network: ValveNetwork) -> int:
    initial_valve = "AA"
    valves_opened = frozenset()
    remaining_time = 30
    return network.total_pressure_released(
        current_valve=initial_valve,
        valves_opened=valves_opened,
        remaining_time=remaining_time,
    )


def part_two(data):
    ...


if __name__ == "__main__":

    day = 16

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
