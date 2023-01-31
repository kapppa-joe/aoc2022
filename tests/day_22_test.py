import pytest

from solutions.day_22 import Facing, MonkeyMapCube, parse_path, parse_raw, part_one

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


def test_get_init_state(monkey_map):
    actual = monkey_map.get_init_state()
    expected = (8, 0, Facing.Right)

    assert expected == actual


def test_next_tile(monkey_map):
    x, y = (15, 8)

    test_cases = [
        (Facing.Down, (15, 9, Facing.Down)),
        (Facing.Left, (14, 8, Facing.Left)),
        (Facing.Right, (8, 8, Facing.Right)),
        (Facing.Up, (15, 11, Facing.Up)),
    ]

    for facing, expected in test_cases:
        actual = monkey_map.next_tile((x, y, facing))
        assert actual == expected

    example_cases = [
        ((11, 6, Facing.Right), (0, 6, Facing.Right)),  # example case point A -> B
        ((5, 7, Facing.Down), (5, 4, Facing.Down)),  # example case point C -> D
    ]

    for state, expected in example_cases:
        actual = monkey_map.next_tile(state)
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
        init_state = (8, 0, Facing.Right)

        actual = monkey_map.follow_path(path=input_path, init_state=init_state)

        assert expected == actual


def test_calc_password(monkey_map):
    expected = 6032
    actual = monkey_map.calc_password((7, 5, Facing.Right))

    assert actual == expected


def test_part_one(monkey_map):
    expected = 6032
    actual = part_one(monkey_map)

    assert actual == expected


def test_parse_cube():
    actual = parse_raw(example, as_cube=True)

    assert isinstance(actual, MonkeyMapCube)
    assert len(actual.faces) == 6
    assert actual.side_width == 4

    assert actual.faces[0] == (range(8, 12), range(0, 4))
    assert actual.faces[1] == (range(0, 4), range(4, 8))
    assert actual.faces[2] == (range(4, 8), range(4, 8))
    assert actual.faces[3] == (range(8, 12), range(4, 8))
    assert actual.faces[4] == (range(8, 12), range(8, 12))
    assert actual.faces[5] == (range(12, 16), range(8, 12))


@pytest.fixture(name="monkey_map_cube")
def make_monkey_map_cube():
    cube = parse_raw(example, as_cube=True)
    if not isinstance(cube, MonkeyMapCube):
        raise RuntimeError
    yield cube


def test_cube_get_neighbour_face(monkey_map_cube):
    actual = monkey_map_cube.get_neighbour_face(from_face=0, direction=Facing.Left)
    expected = (2, Facing.Up)

    assert actual == expected


def test_next_tile_for_cube(monkey_map_cube):
    test_cases = [
        [(11, 5, Facing.Right), (14, 8, Facing.Down)],
        [(10, 11, Facing.Down), (1, 7, Facing.Up)],
    ]

    for init_state, expected in test_cases:
        actual = monkey_map_cube.next_tile(state=init_state)
        assert actual == expected


@pytest.fixture(name="simple_cube")
def make_simple_cube():
    raw_input = """  ....
  ....
  ..
  ..
  ..
  ..
....
....

1L1R"""
    yield parse_raw(raw_input, as_cube=True)


def test_next_tile_for_another_cube_config(simple_cube):

    test_cases = [
        [(2, 0, Facing.Up), (2, 7, Facing.Up)],
        [(2, 0, Facing.Left), (1, 7, Facing.Up)],
        [(2, 0, Facing.Down), (2, 1, Facing.Down)],
        [(4, 1, Facing.Down), (3, 2, Facing.Left)],
        [(3, 5, Facing.Right), (5, 0, Facing.Left)],
        [(3, 7, Facing.Right), (4, 0, Facing.Down)],
        [(3, 7, Facing.Down), (3, 0, Facing.Down)],
    ]
    for init_state, expected in test_cases:
        actual = simple_cube.next_tile(state=init_state)
        assert actual == expected


def test_follow_path_for_cube(monkey_map_cube):
    test_cases = [
        ("10R5L5", (14, 10, Facing.Down)),
        ("10R5L5R", (14, 10, Facing.Left)),
        ("10R5L5R10L4R5L5", (6, 4, Facing.Up)),
    ]

    for (raw_path, expected) in test_cases:
        input_path = parse_path(raw_path)

        actual = monkey_map_cube.follow_path(path=input_path)

        assert actual == expected


def test_part_two(monkey_map_cube):
    expected = 5031
    actual = part_one(monkey_map_cube)

    assert actual == expected
