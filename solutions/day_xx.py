import aoc_helper


def parse_raw(raw: str) -> list[str]:
    return []


def part_one(data):
    ...


def part_two(data):
    ...


if __name__ == '__main__':

    day = 2

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    aoc_helper.lazy_submit(day=day, year=2022, solution=lambda: part_one(parsed_data))
    aoc_helper.lazy_submit(day=day, year=2022, solution=lambda: part_two(parsed_data))
