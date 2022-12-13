from typing import TypeAlias, Union
from itertools import zip_longest
from functools import cache, cmp_to_key
import re

import aoc_helper

Packet: TypeAlias = list[Union[int, "Packet"]]

DividerPackets = ["[[2]]", "[[6]]"]


def parse_raw(raw: str) -> list[tuple[str, str]]:
    sanitised_raw = re.sub(r"[^\[\] \n\d\,]", "", raw)
    return [tuple(pair.split("\n")) for pair in sanitised_raw.split("\n\n")]


def add_divider_packets(pairs: list[tuple[str, str]]) -> list[str]:

    return [packet_str for pair in pairs for packet_str in pair] + DividerPackets


@cache
def parse_packet_string(packet_string: str) -> Packet:
    return eval(packet_string)


def in_right_order(left_str: str, right_str: str) -> bool:
    left, right = parse_packet_string(left_str), parse_packet_string(right_str)
    return compare_packets(left, right) == -1


def compare_packets(left: int | Packet, right: int | Packet) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        return -1 if left < right else 1

    elif isinstance(left, list) and isinstance(right, list):
        for left_elem, right_elem in zip_longest(left, right, fillvalue=None):
            if left_elem is None or right_elem is None:
                return -1 if left_elem is None else 1
            else:
                curr_element_comparison = compare_packets(left_elem, right_elem)
                if curr_element_comparison in [-1, 1]:
                    return curr_element_comparison
        return 0
    else:
        return compare_packets(convert_int_to_list(left), convert_int_to_list(right))

    raise RuntimeError("Got unexpected pattern of input data")


def convert_int_to_list(value: int | list) -> list:
    if isinstance(value, int):
        return [value]
    return value


@cache
def cmp_packets_strings(left_str: str, right_str: str) -> int:
    left, right = parse_packet_string(left_str), parse_packet_string(right_str)
    return compare_packets(left, right)


def sort_packet_strings(packet_strings: list[str]) -> list[str]:
    return sorted(packet_strings, key=cmp_to_key(cmp_packets_strings))


def part_one(pairs: list[tuple[str, str]]) -> int:
    return sum(i + 1 for i, pair in enumerate(pairs) if in_right_order(*pair))


def part_two(packet_strings: list[str]):
    packets_sorted = sort_packet_strings(packet_strings)
    divider_indices = [packets_sorted.index(divider) + 1 for divider in DividerPackets]
    return divider_indices[0] * divider_indices[1]


if __name__ == "__main__":

    day = 13

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")

    packet_strings_with_divider = add_divider_packets(parsed_data)
    print(f"part two solution: {part_two(packet_strings_with_divider)}")
