import pytest

from solutions.day_14 import (
    SandSourceBlocked,
    all_points_in_line,
    drop_sand,
    drop_sand_part_two,
    keep_dropping_sand,
    parse_raw,
    part_one,
    part_two,
    visualize,
)

example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def test_parse_raw():
    expected = {
        (498, 4),
        (498, 5),
        (498, 6),
        (497, 6),
        (496, 6),
        (503, 4),
        (502, 4),
        (502, 5),
        (502, 6),
        (502, 7),
        (502, 8),
        (502, 9),
        (501, 9),
        (500, 9),
        (499, 9),
        (498, 9),
        (497, 9),
        (496, 9),
        (495, 9),
        (494, 9),
    }

    actual = parse_raw(example)

    assert len(actual) == 5 + 15

    assert actual == expected


def test_all_points_in_line():
    test_cases = [
        [(1, 1), (3, 1), [(1, 1), (2, 1), (3, 1)]],
        [(3, 1), (1, 1), [(3, 1), (2, 1), (1, 1)]],
        [(2, 5), (2, 8), [(2, 5), (2, 6), (2, 7), (2, 8)]],
        [(2, 8), (2, 4), [(2, 8), (2, 7), (2, 6), (2, 5), (2, 4)]],
    ]

    for start, end, expected in test_cases:
        actual = all_points_in_line(start, end)
        assert actual == set(expected)


@pytest.fixture
def example_rocks():
    yield parse_raw(example)


def test_drop_sands_1st(example_rocks):
    expected = (500, 8)

    actual = drop_sand(rocks=example_rocks)
    assert actual == expected


def test_drop_sands_2nd(example_rocks):
    sands = {(500, 8)}
    expected = (499, 8)

    actual = drop_sand(rocks=example_rocks, sands=sands)
    assert actual == expected


def test_drop_sands_3rd(example_rocks):
    sands = {(500, 8), (499, 8)}
    expected = (501, 8)

    actual = drop_sand(rocks=example_rocks, sands=sands)
    assert actual == expected


def test_drop_5_units_of_sands(example_rocks):
    expected = {(500, 8), (499, 8), (501, 8), (500, 7), (498, 8)}
    sands = set()
    for _ in range(5):
        sands.add(drop_sand(rocks=example_rocks, sands=sands))

    assert sands == expected


def test_keep_dropping_sand(example_rocks):
    actual = keep_dropping_sand(rocks=example_rocks, times=24)

    assert len(actual) == 24
    for coord in [(497, 8), (498, 8), (498, 7), (500, 2), (495, 8), (497, 5)]:
        assert coord in actual
    for coord in [(x, y) for x in (499, 501) for y in (3, 8)]:
        assert coord in actual


def test_keep_dropping_sand_until_fall_to_abyss(example_rocks):
    actual = keep_dropping_sand(rocks=example_rocks)
    assert len(actual) == 24


def test_part_one():
    rocks = parse_raw(example)
    expected = 24

    actual = part_one(rocks)

    assert actual == expected


def test_detect_sand_source_blocked():
    rocks = set([(499, 1), (500, 1), (501, 1)])
    final_sand = drop_sand_part_two(rocks)
    sands = set([final_sand])
    with pytest.raises(SandSourceBlocked):
        drop_sand_part_two(rocks=rocks, sands=sands)


def test_drop_sand_part_two():
    rocks = set([(0, 9)])
    expected = (500, 10)

    actual = drop_sand_part_two(rocks)
    assert actual == expected


def test_keep_dropping_sand_part_two():
    rocks = set([(0, 9)])
    expected = set([(500, 10), (499, 10), (501, 10), (500, 9)])

    actual = keep_dropping_sand(rocks=rocks, times=4, part_two=True)
    assert actual == expected


def test_part_two():
    rocks = parse_raw(example)

    expected = 93

    actual = part_two(rocks)

    assert actual == expected
