import pytest

from solutions.day_23 import (
    Coord,
    Direction,
    count_empty_ground,
    neighbour_coords,
    parse_raw,
    part_one,
    part_two,
    propose_move,
    resolve_next_turn,
    run_n_turns,
)

example = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

smaller_example = """.....
..##.
..#..
.....
..##.
....."""


def test_parse_raw():
    parsed_data = parse_raw(example)

    expected = example.count("#")
    actual = len(parsed_data)
    assert actual == expected

    assert (4, 0) in parsed_data
    assert (0, 0) not in parsed_data


@pytest.fixture(name="elves")
def make_example_elves():
    yield parse_raw(example)


@pytest.fixture(name="less_elves")
def make_small_example_elves():
    yield parse_raw(smaller_example)


def test_neighbour_coords():
    input_coord = Coord(0, 0)
    input_directions = [
        Direction.N,
        Direction.NE,
        Direction.E,
        Direction.SE,
        Direction.S,
        Direction.SW,
        Direction.W,
        Direction.NW,
    ]
    expected = [
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
    ]

    actual = neighbour_coords(input_coord, input_directions)

    assert actual == expected
    assert all(isinstance(elem, Coord) for elem in actual)


def test_propose_move__rest_if_no_neighbour():

    elves = parse_raw("""...\n.#.\n...""")
    coord = Coord(1, 1)

    for turn_number in range(4):
        actual = propose_move(coord=coord, elves=elves, turn_number=turn_number)
        expected = Coord(1, 1)

        assert actual == expected


def test_propose_move__change_priority_with_turn(less_elves):
    coord = Coord(2, 1)
    assert coord in less_elves

    test_cases = {
        # if turn number is 0, will consider north first
        0: Coord(2, 0),
        # if turn number is 1,2, will consider south/west first. only west is valid.
        1: Coord(1, 1),
        2: Coord(1, 1),
        # if turn number is 1,2, will consider east/north first. should pick north.
        3: Coord(2, 0),
        4: Coord(2, 0),
    }
    for turn_number, expected in test_cases.items():
        actual = propose_move(coord=coord, elves=less_elves, turn_number=turn_number)

        assert actual == expected


def test_resolve_next_turn__smaller_example():

    each_turn_from_example = [
        """.....
..##.
..#..
.....
..##.
.....""",
        """..##.
.....
..#..
...#.
..#..
.....""",
        """.....
..##.
.#...
....#
.....
..#..""",
        """..#..
....#
#....
....#
.....
..#..""",
    ]

    each_turn_as_data = [parse_raw(raw_str) for raw_str in each_turn_from_example]

    for turn_number, elves in enumerate(each_turn_as_data[:-1]):
        expected = each_turn_as_data[turn_number + 1]
        actual = resolve_next_turn(elves=elves, turn_number=turn_number)

        assert actual == expected


def test_resolve_next_turn__larger_example():

    each_turn_from_example = [
        """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............""",
        """..............
.......#......
.....#...#....
...#..#.#.....
.......#..#...
....#.#.##....
..#..#.#......
..#.#.#.##....
..............
....#..#......
..............
..............""",
        """..............
.......#......
....#.....#...
...#..#.#.....
.......#...#..
...#..#.#.....
.#...#.#.#....
..............
..#.#.#.##....
....#..#......
..............
..............""",
        """..............
.......#......
.....#....#...
..#..#...#....
.......#...#..
...#..#.#.....
.#..#.....#...
.......##.....
..##.#....#...
...#..........
.......#......
..............""",
        """..............
.......#......
......#....#..
..#...##......
...#.....#.#..
.........#....
.#...###..#...
..#......#....
....##....#...
....#.........
.......#......
..............""",
        """.......#......
..............
..#..#.....#..
.........#....
......##...#..
.#.#.####.....
...........#..
....##..#.....
..#...........
..........#...
....#..#......
..............""",
    ]

    each_turn_as_data = [parse_raw(raw_str) for raw_str in each_turn_from_example]

    for turn_number, elves in enumerate(each_turn_as_data[:-1]):
        expected = each_turn_as_data[turn_number + 1]
        actual = resolve_next_turn(elves=elves, turn_number=turn_number)

        assert actual == expected


def test_count_empty_ground():
    input_elves = parse_raw(
        """#..
...
..#"""
    )
    expected = 7
    actual = count_empty_ground(input_elves)

    assert actual == expected

    # test for negative coords
    input_elves = frozenset(
        [Coord(-1, -3), Coord(0, -1), Coord(0, 0), Coord(3, 1), Coord(0, 10)]
    )
    # x is -1 to 3, y is -3 to 10. thus total area is 5 * 14.
    expected = (5 * 14) - 5
    actual = count_empty_ground(input_elves)
    assert actual == expected


def test_run_n_turns():
    initial_state = parse_raw(
        """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""
    )

    expected = parse_raw(
        """.......#......
...........#..
..#.#..#......
......#.......
...#.....#..#.
.#......##....
.....##.......
..#........#..
....#.#..#....
..............
....#..#..#...
.............."""
    )

    actual = run_n_turns(elves=initial_state, n=10)

    assert actual == expected


def test_part_one(elves):
    expected = 110
    actual = part_one(elves=elves)

    assert actual == expected


def test_part_two(elves):
    expected = 20
    actual = part_two(elves=elves)

    assert actual == expected
