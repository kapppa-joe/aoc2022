import pytest
from solutions.day_19 import parse_raw, part_one, part_two, Blueprint, State

example = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

def test_parse_raw():
    expected = [
        Blueprint(4,2,3,14,2,7),
        Blueprint(2,3,3,8,3,12)
    ]

    factory = parse_raw(example)

    assert factory.blueprints == expected

@pytest.fixture(name='factory')
def create_example_factory():
    factory = parse_raw(example)
    yield factory


def test_run_blueprint_1_turn_1(factory):
    input_state = State(ore_bot=1)
    expected = [
        State(ore_bot=1, ore=1)
    ]
    actual = factory.run_blueprint(blueprint_num=1, input_state=input_state)
    
    assert actual == expected


def test_run_blueprint_1_turn_2(factory):
    input_state = State(ore_bot=1, ore=1)
    expected = [
        State(ore_bot=1, ore=2)
    ]
    actual = factory.run_blueprint(blueprint_num=1, input_state=input_state)
    
    assert actual == expected


def test_run_blueprint_1_turn_3(factory):
    input_state = State(ore_bot=1, ore=2)
    expected = [
        State(ore_bot=1, clay_bot=1, ore=1),
        State(ore_bot=1, ore=3)
    ]
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
        ['clay_bot', State(ore=2)],
        ['ore_bot', State(ore=4)],
        ['obsidian_bot', State(ore=3, clay=14)],
        ['geode_bot', State(ore=2, obsidian=7)],
    ]

    for bot_type, expected in test_cases_blueprint_1:
        actual = factory.get_bot_cost(1, bot_type)
        print(actual)
        print(expected)
        assert actual == expected

def test_can_make_bot(factory):

    test_cases_blueprint_1 = [
        [State(0,0,0,0,0,0,0,0), []],
        [State(ore=2), ['clay_bot']],
        [State(ore=4), ['ore_bot','clay_bot']],
        [State(ore=5, clay=13), ['ore_bot','clay_bot']],
        [State(ore=4, clay=14), ['ore_bot','clay_bot', 'obsidian_bot']],
        [State(ore=3, clay=14), ['clay_bot', 'obsidian_bot']],
        [State(ore=4, clay=14, obsidian=7), ['ore_bot','clay_bot', 'obsidian_bot', 'geode_bot']],
        [State(ore=10, obsidian=10), ['ore_bot','clay_bot', 'geode_bot']],
    ]

    for input_state, expected in test_cases_blueprint_1:
        actual = factory.can_make_bot(1, input_state)
        assert sorted(actual) == sorted(expected)



def test_trim_inferior_state(factory):
    input_sets = {
        State(ore_bot=2, clay_bot=0, obsidian_bot=0, geode_bot=0, ore=1, clay=0, obsidian=0, geode=0), 
        State(ore_bot=1, clay_bot=2, obsidian_bot=0, geode_bot=0, ore=1, clay=2, obsidian=0, geode=0), 
        State(ore_bot=1, clay_bot=2, obsidian_bot=0, geode_bot=0, ore=1, clay=1, obsidian=0, geode=0), 
        State(ore_bot=1, clay_bot=1, obsidian_bot=0, geode_bot=0, ore=3, clay=2, obsidian=0, geode=0), 
        State(ore_bot=1, clay_bot=1, obsidian_bot=0, geode_bot=0, ore=3, clay=1, obsidian=0, geode=0),
        State(ore_bot=1, clay_bot=1, obsidian_bot=0, geode_bot=0, ore=3, clay=0, obsidian=0, geode=0), 
        State(ore_bot=1, clay_bot=0, obsidian_bot=0, geode_bot=0, ore=5, clay=0, obsidian=0, geode=0), 
    }
    
    expected = {
        State(ore_bot=2, clay_bot=0, obsidian_bot=0, geode_bot=0, ore=1, clay=0, obsidian=0, geode=0), 
        State(ore_bot=1, clay_bot=2, obsidian_bot=0, geode_bot=0, ore=1, clay=2, obsidian=0, geode=0), 
        State(ore_bot=1, clay_bot=1, obsidian_bot=0, geode_bot=0, ore=3, clay=2, obsidian=0, geode=0), 
        State(ore_bot=1, clay_bot=0, obsidian_bot=0, geode_bot=0, ore=5, clay=0, obsidian=0, geode=0), 
    }

    actual = factory.trim_inferior_state(input_sets)

    assert actual == expected


def test_run_n_turns_basic(factory):
    input_state = State(ore_bot=1)
    expected = set([
        State(ore_bot=1, clay_bot=1, ore=3, clay=2),
        State(ore_bot=1, clay_bot=2, ore=1, clay=2),
        State(ore_bot=1, clay_bot=0, ore=5, clay=0),
        State(ore_bot=2, clay_bot=0, ore=1, clay=0),
    ])

    actual = factory.run_n_turns(turn_count=5, blueprint_num=1, initial_state=input_state)

    assert actual == expected



# def test_run_n_turns_example_run_down(factory):
#     example_rundown = [
#         # [5, State(ore_bot=1, clay_bot=2, ore=1, clay=2)],
#         # [6, State(ore_bot=1, clay_bot=2, ore=2, clay=4)],
#         # [7, State(ore_bot=1, clay_bot=3, ore=1, clay=6)],
#         # [8, State(ore_bot=1, clay_bot=3, ore=2, clay=9)],
#         # [9, State(ore_bot=1, clay_bot=3, ore=3, clay=12)],
#         # [10, State(ore_bot=1, clay_bot=3, ore=4, clay=15)],
#         # [11, State(ore_bot=1, clay_bot=3, obsidian_bot=1, ore=2, clay=4)],
#         # [12, State(ore_bot=1, clay_bot=4, obsidian_bot=1, ore=1, clay=7, obsidian=1)],
#         # [13, State(ore_bot=1, clay_bot=4, obsidian_bot=1, ore=2, clay=11, obsidian=2)],
#         # [14, State(ore_bot=1, clay_bot=4, obsidian_bot=1, ore=3, clay=15, obsidian=3)],
#         # [15, State(ore_bot=1, clay_bot=4, obsidian_bot=2, ore=1, clay=5, obsidian=4)],
#         # [16, State(ore_bot=1, clay_bot=4, obsidian_bot=2, ore=2, clay=9, obsidian=6)],
#         # [17, State(ore_bot=1, clay_bot=4, obsidian_bot=2, ore=3, clay=13, obsidian=8)],
#         # [18, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=1, ore=2, clay=17, obsidian=3)],
#         # [19, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=1, ore=3, clay=21, obsidian=5, geode=1)],
#         # [20, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=1, ore=4, clay=25, obsidian=7, geode=2)],
#         # [21, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=2, ore=3, clay=29, obsidian=2, geode=3)],
#         # [22, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=2, ore=4, clay=33, obsidian=4, geode=5)],
#         # [23, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=2, ore=5, clay=37, obsidian=6, geode=7)],
#         [24, State(ore_bot=1, clay_bot=4, obsidian_bot=2, geode_bot=2, ore=6, clay=41, obsidian=8, geode=9)],
#     ]
#     initial_state = State(ore_bot=1)

#     for turn_count, expected_state in example_rundown:
#         actual = factory.run_n_turns(turn_count=turn_count, blueprint_num=1, initial_state=initial_state)
#         assert expected_state in actual

# def test_best_geode_for_blueprint(factory):
#     expected = 12
#     actual = factory.best_geode_for_blueprint(blueprint_num=2)

#     assert actual == expected

def test_part_one(factory):
    expected = 33
    actual = part_one(factory)

    assert actual == expected