PartTwoMagicNum = 811589153


class NumberBoxes:
    def __init__(self, numbers: list[int]):
        self._boxes = tuple(numbers)
        self.len = len(tuple(numbers))

    def __getitem__(self, token: int) -> int:
        return self._boxes[token]

    def initial_tokens(self) -> tuple[int]:
        return tuple(range(len(self._boxes)))

    def rotate_number(
        self, token_list: tuple[int], token: int, move: int
    ) -> tuple[int]:
        curr_pos = token_list.index(token)
        next_pos = token_list.index(token) + 1
        next_pos_after_rotate = (next_pos + move) % (self.len - 1)

        new_list = token_list[:curr_pos] + token_list[curr_pos + 1 :]
        new_pos = next_pos_after_rotate - 1
        if new_pos < 1:
            new_pos += self.len - 1

        return new_list[:new_pos] + (token,) + new_list[new_pos:]

    def unbox_numbers(self, token_list: tuple[int]) -> tuple[int]:
        return tuple((self._boxes[token] for token in token_list))

    def mix_number(self, token_list: tuple[int], token: int) -> tuple[int]:
        move = self[token]
        after_rotation = self.rotate_number(
            token_list=token_list, token=token, move=move
        )

        return after_rotation

    def mix_whole_list(self, times=1) -> tuple[int]:
        token_list = self.initial_tokens()
        for _ in range(times):
            for token in range(self.len):
                token_list = self.mix_number(token_list=token_list, token=token)
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


def part_two(box: NumberBoxes) -> int:
    box._boxes = tuple(num * PartTwoMagicNum for num in box._boxes)
    token_list_after_mixed = box.mix_whole_list(times=10)
    return sum(
        box.nth_after_zero(token_list=token_list_after_mixed, n=n)
        for n in [1000, 2000, 3000]
    )


if __name__ == "__main__":

    day = 20

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
