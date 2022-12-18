import re

import aoc_helper


def parse_raw(raw: str) -> dict:
    crates_raw, instruction_raw = raw.split("\n\n")

    crates_transposed = [
        "".join(line)
        for line in zip(*crates_raw.split("\n"))
        if any(char in "123456789" for char in line)
    ]
    crates_reversed_order = [reversed(stack) for stack in crates_transposed]
    crates = [
        [crate for crate in stack if (crate >= "A" and crate <= "Z")]
        for stack in crates_reversed_order
    ]

    instructions = [
        tuple(map(int, re.findall(r"\d+", line)))
        for line in instruction_raw.split("\n")
    ]

    return {"crates": crates, "instructions": instructions}


def run_instruction(
    crates: list[list[str]],
    num: int,
    from_stack: int,
    to_stack: int,
    is_part_two: bool = False,
) -> list[list[str]]:
    from_stack, to_stack = from_stack - 1, to_stack - 1  # account for 1-base index

    crates_remain, crate_taken = crates[from_stack][:-num], crates[from_stack][-num:]
    crates[from_stack] = crates_remain
    if is_part_two:
        crates[to_stack] += crate_taken
    else:
        crates[to_stack] += reversed(crate_taken)

    return crates


def part_one(data) -> str:
    crates, instructions = data["crates"], data["instructions"]
    for inst in instructions:
        crates = run_instruction(crates, *inst)

    return "".join(stack[-1] for stack in crates)


def part_two(data):
    crates, instructions = data["crates"], data["instructions"]
    for inst in instructions:
        crates = run_instruction(crates, *inst, is_part_two=True)

    return "".join(stack[-1] for stack in crates)


if __name__ == "__main__":

    day = 5

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")

    # parse the data again as part one mutates the crates
    parsed_data = parse_raw(raw_data)
    print(f"part two solution: {part_two(parsed_data)}")
