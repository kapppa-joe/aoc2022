import pytest
from solutions.day_16 import ValveNetwork, parse_raw, part_one, part_two

example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def test_parse_raw():
    expected = [
        ("AA", 0, {"DD", "II", "BB"}),
        ("BB", 13, {"CC", "AA"}),
        ("CC", 2, {"DD", "BB"}),
        ("DD", 20, {"CC", "AA", "EE"}),
        ("EE", 3, {"FF", "DD"}),
        ("FF", 0, {"EE", "GG"}),
        ("GG", 0, {"FF", "HH"}),
        ("HH", 22, {"GG"}),
        ("II", 0, {"AA", "JJ"}),
        ("JJ", 21, {"II"}),
    ]

    network = parse_raw(raw=example)

    assert network.valves == [row[0] for row in expected]
    for valve_name, rate, neighbour_valves in expected:
        assert network.neighbour_valves(valve_name) == neighbour_valves
        assert network.flow_rate(valve_name) == rate


@pytest.fixture(name="network")
def create_example_network():
    return parse_raw(example)


class TestTotalPressureReleased:
    def test_naive_case(self, network):
        current_valve = "AA"
        valves_opened = frozenset(network.valves)
        remaining_time = 0

        actual = network.total_pressure_released(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )
        assert actual == 0

    def test_1_minute_case(self, network):
        current_valve = "BB"
        valves_opened = frozenset(["BB"])
        remaining_time = 1

        expected = 0
        actual = network.total_pressure_released(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )
        assert actual == expected

    def test_try_open_current_valve(self, network):
        current_valve = "BB"
        valves_opened = frozenset()
        remaining_time = 2

        expected = 13
        actual = network.total_pressure_released(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )
        assert actual == expected

    def test_try_open_neighbour_valve(self, network):
        current_valve = "AA"
        valves_opened = frozenset()
        remaining_time = 3

        expected = 20
        actual = network.total_pressure_released(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )
        assert actual == expected

    def test_5_minutes(self, network):
        current_valve = "HH"
        valves_opened = frozenset()
        remaining_time = 5

        expected = 88
        actual = network.total_pressure_released(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )
        assert actual == expected

    def test_solve_example_case(self, network):
        current_valve = "AA"
        valves_opened = frozenset()
        remaining_time = 30

        expected = 1651

        actual = network.total_pressure_released(
            current_valve=current_valve,
            valves_opened=valves_opened,
            remaining_time=remaining_time,
        )
        assert actual == expected


def test_part_one(network):
    expected = 1651
    actual = part_one(network=network)

    assert actual == expected
