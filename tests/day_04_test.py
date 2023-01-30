from solutions.day_04 import find_overlap, parse_raw, part_one, part_two

example = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def test_parse_raw():
    expected = [
        [(2, 4), (6, 8)],
        [(2, 3), (4, 5)],
        [(5, 7), (7, 9)],
        [(2, 8), (3, 7)],
        [(6, 6), (4, 6)],
        [(2, 6), (4, 8)],
    ]

    actual = parse_raw(example)

    assert actual == expected


def test_find_overlap():
    input_cases = [
        [(2, 4), (6, 8)],
        [(2, 3), (4, 5)],
        [(5, 7), (7, 9)],
        [(2, 8), (3, 7)],
        [(6, 6), (4, 6)],
        [(2, 6), (4, 8)],
    ]

    expected = [None, None, (7, 7), (3, 7), (6, 6), (4, 6)]

    actual = [find_overlap(*pair) for pair in input_cases]

    assert actual == expected


def test_part_one():
    input_data = parse_raw(raw=example)
    expected = 2

    actual = part_one(data=input_data)

    assert actual == expected


def test_part_two():
    input_data = parse_raw(raw=example)
    expected = 4

    actual = part_two(data=input_data)

    assert actual == expected
