from typing import TypeAlias
from itertools import accumulate

import aoc_helper


def parse_raw(raw: str) -> list[tuple[int, int]]:
    lines = raw.split("\n")

    cycle = 0
    delta_x = []

    for line in lines:
        if line.startswith("addx"):
            cycle += 2
            inc_value = int(line[5:])
            delta_x.append((cycle, inc_value))
        else:
            cycle += 1

    return delta_x


def x_values_for_all_cycles(delta_x: tuple[int, int]) -> list[int]:
    result = [1]
    for cycle, inc_value in delta_x:
        latest_value = result[-1]
        result += [latest_value] * (cycle + 1 - len(result))
        result.append(latest_value + inc_value)

    return result


def part_one(delta_x: tuple[int, int]) -> int:
    x_values = x_values_for_all_cycles(delta_x)

    return sum(cycle * x_values[cycle] for cycle in range(20, 220 + 1, 40))


def pixel_onoff_at_cycle(x_values: list[int], cycle: int) -> bool:
    crt_x_pos = (cycle - 1) % 40
    x_value_at_cycle = x_values[cycle] if cycle < len(x_values) else x_values[-1]
    return abs(x_value_at_cycle - crt_x_pos) <= 1


def part_two(delta_x: tuple[int, int]) -> str:
    x_values = x_values_for_all_cycles(delta_x)

    screen = []
    pixel_representation = ".#"

    for y in range(6):
        pixels_for_this_row = [
            pixel_onoff_at_cycle(x_values=x_values, cycle=y * 40 + x + 1)
            for x in range(40)
        ]
        row = "".join(pixel_representation[on_off] for on_off in pixels_for_this_row)
        screen.append(row)

    return "\n".join(screen)


if __name__ == "__main__":

    day = 10

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: \n\n{part_two(parsed_data)}")
