from typing import Optional, Callable, cast
import itertools
import aoc_helper

Coord = tuple[int, int]

SourceOfSand = (500, 0)


class FallToAbyss(RuntimeError):
    "Sand starts falling to abyss."
    pass


class SandSourceBlocked(RuntimeError):
    "The source of flowing sand is blocked. You are safe now."
    pass


def parse_raw(raw: str) -> set[Coord]:
    lines = raw.split("\n")
    rock_lines_list = [
        [tuple(map(int, point.split(","))) for point in line.split(" -> ")]
        for line in lines
    ]

    result = set()
    # for rock_lines in rock_lines_list:
    #     current_point = None
    #     for next_point in rock_lines:
    #         if not current_point:
    #             current_point = next_point
    #             continue
    #         result = result.union(all_points_in_line(current_point, next_point))
    #         current_point = next_point
    for rock_lines in rock_lines_list:
        for line_start, line_end in itertools.pairwise(rock_lines):
            result = result.union(all_points_in_line(line_start, line_end))
    return result


def all_points_in_line(start: Coord, end: Coord) -> set[Coord]:
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0

    if dx != 0 and dy != 0:
        raise ValueError("start point and end point do not have a common axis.")

    if dx == 0:
        return set(itertools.product([x0], range(min(y0, y1), max(y0, y1) + 1)))
    else:
        return set(itertools.product(range(min(x0, x1), max(x0, x1) + 1), [y0]))


def drop_sand(rocks: set[Coord], sands: set[Coord] = set()) -> Coord:
    lowest_rock_y = max(y for (_, y) in rocks)

    x, y = simulate_sand_falling_down(
        rocks=rocks, sands=sands, stop_condition=lambda _, y: y >= lowest_rock_y
    )
    if y >= lowest_rock_y:
        raise FallToAbyss

    return x, y


def drop_sand_part_two(rocks: set[Coord], sands: set[Coord] = set()) -> Coord:
    lowest_rock_y = max(y for (_, y) in rocks)

    return simulate_sand_falling_down(
        rocks=rocks, sands=sands, stop_condition=lambda _, y: y >= lowest_rock_y + 1
    )


def simulate_sand_falling_down(
    rocks: set[Coord], sands: set[Coord], stop_condition: Callable[[int, int], bool]
) -> Coord:
    x, y = SourceOfSand
    obstacles = rocks.union(sands)
    if SourceOfSand in obstacles:
        raise SandSourceBlocked

    while not stop_condition(x, y):
        possible_steps = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]

        next_step = next(
            (coord for coord in possible_steps if coord not in obstacles), None
        )
        match next_step:
            case (int(), int()):
                x, y = next_step
                continue
            case None:
                return (x, y)
                # source is block if next step is None and current x, y is source

    return x, y


def keep_dropping_sand(
    rocks: set[Coord], times: Optional[int] = None, part_two=False
) -> set[Coord]:
    sands = set()

    counter = range(times) if times else itertools.repeat(None)
    for _ in counter:
        try:
            if part_two:
                new_sand = drop_sand_part_two(rocks, sands)
            else:
                new_sand = drop_sand(rocks, sands)
            sands.add(new_sand)
        except (FallToAbyss, SandSourceBlocked):
            break

    return sands


def visualize(rocks: set[Coord], sands: set[Coord]):
    obstacles = rocks.union(sands)
    min_x = min(x for (x, _) in obstacles)
    max_x = max(x for (x, _) in obstacles)

    min_y = min(y for (_, y) in obstacles)
    max_y = max(y for (_, y) in obstacles)

    def to_char(coord: Coord) -> str:
        if coord in rocks:
            return "#"
        return "o" if coord in sands else " "

    return "\n".join(
        "".join(to_char((x, y)) for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1)
    )


def part_one(rocks: set[Coord]) -> int:
    sands_until_fall_into_abyss = keep_dropping_sand(rocks=rocks)
    v = visualize(rocks=rocks, sands=sands_until_fall_into_abyss)
    print(v)
    return len(sands_until_fall_into_abyss)


def part_two(rocks: set[Coord]) -> int:
    sands_until_source_blocked = keep_dropping_sand(rocks=rocks, part_two=True)
    # v = visualize(rocks=rocks, sands=sands_until_source_blocked)
    # print(v)
    return len(sands_until_source_blocked)


if __name__ == "__main__":

    day = 14

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
