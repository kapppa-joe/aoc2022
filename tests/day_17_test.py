import pytest
import numpy as np
from solutions.day_17 import (
    parse_raw,
    part_one,
    part_two,
    Cave,
    Rock,
    Jet,
    RockComeToRest,
)

example = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def test_jet():
    jet = Jet(pattern=example)

    assert "".join(jet.take(3)) == ">>>"
    assert "".join(jet.take(3)) == "<<>"
    assert "".join(jet.take(30)) == "<>><<<>><>>><<<>>><<<><<<>><>>"
    assert "".join(jet.take(10)) == "<<>>>>><<>"  # should seemlessly loopback

    jet2 = Jet(pattern=example)

    # try iter through the end one by one
    i = 0
    expected = example + example[0:5]
    try:
        for jet_direction in jet2:
            assert jet_direction == expected[i]
            assert jet2.counter == i + 1
            i += 1
            if i >= len(expected):
                raise RockComeToRest
    except RockComeToRest:
        pass

    take_5_more = jet2.take(5)
    assert "".join(take_5_more) == example[5:10]

    take_45_more_again = jet2.take(45)
    assert "".join(take_45_more_again) == example[10:] + example[0:15]


@pytest.fixture(name="cave")
def make_example_cave():
    yield parse_raw(raw=example)


def test_parse_raw():
    actual = parse_raw(raw=example)
    assert isinstance(actual, Cave)
    assert actual.jet.pattern == example


def test_cave_basic(cave):
    assert cave.rock_tower_height == 0
    assert cave.rest_rock_count == 0


def test_make_rock(cave):
    rock = cave.make_next_rock()

    assert rock.kind == 0
    assert cave.current_rock_pos == (3, 2)
    assert (rock.array == [[1, 1, 1, 1]]).all()


def test_rocks_max_x():
    rocks = [Rock(kind=kind) for kind in range(5)]
    expected = [3, 4, 4, 6, 5]
    actual = [rock.max_x() for rock in rocks]

    assert actual == expected


def test_rock_left_right_movement(cave):
    rock = cave.make_next_rock()

    cave.blow_rock(">")
    assert cave.current_rock_pos == (3, 3)

    cave.blow_rock(">")
    assert cave.current_rock_pos == (3, 3)

    cave.blow_rock("<")
    assert cave.current_rock_pos == (3, 2)

    cave.blow_rock("<")
    assert cave.current_rock_pos == (3, 1)

    cave.blow_rock("<")
    assert cave.current_rock_pos == (3, 0)

    cave.blow_rock("<")
    assert cave.current_rock_pos == (3, 0)

    cave.blow_rock(">")
    assert cave.current_rock_pos == (3, 1)


def test_simulate_first_rock_fall(cave):
    cave.make_next_rock()
    cave.fall_until_rock_rest()

    assert cave.rock_tower_height == 1
    assert cave.rest_rock_count == 1
    assert cave.array.tolist() == [
        [0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_select_cave_by_rock_shape(cave):
    # simulate the case of 2nd rock
    cave.array = np.array(
        [
            [0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
    )
    actual = cave.select_area_by_rock_shape(pos=(0, 2), kind=1)  # x=2, y=0
    expected = [
        [1, 1, 1],
        [0, 0, 0],
        [0, 0, 0],
    ]
    assert actual.tolist() == expected

    cave.array = np.array(
        [
            [0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ]
    )
    actual = cave.select_area_by_rock_shape(pos=(1, 2), kind=1)  # x=2, y=1
    expected = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]

    assert actual.tolist() == expected

    actual = cave.select_area_by_rock_shape(pos=(0, 3), kind=4)  # x=3, y=0
    expected = [
        [1, 1],
        [1, 0],
    ]

    assert actual.tolist() == expected


def test_simulate_second_rock_fall(cave):
    cave.make_next_rock()
    cave.fall_until_rock_rest()

    rock = cave.make_next_rock()
    assert rock.kind == 1
    assert rock.shape == (3, 3)

    cave.fall_until_rock_rest()
    assert cave.rock_tower_height == 4
    assert cave.rest_rock_count == 2
    assert cave.array.tolist() == [
        [0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
