from typing import Callable
import re
import math

import aoc_helper


class Monkey:
    _all_monkeys = []
    _monkey_lcm = None

    def __init__(
        self,
        starting_items: list[int],
        operation: Callable[[int], int],
        test_divisor: int,
        next_monkey_true: int,
        next_monkey_false: int,
    ):
        self.items = starting_items
        self.operation = operation
        self.test_divisor = test_divisor
        self.next_monkeys = [next_monkey_false, next_monkey_true]
        self.inspect_item_counts = 0
        self.index = len(self.__class__._all_monkeys)

        self.__class__._all_monkeys.append(self)

    def play(self, part_two=False):
        for item in self.items:
            if part_two:
                item_worry_level = self.inspect_item(item) % self.__class__.monkey_lcm()
            else:
                item_worry_level = self.inspect_item(item) // 3
            next_monkey = self.determine_next_monkey(item_worry_level)
            self.__class__.get_monkey(next_monkey).receive_item(item_worry_level)
        self.items = []

    def receive_item(self, item: int):
        self.items.append(item)

    def inspect_item(self, item: int) -> int:
        self.inspect_item_counts += 1
        return self.operation(item)

    def determine_next_monkey(self, item_worry_level: int) -> int:
        test_result = item_worry_level % self.test_divisor == 0
        return self.next_monkeys[test_result]

    @classmethod
    def reset_monkeys(cls):
        cls._all_monkeys = []
        cls._monkey_lcm = None

    @classmethod
    def monkey_lcm(cls) -> int:
        if not cls._monkey_lcm:
            monkey_divisors = [monkey.test_divisor for monkey in cls._all_monkeys]
            cls._monkey_lcm = math.lcm(*monkey_divisors)
        return cls._monkey_lcm

    @classmethod
    def get_monkey(cls, index: int) -> "Monkey":
        monkey = cls._all_monkeys[index]
        if not monkey:
            raise ValueError(f"Monkey #{index} does not exist")
        return monkey

    @classmethod
    def all_monkeys_take_turn(cls, part_two=False):
        for monkey in cls._all_monkeys:
            monkey.play(part_two=part_two)

    @classmethod
    def monkey_business_index(cls) -> int:
        most_annoying_monkey, second_annoying_monkey, *rest = sorted(
            cls._all_monkeys,
            key=lambda monkey: monkey.inspect_item_counts,
            reverse=True,
        )
        return (
            most_annoying_monkey.inspect_item_counts
            * second_annoying_monkey.inspect_item_counts
        )


def create_monkey(lines: list[str], part_two=False) -> Monkey:
    starting_items = [int(item) for item in re.findall(r"\d+", lines[1])]

    operation_raw = lines[2].replace("Operation: new = ", "")
    operation_sanitised = re.sub(r"[^0-9old =\+\-\*]", "", operation_raw)
    operation = lambda old: eval(operation_sanitised)

    test_divisor, next_monkey_true, next_monkey_false = [
        int(re.findall(r"\d+", line)[0]) for line in lines[3:6]
    ]

    return Monkey(
        starting_items, operation, test_divisor, next_monkey_true, next_monkey_false
    )


def parse_raw(raw: str, part_two=False) -> list[Monkey]:
    monkey_blocks = raw.split("\n\n")
    monkeys = []
    for block in monkey_blocks:
        monkey = create_monkey(lines=block.split("\n"), part_two=part_two)
        monkeys.append(monkey)

    return monkeys


def part_one(monkeys: list[Monkey]) -> int:
    for _ in range(20):
        Monkey.all_monkeys_take_turn()

    return Monkey.monkey_business_index()


def part_two(monkeys: list[Monkey]) -> int:
    for _ in range(10000):
        Monkey.all_monkeys_take_turn(part_two=True)

    return Monkey.monkey_business_index()


if __name__ == "__main__":

    day = 11

    raw_data = aoc_helper.fetch(day, 2022)
    monkeys = parse_raw(raw_data)

    print(f"part one solution: {part_one(monkeys)}")

    Monkey.reset_monkeys()
    monkeys_part_two = parse_raw(raw_data)
    print(f"part two solution: {part_two(monkeys_part_two)}")
