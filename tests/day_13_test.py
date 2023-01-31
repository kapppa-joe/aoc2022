import pytest

from solutions.day_13 import (
    add_divider_packets,
    compare_packets,
    parse_packet_string,
    parse_raw,
    part_one,
    part_two,
    sort_packet_strings,
)

example = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def test_parse_packet_string():
    expected = [
        ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
        ([[1], [2, 3, 4]], [[1], 4]),
        ([9], [[8, 7, 6]]),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
        ([7, 7, 7, 7], [7, 7, 7]),
        ([], [3]),
        ([[[]]], [[]]),
        ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]),
    ]
    for i, str_pair in enumerate(parse_raw(example)):
        actual = (parse_packet_string(str_pair[0]), parse_packet_string(str_pair[1]))
        assert actual == expected[i]


def test_compare_packets():
    expected_results = [-1, -1, 1, -1, 1, -1, 1, 1]

    pairs = [
        (parse_packet_string(left), parse_packet_string(right))
        for (left, right) in parse_raw(example)
    ]

    for i, pair in enumerate(pairs):
        actual = compare_packets(*pair)
        assert actual == expected_results[i]


def test_part_one():
    pairs = parse_raw(example)
    expected = 13

    actual = part_one(pairs)

    assert actual == expected


def test_add_divider_packets():
    pairs = parse_raw(example)

    expected = [
        "[1,1,3,1,1]",
        "[1,1,5,1,1]",
        "[[1],[2,3,4]]",
        "[[1],4]",
        "[9]",
        "[[8,7,6]]",
        "[[4,4],4,4]",
        "[[4,4],4,4,4]",
        "[7,7,7,7]",
        "[7,7,7]",
        "[]",
        "[3]",
        "[[[]]]",
        "[[]]",
        "[1,[2,[3,[4,[5,6,7]]]],8,9]",
        "[1,[2,[3,[4,[5,6,0]]]],8,9]",
        "[[2]]",
        "[[6]]",
    ]

    actual = add_divider_packets(pairs)

    assert actual == expected


@pytest.fixture(name="part_two_packet_strings")
def make_part_two_input():
    pairs = parse_raw(example)
    part_two_packet_strings = add_divider_packets(pairs)
    yield part_two_packet_strings


def test_sort_packet_strings(part_two_packet_strings):
    expected = """[]
[[]]
[[[]]]
[1,1,3,1,1]
[1,1,5,1,1]
[[1],[2,3,4]]
[1,[2,[3,[4,[5,6,0]]]],8,9]
[1,[2,[3,[4,[5,6,7]]]],8,9]
[[1],4]
[[2]]
[3]
[[4,4],4,4]
[[4,4],4,4,4]
[[6]]
[7,7,7]
[7,7,7,7]
[[8,7,6]]
[9]""".split(
        "\n"
    )

    actual = sort_packet_strings(part_two_packet_strings)

    assert actual == expected


def test_part_two(part_two_packet_strings):
    expected = 140
    actual = part_two(part_two_packet_strings)

    assert actual == expected
