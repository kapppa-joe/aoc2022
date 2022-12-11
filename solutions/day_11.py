from typing import Callable
import re

import aoc_helper


class Monkey:
    _all_monkeys = []
    part_two = False

    def __init__(
        self,
        starting_items: list[int],
        operation: Callable[[int], int],
        test_divisor: int,
        next_monkey_true: int,
        next_monkey_false: int,
        part_two: bool = False
    ):
        self.items = starting_items
        self.operation = operation
        self.test_divisor = test_divisor
        self.next_monkeys = [next_monkey_false, next_monkey_true]
        self.inspect_item_counts = 0

        Monkey._all_monkeys.append(self)

    def play(self):
        for item in self.items:
            item_worry_level = self.inspect_item(item)
            if not Monkey.part_two:
                item_worry_level = item_worry_level // 3
            test_result = item_worry_level % self.test_divisor == 0
            next_monkey = self.next_monkeys[test_result]
            Monkey.get_monkey(next_monkey).receive_item(item_worry_level)
        self.items = []


    def receive_item(self, item: int):
        self.items.append(item)

    def inspect_item(self, item: int) -> int:
        self.inspect_item_counts += 1
        return self.operation(item)

    @classmethod
    def get_monkey(cls, index: int) -> "Monkey":
        monkey = cls._all_monkeys[index]
        if not monkey:
            raise ValueError(f"Monkey #{index} does not exist")
        return monkey

    @classmethod
    def all_monkeys_take_turn(cls):
        for monkey in cls._all_monkeys:
            monkey.play()


def create_monkey(lines: list[str]) -> Monkey:
    starting_items = [int(item) for item in re.findall(r"\d+", lines[1])]

    operation_raw = lines[2].replace("Operation: new = ", "")
    operation_sanitised = re.sub(r"[^0-9old =\+\-\*]", "", operation_raw)
    operation = lambda old: eval(operation_sanitised)

    test_divisor, next_monkey_true, next_monkey_false = [
        int(re.search(r"\d+", line)[0]) for line in lines[3:6]
    ]

    return Monkey(starting_items, operation, test_divisor, next_monkey_true, next_monkey_false)

def parse_raw(raw: str) -> list[Monkey]:
    monkey_blocks = raw.split("\n\n")
    monkeys = []
    for block in monkey_blocks:
        monkey = create_monkey(lines = block.split('\n')) 
        monkeys.append(monkey)

    return monkeys


def part_one(monkeys: list[Monkey]) -> int:
    for _ in range(20):
        Monkey.all_monkeys_take_turn()

    most_annoying_monkey, second_annoying_monkey, *rest = sorted(monkeys, key=lambda monkey: monkey.inspect_item_counts, reverse=True)
    return most_annoying_monkey.inspect_item_counts * second_annoying_monkey.inspect_item_counts

def part_two(monkeys: list[Monkey]) -> int:
    Monkey.part_two = True
    for _ in range(1000):
        Monkey.all_monkeys_take_turn()
    print(monkey.items for monkey in monkeys)


if __name__ == "__main__":

    day = 11

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
