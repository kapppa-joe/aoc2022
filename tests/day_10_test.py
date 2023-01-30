from solutions.day_10 import (parse_raw, part_one, part_two,
                              pixel_onoff_at_cycle, x_values_for_all_cycles)

example_small = """noop
addx 3
addx -5"""

example_large = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def test_parse_raw():
    expected = [(3, 3), (5, -5)]
    actual = parse_raw(example_small)

    assert actual == expected


def test_x_values_for_all_cycles():
    delta_x = parse_raw(example_small)

    expected = [1, 1, 1, 1, 4, 4, -1]

    actual = x_values_for_all_cycles(delta_x=delta_x)

    assert actual == expected


def test_x_values_for_all_cycles_larger_example():
    delta_x = parse_raw(example_large)

    actual = x_values_for_all_cycles(delta_x=delta_x)
    known_cycle_values = [
        (20, 21),
        (60, 19),
        (100, 18),
        (140, 21),
        (180, 16),
        (220, 18),
    ]
    for cycle, expected_value in known_cycle_values:
        assert actual[cycle] == expected_value


def test_part_one():
    input_data = parse_raw(example_large)
    expected = 13140

    actual = part_one(input_data)

    assert actual == expected


def test_pixel_onoff_at_cycle():
    delta_x = parse_raw(example_large)
    x_values = x_values_for_all_cycles(delta_x=delta_x)

    test_cases = [
        (1, True),
        (2, True),
        (3, False),
        (4, False),
        (5, True),
        (6, True),
        (7, False),
        (8, False),
        (9, True),
        (10, True),
        (11, False),
        (12, False),
    ]

    for cycle, expected in test_cases:
        actual = pixel_onoff_at_cycle(x_values=x_values, cycle=cycle)

        assert actual == expected


def test_part_two():

    input_data = parse_raw(example_large)

    expected = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""

    actual = part_two(input_data)

    assert actual == expected
