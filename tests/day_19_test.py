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
    input_state = State()
    expected = [
        State(ore_bot=1, ore=1)
    ]
    actual = factory.run_blueprint(blueprint_number=1, input_state=input_state)
    
    assert actual == expected


def test_run_blueprint_1_turn_2(factory):
    input_state = State(ore_bot=1, ore=1)
    expected = [
        State(ore_bot=1, ore=2)
    ]
    actual = factory.run_blueprint(blueprint_number=1, input_state=input_state)
    
    assert actual == expected


def test_run_blueprint_1_turn_3(factory):
    input_state = State(ore_bot=1, ore=2)
    expected = [
        State(ore_bot=1, clay_bot=1, ore=1),
        State(ore_bot=1, ore=3)
    ]
    actual = factory.run_blueprint(blueprint_number=1, input_state=input_state)
    
    assert sorted(actual) == sorted(expected)


def test_bot_cost(factory):
    test_cases_blueprint_1 = [
        ['clay_bot', State(ore=2)],
        ['ore_bot', State(ore=4)],
        ['obsidian_bot', State(ore=3, clay=14)],
        ['geode_bot', State(ore=2, obsidian=7)],
    ]

    for bot_name, expected in test_cases_blueprint_1:
        actual = factory.bot_cost(1, bot_name)
        assert actual == expected

def test_can_make_bot(factory):

    test_cases_blueprint_1 = [
        [State(0,0,0,0,0,0,0,0), ['clay_bot']],
        [State(0,0,0,0,2,0,0,0), ['clay_bot']],
        [State(0,0,0,0,4,0,0,0), ['ore_bot','clay_bot']],
        [State(0,0,0,0,4,14,0,0), ['ore_bot','clay_bot']],
        [State(0,0,0,0,4,14,0,0), ['ore_bot','clay_bot', 'obsidian_bot']],
        [State(0,0,0,0,3,14,0,0), ['clay_bot', 'obsidian_bot']],
        [State(0,0,0,0,4,14,7,0), ['ore_bot','clay_bot', 'obsidian_bot', 'geode_bot']],
        [State(0,0,0,0,10,0,10,0), ['ore_bot','clay_bot', 'geode_bot']],
    ]

    for input_state, expected in test_cases_blueprint_1:
        actual = factory.can_make_bot(1, input_state)
        assert actual == expected