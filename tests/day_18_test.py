from solutions.day_18 import parse_raw, is_touching, part_one, part_two

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
