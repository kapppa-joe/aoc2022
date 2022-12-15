from typing import Optional, Iterable
import re
import functools

import aoc_helper

Coord = tuple[int, int]
Coverage = tuple[int, int] | None


def parse_raw(raw: str) -> list[list[Coord]]:
    numbers_in_each_line = [
        [int(num) for num in re.findall(r"-?\d+", line)] for line in raw.split("\n")
    ]

    return [[(a, b), (c, d)] for (a, b, c, d) in numbers_in_each_line]


@functools.cache
def manhattan_distance(start: Coord, end: Coord) -> int:
    x0, y0 = start
    x1, y1 = end
    return abs(x1 - x0) + abs(y1 - y0)


def sensor_x_coverage_at_given_y(sensor: Coord, beacon: Coord, y: int) -> Coverage:
    x0, y0 = sensor
    dist = manhattan_distance(sensor, beacon)
    x_dist = dist - abs(y0 - y)
    if x_dist >= 0:
        return (x0 - x_dist, x0 + x_dist)
    else:
        return None


def all_x_coverages_at_given_y(
    sensor_and_beacons: list[list[Coord]], y: int
) -> Iterable[Coverage]:
    return (
        sensor_x_coverage_at_given_y(sensor=sensor, beacon=beacon, y=y)
        for sensor, beacon in sensor_and_beacons
    )


def merge_x_coverages(x_coverages: Iterable[Coverage]) -> tuple[int, int]:
    removed_nones = filter(None, x_coverages)
    return functools.reduce(
        lambda acc, x_range: (min(acc[0], x_range[0]), max(acc[1], x_range[1])),
        removed_nones,
    )


def part_one(sensor_and_beacons: list[list[Coord]], y: int) -> int:
    x_coverages = all_x_coverages_at_given_y(sensor_and_beacons=sensor_and_beacons, y=y)
    left, right = merge_x_coverages(x_coverages)
    return abs(left - right)


def detect_hole(
    x_coverages: Iterable[Coverage], left_boundry=0, right_boundry=4000000
) -> Optional[int]:
    removed_nones = filter(None, x_coverages)
    sorted_coverages = sorted(removed_nones)
    _, right_limit = sorted_coverages[0]

    hole_is_in_boundry = (
        lambda right_limit: right_limit + 1 >= left_boundry
        and right_limit + 1 <= right_boundry
    )

    for left, right in sorted_coverages[1:]:
        if left - right_limit == 2:
            if hole_is_in_boundry(right_limit):
                return right_limit + 1  # hole found
            right_limit = max(right, right_limit)
        elif left <= right_limit + 1:
            right_limit = max(right, right_limit)
        else:
            raise RuntimeError(
                f"Found a hole which is larger then size 1. curr range:{left, right}, curr right limit: {right_limit}"
            )
    return None


def find_only_hole_on_map(
    sensor_and_beacons: list[list[Coord]], boundary: int
) -> Coord:
    possible_y = range(0, boundary + 1)
    all_y_and_their_x_coverages = (
        (y, all_x_coverages_at_given_y(sensor_and_beacons=sensor_and_beacons, y=y))
        for y in possible_y
    )
    find_holes_iterator = (
        (detect_hole(x_coverages), y)
        for (y, x_coverages) in all_y_and_their_x_coverages
    )
    return next((x, y) for x, y in find_holes_iterator if x is not None)


def part_two(sensor_and_beacons: list[list[Coord]], boundary: int) -> int:
    x, y = find_only_hole_on_map(
        sensor_and_beacons=sensor_and_beacons, boundary=boundary
    )
    return x * 4000000 + y


if __name__ == "__main__":

    day = 15

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data, y=2000000)}")
    print(f"part two solution: {part_two(parsed_data, boundary=4000000)}")
