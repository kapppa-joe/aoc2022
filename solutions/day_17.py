import numpy as np
from dataclasses import dataclass
import itertools
import functools
from typing import Iterable

import aoc_helper

Coord = tuple[int, int]


class RockComeToRest(RuntimeError):
    "Current rock come to rest"
    pass


class Jet:
    def __init__(self, pattern: str):
        self.counter = 0
        self.pattern = pattern
        self.iter = itertools.cycle(pattern)

    def take(self, n: int) -> Iterable[str]:
        self.counter += n
        return itertools.islice(self.iter, n)

    def __iter__(self):
        while True:
            self.counter += 1
            yield next(self.iter)


@functools.cache
def rock_array(kind: int) -> np.ndarray:
    match (kind):
        case 0:
            return np.array([[1, 1, 1, 1]])
        case 1:
            return np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        case 2:
            return np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]])
        case 3:
            return np.ones((4, 1), int)
        case 4:
            return np.ones((2, 2), int)
        case _:
            raise RuntimeError("rock of invalid kind")


@functools.cache
def rock_width(kind: int) -> int:
    return rock_array(kind).shape[1]


@functools.cache
def rock_max_x(kind: int, boundry=7) -> int:
    return boundry - rock_width(kind)


@functools.cache
def rock_shape(kind: int) -> tuple[int, int]:
    return rock_array(kind).shape


@dataclass
class Rock:
    kind: int

    @property
    def array(self) -> np.ndarray:
        return rock_array(self.kind)

    @property
    def width(self) -> int:
        return rock_width(self.kind)

    def max_x(self, boundry=7) -> int:
        return rock_max_x(kind=self.kind, boundry=boundry)

    @property
    def shape(self) -> tuple[int, int]:
        return rock_shape(self.kind)


Rocks = [Rock(i) for i in range(5)]


class Cave:
    def __init__(self, jet: Jet, width=7, array=None):
        self.jet = jet
        self.width = width
        if array:
            self.array = np.ndarray(array)
        else:
            self.array: np.ndarray = np.zeros((1, self.width), int)
        self.rock_tower_height = 0
        self.rest_rock_count = 0
        self.current_rock = None
        self.current_rock_pos = None

    def extend(self, n: int = 3):
        self.array = np.append(self.array, np.zeros((n, self.width), int), axis=0)

    def make_next_rock(self):
        cave_height_needed = (self.rock_tower_height + 4) - self.cave_height
        if cave_height_needed > 0:
            self.extend(cave_height_needed)

        self.current_rock_pos = (self.rock_tower_height + 3, 2)
        rock_kind = self.rest_rock_count % 5

        self.current_rock = Rocks[rock_kind]
        return self.current_rock

    def blow_rock(self, jet_direction: str):
        y, x = self.current_rock_pos

        match jet_direction:
            case "<":
                new_x = max(0, x - 1)
            case ">":
                max_x = self.current_rock.max_x(boundry=self.width)
                new_x = min(max_x, x + 1)
            case _:
                raise RuntimeError("invalid jet direction")
        self.current_rock_pos = (y, new_x)

    def rock_fall(self, handle_collision=True):
        y, x = self.current_rock_pos
        if handle_collision:
            # print(y, x, "<- y, x")
            # print(self.array)
            area_to_occupy_in_next_tick = self.select_area_by_rock_shape(
                pos=(y - 1, x), kind=self.current_rock.kind
            )
            # print(area_to_occupy_in_next_tick, "<--- this")
            # print(self.current_rock.array == area_to_occupy_in_next_tick, "<--- this")
            if (self.current_rock.array == area_to_occupy_in_next_tick).any():
                raise RockComeToRest
        if y <= 0:
            raise RockComeToRest
        self.current_rock_pos = y - 1, x

    @property
    def cave_height(self):
        return self.array.shape[0]

    def select_area_by_rock_shape(self, pos: Coord, kind: int) -> np.array:
        y0, x0 = pos
        dy, dx = rock_shape(kind)
        return self.array[y0 : y0 + dy, x0 : x0 + dx]

    def handle_rock_rest(self):
        y0, x0 = self.current_rock_pos
        dy, dx = self.current_rock.shape
        self.array[y0 : y0 + dy, x0 : x0 + dx] = self.current_rock.array

        self.update_rock_tower_height()
        self.rest_rock_count += 1

    def update_rock_tower_height(self):
        self.rock_tower_height = next(
            y + 1 for y in range(self.cave_height - 1, -1, -1) if self.array[y, :].any()
        )

    def fall_until_rock_rest(self) -> bool:
        try:
            for jet_direction in self.jet.take(3):
                self.blow_rock(jet_direction)
                self.rock_fall(handle_collision=False)
            for jet_direction in self.jet.iter:
                self.blow_rock(jet_direction)
                self.rock_fall()
        except RockComeToRest:
            self.handle_rock_rest()
            return True
        raise RuntimeError("Rock not come to rest but iter stopped")

    # def simulate_rock_fall(self):


def parse_raw(raw: str) -> Cave:
    jet = Jet(pattern=raw)
    return Cave(jet=jet)


def part_one(data):
    ...


def part_two(data):
    ...


if __name__ == "__main__":

    day = None

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
