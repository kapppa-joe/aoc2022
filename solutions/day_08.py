import itertools

import aoc_helper
import numpy as np


def parse_raw(raw: str) -> np.ndarray:
    return np.array([[int(digit) for digit in line] for line in raw.split("\n")])


def trees_in_four_directions(grid: np.ndarray, x: int, y: int) -> list[list[int]]:
    return [
        list(arr)
        for arr in [
            reversed(grid[0:y, x]),
            grid[y, x + 1 :],
            grid[y + 1 :, x],
            reversed(grid[y, 0:x]),
        ]
    ]


def visibility_from_four_directions(grid: np.ndarray, x: int, y: int) -> list[bool]:
    self_height = grid[y][x]
    return [all(trees < self_height) for trees in trees_in_four_directions(grid, x, y)]


def is_visible(grid: np.ndarray, x: int, y: int) -> bool:
    return any(visibility_from_four_directions(grid, x, y))


def count_trees_saw(grid: np.ndarray, x: int, y: int) -> list[int]:
    self_height = grid[y][x]
    counts = []

    for trees in trees_in_four_directions(grid, x, y):
        not_blocked = list(itertools.takewhile(lambda tree: tree < self_height, trees))
        blocked = itertools.dropwhile(lambda tree: tree < self_height, trees)
        seen = sum(1 for _ in not_blocked)
        seen += 1 if any(tree for tree in blocked) else 0
        counts.append(seen)

    return counts


def part_one(grid: np.ndarray) -> int:
    return sum(
        1
        for y in range(grid.shape[0])
        for x in range(grid.shape[1])
        if is_visible(grid, x, y)
    )


def part_two(grid: np.ndarray) -> int:

    return max(
        np.prod(a=count_trees_saw(grid, x, y), dtype=int)
        for y in range(grid.shape[0])
        for x in range(grid.shape[1])
    )


if __name__ == "__main__":

    day = 8

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
