import pytest

from solutions.day_12 import (
    find_shortest_path_length,
    parse_raw,
    part_one,
    part_two,
    reachable_neighbours,
)

example = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def test_parse_raw():
    expected = (
        (0, 0),
        (5, 2),
        [
            [0, 0, 1, 16, 15, 14, 13, 12],
            [0, 1, 2, 17, 24, 23, 23, 11],
            [0, 2, 2, 18, 25, 25, 23, 10],
            [0, 2, 2, 19, 20, 21, 22, 9],
            [0, 1, 3, 4, 5, 6, 7, 8],
        ],
    )

    actual = parse_raw(example)

    assert actual == expected


@pytest.fixture(name="example_grid", scope="session")
def create_example_grid():
    start, dest, grid = parse_raw(example)
    yield grid


def test_reachable_neighbours(example_grid):
    test_cases = [
        [(0, 0), [(0, 1), (1, 0)]],
        # top b, can go back to a or c
        [(2, 0), [(1, 0), (2, 1)]],
        # top q, can go to p, r or b
        [(3, 0), [(4, 0), (3, 1), (2, 0)]],
        # second row y, can go to p r x z
        [(4, 1), [(5, 1), (4, 2), (3, 1), (4, 0)]],
        # third row a, can only go up or down
        [(0, 2), [(0, 3), (0, 1)]],
        # last row a, can go up or right
        [(0, 4), [(1, 4), (0, 3)]],
    ]

    for curr_coord, expected in test_cases:
        actual = reachable_neighbours(curr_coord=curr_coord, grid=example_grid)
        assert sorted(actual) == sorted(expected)


def test_reachable_neighbours_reverse(example_grid):
    """reverse the reachable function to get path from dest to start"""
    test_cases = [
        # third row z, can go to y or dest only
        [(4, 2), [(4, 1), (5, 2)]],
        # second row y, can go to x or z only
        [(4, 1), [(5, 1), (4, 2)]],
        # top q, can go to p or r only
        [(3, 0), [(4, 0), (3, 1)]],
        # top b, can go to a, c, or q (as this is reverse)
        [(2, 0), [(1, 0), (2, 1), (3, 0)]],
    ]

    for curr_coord, expected in test_cases:
        actual = reachable_neighbours(
            curr_coord=curr_coord, grid=example_grid, reversed=True
        )
        assert sorted(actual) == sorted(expected)


def test_part_one():
    start, destination, grid = parse_raw(example)
    expected = 31

    actual = part_one(start=start, destination=destination, grid=grid)

    assert actual == expected


def test_reverse_find_path():
    start, destination, grid = parse_raw(example)
    expected = 31

    actual = find_shortest_path_length(
        start=destination,
        stop_criteria=lambda coord, _: coord == start,
        grid=grid,
        reversed=True,
    )

    assert actual == expected


def test_part_two():
    _, destination, grid = parse_raw(example)
    expected = 29

    actual = part_two(destination=destination, grid=grid)

    assert actual == expected
