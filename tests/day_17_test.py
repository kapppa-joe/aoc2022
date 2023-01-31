import numpy as np
import pytest

from solutions.day_17 import (
    Cave,
    Jet,
    Rock,
    RockComeToRest,
    parse_raw,
    part_one,
    part_two,
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
            assert jet2.counter == (i + 1) % len(example)
            i += 1
            if i >= len(expected):
                raise RockComeToRest
    except RockComeToRest:
        pass

    take_5_more = jet2.take(5)
    assert "".join(take_5_more) == example[5:10]
    assert jet2.counter == 10

    take_45_more_again = jet2.take(45)
    assert "".join(take_45_more_again) == example[10:] + example[0:15]
    assert jet2.counter == 15


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


def test_simulate_third_rock_fall(cave):
    for _ in range(2):
        cave.make_next_rock()
        cave.fall_until_rock_rest()

    rock = cave.make_next_rock()
    assert rock.kind == 2

    cave.fall_until_rock_rest()
    assert cave.rock_tower_height == 6
    assert cave.rest_rock_count == 3
    assert cave.array.tolist() == [
        [0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_simulate_rock_fall_3(cave):
    cave.simulate_rock_fall(number_of_rocks=3)
    assert cave.rock_tower_height == 6


test_case_for_part_one_simulation = [
    [3, 6],
    [4, 7],
    [5, 9],
    [6, 10],
    [7, 13],
    [8, 15],
    [9, 17],
    [10, 17],
]


@pytest.mark.parametrize("n, expected", test_case_for_part_one_simulation)
def test_simulate_rock_fall_part_one(cave, n, expected):
    cave.simulate_rock_fall(number_of_rocks=n)
    assert cave.rock_tower_height == expected


def test_part_one():
    expected = 3068

    cave = parse_raw(example)
    actual = part_one(cave=cave)

    assert actual == expected


def test_capture_upper_rows_shape(cave: Cave):
    cave.array = np.array(
        # actual tower is UPSIDE DOWN. last row here is the top of tower.
        [
            [0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 1],
            # 6th col got stone at below row. upwards should be omitted.
            [0, 1, 0, 0, 0, 1, 0],  # 0th bit.
            [1, 0, 0, 1, 0, 0, 1],
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 0, 1],
            [0, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1],  # 7th bit. 0~7 are packed together.
            [1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 1, 0, 1],  # 9th bit . this is the top of tower
        ]
    )

    cave.update_rock_tower_height()

    # fmt: off
    expected = [
        0b1001010, 0b10001000, 0b100100, 0b1101110, 1, 0b10000000, 0b1011111, #0~7 bit . each bit is 8 floor of a column 
        0b10000000, 0b10000000, 0b10000000, 0, 0b11000000, 0, 0b11000000] #8~9 bits
    # fmt: on
    actual = cave.capture_upper_rows_shape()
    assert actual == expected


def test_find_tower_height_by_repeat_pattern(cave):
    expected = 3068

    cave = parse_raw(example)
    actual = cave.find_tower_height_by_repeat_pattern(number_of_rocks=2022)

    assert actual == expected

    # part two
    expected = 1514285714288

    cave = parse_raw(example)
    actual = cave.find_tower_height_by_repeat_pattern(number_of_rocks=1000000000000)

    assert actual == expected


def test_part_two():
    expected = 1514285714288

    cave = parse_raw(example)
    actual = part_two(cave)

    assert actual == expected
