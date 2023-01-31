from solutions.day_15 import (
    detect_hole,
    find_only_hole_on_map,
    manhattan_distance,
    parse_raw,
    part_one,
    part_two,
    sensor_x_coverage_at_given_y,
)

example = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


def test_parse_raw():
    expected = [
        [(2, 18), (-2, 15)],
        [(9, 16), (10, 16)],
        [(13, 2), (15, 3)],
        [(12, 14), (10, 16)],
        [(10, 20), (10, 16)],
        [(14, 17), (10, 16)],
        [(8, 7), (2, 10)],
        [(2, 0), (2, 10)],
        [(0, 11), (2, 10)],
        [(20, 14), (25, 17)],
        [(17, 20), (21, 22)],
        [(16, 7), (15, 3)],
        [(14, 3), (15, 3)],
        [(20, 1), (15, 3)],
    ]
    actual = parse_raw(example)

    assert actual == expected


def test_manhattan_distance():
    test_cases = [[(2, 18), (-2, 15), 7], [(8, 7), (2, 10), 9]]

    for start, end, expected in test_cases:
        actual = manhattan_distance(start, end)
        assert actual == expected


def test_sensor_x_coverage_at_given_y():
    test_cases = [
        [(8, 7), (2, 10), 10, (2, 14)],
        [(8, 7), (2, 10), 9, (1, 15)],
        [(8, 7), (2, 10), 16, (8, 8)],
        [(8, 7), (2, 10), 17, None],
        [(8, 7), (2, 10), 0, (6, 10)],
    ]

    for sensor, beacon, y, expected in test_cases:
        actual = sensor_x_coverage_at_given_y(sensor=sensor, beacon=beacon, y=y)

        assert actual == expected


def test_part_one():
    sensor_and_beacons = parse_raw(example)
    expected = 26
    actual = part_one(sensor_and_beacons=sensor_and_beacons, y=10)

    assert actual == expected


def test_detect_hole():
    x_ranges = [(0, 10), (-13, 15), (2, 6), (4, 9), (-3, 5), None, None, (17, 22)]
    expected = 16
    actual = detect_hole(x_ranges)

    assert actual == expected


def test_detect_hole_dont_report_when_two_ranges_barely_touches():
    x_ranges = [(0, 10), (11, 20)]
    expected = None
    actual = detect_hole(x_ranges)

    assert actual == expected


def test_detect_hole_out_of_boundry():
    x_ranges = [
        # hole at -6
        None,
        None,
        (1, 4),
        (2, 5),
        (-10, -7),
        (-5, 20),
    ]
    expected = None
    actual = detect_hole(x_ranges)

    assert actual == expected

    x_ranges_2 = [
        # hole at 21 , right_boundry is 20
        None,
        (22, 30),
        None,
        (1, 15),
        (10, 20),
    ]
    expected = None
    actual = detect_hole(x_ranges_2, right_boundry=20)

    assert actual == expected

    x_ranges_3 = [
        # hole at 20 , right_boundry is 20
        None,
        (21, 30),
        None,
        (1, 15),
        (10, 19),
    ]
    expected = 20
    actual = detect_hole(x_ranges_3, right_boundry=20)

    assert actual == expected


def test_find_only_hole_on_map():
    sensor_and_beacons = parse_raw(example)
    expected = (14, 11)

    actual = find_only_hole_on_map(sensor_and_beacons, 20)
    assert actual == expected


def test_part_two():
    sensor_and_beacons = parse_raw(example)
    expected = 56000011

    actual = part_two(sensor_and_beacons, 20)
    assert actual == expected
