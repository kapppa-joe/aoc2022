from typing import TypeAlias, Union
from itertools import zip_longest
import re

import aoc_helper

Packet: TypeAlias = list[Union[int, "Packet"]]


def parse_raw(raw: str) -> list[tuple[Packet, Packet]]:
    sanitised_raw = re.sub(r"[^\[\] \n\d\,]", "", raw)
    pairs = [pair.split("\n") for pair in sanitised_raw.split("\n\n")]

    return [(eval(pair[0]), eval(pair[1])) for pair in pairs]


def in_right_order(left: int | Packet, right: int | Packet) -> bool:
    if isinstance(left, int) and isinstance(right, int):
        return left < right
    elif isinstance(left, list) and isinstance(right, list):
        for left_elem, right_elem in zip_longest(left, right, fillvalue=None):
            if left_elem == right_elem:
                continue
            elif left_elem is None or right_elem is None:
                return left_elem is None
            else:
                return in_right_order(left_elem, right_elem)
    else:
        return in_right_order(convert_int_to_list(left), convert_int_to_list(right))

    raise RuntimeError("Got unexpected pattern of input data")


def convert_int_to_list(value: int | list) -> list:
    if isinstance(value, int):
        return [value]
    return value


def cmp_packets(left: Packet, right: Packet) -> int:
    return -1 if in_right_order(left, right) else 1


def part_one(pairs: list[tuple[Packet, Packet]]) -> int:
    return sum(i + 1 for i, pair in enumerate(pairs) if in_right_order(*pair))


def part_two(data):
    ...


if __name__ == "__main__":

    day = 13

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
