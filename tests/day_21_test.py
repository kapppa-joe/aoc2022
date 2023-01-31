import pytest

from solutions.day_21 import (
    ConstantNode,
    Node,
    Op,
    OperationNode,
    parse_raw,
    part_one,
    part_two,
)

example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


def test_parse_raw():
    actual = parse_raw(example)

    assert len(actual.all_nodes) == len(example.splitlines())

    assert actual.all_nodes["dbpl"].value == 5

    assert actual.all_nodes["root"].left_name == "pppw"
    assert actual.all_nodes["root"].right_name == "sjmn"
    assert actual.all_nodes["root"].op == Op.Add

    assert actual.all_nodes["root"].left == actual.all_nodes["pppw"]
    assert actual.all_nodes["root"].right == actual.all_nodes["sjmn"]


@pytest.fixture(name="example_tree")
def make_example_tree():
    yield parse_raw(example)


def test_simplify_nodes(example_tree):
    assert isinstance(example_tree["drzm"], OperationNode)

    example_tree.simplify_nodes()

    assert isinstance(example_tree["drzm"], ConstantNode)
    assert example_tree["drzm"].value == 32 - 2


def test_simplify_until_end(example_tree):
    example_tree.simplify_until_end()

    expected = 152
    actual = example_tree["root"].value

    assert actual == expected
    assert example_tree.count_operation_nodes() == 0


def test_part_one(example_tree):
    actual = part_one(example_tree)
    expected = 152

    assert actual == expected


def test_build_reverse_tree(example_tree):
    example_tree["humn"] = Node("variable")
    example_tree.simplify_until_end()
    actual = example_tree.build_reverse_tree()

    assert actual["root"].value == 0

    assert actual["pppw"].left_name == "root"
    assert actual["pppw"].right_name == "sjmn"
    assert actual["pppw"].op == Op.Add

    assert isinstance(actual["humn"], OperationNode)
    assert actual["humn"].left_name == "ptdq"
    assert actual["humn"].right_name == "dvpt"
    assert actual["humn"].op == Op.Add


def test_part_two(example_tree):
    actual = part_two(example_tree)
    expected = 301

    assert actual == expected
