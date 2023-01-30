import pytest

from solutions.day_11 import Monkey, parse_raw, part_one, part_two


@pytest.fixture(autouse=True)
def reset_monkeys_after_each_test():
    yield
    Monkey._all_monkeys = []


example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


def test_make_a_monkey():
    monkey = Monkey(
        starting_items=[79, 98],
        operation=lambda old: old * 19,
        test_divisor=23,
        next_monkey_true=2,
        next_monkey_false=3,
    )
    assert monkey.items == [79, 98]


def test_get_monkey():
    monkey = Monkey(
        starting_items=[79, 98],
        operation=lambda old: old * 19,
        test_divisor=23,
        next_monkey_true=2,
        next_monkey_false=3,
    )

    monkey_got = Monkey.get_monkey(0)

    assert monkey is monkey_got


def test_parse_raw():
    monkeys = parse_raw(example)

    assert len(monkeys) == 4
    assert monkeys[2].items == [79, 60, 97]
    assert monkeys[3].test_divisor == 17

    assert monkeys[0].operation(4) == 4 * 19
    assert monkeys[1].operation(4) == 4 + 6
    assert monkeys[2].operation(4) == 4 * 4
    assert monkeys[3].operation(4) == 4 + 3

    assert monkeys[0].next_monkeys == [3, 2]
    assert monkeys[1].next_monkeys == [0, 2]


@pytest.fixture(name="monkeys")
def setup_monkeys():
    monkeys = parse_raw(example)
    yield monkeys


def test_monkey_play_round(monkeys):
    monkeys[0].play()

    assert monkeys[0].items == []
    assert monkeys[3].items == [74, 500, 620]

    monkeys[1].play()

    assert monkeys[1].items == []
    assert monkeys[0].items == [20, 23, 27, 26]

    monkeys[2].play()

    assert monkeys[2].items == []
    assert monkeys[1].items == [2080]
    assert monkeys[3].items == [74, 500, 620, 1200, 3136]

    monkeys[3].play()

    assert monkeys[3].items == []
    assert monkeys[1].items == [2080, 25, 167, 207, 401, 1046]


def test_inspect_item_counts(monkeys):
    monkeys[0].play()
    assert monkeys[0].inspect_item_counts == 2


def test_inspect_item_count_after_20_rounds(monkeys):
    for _ in range(20):
        Monkey.all_monkeys_take_turn()

    expected = [101, 95, 7, 105]
    actual = [monkeys[i].inspect_item_counts for i in range(4)]

    assert actual == expected


def test_part_one():
    monkeys = parse_raw(example)
    expected = 10605

    actual = part_one(monkeys)

    assert actual == expected


def test_monkey_index(monkeys):
    assert all(monkey.index == i for (i, monkey) in enumerate(monkeys))


def get_new_monkeys():
    Monkey._all_monkeys = []
    monkeys = parse_raw(example)
    return monkeys


def test_part_two_inspect_counts(monkeys):
    test_cases = [
        [1, [2, 4, 3, 6]],
        [20, [99, 97, 8, 103]],
        [1000, [5204, 4792, 199, 5192]],
        [5000, [26075, 23921, 974, 26000]],
    ]

    for rounds_count, expected in test_cases:
        monkeys = get_new_monkeys()
        for _ in range(rounds_count):
            Monkey.all_monkeys_take_turn(part_two=True)

        actual = [monkey.inspect_item_counts for monkey in monkeys]

        assert actual == expected


def test_part_two(monkeys):
    expected = 2713310158
    actual = part_two(monkeys)

    assert actual == expected
