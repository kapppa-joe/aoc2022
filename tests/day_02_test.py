from solutions.day_02 import (
    parse_raw,
    part_one,
    part_two,
    player_shape_score_part_two,
    win_lose_score,
)


def test_parse_raw():
    raw = "A X\nB Y\nC Z"
    expected = [("A", "X"), ("B", "Y"), ("C", "Z")]
    actual = parse_raw(raw)

    assert actual == expected


def test_win_lose_score():
    wins = [("A", "Y"), ("B", "Z"), ("C", "X")]

    draws = [("A", "X"), ("B", "Y"), ("C", "Z")]

    loses = [("A", "Z"), ("B", "X"), ("C", "Y")]

    for combination in wins:
        assert win_lose_score(*combination) == 6

    for combination in draws:
        assert win_lose_score(*combination) == 3

    for combination in loses:
        assert win_lose_score(*combination) == 0


def test_part_one():
    input_data = [("A", "Y"), ("B", "X"), ("C", "Z")]

    assert part_one(input_data) == 15


def test_player_shape_score_part_two():
    test_cases = [
        [("A", "Y"), 1],
        [("B", "X"), 1],
        [("C", "Z"), 1],
        [("A", "X"), 3],
        [("A", "Z"), 2],
    ]

    for round_input, expected_shape_score in test_cases:
        assert player_shape_score_part_two(*round_input) == expected_shape_score


def test_part_two():
    input_data = [("A", "Y"), ("B", "X"), ("C", "Z")]

    assert part_two(input_data) == 12
