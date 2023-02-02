import pytest
import numpy as np
from solutions.day_24 import parse_raw, part_one, part_two, BlizzardBasin, Tile

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

    actual = basin.obstacles_for_turn_n(n=1)

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

    actual_obstacle_maps = basin.obstacles_for_turn_n(n=3)
    actual = basin.obstacle_map_as_string(actual_obstacle_maps)

    assert actual == expected


@pytest.fixture(name="example_basin")
def make_example_basin():
    yield parse_raw(example)


def test_obstacles_for_turn_n__complex_example(example_basin):

    each_turn = [
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

    for turn_number, expected in enumerate(each_turn):
        actual_obstacle_maps = example_basin.obstacles_for_turn_n(n=turn_number)
        actual = example_basin.obstacle_map_as_string(actual_obstacle_maps)

        assert actual == expected
