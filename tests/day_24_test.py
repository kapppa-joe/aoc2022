import numpy as np
import pytest

from solutions.day_24 import BlizzardBasin, Tile, parse_raw, part_one, part_two

simple_example = """#.######
#>..<^.#
#......#
#.v....#
#......#
######.#"""

example = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""


def test_parse_raw():
    basin = parse_raw(simple_example)
    assert isinstance(basin, BlizzardBasin)

    wall_map = basin.obstacle_maps[Tile.Wall]
    assert wall_map[0, 0] == True
    assert wall_map[0, 1] == False
    assert wall_map[0, 2] == True

    blizzard_up_map = basin.obstacle_maps[Tile.BlizzardUp]
    assert blizzard_up_map[1, 5] == True
    assert np.count_nonzero(blizzard_up_map) == 1

    blizzard_down_map = basin.obstacle_maps[Tile.BlizzardDown]
    assert blizzard_down_map[3, 2] == True
    assert np.count_nonzero(blizzard_down_map) == 1

    blizzard_right_map = basin.obstacle_maps[Tile.BlizzardRight]
    assert blizzard_right_map[1, 1] == True
    assert np.count_nonzero(blizzard_right_map) == 1

    blizzard_left_map = basin.obstacle_maps[Tile.BlizzardLeft]
    assert blizzard_left_map[1, 4] == True
    assert np.count_nonzero(blizzard_left_map) == 1


def test_convert_map_back_to_str():
    basin = parse_raw(simple_example)

    expected = simple_example
    actual = basin.obstacle_map_as_string(obstacle_maps=basin.obstacle_maps)

    assert actual == expected


def test_obstacles_for_turn_1():
    basin = parse_raw(simple_example)

    actual = basin.make_obstacle_maps_for_turn_n(n=1)

    # wall doesn't change
    wall_map = actual[Tile.Wall]
    assert (wall_map == basin.obstacle_maps[Tile.Wall]).all()

    # blizzard should move
    blizzard_right_map = actual[Tile.BlizzardRight]
    assert blizzard_right_map[1, 1] == False
    assert blizzard_right_map[1, 2] == True

    blizzard_up_map = actual[Tile.BlizzardUp]
    assert blizzard_up_map[1, 5] == False
    assert blizzard_up_map[4, 5] == True

    blizzard_down_map = actual[Tile.BlizzardDown]
    assert blizzard_down_map[3, 2] == False
    assert blizzard_down_map[4, 2] == True

    blizzard_left_map = actual[Tile.BlizzardLeft]
    assert blizzard_left_map[1, 4] == False
    assert blizzard_left_map[1, 3] == True


def test_obstacles_for_turn_3():
    basin = parse_raw(simple_example)
    expected = """#.######
#<..>..#
#.v..^.#
#......#
#......#
######.#"""

    actual_obstacle_maps = basin.make_obstacle_maps_for_turn_n(n=3)
    actual = basin.obstacle_map_as_string(actual_obstacle_maps)

    assert actual == expected


@pytest.fixture(name="basin")
def make_basin():
    yield parse_raw(example)


ExampleBasinFirst5Turns = [
    """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""",
    """#.######
#.>3.<.#
#<..<<.#
#>2.22.#
#>v..^<#
######.#""",
    """#.######
#.2>2..#
#.^22^<#
#.>2.^>#
#.>..<.#
######.#""",
    """#.######
#<^<22.#
#.2<.2.#
#><2>..#
#..><..#
######.#""",
    """#.######
#.<..22#
#<<.<..#
#<2.>>.#
#.^22^.#
######.#""",
]


def test_make_obstacle_maps_for_turn_n__complex_example(basin):

    for turn_number, expected in enumerate(ExampleBasinFirst5Turns):
        actual_obstacle_maps = basin.make_obstacle_maps_for_turn_n(n=turn_number)
        actual = basin.obstacle_map_as_string(actual_obstacle_maps)

        assert actual == expected


def test_obstacle_forecast_cache_working(basin):
    vertical_repeat_num = basin.inner_height
    horizontal_repeat_num = basin.inner_width

    def gcd(a, b):
        if b == 0:
            return a
        return gcd(b, a % b)

    lcm = (
        vertical_repeat_num
        * horizontal_repeat_num
        // gcd(vertical_repeat_num, horizontal_repeat_num)
    )

    for turn_number in range(lcm):
        expected = basin.make_obstacle_maps_for_turn_n(n=turn_number)
        actual = basin.make_obstacle_maps_for_turn_n(n=(turn_number + lcm))

        for obstacle_type in expected:
            assert (actual[obstacle_type] == expected[obstacle_type]).all()


def test_start_and_goal(basin):
    expected = (0, 1)  # y, x
    actual = basin.start

    assert actual == expected

    expected = (5, 6)  # y, x
    actual = basin.goal

    assert actual == expected


def test_next_turn_moves(basin):
    raw_input = """.E......
........
........
........
........
........"""

    raw_expected = """EEE.....
.E......
........
........
........
........"""

    input_state = basin.string_to_combined_map(raw_input).astype(bool)
    expected = basin.string_to_combined_map(raw_expected).astype(bool)

    actual = basin.next_turn_moves(current_locations=input_state)

    assert (actual == expected).all()


def test_next_turn_moves__multiple_locations(basin):
    raw_input = """.E.E....
........
...E..E.
....E...
.E....E.
........"""

    raw_expected = """EEEEE...
.E.E..E.
..EEEEEE
.E.EEEE.
EEE.EEEE
.E....E."""

    input_state = basin.string_to_combined_map(raw_input).astype(bool)
    expected = basin.string_to_combined_map(raw_expected).astype(bool)

    actual = basin.next_turn_moves(current_locations=input_state)

    assert (actual == expected).all()


def test_simulate_next_turn(basin):
    raw_input = """.E.E....
........
...E..E.
....E...
.E....E.
........"""

    next_turn_obstacles = basin.make_obstacle_maps_for_turn_n(n=1)
    # """ #.######
    #     #.>3.<.#
    #     #<..<<.#
    #     #>2.22.#
    #     #>v..^<#
    #     ######.#"""

    raw_expected = """.E......
.E....E.
..EE..E.
...E..E.
....E...
......E."""

    input_state = basin.string_to_combined_map(raw_input).astype(bool)
    expected = basin.string_to_combined_map(raw_expected).astype(bool)

    actual = basin.simulate_next_turn(
        current_locations=input_state, next_turn_obstacles=next_turn_obstacles
    )

    assert (actual == expected).all()


def test_bfs(basin):
    expected = 18
    actual = basin.bfs(start=basin.start, goal=basin.goal, starting_turn=0)

    assert actual == expected


def test_part_one(basin):
    expected = 18
    actual = part_one(basin)

    assert actual == expected


def test_part_two(basin):
    expected = 54
    actual = part_two(basin)

    assert actual == expected
