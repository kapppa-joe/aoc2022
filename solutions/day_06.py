import aoc_helper


def find_start_of_unique_set(size: int, data: str) -> int:
    return next(
        i for i in range(size - 1, len(data)) if len(set(data[i - size : i])) == size
    )


def part_one(data: str) -> int:
    return find_start_of_unique_set(size=4, data=data)


def part_two(data: str) -> int:
    return find_start_of_unique_set(size=14, data=data)


if __name__ == "__main__":

    day = 6

    raw_data = aoc_helper.fetch(day, 2022)

    print(f"part one solution: {part_one(raw_data)}")
    print(f"part two solution: {part_two(raw_data)}")
