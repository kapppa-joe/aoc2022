import re
from enum import Enum
from fractions import Fraction
import functools


class Op(Enum):
    Add, Minus, Multiply, Divide = range(4)


class Node:
    def __init__(self, name: str) -> None:
        self.name = name

    def children(self) -> list["Node"]:
        return []


class ConstantNode(Node):
    def __init__(self, name: str, value: int | Fraction) -> None:
        self.value = value
        super().__init__(name)


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

class MathTree:
    def __init__(self, raw: str):
        self.all_nodes = {}

        for name, expr in re.findall(r"(\w{4}): ([^\n]+)", raw):
            node = self.build_node(name, expr)
            self.all_nodes[name] = node

    def __getitem__(self, key: str):
        return self.all_nodes[key]

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
            if isinstance(node.left, ConstantNode) and isinstance(node.right, ConstantNode):
                left, right = node.left.value, node.right.value
                match node.op:
                    case Op.Add:
                        value = left + right
                    case Op.Minus:
                        value = left - right
                    case Op.Multiply:
                        value = left * right
                    case Op.Divide:
                        value = Fraction(left, right)
                    case _:
                        raise RuntimeError('Unknown operator')
                new_node = ConstantNode(node.name, value)
                self.all_nodes[node.name] = new_node
    
    def count_operation_nodes(self) -> int:
        return sum(1 for node in self.all_nodes.values() if isinstance(node, OperationNode))
    
    def simplify_until_end(self):
        prev_count = 0
        curr_count = self.count_operation_nodes()
        
        while prev_count != curr_count:
            self.simplify_nodes()
            prev_count = curr_count
            curr_count = self.count_operation_nodes()

                    
        


def parse_raw(raw: str) -> MathTree:
    return MathTree(raw)


def part_one(tree: MathTree) -> int:
    tree.simplify_until_end()
    return tree['root'].value


def part_two(data):
    ...


if __name__ == "__main__":

    day = 21

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()

    parsed_data = parse_raw(raw_data)
    print(f"part one solution: {part_one(parsed_data)}")

    parsed_data = parse_raw(raw_data)
    print(f"part two solution: {part_two(parsed_data)}")
