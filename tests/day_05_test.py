from solutions.day_05 import parse_raw, part_one, part_two, run_instruction

example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def test_parse_raw():
    expected = {
        "crates": [["Z", "N"], ["M", "C", "D"], ["P"]],
        "instructions": [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)],
    }

    actual = parse_raw(raw=example)

    assert actual == expected


def test_run_instruction():
    input_crates = [["Z", "N"], ["M", "C", "D"], ["P"]]
    input_instructions = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]

    expected_round_2 = [["Z", "N", "D"], ["M", "C"], ["P"]]

    expected_round_3 = [[], ["M", "C"], ["P", "D", "N", "Z"]]

    expected_round_4 = [["C", "M"], [], ["P", "D", "N", "Z"]]

    expected_round_5 = [["C"], ["M"], ["P", "D", "N", "Z"]]

    expected = [expected_round_2, expected_round_3, expected_round_4, expected_round_5]

    crates = input_crates
    for i, instruction in enumerate(input_instructions):
        crates = run_instruction(crates, *instruction)
        assert crates == expected[i]


def test_run_instruction_part_two():

    input_crates = [["Z", "N"], ["M", "C", "D"], ["P"]]
    input_instructions = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]

    expected_round_2 = [["Z", "N", "D"], ["M", "C"], ["P"]]

    expected_round_3 = [[], ["M", "C"], ["P", "Z", "N", "D"]]

    expected_round_4 = [["M", "C"], [], ["P", "Z", "N", "D"]]

    expected_round_5 = [["M"], ["C"], ["P", "Z", "N", "D"]]

    expected = [expected_round_2, expected_round_3, expected_round_4, expected_round_5]

    crates = input_crates
    for i, instruction in enumerate(input_instructions):
        crates = run_instruction(crates, *instruction, is_part_two=True)
        assert crates == expected[i]


def test_part_one():
    input_data = parse_raw(example)

    expected = "CMZ"
    actual = part_one(input_data)

    assert actual == expected


def test_part_two():
    input_data = parse_raw(example)

    expected = "MCD"
    actual = part_two(input_data)

    assert actual == expected
