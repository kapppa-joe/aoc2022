import aoc_helper
raw = aoc_helper.fetch(1, 2022)


def parse_raw(raw_input: str) -> list[list[int]]:
    elves = raw_input.split("\n\n")
    elves_calories = [[int(line) for line in elf.split("\n")] for elf in elves]
    return elves_calories


data = parse_raw(raw)


def part_one() -> int:
    return max(sum(elf) for elf in data)


def part_two() -> int:
    elves_sorted = sorted((sum(elf) for elf in data), reverse=True)
    return sum(elves_sorted[:3])


aoc_helper.lazy_submit(day=1, year=2022, solution=part_one)
aoc_helper.lazy_submit(day=1, year=2022, solution=part_two)
