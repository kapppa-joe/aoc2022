from typing import TypeAlias

import aoc_helper

Grid: TypeAlias = list[list[int]]
Coord: TypeAlias = tuple[int, int]


def parse_raw(raw: str) -> tuple[Coord, Coord, Grid]:
    start, dest = [find_coordinate(raw=raw, char=char) for char in ("S", "E")]
    grid = [
        [ord(char) - ord("a") for char in line]
        for line in raw.replace("S", "a").replace("E", "z").split("\n")
    ]
    return (start, dest, grid)


def find_coordinate(raw: str, char: str) -> Coord:
    char_index = raw.index(char)
    y = raw[:char_index].count("\n")
    x = (
        char_index - raw[:char_index].rindex("\n") - 1
        if "\n" in raw[:char_index]
        else char_index
    )

    return (x, y)


def neighbours(curr_coord: Coord, grid: Grid) -> list[Coord]:
    x, y = curr_coord
    y_limit = len(grid) - 1
    x_limit = len(grid[0]) - 1

    return [
        (a, b)
        for (a, b) in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        if 0 <= a <= x_limit and 0 <= b <= y_limit
    ]


def get_height(coord: Coord, grid: Grid) -> int:
    x, y = coord
    return grid[y][x]


def reachable_neighbours(curr_coord: Coord, grid: Grid) -> list[Coord]:
    reachable = (
        lambda curr, to_reach: get_height(curr, grid) - get_height(to_reach, grid) >= -1
    )
    return [
        neighbour_coord
        for neighbour_coord in neighbours(curr_coord, grid)
        if reachable(curr=curr_coord, to_reach=neighbour_coord)
    ]


def part_one(start: Coord, destination: Coord, grid: Grid) -> int:
    candidates = {start: 0}
    visited = set()

    while candidates:
        curr = min(candidates, key=candidates.get)
        curr_distance = candidates[curr]
        next_candidates = {
            coord: curr_distance + 1
            for coord in reachable_neighbours(curr_coord=curr, grid=grid)
            if not coord in visited
        }

        if destination in next_candidates:
            return next_candidates[destination]

        candidates.update(next_candidates)
        visited.add(curr)
        candidates.pop(curr)

    raise RuntimeError("Fail to reach destination")


def part_two(data):
    ...


if __name__ == "__main__":

    day = 12

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(*parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
