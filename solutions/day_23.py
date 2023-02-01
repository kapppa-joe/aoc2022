import functools
from collections import Counter
from enum import Enum
from typing import NamedTuple, TypeAlias


class Direction(tuple, Enum):
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)
    W = (-1, 0)
    NW = (-1, -1)

    @functools.cached_property
    def AllDirections(self):
        return [*Direction]

    @functools.cached_property
    def prev(self):
        index = self.AllDirections.index(self.value)
        prev_index = (index - 1 + len(AllDirections)) % len(AllDirections)
        return AllDirections[prev_index]

    @functools.cached_property
    def succ(self):
        index = self.AllDirections.index(self.value)
        succ_index = (index + 1 + len(AllDirections)) % len(AllDirections)
        return AllDirections[succ_index]

    @functools.cached_property
    def with_two_adjs(self):
        """helper method to return a direction with its two adjacents
        >>> Direction.N.with_two_adjs
        [Direction.NW, Direction.N, Direction.NE]
        """
        return (self.prev, self, self.succ)


AllDirections = [*Direction]


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: tuple[int, int] | Direction) -> "Coord":
        """helper method for easy vector summing
        >>> Coord(1, 3) + Coord(2, 3)
        Coord(3, 6)
        """
        if isinstance(other, Direction) or isinstance(other, tuple):
            dx, dy = other
            return Coord(self.x + dx, self.y + dy)
        else:
            raise ValueError("Can only add a coordinate to a pair of int")

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"


class Tile(str, Enum):
    Elf = "#"
    Empty = "."


Elves: TypeAlias = frozenset[Coord]


def parse_raw(raw: str) -> Elves:
    lines = raw.splitlines()
    width = len(lines[0])
    height = len(lines)

    elves_positions = (
        Coord(x, y)
        for y in range(height)
        for x in range(width)
        if lines[y][x] == Tile.Elf
    )

    return frozenset(elves_positions)


def neighbour_coords(coord: Coord, directions: list[Direction]) -> list[Coord]:
    return [coord + dir for dir in directions]


def propose_move(coord: Coord, elves: Elves, turn_number: int) -> Coord:
    neighbour_elves = {dir for dir in AllDirections if (coord + dir) in elves}
    if not neighbour_elves:
        return coord

    rule_order = (Direction.N, Direction.S, Direction.W, Direction.E)
    for i in range(4):
        direction_to_try = rule_order[(turn_number + i) % 4]
        got_elves_for_this_direction = neighbour_elves.intersection(
            direction_to_try.with_two_adjs
        )
        if got_elves_for_this_direction:
            continue
        return coord + direction_to_try

    return coord


def resolve_next_turn(elves: Elves, turn_number: int) -> Elves:
    all_elves = list(elves)
    all_proposed_moves = {
        elf: propose_move(coord=elf, elves=elves, turn_number=turn_number)
        for elf in all_elves
    }
    counts = Counter(all_proposed_moves.values())

    resolved_moves = [
        proposed_move if counts[proposed_move] == 1 else current_position
        for current_position, proposed_move in all_proposed_moves.items()
    ]
    convert_to_set = frozenset(resolved_moves)

    if len(convert_to_set) != len(all_elves):
        raise RuntimeError("some elves disappeared! a bug caught")

    return convert_to_set


def count_empty_ground(elves: Elves) -> int:
    all_elves = list(elves)
    min_x, min_y, max_x, max_y = [*all_elves[0], *all_elves[0]]
    for elf in all_elves[1:]:
        min_x = min(elf.x, min_x)
        min_y = min(elf.y, min_y)
        max_x = max(elf.x, max_x)
        max_y = max(elf.y, max_y)
    total_area = (max_x - min_x + 1) * (max_y - min_y + 1)

    return total_area - len(all_elves)


def run_n_turns(elves: Elves, n: int) -> Elves:
    state = elves
    for i in range(n):
        state = resolve_next_turn(elves=state, turn_number=i)
    return state


def part_one(elves: Elves) -> int:
    final_state = run_n_turns(elves, 10)
    return count_empty_ground(final_state)


def part_two(elves: Elves) -> int:
    prev_state = None
    curr_state = elves
    i = 0
    while prev_state != curr_state:
        prev_state = curr_state
        curr_state = resolve_next_turn(elves=curr_state, turn_number=i)
        i += 1
    return i


if __name__ == "__main__":

    day = 23

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
