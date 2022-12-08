import pytest
import numpy as np

from solutions.day_08 import (
    parse_raw,
    part_one,
    part_two,
    trees_in_four_directions,
    visibility_from_four_directions,
    is_visible,
    count_trees_saw,
)

example = """30373
25512
65332
33549
35390"""


def test_parse_raw():
    expected = np.array(
        [
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0],
        ]
    )

    actual = parse_raw(example)

    assert (actual == expected).all()


def test_trees_in_four_directions():
    grid = parse_raw(example)

    coord = (2, 1)
    expected = [[3], [1, 2], [3, 5, 3], [5, 2]]
    actual = trees_in_four_directions(grid, *coord)
    assert actual == expected


def test_visibility_from_four_directions():
    grid = parse_raw(example)

    test_cases = [
        # top-left 5 is visible from the left and top.
        [
            (1, 1),
            [True, False, False, True],
        ],
        # top-middle 5 is visible from the top and right.
        [
            (2, 1),
            [True, True, False, False],
        ],
        # top-left 3 is visible from two edges.
        [
            (0, 0),
            [True, False, False, True],
        ],
    ]

    for coord, expected in test_cases:
        actual = visibility_from_four_directions(grid, *coord)
        assert actual == expected


is_visible_test_cases = [
    [(0, 0), True],
    [(0, 4), True],
    [(1, 4), True],
    [(4, 1), True],
    [(1, 1), True],
    [(1, 2), True],
    [(1, 3), False],
    [(2, 1), True],
    [(2, 2), False],
    [(2, 3), True],
    [(3, 1), False],
    [(3, 2), True],
    [(3, 3), False],
]


@pytest.mark.parametrize("coord, expected", is_visible_test_cases)
def test_is_visible(coord, expected):
    grid = parse_raw(example)

    actual = is_visible(grid, *coord)
    assert actual == expected


def test_part_one():
    grid = parse_raw(example)

    expected = 21

    actual = part_one(grid)

    assert actual == expected


def test_count_trees_saw():
    grid = parse_raw(example)

    coord = (2, 1)
    expected = [1, 2, 2, 1]
    actual = count_trees_saw(grid, *coord)
    assert actual == expected


def test_part_two():
    grid = parse_raw(example)

    expected = 8
    actual = part_two(grid)

    assert actual == expected
