import pytest
from solutions.day_20 import parse_raw, part_one, part_two, PartTwoMagicNum


example = """1
2
-3
3
-2
0
4"""


def test_parse_raw():
    actual = parse_raw(example)

    assert actual._boxes == (1, 2, -3, 3, -2, 0, 4)


@pytest.fixture(name="box")
def make_example_box():
    yield parse_raw(example)


def test_get_index(box):
    assert box[1] == 2
    assert box[2] == -3


def test_rotate_number(box):
    initial_list = (1, 2, -3, 3, -2, 0, 4)

    expected = [
        (2, 1, -3, 3, -2, 0, 4),
        (1, -3, 2, 3, -2, 0, 4),
        (1, 2, 3, -2, -3, 0, 4),
        (1, 2, -2, -3, 0, 3, 4),
        (1, 2, -3, 0, 3, 4, -2),
        (1, 2, -3, 0, 3, 4, -2),
        (1, 2, -3, 4, 0, 3, -2),
    ]

    list = initial_list[:]
    for i, n in enumerate(initial_list):
        list = box.rotate_number(token_list=list, token=n, move=n)
        assert list == expected[i]


def test_unbox_numbers(box):
    test_cases = [
        [(0, 1, 2, 3, 4, 5, 6), (1, 2, -3, 3, -2, 0, 4)],
        [(1, 3, 5, 2, 4, 6, 0), (2, 3, 0, -3, -2, 4, 1)],
    ]

    for token_list, expected in test_cases:
        actual = box.unbox_numbers(token_list=token_list)
        assert actual == expected


def test_mix_number(box):
    initial_token_list = box.initial_tokens()
    token_list = initial_token_list

    expected = [
        (2, 1, -3, 3, -2, 0, 4),
        (1, -3, 2, 3, -2, 0, 4),
        (1, 2, 3, -2, -3, 0, 4),
        (1, 2, -2, -3, 0, 3, 4),
        (1, 2, -3, 0, 3, 4, -2),
        (1, 2, -3, 0, 3, 4, -2),
        (1, 2, -3, 4, 0, 3, -2),
    ]

    for token in range(7):
        token_list = box.mix_number(token_list=token_list, token=token)
        unboxed = box.unbox_numbers(token_list=token_list)
        assert unboxed == expected[token]


def test_mix_whole_list(box):
    expected_boxed = (0, 1, 2, 6, 5, 3, 4)
    expected_unboxed = (1, 2, -3, 4, 0, 3, -2)

    actual_boxed = box.mix_whole_list()
    actual_unboxed = box.unbox_numbers(token_list=actual_boxed)

    assert actual_boxed == expected_boxed
    assert actual_unboxed == expected_unboxed


def test_nth_after_zero(box):
    token_list_after_mixed = box.mix_whole_list()
    assert box.nth_after_zero(token_list=token_list_after_mixed, n=1000) == 4
    assert box.nth_after_zero(token_list=token_list_after_mixed, n=2000) == -3
    assert box.nth_after_zero(token_list=token_list_after_mixed, n=3000) == 2


def test_part_one(box):
    expected = 3
    actual = part_one(box)
    assert actual == expected


def in_same_order(list_a, list_b) -> bool:
    zero_pos_diff = list_b.index(0) - list_a.index(0)
    rotated_list_b = list_b[zero_pos_diff:] + list_b[:zero_pos_diff]
    return list_a == rotated_list_b


def test_part_two_mix_list(box):
    box._boxes = tuple(num * PartTwoMagicNum for num in box._boxes)

    expected = [
        (811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612),
        (0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153),
        (0, 2434767459, 1623178306, 3246356612, -2434767459, -1623178306, 811589153),
        (0, 811589153, 2434767459, 3246356612, 1623178306, -1623178306, -2434767459),
        (0, 1623178306, -2434767459, 811589153, 2434767459, 3246356612, -1623178306),
        (0, 811589153, -1623178306, 1623178306, -2434767459, 3246356612, 2434767459),
        (0, 811589153, -1623178306, 3246356612, -2434767459, 1623178306, 2434767459),
        (0, -2434767459, 2434767459, 1623178306, -1623178306, 811589153, 3246356612),
        (0, 1623178306, 3246356612, 811589153, -2434767459, 2434767459, -1623178306),
        (0, 811589153, 1623178306, -2434767459, 3246356612, 2434767459, -1623178306),
        (0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153),
    ]

    for times in range(11):
        token_after_mix = box.mix_whole_list(times=times)
        actual_unboxed = box.unbox_numbers(token_after_mix)
        assert in_same_order(actual_unboxed, expected[times])


def test_part_two(box):
    expected = 1623178306
    actual = part_two(box)

    assert actual == expected
