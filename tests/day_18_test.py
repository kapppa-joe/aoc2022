from solutions.day_18 import (
    parse_raw,
    is_touching,
    part_one,
    DisjointSets,
    find_boundries,
    all_cubes_in_space,
    is_at_boundry,
    classify_cubes,
    all_touching_pairs,
    find_surface_area,
    part_two,
)

example = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def test_parse_raw():
    expected = [
        (2, 2, 2),
        (1, 2, 2),
        (3, 2, 2),
        (2, 1, 2),
        (2, 3, 2),
        (2, 2, 1),
        (2, 2, 3),
        (2, 2, 4),
        (2, 2, 6),
        (1, 2, 5),
        (3, 2, 5),
        (2, 1, 5),
        (2, 3, 5),
    ]

    actual = parse_raw(example)

    assert actual == expected


def test_is_touching():
    a = (1, 1, 1)
    b = (2, 1, 1)
    c = (1, 2, 1)
    d = (1, 2, 2)
    e = (2, 2, 1)

    assert is_touching(a, b) == True
    assert is_touching(b, a) == True
    assert is_touching(a, c) == True
    assert is_touching(b, e) == True
    assert is_touching(c, d) == True
    assert is_touching(c, e) == True
    assert is_touching(a, d) == False
    assert is_touching(b, d) == False
    assert is_touching(b, c) == False
    assert is_touching(b, d) == False


def test_part_one():
    cubes = parse_raw(example)
    expected = 64

    actual = part_one(cubes)

    assert actual == expected


def test_disjoint_sets():
    # test case:
    # 2,3,5,7 - one group
    # 1 - one group
    # 4,6,8,9,10 - one group

    ds = DisjointSets()
    ds.union(2, 3)
    ds.union(3, 5)
    ds.union(5, 7)
    ds.union(4, 6)
    ds.union(6, 9)
    ds.union(8, 10)
    ds.union(4, 10)
    for i in range(1, 11):
        ds.find(i)

    groups = list(ds.list_groups())
    assert {2, 3, 5, 7} in groups
    assert {1} in groups
    assert {4, 6, 8, 9, 10} in groups


def test_find_boundries():
    lava_cubes = parse_raw(example)
    expected = [(1, 3), (1, 3), (1, 6)]

    actual = find_boundries(lava_cubes)
    assert actual == expected


def test_all_cubes_in_space():
    lava_cubes = parse_raw(example)
    boundries = find_boundries(lava_cubes)

    actual = list(all_cubes_in_space(boundries=boundries))
    assert len(actual) == 3 * 3 * 6
    assert (1, 1, 1) in actual
    assert (1, 1, 6) in actual
    assert (3, 3, 6) in actual
    assert (1, 6, 1) not in actual
    assert (4, 1, 1) not in actual
    assert all(cube in actual for cube in lava_cubes)


def test_is_at_boundry():
    # 4 x 4 cube, only 8 pieces in center is not at boundry.
    test_cases = [
        (x, y, z) for x in range(1, 5) for y in range(1, 5) for z in range(1, 5)
    ]

    boundries = [(1, 4), (1, 4), (1, 4)]
    cubes_in_center = [
        (2, 2, 2),
        (2, 2, 3),
        (2, 3, 2),
        (2, 3, 3),
        (3, 2, 2),
        (3, 2, 3),
        (3, 3, 2),
        (3, 3, 3),
    ]
    for cube in test_cases:
        if cube in cubes_in_center:
            assert is_at_boundry(cube, boundries) == False
        else:
            assert is_at_boundry(cube, boundries) == True


def test_all_touching_pairs():
    boundries = ((1, 3), (1, 3), (1, 3))
    actual = list(all_touching_pairs(boundries=boundries))

    assert len(actual) == (27 * 6 - 9 * 6) // 2
    # all surface area - outside facing 6 faces * 9 units
    # for each touching pair, there are two unit of touching surface.

    assert len(set(actual)) == len(actual)

    assert frozenset([(1, 1, 1), (1, 1, 2)]) in actual
    assert frozenset([(2, 2, 1), (2, 3, 1)]) in actual
    assert frozenset([(3, 3, 3), (2, 3, 3)]) in actual
    assert frozenset([(1, 1, 1), (1, 1, 3)]) not in actual
    assert frozenset([(3, 1, 3), (1, 1, 3)]) not in actual
    assert frozenset([(1, 1, 1), (1, 2, 2)]) not in actual

    for pairs in actual:
        assert is_touching(*pairs) == True


def test_classify_cubes():
    lava_cubes = parse_raw(example)
    actual = classify_cubes(lava_cubes)

    assert actual["lava_cubes"] == set(lava_cubes)

    assert actual["trapped_air"] == set([(2, 2, 5)])

    assert len(actual["exposed_air"]) == 3 * 3 * 6 - 13 - 1


def test_find_surface_area():
    test_cases = [
        # fmt: off
        [set([(1,1,1)]), 6],
        [set([(1,1,1), (1,1,2), (2,1,1)]), 5 + 5 + 4], # L shape
        [set([(1,1,1), (1,1,2), (2,1,1), (2,1,2)]), 4 * 4], # square
        [set([(1,1,1), (1,1,2), (2,1,2), (2,2,2), (3,2,2)]), 5 + 5 + 2 * 6], # W shape
        [set([(1,1,1), (1,1,2), (1,0,2), (0,1,2), (0,1,3)]), 4 + 4 + 4 + 4 + 3 + 3],
        # fmt: on
    ]

    for groups, expected in test_cases:
        actual = find_surface_area(cubes=groups)
        assert actual == expected


def test_part_two():
    lava_cubes = parse_raw(example)
    expected = 58
    actual = part_two(lava_cubes)

    assert actual == expected
