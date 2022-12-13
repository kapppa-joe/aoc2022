import aoc_helper

raw = aoc_helper.fetch(1, 2022)


def parse_raw(raw_input: str) -> list[list[int]]:
    elves = raw_input.split("\n\n")
    elves_calories = [[int(line) for line in elf.split("\n")] for elf in elves]
    return elves_calories


def part_one(data: list[list[int]]) -> int:
    return max(sum(elf) for elf in data)


def part_two(data: list[list[int]]) -> int:
    elves_sorted = sorted((sum(elf) for elf in data), reverse=True)
    return sum(elves_sorted[:3])


if __name__ == "__main__":
    day = 1

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
