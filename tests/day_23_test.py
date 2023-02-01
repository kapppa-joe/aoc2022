import pytest

from solutions.day_23 import (
    parse_raw,
    part_one,
    part_two,
    neighbour_coords,
    Direction,
    Coord,
    propose_move,
    resolve_next_turn,
    count_empty_ground,
    run_n_turns
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


@pytest.fixture(name="grove")
def make_example_grove():
    yield parse_raw(example)


@pytest.fixture(name="small_grove")
def make_small_example_grove():
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

    grove = parse_raw("""...\n.#.\n...""")
    coord = Coord(1, 1)

    for turn_number in range(4):
        actual = propose_move(coord=coord, grove=grove, turn_number=turn_number)
        expected = Coord(1, 1)

        assert actual == expected


def test_propose_move__change_priority_with_turn(small_grove):
    coord = Coord(2, 1)
    assert coord in small_grove

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
        actual = propose_move(coord=coord, grove=small_grove, turn_number=turn_number)

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

    for turn_number, grove in enumerate(each_turn_as_data[:-1]):
        expected = each_turn_as_data[turn_number + 1]
        actual = resolve_next_turn(grove=grove, turn_number=turn_number)

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

    for turn_number, grove in enumerate(each_turn_as_data[:-1]):
        expected = each_turn_as_data[turn_number + 1]
        actual = resolve_next_turn(grove=grove, turn_number=turn_number)

        assert actual == expected
        
def test_count_empty_ground():
    input_grove = parse_raw("""#..
...
..#""")
    expected = 7
    actual = count_empty_ground(input_grove)
    
    assert actual == expected
    
    
    # test for negative coords
    input_grove = frozenset([Coord(-1, -3), Coord(0,-1), Coord(0, 0), Coord(3, 1), Coord(0, 10)])
    # x is -1 to 3, y is -3 to 10. thus total area is 5 * 14.
    expected = (5 * 14) - 5
    actual = count_empty_ground(input_grove)
    assert actual == expected


def test_run_n_turns():
    initial_state = parse_raw("""..............
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
..............""")
    
    
    expected = parse_raw(""".......#......
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
..............""")

    actual = run_n_turns(grove=initial_state, n = 10)

    assert actual == expected

def test_part_one(grove):
    expected = 110
    actual = part_one(grove=grove)
    
    assert actual == expected
    

def test_part_two(grove):
    expected = 20
    actual = part_two(grove=grove)
    
    assert actual == expected