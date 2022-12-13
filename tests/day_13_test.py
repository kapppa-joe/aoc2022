from solutions.day_13 import parse_raw, in_right_order, part_one, part_two

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


def test_parse_raw():
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
    actual = parse_raw(example)

    assert actual == expected


def test_in_right_order():
    expected_results = [True, True, False, True, False, True, False, False]

    pairs = parse_raw(example)

    for i, pair in enumerate(pairs):
        actual = in_right_order(*pair)
        assert actual == expected_results[i]


def test_part_one():
    pairs = parse_raw(example)
    expected = 13

    actual = part_one(pairs)

    assert actual == expected
