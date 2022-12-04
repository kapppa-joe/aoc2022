import re
import aoc_helper


def parse_raw(raw: str) -> list[list[tuple[int, int]]]:
    lines = raw.split("\n")
    extract_numbers = map(lambda line: re.findall(r"\d+", line), lines)
    convert_to_int = [[int(num) for num in line] for line in extract_numbers]
    return [[tuple(nums[0:2]), tuple(nums[2:4])] for nums in convert_to_int]


def find_overlap(a: tuple[int, int], b: tuple[int, int]):
    left = max(a[0], b[0])
    right = min(a[1], b[1])
    return None if left > right else (left, right)


def part_one(data: list[list[tuple[int, int]]]) -> int:
    return sum(1 for pair in data if find_overlap(*pair) in pair)


def part_two(data: list[list[tuple[int, int]]]) -> int:
    return sum(1 for pair in data if find_overlap(*pair))


if __name__ == "__main__":

    day = 4

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
