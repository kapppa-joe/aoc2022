import numpy as np
import itertools
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


class Rock:
    def __init__(self, kind: int, pos: Coord):
        self.kind = kind
        self.pos = pos

    def array(self) -> np.ndarray:
        match (self.kind):
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

    def width(self) -> int:
        return self.array().shape[1]

    def max_x(self, boundry=7) -> int:
        return boundry - self.width()


class Cave:
    def __init__(self, jet: Jet, width=7, array=None):
        self.jet = jet
        self.width = width
        self.array = np.zeros((1, self.width), int)
        self.rock_height = 0
        self.rest_rock_count = 0
        self.current_rock = None

    def extend(self):
        self.array = np.append(self.array, np.zeros((3, self.width), int), axis=0)

    def make_next_rock(self):
        rock_pos = (2, self.rock_height + 3)
        rock_kind = self.rest_rock_count % 5

        self.current_rock = Rock(kind=rock_kind, pos=rock_pos)
        return self.current_rock

    def blow_rock(self, jet_direction: str):
        x, y = self.current_rock.pos

        match jet_direction:
            case "<":
                new_x = max(0, x - 1)
            case ">":
                max_x = self.current_rock.max_x(boundry=self.width)
                new_x = min(max_x, x + 1)
            case _:
                raise RuntimeError("invalid jet direction")
        self.current_rock.pos = (new_x, y)

    def rock_fall(self):
        x, y = self.current_rock.pos
        if y <= 0:
            raise RockComeToRest
        self.current_rock.pos = x, y - 1

    # def update_rock_height(self):

    def fall_until_rock_rest(self) -> bool:
        try:
            for jet_direction in self.jet.iter:
                self.blow_rock(jet_direction)
                self.rock_fall()
        except RockComeToRest:

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
