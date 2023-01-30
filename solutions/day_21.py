import re
from enum import Enum
from fractions import Fraction
import functools


class Op(Enum):
    Add, Subtract, Multiply, Divide = range(4)

    def reverse(self) -> "Op":
        match self:
            case Op.Add:
                return Op(Op.Subtract)
            case Op.Subtract:
                return Op(Op.Add)
            case Op.Multiply:
                return Op(Op.Divide)
            case Op.Divide:
                return Op(Op.Multiply)


class Node:
    def __init__(self, name: str) -> None:
        self.name = name

    def children(self) -> list["Node"]:
        return []


class ConstantNode(Node):
    def __init__(self, name: str, value: int | Fraction) -> None:
        self.value = value
        super().__init__(name)

    def __repr__(self) -> str:
        return f"<{self.value}>"


class OperationNode(Node):
    def __init__(
        self, name: str, tree: "MathTree", left_name: str, right_name: str, op: Op
    ) -> None:
        self.tree = tree
        self.left_name = left_name
        self.right_name = right_name
        self.op = op
        super().__init__(name)

    @property
    def left(self) -> Node:
        return self.tree[self.left_name]

    @property
    def right(self) -> Node:
        return self.tree[self.right_name]

    def __repr__(self) -> str:
        return f"{self.left_name} {self.op} {self.right_name}"


class MathTree:
    def __init__(self, raw: str):
        self.all_nodes = {}

        for name, expr in re.findall(r"(\w{4}): ([^\n]+)", raw):
            node = self.build_node(name, expr)
            self.all_nodes[name] = node

    def __getitem__(self, key: str):
        return self.all_nodes[key]

    def __setitem__(self, key: str, value: Node):
        self.all_nodes[key] = value

    def build_node(self, name: str, expr: str) -> Node:
        operators = [op for op in "+-*/"]
        if expr.isnumeric():
            return ConstantNode(name, int(expr))
        elif match := re.match(r"(\w{4}) ([\+\-\*\/]) (\w{4})", expr):
            left_name, op, right_name = match.groups()
            operator = Op(operators.index(op))
            return OperationNode(
                tree=self,
                name=name,
                left_name=left_name,
                right_name=right_name,
                op=operator,
            )
        else:
            raise RuntimeError("Cannot interpret current node: {name, expr}")

    def simplify_nodes(self):
        for node in self.all_nodes.values():
            if not isinstance(node, OperationNode):
                continue
            if isinstance(node.left, ConstantNode) and isinstance(
                node.right, ConstantNode
            ):
                left, right = node.left.value, node.right.value
                match node.op:
                    case Op.Add:
                        value = left + right
                    case Op.Subtract:
                        value = left - right
                    case Op.Multiply:
                        value = left * right
                    case Op.Divide:
                        value = Fraction(left, right)
                    case _:
                        raise RuntimeError("Unknown operator")
                new_node = ConstantNode(node.name, value)
                self.all_nodes[node.name] = new_node

    def count_operation_nodes(self) -> int:
        return sum(
            1 for node in self.all_nodes.values() if isinstance(node, OperationNode)
        )

    def simplify_until_end(self):
        prev_count = 0
        curr_count = self.count_operation_nodes()

        while prev_count != curr_count:
            self.simplify_nodes()
            prev_count = curr_count
            curr_count = self.count_operation_nodes()

    def build_reverse_tree(self) -> "MathTree":
        """Build a reverse math tree so that root = 0 and humn being the new root, so that we can trace the value of humn node.

        Returns:
            MathTree: A new tree that all operations from root to humn nodes are reversed.
        """
        new_tree = MathTree("")

        const_nodes = []
        op_nodes = []

        for node in self.all_nodes.values():
            if isinstance(node, ConstantNode):
                const_nodes.append(node.name)
            elif isinstance(node, OperationNode):
                op_nodes.append(node.name)

        new_tree.all_nodes.update(
            {
                name: ConstantNode(name=name, value=self[name].value)
                for name in const_nodes
            }
        )
        new_tree["root"] = ConstantNode(name="root", value=0)
        self["root"].op = Op.Subtract

        for node_name in op_nodes:
            node: OperationNode = self[node_name]

            # flip    a = b + c --> b = a - c
            if node.left_name not in new_tree.all_nodes:
                new_op = node.op.reverse()
                new_node = OperationNode(
                    name=node.left_name,
                    tree=new_tree,
                    left_name=node_name,
                    right_name=node.right_name,
                    op=new_op,
                )
                new_tree[node.left_name] = new_node

            # flip    a = b + c --> c = a - b
            if node.right_name not in new_tree.all_nodes:
                if node.op in [Op.Add, Op.Multiply]:
                    new_op = node.op.reverse()
                    new_node = OperationNode(
                        name=node.right_name,
                        tree=new_tree,
                        left_name=node_name,
                        right_name=node.left_name,
                        op=new_op,
                    )
                else:
                    new_node = OperationNode(
                        name=node.right_name,
                        tree=new_tree,
                        left_name=node.left_name,
                        right_name=node.name,
                        op=node.op,
                    )

                new_tree[node.right_name] = new_node

        return new_tree


def parse_raw(raw: str) -> MathTree:
    return MathTree(raw)


def part_one(tree: MathTree) -> int:
    tree.simplify_until_end()
    return tree["root"].value


def part_two(tree: MathTree) -> int:
    tree["humn"] = Node("variable")
    tree.simplify_until_end()

    if isinstance(tree["root"].left, OperationNode) and isinstance(
        tree["root"].right, OperationNode
    ):
        raise NotImplementedError(
            "both left and right of root depends on humn node. solution not implemented for this case"
        )
    elif isinstance(tree["root"].left, ConstantNode) and isinstance(
        tree["root"].right, ConstantNode
    ):
        raise ValueError(
            "root node does not depend on humn node. Either unsolvable case or any solution is valid"
        )
    else:
        reversed_tree = tree.build_reverse_tree()
        reversed_tree.simplify_until_end()

        return reversed_tree["humn"].value


if __name__ == "__main__":

    day = 21

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()

    parsed_data = parse_raw(raw_data)
    print(f"part one solution: {part_one(parsed_data)}")

    parsed_data = parse_raw(raw_data)
    print(f"part two solution: {part_two(parsed_data)}")
