import pytest
from solutions.day_19 import parse_raw, part_one, part_two, Blueprint, State, BotTypes

example = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""


def test_parse_raw():
    expected = [Blueprint(4, 2, 3, 14, 2, 7), Blueprint(2, 3, 3, 8, 3, 12)]

    factory = parse_raw(example)

    assert factory.blueprints == expected


@pytest.fixture(name="factory")
def create_example_factory():
    factory = parse_raw(example)
    yield factory


def test_run_blueprint_1_turn_1(factory):
    input_state = State(ore_bot=1)
    expected = [State(ore_bot=1, ore=1)]
    actual = factory.run_blueprint(blueprint_num=1, input_state=input_state)

    assert actual == expected


def test_run_blueprint_1_turn_2(factory):
    input_state = State(ore_bot=1, ore=1)
    expected = [State(ore_bot=1, ore=2)]
    actual = factory.run_blueprint(blueprint_num=1, input_state=input_state)

    assert actual == expected


def test_run_blueprint_1_turn_3(factory):
    input_state = State(ore_bot=1, ore=2)
    expected = [State(ore_bot=1, clay_bot=1, ore=1), State(ore_bot=1, ore=3)]
    actual = factory.run_blueprint(blueprint_num=1, input_state=input_state)

    assert sorted(actual) == sorted(expected)


def test_run_blueprint_1_turn_4(factory):
    input_state = State(ore_bot=1, clay_bot=1, ore=1)
    expected = [
        State(ore_bot=1, clay_bot=1, ore=2, clay=1),
    ]
    actual = factory.run_blueprint(blueprint_num=1, input_state=input_state)

    assert sorted(actual) == sorted(expected)


def test_run_blueprint_1_turn_5(factory):
    input_state = State(ore_bot=1, clay_bot=1, ore=2, clay=1)
    expected = [
        State(ore_bot=1, clay_bot=1, ore=3, clay=2),
        State(ore_bot=1, clay_bot=2, ore=1, clay=2),
    ]
    actual = factory.run_blueprint(blueprint_num=1, input_state=input_state)

    assert sorted(actual) == sorted(expected)


def test_get_bot_cost(factory):
    test_cases_blueprint_1 = [
        ["clay_bot", State(ore=2)],
        ["ore_bot", State(ore=4)],
        ["obsidian_bot", State(ore=3, clay=14)],
        ["geode_bot", State(ore=2, obsidian=7)],
    ]

    for bot_type, expected in test_cases_blueprint_1:
        actual = factory.get_bot_cost(1, bot_type)
        assert actual == expected


# old version. comment out.
# def test_can_make_bot(factory):
#     test_cases_blueprint_1 = [
#         [State(), []],
#         [State(ore=2), ['clay_bot']],
#         [State(ore=4), ['ore_bot','clay_bot']],
#         [State(ore=5, clay=13), ['ore_bot','clay_bot']],
#         [State(ore=4, clay=14), ['ore_bot','clay_bot', 'obsidian_bot']],
#         [State(ore=3, clay=14), ['clay_bot', 'obsidian_bot']],
#         [State(ore=4, clay=14, obsidian=7), ['ore_bot','clay_bot', 'obsidian_bot', 'geode_bot']],
#         [State(ore=10, obsidian=10), ['ore_bot','clay_bot', 'geode_bot']],
#     ]

#     for input_state, expected in test_cases_blueprint_1:
#         actual = factory.can_make_bot(1, input_state)
#         assert sorted(actual) == sorted(expected)


def test_can_make_bot(factory):

    test_cases_blueprint_1 = [
        [State(), []],
        [State(ore=2), ["clay_bot"]],
        [State(ore=4), ["ore_bot", "clay_bot"]],
        [State(ore=5, clay=13), ["ore_bot", "clay_bot"]],
        [State(ore=4, clay=14), ["ore_bot", "clay_bot", "obsidian_bot"]],
        [State(ore=3, clay=14), ["clay_bot", "obsidian_bot"]],
        [
            State(ore=4, clay=14, obsidian=7),
            ["ore_bot", "clay_bot", "obsidian_bot", "geode_bot"],
        ],
        [State(ore=10, obsidian=10), ["ore_bot", "clay_bot", "geode_bot"]],
    ]

    for state, expected in test_cases_blueprint_1:
        actual = [
            bot_type
            for bot_type in BotTypes
            if factory.can_make_bot(
                blueprint_num=1, input_state=state, bot_type=bot_type
            )
        ]

        assert sorted(actual) == sorted(expected)


# def test_could_make_bot_last_turn(factory):
#     blueprint_num = 1

#     test_cases = [
#         [State(ore=2, ore_bot=1), 'clay_bot', False],
#         [State(ore=3, ore_bot=1), 'clay_bot', True]
#     ]

#     for state, bot_type, expected in test_cases:
#         actual = factory.could_make_bot_last_turn(
#             blueprint_num=blueprint_num, input_state=state, bot_type=bot_type)
#         assert actual == expected


def test_prune_inferior_state(factory):
    # fmt: off
    input_sets = {
        State( ore_bot=2, clay_bot=0, obsidian_bot=0, geode_bot=0, ore=1, clay=0, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=2, obsidian_bot=0, geode_bot=0, ore=1, clay=2, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=2, obsidian_bot=0, geode_bot=0, ore=1, clay=1, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=1, obsidian_bot=0, geode_bot=0, ore=3, clay=2, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=1, obsidian_bot=0, geode_bot=0, ore=3, clay=1, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=1, obsidian_bot=0, geode_bot=0, ore=3, clay=0, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=0, obsidian_bot=0, geode_bot=0, ore=5, clay=0, obsidian=0, geode=0,),
    }

    expected = {
        State( ore_bot=2, clay_bot=0, obsidian_bot=0, geode_bot=0, ore=1, clay=0, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=2, obsidian_bot=0, geode_bot=0, ore=1, clay=2, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=1, obsidian_bot=0, geode_bot=0, ore=3, clay=2, obsidian=0, geode=0,),
        State( ore_bot=1, clay_bot=0, obsidian_bot=0, geode_bot=0, ore=5, clay=0, obsidian=0, geode=0,),
    }
    # fmt: on

    actual = factory.prune_inferior_state(input_sets)

    assert actual == expected


def test_run_n_turns_basic(factory):
    input_state = State(ore_bot=1)
    expected = set(
        [
            State(ore_bot=1, clay_bot=1, ore=3, clay=2),
            State(ore_bot=1, clay_bot=2, ore=1, clay=2),
            State(ore_bot=1, clay_bot=0, ore=5, clay=0),
            State(ore_bot=2, clay_bot=0, ore=1, clay=0),
        ]
    )

    actual = factory.run_n_turns(
        turn_count=5, blueprint_num=1, initial_state=input_state
    )

    assert actual == expected


# def test_dfs_basic(factory):
#     expected = 1
#     initial_state = State(ore_bot=1)
#     actual = factory.dfs(blueprint_num=1, state=initial_state, minutes = 19)

#     assert actual == expected


# def test_dfs_blueprint_1_turn_20(factory):
#     expected = 2
#     initial_state = State(ore_bot=1)
#     actual = factory.dfs(blueprint_num=1, state=initial_state, minutes = 20)

#     assert actual == expected


# def test_dfs_blueprint_1_turn_21(factory):
#     expected = 3
#     initial_state = State(ore_bot=1)
#     actual = factory.dfs(blueprint_num=1, state=initial_state, minutes = 21)

#     assert actual == expected


# def test_dfs_blueprint_1_turn_24(factory):
#     expected = 9
#     initial_state = State(ore_bot=1)
#     actual = factory.dfs(blueprint_num=1, state=initial_state, minutes = 24)

#     assert actual == expected


def test_run_n_turns_example_run_down(factory):
    example_rundown = [
        [5, State(ore_bot=1, clay_bot=2, ore=1, clay=2)],
        [6, State(ore_bot=1, clay_bot=2, ore=2, clay=4)],
        [7, State(ore_bot=1, clay_bot=3, ore=1, clay=6)],
        [8, State(ore_bot=1, clay_bot=3, ore=2, clay=9)],
        [9, State(ore_bot=1, clay_bot=3, ore=3, clay=12)],
        [10, State(ore_bot=1, clay_bot=3, ore=4, clay=15)],
        [11, State(ore_bot=1, clay_bot=3, obsidian_bot=1, ore=2, clay=4)],
        [12, State(ore_bot=1, clay_bot=4, obsidian_bot=1, ore=1, clay=7, obsidian=1)],
        [13, State(ore_bot=1, clay_bot=4, obsidian_bot=1, ore=2, clay=11, obsidian=2)],
        [14, State(ore_bot=1, clay_bot=4, obsidian_bot=1, ore=3, clay=15, obsidian=3)],
        [15, State(ore_bot=1, clay_bot=4, obsidian_bot=2, ore=1, clay=5, obsidian=4)],
        [16, State(ore_bot=1, clay_bot=4, obsidian_bot=2, ore=2, clay=9, obsidian=6)],
        [17, State(ore_bot=1, clay_bot=4, obsidian_bot=2, ore=3, clay=13, obsidian=8)],
        [18, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=1, ore=2, clay=17, obsidian=3)],
        [19, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=1, ore=3, clay=21, obsidian=5, geode=1)],
        [20, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=1, ore=4, clay=25, obsidian=7, geode=2)],
        [21, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=2, ore=3, clay=29, obsidian=2, geode=3)],
        [22, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=2, ore=4, clay=33, obsidian=4, geode=5)],
        [23, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=2, ore=5, clay=37, obsidian=6, geode=7)],
        [24, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=2, ore=6, clay=41, obsidian=8, geode=9)],
    ]
    initial_state = State(ore_bot=1)

    for turn_count, expected_state in example_rundown:
        actual = factory.run_n_turns(turn_count=turn_count, blueprint_num=1, initial_state=initial_state)
        expected_state_capped = factory.cap_resource(blueprint_num=1, state=expected_state)
        assert expected_state_capped in actual




def test_run_n_turns_example_run_down_part_2(factory):
    example_rundown = [
        [4, State(ore_bot=1, ore=4)],
        [6, State(ore_bot=2, ore=3)],
        [12, State(ore_bot=2, clay_bot=2, ore=3, clay=15)],
    ]
    initial_state = State(ore_bot=1)

    for turn_count, expected_state in example_rundown:
        actual = factory.run_n_turns(turn_count=turn_count, blueprint_num=1, initial_state=initial_state)
        expected_state_capped = factory.cap_resource(blueprint_num=1, state=expected_state)
        assert expected_state_capped in actual

def test_best_geode_for_blueprint(factory):
    assert factory.best_geode_for_blueprint(blueprint_num=1) == 9
    assert factory.best_geode_for_blueprint(blueprint_num=2) == 12


def test_part_one(factory):
    expected = 33
    actual = part_one(factory)

    assert actual == expected


def test_best_geode_part_two(factory):
    assert factory.best_geode_for_blueprint(1, 32) == 56
    assert factory.best_geode_for_blueprint(2, 32) == 62

def test_max_resource_needed(factory):
    test_cases = [
        [1, State(ore=4, clay=14, obsidian=7)],
        [2, State(ore=3, clay=8, obsidian=12)],
    ]

    for blueprint_num, expected in test_cases:
        actual = factory.max_resource_needed(blueprint_num=blueprint_num)
        assert actual == expected


def test_cap_resource(factory):
    test_cases = [
        [
            1,
            State(geode=10, ore=99, clay=99, obsidian=99, clay_bot=3),
            State(geode=10, ore=6, clay=16, obsidian=9, clay_bot=3),
        ],
        [
            2,
            State(geode=10, ore=99, clay=99, obsidian=99, ore_bot=3),
            State(geode=10, ore=5, clay=10, obsidian=14, ore_bot=3),
        ],
        [1, State(ore_bot=1, ore=2), State(ore_bot=1, ore=2)],
    ]

    for blueprint_num, state, expected in test_cases:
        actual = factory.cap_resource(blueprint_num=blueprint_num, state=state)
        assert actual == expected

def test_part_two(factory):
    expected = 62 * 56
    actual = part_two(factory)

    assert actual == expected