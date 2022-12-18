import itertools, functools, numpy as np

import aoc_helper

Cube = tuple[int, int, int]


def parse_raw(raw: str) -> list[Cube]:
    lines = raw.splitlines()
    return [tuple(map(int, line.split(","))) for line in lines]


def is_touching(cube_a: Cube, cube_b: Cube) -> bool:
    each_axis = zip(cube_a, cube_b)
    diff_per_axes = (abs(a - b) for a, b in each_axis)
    # two axis same + one axis touching
    return sorted(diff_per_axes) == [0, 0, 1]


def part_one(cubes: list[Cube]) -> int:
    possible_pairs = itertools.combinations(cubes, r=2)
    touching_faces = sum(is_touching(a, b) for a, b in possible_pairs)
    total_faces = len(cubes) * 6

    return total_faces - touching_faces * 2


def part_two(data):
    ...


if __name__ == "__main__":

    day = 18

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
