class SNAFU:
    @classmethod
    def to_int(cls, snafu_number: str) -> int:
        digit_table = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
        digits_reversed = reversed(snafu_number)

        return sum(
            5**i * digit_table[digit] for i, digit in enumerate(digits_reversed)
        )

    @classmethod
    def from_int(cls, number: int) -> str:
        digits = "012=-"
        modulus = number % 5
        digit = digits[modulus]

        remaining = number - modulus
        if modulus in (3, 4):
            remaining += 5

        if remaining == 0:
            return digit
        else:
            return SNAFU.from_int(remaining // 5) + digit


def parse_raw(raw: str) -> list[str]:
    return raw.splitlines()


def part_one(snafu_number_list: list[str]) -> str:
    sum_of_snafu_numbers = sum(SNAFU.to_int(snafu) for snafu in snafu_number_list)
    return SNAFU.from_int(sum_of_snafu_numbers)


if __name__ == "__main__":

    day = 25

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
