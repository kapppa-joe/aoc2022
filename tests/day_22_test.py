import pytest

from solutions.day_22 import (
    Facing,
    MonkeyMap,
    parse_path,
    parse_raw,
    part_one,
    part_two,
)

example = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


def test_parse_raw():
    monkey_map = parse_raw(example)

    assert monkey_map.map[0] == "        ...#    "
    assert monkey_map.map_size == (12, 16)  # height, width
    assert monkey_map.path == [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5]


@pytest.fixture(name="monkey_map")
def make_monkey_map():
    yield parse_raw(example)


def test_get_init_position(monkey_map):
    actual = monkey_map.get_init_position()
    expected = (8, 0, Facing.Right)

    assert expected == actual


def test_next_tile(monkey_map):
    x, y = (15, 8)

    test_cases = [
        (Facing.Down, (15, 9)),
        (Facing.Left, (14, 8)),
        (Facing.Right, (8, 8)),
        (Facing.Up, (15, 11)),
    ]

    for facing, expected in test_cases:
        actual = monkey_map.next_tile((x, y, facing))
        assert actual == expected

    example_cases = [
        ((11, 6, Facing.Right), (0, 6)),  # example case point A -> B
        ((5, 7, Facing.Down), (5, 4)),  # example case point C -> D
    ]

    for position, expected in example_cases:
        actual = monkey_map.next_tile(position)
        assert actual == expected


def test_follow_path(monkey_map):

    test_cases = [
        ("10", (10, 0, Facing.Right)),
        ("10R", (10, 0, Facing.Down)),
        ("10R5L5", (3, 5, Facing.Right)),
        ("10R5L5R", (3, 5, Facing.Down)),
        ("10R5L5R10", (3, 7, Facing.Down)),
        ("10R5L5R10", (3, 7, Facing.Down)),
        ("10R5L5R10L4R5L5", (7, 5, Facing.Right)),
    ]

    for (raw_path, expected) in test_cases:
        input_path = parse_path(raw_path)
        init_position = (8, 0, Facing.Right)

        actual = monkey_map.follow_path(path=input_path, init_pos=init_position)

        assert expected == actual


def test_calc_password(monkey_map):
    expected = 6032
    actual = monkey_map.calc_password((7, 5, Facing.Right))

    assert actual == expected


def test_part_one(monkey_map):
    expected = 6032
    actual = part_one(monkey_map)

    assert actual == expected
