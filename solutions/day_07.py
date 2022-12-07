import re
from functools import cached_property
import aoc_helper


class Directory:
    def __init__(self, parent=None, name: str = ""):
        self.children = {}
        self.parent = parent
        self.name = name

    @cached_property
    def size(self) -> int:
        return sum(
            child.size if isinstance(child, Directory) else child
            for child in self.children.values()
        )

    def add_file(self, name: str, size: int):
        self.children[name] = size

    def add_child_directory(self, name):
        self.children[name] = Directory(parent=self, name=name)

    def __getitem__(self, key: str):
        return self.children[key]

    def sub_dir(self) -> list["Directory"]:
        return [
            child for child in self.children.values() if isinstance(child, Directory)
        ]

    def list_directory_size(self) -> dict[str, int]:
        result = {"/" if self.name == "" else self.name: self.size}
        for child in self.sub_dir():
            result.update(
                {
                    f"{self.name}/{key}": value
                    for key, value in child.list_directory_size().items()
                }
            )
        return result


def parse_raw(raw: str) -> Directory:
    root = Directory()
    cwd = root

    for line in raw.split("\n"):
        if match := re.match(r"(\d+) (.+)", line):
            size, filename = match.groups()
            cwd.add_file(name=filename, size=int(size))
        elif line.startswith("dir "):
            dirname = line[4:]
            cwd.add_child_directory(dirname)
        elif line == "$ cd /":
            cwd = root
        elif line == "$ cd ..":
            if not cwd.parent:
                raise RuntimeError("Already at root")
            cwd = cwd.parent
        elif match := re.match(r"\$ cd (.+)", line):
            child_dir = match.group(1)
            cwd = cwd[child_dir]

    return root


def list_directories_size(directory: Directory) -> dict[str, int]:
    return directory.list_directory_size()


def part_one(root: Directory) -> int:
    target_size = 1e5
    return sum(
        value for value in list_directories_size(root).values() if value < target_size
    )


def part_two(root: Directory):
    total_size = 70000000
    target_size = 30000000
    current_used_size = root.size

    additional_size_needed = target_size - (total_size - current_used_size)

    return min(
        value
        for value in list_directories_size(root).values()
        if value > additional_size_needed
    )


if __name__ == "__main__":

    day = 7

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
