from solutions.day_03 import (
    parse_raw,
    find_repeat_item,
    item_priority,
    part_one,
    part_two,
    parse_raw_part_two,
)


example = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def test_parse_raw():
    input_data = "\n".join(example.split("\n")[0:3])
    expected = [
        ("vJrwpWtwJgWr", "hcsFMMfFFhFp"),
        ("jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL"),
        ("PmmdzqPrV", "vPwwTWBwg"),
    ]

    actual = parse_raw(input_data)

    assert actual == expected


def test_find_repeat_item():
    input_data = parse_raw(example)
    expected = ["p", "L", "P", "v", "t", "s"]

    actual = [find_repeat_item(*rucksack) for rucksack in input_data]
    assert actual == expected


def test_item_priority():
    input_data = ["p", "L", "P", "v", "t", "s"]
    expected = [16, 38, 42, 22, 20, 19]

    actual = [item_priority(item) for item in input_data]

    assert actual == expected


def test_part_one():
    expected = 157

    input_data = parse_raw(example)
    actual = part_one(input_data)

    assert actual == expected


def test_parse_raw_part_two():
    actual = parse_raw_part_two("123\n456\n789\nabc\ndef\nghi")
    expected = [("123", "456", "789"), ("abc", "def", "ghi")]

    assert actual == expected


def test_find_repeat_item_part_two():
    input_data = parse_raw_part_two(example)
    expected = ["r", "Z"]

    actual = [find_repeat_item(*group) for group in input_data]

    assert actual == expected


def test_part_two():

    input_data = parse_raw_part_two(example)
    expected = 70

    actual = part_two(input_data)

    assert actual == expected
