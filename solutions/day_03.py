from functools import reduce
import aoc_helper


def parse_raw(raw: str) -> list[tuple[str, str]]:
    return [
        (line[0 : (len(line) // 2)], line[len(line) // 2 :]) for line in raw.split("\n")
    ]


def parse_raw_part_two(raw: str) -> list[tuple[str, str, str]]:
    lines = raw.split("\n")
    return [tuple(lines[i * 3 : i * 3 + 3]) for i in range(len(lines) // 3)]


def find_repeat_item(*groups: list[str]) -> str:
    intersect = reduce(lambda a, b: a & b, [set(group) for group in groups])
    if len(intersect) != 1:
        raise ValueError
    return intersect.pop()


def item_priority(char: str) -> int:
    return ord(char.lower()) - ord("a") + (27 if char.isupper() else 1)


def part_one(rucksacks: list[tuple[str, str]]):
    return sum(item_priority(find_repeat_item(*rucksack)) for rucksack in rucksacks)


def part_two(groups: list[tuple[str, str, str]]):
    return sum(item_priority(find_repeat_item(*group)) for group in groups)


if __name__ == "__main__":

    day = 3

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)
    parsed_data_part_two = parse_raw_part_two(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data_part_two)}")
