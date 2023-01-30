from solutions.day_07 import (Directory, list_directories_size, parse_raw,
                              part_one, part_two)

example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


def test_parse_raw():
    actual = parse_raw(example)

    assert isinstance(actual, Directory)
    assert list(actual.children.keys()) == ["a", "b.txt", "c.dat", "d"]
    assert actual["d"].size == 24933642
    assert actual.size == 48381165


def test_list_directories_sizes():
    input_data = parse_raw(example)

    expected = {"/": 48381165, "/d": 24933642, "/a": 94853, "/a/e": 584}

    actual = list_directories_size(input_data)

    assert actual == expected


def test_part_one():
    input_data = parse_raw(example)

    expected = 95437

    actual = part_one(input_data)

    assert actual == expected


def test_part_two():
    input_data = parse_raw(example)

    expected = 24933642

    actual = part_two(input_data)

    assert actual == expected
