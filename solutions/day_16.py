import re
import functools
from typing import Iterable
from dataclasses import dataclass, asdict

import aoc_helper


@dataclass(frozen=True)
class State:
    current_valve: str | tuple[str, str]
    valves_opened: frozenset[set]
    remaining_time: int

    def open_valve(self, valve_names: Iterable[str]) -> "State":
        return State(
            current_valve=self.current_valve,
            remaining_time=self.remaining_time - 1,
            valves_opened=self.valves_opened.union(valve_names),
        )

    def change_location(self, new_location: str | tuple[str, str]):
        if type(self.current_valve) != type(new_location):
            raise "location type doesn't match current. be careful to separate case working alone or working together with an elephant"
        return State(
            current_valve=new_location,
            remaining_time=self.remaining_time - 1,
            valves_opened=self.valves_opened,
        )

    def open_valve_and_change_location(
        self,
        new_location: tuple[str, str],
        valve_names: Iterable[str],
    ):
        if type(self.current_valve) == str:
            raise "location type doesn't match current. be careful to separate case working alone or working together with an elephant"
        return State(
            current_valve=new_location,
            remaining_time=self.remaining_time - 1,
            valves_opened=self.valves_opened.union(valve_names),
        )


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
            remaining_time=remaining_time - 1,
        )
        # open the current valve
        if current_valve not in valves_opened and self.flow_rate(current_valve) > 0:
            total_gain_from_current_valve = self.flow_rate(current_valve) * (
                remaining_time - 1
            )
            yield total_gain_from_current_valve + self.total_pressure_released(
                current_valve=current_valve,
                valves_opened=valves_opened.union([current_valve]),
                remaining_time=remaining_time - 1,
            )
        # go to a neighbour value
        for neighbour in self.neighbour_valves(current_valve):
            yield self.total_pressure_released(
                current_valve=neighbour,
                valves_opened=valves_opened,
                remaining_time=remaining_time - 1,
            )

    @functools.cache
    def maximized_release_from_choice(
        self,
        current_valve: str,
        valves_opened: frozenset[set],
        remaining_time: int,
    ):
        possible_choices = self.possible_choices(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )

        return max(
            self.possible_choices(
                current_valve=current_valve,
                valves_opened=valves_opened,
                remaining_time=remaining_time,
            )
        )

    def total_pressure_released(
        self,
        current_valve: str,
        valves_opened: frozenset[set],
        remaining_time: int,
    ) -> int:
        if remaining_time < 2:
            return 0

        best_choice = self.maximized_release_from_choice(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )
        return best_choice


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
