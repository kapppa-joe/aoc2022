from itertools import accumulate
from typing import TypeAlias

import aoc_helper

Motion: TypeAlias = tuple[str, int]
Coord: TypeAlias = tuple[int, int]


def parse_raw(raw: str) -> list[Motion]:
    lines = raw.split("\n")
    pairs = [line.split(" ") for line in lines]
    return [(pair[0], int(pair[1])) for pair in pairs]


def trace_head_position(
    motions: list[Motion], start_pos: Coord = (0, 0)
) -> list[Coord]:
    pos = start_pos
    position_record = [pos]
    direction_delta = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }
    for direction, steps in motions:
        dx, dy = direction_delta[direction]
        x0, y0 = pos
        position_record += [(x0 + dx * i, y0 + dy * i) for i in range(1, steps + 1)]
        pos = position_record[-1]

    return position_record


def is_touching(head_pos: Coord, tail_pos: Coord) -> bool:
    x0, y0 = head_pos
    x1, y1 = tail_pos

    return abs(x0 - x1) <= 1 and abs(y0 - y1) <= 1


def coords_diff(coord1: Coord, coord2: Coord) -> tuple[int, int]:
    x0, y0 = coord1
    x1, y1 = coord2

    return (x0 - x1, y0 - y1)


def coords_add(coord: Coord, delta: tuple[int, int]) -> Coord:

    return (coord[0] + delta[0], coord[1] + delta[1])


def new_tail_position(tail_pos: Coord, head_pos: Coord) -> Coord:
    if is_touching(head_pos=head_pos, tail_pos=tail_pos):
        return tail_pos
    dx, dy = coords_diff(head_pos, tail_pos)

    if abs(dx) > 2 or abs(dy) > 2:
        raise RuntimeError(
            f"Got unexpected movement, input params: head_pos={head_pos}, tail_pos={tail_pos}"
        )

    dx = dx // 2 if abs(dx) == 2 else dx
    dy = dy // 2 if abs(dy) == 2 else dy

    return coords_add(tail_pos, (dx, dy))


def map_next_knot_movements(prev_knot_movement: list[Coord]) -> list[Coord]:
    return list(accumulate(iterable=prev_knot_movement, func=new_tail_position))


def part_one(motions: list[Motion]) -> int:
    head_movements = trace_head_position(motions)
    tail_movements = map_next_knot_movements(prev_knot_movement=head_movements)
    return len(set(tail_movements))


def part_two(motions: list[Motion]) -> int:
    curr_knot_movement = trace_head_position(motions)
    for _ in range(9):
        curr_knot_movement = map_next_knot_movements(curr_knot_movement)
    return len(set(curr_knot_movement))


if __name__ == "__main__":

    day = 9

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
