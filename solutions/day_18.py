import itertools
from typing import Iterable, Iterator
from collections import defaultdict

import aoc_helper

Cube = tuple[int, int, int]
Boundries = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


def parse_raw(raw: str) -> list[Cube]:
    lines = raw.splitlines()
    return [tuple(map(int, line.split(","))) for line in lines]


def is_touching(cube_a: Cube, cube_b: Cube) -> bool:
    each_axis = zip(cube_a, cube_b)
    diff_per_axes = (abs(a - b) for a, b in each_axis)
    # two axis same + one axis touching
    return sorted(diff_per_axes) == [0, 0, 1]


def object_surface_area(cubes: Iterable[Cube]) -> int:
    possible_pairs = itertools.combinations(cubes, r=2)
    touching_pairs = sum(is_touching(a, b) for a, b in possible_pairs)
    total_faces = len(cubes) * 6

    return total_faces - touching_pairs * 2


def part_one(lava_cubes: list[Cube]) -> int:
    return object_surface_area(lava_cubes)


class DisjointSets:
    def __init__(self):
        self._parent = {}

    def __contains__(self, cube: Cube) -> bool:
        return cube in self._parent

    def list_groups(self) -> Iterator[tuple[Cube, set[Cube]]]:
        group_dict: dict[Cube, set[Cube]] = defaultdict(set)
        for member in self._parent:
            group_dict[self.find(member)].add(member)
        yield from group_dict.values()

    def find(self, cube: Cube) -> Cube:
        node = cube
        if node not in self._parent:
            self._parent[node] = node

        while self._parent[node] != node:
            self._parent[node] = self._parent[self._parent[node]]
            node = self._parent[node]
        return node

    def union(self, a: Cube, b: Cube):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a != root_b:
            self._parent[root_a] = root_b


def find_boundries(lava_cubes: list[Cube]) -> Boundries:
    each_axis = [[cube[i] for cube in lava_cubes] for i in range(3)]
    return [(min(axis), max(axis)) for axis in each_axis]


def is_at_boundry(cube: Cube, boundries: Boundries) -> bool:
    return any(cube[axis] in boundries[axis] for axis in [0, 1, 2])


def all_spaces(boundries: Boundries) -> Iterator[Cube]:
    as_ranges = map(lambda minmax: range(minmax[0], minmax[1] + 1), boundries)
    return itertools.product(*as_ranges)


def all_touching_pairs(boundries: Boundries) -> Iterator[frozenset[Cube, Cube]]:
    upper_boundries = [upper for _, upper in boundries]
    for cube in all_spaces(boundries=boundries):
        x, y, z = cube
        if x != upper_boundries[0]:
            yield frozenset([cube, (x + 1, y, z)])
        if y != upper_boundries[1]:
            yield frozenset([cube, (x, y + 1, z)])
        if z != upper_boundries[2]:
            yield frozenset([cube, (x, y, z + 1)])
    return


def group_cubes(lava_cubes: list[Cube]) -> dict:
    boundries = find_boundries(lava_cubes)
    lava_set = set(lava_cubes)
    not_lava = lambda cube: cube not in lava_set
    confirmed_expose = lambda cube: not_lava(cube) and is_at_boundry(
        cube=cube, boundries=boundries
    )

    ds = DisjointSets()
    lava_root = lava_cubes[0]
    for cube in lava_cubes[1:]:
        ds.union(cube, lava_root)

    for cube_a, cube_b in all_touching_pairs(boundries=boundries):
        if not_lava(cube_a) and not_lava(cube_b):
            ds.union(cube_b, cube_a)
        ds.find(cube_a)

    result = defaultdict(set)
    trapped_air_groups = defaultdict(set)
    result["trapped_air_groups"] = trapped_air_groups

    for group in ds.list_groups():
        if any(cube in lava_set for cube in group):
            result["lava_cubes"].update(group)
        elif any(confirmed_expose(cube) for cube in group):
            result["exposed_air"].update(group)
        else:
            result["trapped_air"].update(group)

    return result


def part_two(lava_cubes: list[Cube]) -> int:
    groups = group_cubes(lava_cubes=lava_cubes)
    trapped_air = groups["trapped_air"]

    return object_surface_area(lava_cubes) - object_surface_area(trapped_air)


if __name__ == "__main__":

    day = 18

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
