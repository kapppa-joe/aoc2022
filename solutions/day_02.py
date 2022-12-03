import aoc_helper


def parse_raw(raw: str) -> list[tuple[str, str]]:
    return [tuple(line.split(" ")) for line in raw.split("\n")]


def win_lose_score(opponent: str, player: str) -> int:
    opponent_choice = "ABC".index(opponent)
    player_choice = "XYZ".index(player)

    if player_choice == opponent_choice:
        return 3
    if player_choice - opponent_choice in [1, -2]:
        return 6

    return 0


def shape_score(player: str) -> int:
    player_choice = "XYZ".index(player)
    scores_of_shapes = [1, 2, 3]

    return scores_of_shapes[player_choice]


def player_shape_score_part_two(opponent: str, winlose: str) -> int:
    opponent_choice = "ABC".index(opponent)
    choice_offset = [-1, 0, 1]["XYZ".index(winlose)]

    scores_of_shapes = [1, 2, 3]

    player_choice = (opponent_choice + choice_offset + 3) % 3
    return scores_of_shapes[player_choice]


def round_score(opponent: str, player: str) -> int:
    return win_lose_score(opponent, player) + shape_score(player)


def part_one(data):
    return sum(round_score(*combination) for combination in data)


def round_score_part_two(opponent: str, winlose: str) -> int:
    return [0, 3, 6]["XYZ".index(winlose)] + player_shape_score_part_two(
        opponent, winlose
    )


def part_two(data):
    return sum(round_score_part_two(*combination) for combination in data)


if __name__ == "__main__":

    raw_data = aoc_helper.fetch(2, 2022)
    parsed_data = parse_raw(raw_data)

    aoc_helper.lazy_submit(day=2, year=2022, solution=lambda: part_one(parsed_data))
    aoc_helper.lazy_submit(day=2, year=2022, solution=lambda: part_two(parsed_data))
