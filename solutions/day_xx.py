def parse_raw(raw: str) -> list[str]:
    return []


def part_one(data):
    ...


def part_two(data):
    ...


if __name__ == "__main__":

    day = None

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
