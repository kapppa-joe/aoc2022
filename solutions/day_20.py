from typing import Iterable
import itertools

import aoc_helper


class NumberBoxes:
    def __init__(self, numbers: list[int]):
        self._boxes = tuple(numbers)
        self.len = len(tuple(numbers))

    def __getitem__(self, index: int) -> int:
        return self._boxes[index]

    def initial_index(self) -> tuple[int]:
        return tuple(range(len(self._boxes)))

    def rotate_number(
        self, token_list: tuple[int], index: int, move: int
    ) -> tuple[int]:
        curr_pos = token_list.index(index)
        next_pos = token_list.index(index) + 1
        next_pos_after_rotate = (next_pos + move) % (self.len - 1)

        new_list = token_list[:curr_pos] + token_list[curr_pos + 1 :]
        new_pos = next_pos_after_rotate - 1
        if new_pos < 1:
            new_pos += self.len - 1

        return new_list[:new_pos] + (index,) + new_list[new_pos:]

    def unbox_numbers(self, token_list: tuple[int]) -> tuple[int]:
        return tuple((self._boxes[index] for index in token_list))

    def mix_number(self, token_list: tuple[int], index: int) -> tuple[int]:
        move = self[index]
        after_rotation = self.rotate_number(
            token_list=token_list, index=index, move=move
        )

        return after_rotation

    def mix_whole_list(self) -> tuple[int]:
        token_list = self.initial_index()
        for token in range(self.len):
            token_list = self.mix_number(token_list=token_list, index=token)
        return token_list

    def nth_after_zero(self, token_list: tuple[int], n: int) -> int:
        token_of_zero = self._boxes.index(0)
        pos_of_zero = token_list.index(token_of_zero)
        pos_of_wanted_number = (pos_of_zero + n) % self.len
        token_of_wanted_number = token_list[pos_of_wanted_number]
        return self[token_of_wanted_number]


def parse_raw(raw: str) -> NumberBoxes:
    numbers = [int(line) for line in raw.splitlines()]
    return NumberBoxes(numbers=numbers)


def part_one(box: NumberBoxes) -> int:
    token_list_after_mixed = box.mix_whole_list()
    return sum(
        box.nth_after_zero(token_list=token_list_after_mixed, n=n)
        for n in [1000, 2000, 3000]
    )


def part_two(data):
    ...


if __name__ == "__main__":

    day = 20

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
