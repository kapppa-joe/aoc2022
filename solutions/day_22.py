import re
from enum import Enum
from typing import NamedTuple, Optional


class Facing(Enum):
    Right, Down, Left, Up = range(4)


class Tile(str, Enum):
    Space = "."
    Block = "#"
    Void = " "


class TurnDirection(str, Enum):
    Left = "L"
    Right = "R"


Step = int | TurnDirection

State = tuple[int, int, Facing]
Path = list[Step]


class MonkeyMap:
    def __init__(self, input_map: list[str], path: list[Step]):
        self.map = input_map
        self.map_width = len(input_map[0])
        self.map_height = len(input_map)
        self.path = path

    @property
    def map_size(self) -> tuple[int, int]:
        return (self.map_height, self.map_width)

    def get_tile(self, x: int, y: int) -> Tile:
        return Tile(self.map[y][x])

    def get_init_position(self) -> State:
        try:
            open_tile_x = self.map[0].index(Tile.Space)
        except ValueError:
            raise ValueError("No open tile in the first row of map")

        return (open_tile_x, 0, Facing(0))

    def next_tile(self, position: State) -> tuple[int, int]:
        x, y, facing = position

        delta = {
            Facing.Right: (1, 0),
            Facing.Down: (0, 1),
            Facing.Left: (-1, 0),
            Facing.Up: (0, -1),
        }
        dx, dy = delta[facing]

        x1 = (x + dx) % self.map_width
        y1 = (y + dy) % self.map_height

        while self.get_tile(x=x1, y=y1) == Tile.Void:
            x1 = (x1 + dx) % self.map_width
            y1 = (y1 + dy) % self.map_height

        return (x1, y1)

    def follow_path(self, path: Path, init_pos: Optional[State] = None) -> State:
        x, y, facing = self.get_init_position() if init_pos is None else init_pos

        for step in path:
            match step:
                case TurnDirection.Left:
                    facing = Facing((facing.value - 1) % 4)
                case TurnDirection.Right:
                    facing = Facing((facing.value + 1) % 4)
                case step if isinstance(step, int):
                    for _ in range(step):
                        x1, y1 = self.next_tile((x, y, facing))
                        if self.get_tile(x=x1, y=y1) == Tile.Block:
                            break
                        x, y = x1, y1

        return (x, y, facing)

    def calc_password(self, position: State) -> int:
        x, y, facing = position
        return (y + 1) * 1000 + (x + 1) * 4 + facing.value


def parse_raw(raw: str) -> MonkeyMap:
    raw_map, raw_path = raw.split("\n\n")
    max_y = max(len(line) for line in raw_map.splitlines())
    input_map = [line.ljust(max_y) for line in raw_map.splitlines()]

    path = parse_path(raw_path)

    return MonkeyMap(input_map, path)


def parse_path(raw_path: str) -> Path:
    path_in_string: list[str] = re.findall(pattern=r"(\d+|L|R)", string=raw_path)
    parsed_path = [
        int(step) if step.isnumeric() else TurnDirection(step)
        for step in path_in_string
    ]
    return parsed_path


def part_one(monkey_map: MonkeyMap) -> int:
    path = monkey_map.path
    final_position = monkey_map.follow_path(path)

    return monkey_map.calc_password(position=final_position)


def part_two(data):
    ...


if __name__ == "__main__":

    day = 22

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
