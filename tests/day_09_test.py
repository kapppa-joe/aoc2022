from solutions.day_09 import (
    is_touching,
    new_tail_position,
    parse_raw,
    part_one,
    part_two,
    trace_head_position,
)

example = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def test_parse_raw():
    expected = [
        ("R", 4),
        ("U", 4),
        ("L", 3),
        ("D", 1),
        ("R", 4),
        ("D", 1),
        ("L", 5),
        ("R", 2),
    ]

    actual = parse_raw(example)

    assert actual == expected


def test_trace_head_position():
    input_data = parse_raw(example)[0:4]

    expected = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (3, 4),
        (2, 4),
        (1, 4),
        (1, 3),
    ]

    actual = trace_head_position(input_data)
    assert actual == expected


def test_is_touching():
    test_cases = [
        [(0, 0), (0, 0), True],
        [(0, 0), (0, 2), False],
        [(0, 0), (0, 1), True],
        [(3, 5), (2, 4), True],
        [(3, 5), (2, 3), False],
        [(3, 5), (4, 6), True],
        [(3, 5), (3, 4), True],
        [(3, 5), (2, 6), True],
        [(3, 5), (4, 4), True],
        [(3, 5), (4, 3), False],
    ]

    for head_pos, tail_pos, expected in test_cases:
        actual = is_touching(head_pos, tail_pos)

        assert actual == expected


def test_new_tail_position():
    test_cases = [
        # tail pos, head pos, new tail pos
        [(0, 0), (0, 0), (0, 0)],
        [(0, 0), (1, 0), (0, 0)],
        [(0, 0), (2, 0), (1, 0)],
        [(1, 0), (3, 0), (2, 0)],
        [(3, 0), (4, 1), (3, 0)],
        [(3, 0), (4, 2), (4, 1)],
        [(4, 3), (3, 4), (4, 3)],
        [(4, 3), (2, 4), (3, 4)],
    ]

    for tail_pos, head_pos, expected in test_cases:
        actual = new_tail_position(head_pos=head_pos, tail_pos=tail_pos)

        assert actual == expected


def test_part_one():
    input_data = parse_raw(example)

    expected = 13
    actual = part_one(input_data)

    assert actual == expected


def test_part_two_small_example():
    input_data = parse_raw(example)

    expected = 1
    actual = part_two(input_data)

    assert actual == expected


def test_part_two_larger_example():
    larger_example = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
    input_data = parse_raw(larger_example)

    expected = 36
    actual = part_two(input_data)

    assert actual == expected
