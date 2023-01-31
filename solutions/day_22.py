import functools
import itertools
import re
from enum import Enum
from typing import Optional


class Facing(Enum):
    Right, Down, Left, Up = range(4)

    def __sub__(self, other: "Facing") -> int:
        return (self.value - other.value + 4) % 4

    def turn_clockwise(self, times: int = 1) -> "Facing":
        return self.__class__((self.value + times) % 4)


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

    def get_init_state(self) -> State:
        try:
            open_tile_x = self.map[0].index(Tile.Space)
        except ValueError:
            raise ValueError("No open tile in the first row of map")

        return (open_tile_x, 0, Facing(0))

    def next_tile(self, state: State) -> State:
        x, y, facing = state

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

        return (x1, y1, facing)

    def follow_path(self, path: Path, init_state: Optional[State] = None) -> State:
        x, y, facing = self.get_init_state() if init_state is None else init_state

        for step in path:
            match step:
                case TurnDirection.Left:
                    facing = Facing((facing.value - 1) % 4)
                case TurnDirection.Right:
                    facing = Facing((facing.value + 1) % 4)
                case step if isinstance(step, int):
                    for _ in range(step):
                        x1, y1, facing1 = self.next_tile((x, y, facing))
                        if self.get_tile(x=x1, y=y1) == Tile.Block:
                            break
                        x, y, facing = x1, y1, facing1

        return (x, y, facing)

    def calc_password(self, state: State) -> int:
        x, y, facing = state
        return (y + 1) * 1000 + (x + 1) * 4 + facing.value


class MonkeyMapCube(MonkeyMap):
    def __init__(self, input_map: list[str], path: list[Step]):
        super().__init__(input_map=input_map, path=path)

        self.side_width = self.detect_side_width()
        self.faces = self.detect_faces()
        self.connect_faces()

    def detect_side_width(self) -> int:
        total_area = sum(
            1 for tile in "".join(self.map) if tile in (Tile.Block, Tile.Space)
        )

        sqrt_of_one_face = (total_area / 6) ** 0.5
        if sqrt_of_one_face**2 != (total_area // 6):
            raise ValueError(
                "Cannot parse cube face. Each side of the cube doesn't seem to be an integer"
            )

        return int(sqrt_of_one_face)

    def detect_faces(self) -> list[tuple[range, range]]:
        top_left_corners_of_faces = [
            (x, y)
            for y in range(0, self.map_height, self.side_width)
            for x in range(0, self.map_width, self.side_width)
        ]
        faces = [
            (range(x, x + self.side_width), range(y, y + self.side_width))
            for x, y in top_left_corners_of_faces
            if self.get_tile(x=x, y=y) in (Tile.Block, Tile.Space)
        ]
        if len(faces) != 6:
            raise ValueError("Fail to detect the 6 faces of cube map.")

        return faces

    def connect_faces(self):
        """Establish the connections between faces."""
        connections = {}
        # add pairs of direct touching faces
        for a, b in itertools.combinations(range(6), r=2):
            x_range_a, y_range_a = self.faces[a]
            x_range_b, y_range_b = self.faces[b]
            if x_range_a != x_range_b and y_range_a != y_range_b:
                # return early if not directly touching
                continue
            elif (x_range_a == x_range_b) and (y_range_a.stop == y_range_b.start):
                connections[(a, Facing.Down)] = (b, Facing.Up)
                connections[(b, Facing.Up)] = (a, Facing.Down)
            elif (y_range_a == y_range_b) and (x_range_a.stop == x_range_b.start):
                connections[(a, Facing.Right)] = (b, Facing.Left)
                connections[(b, Facing.Left)] = (a, Facing.Right)

        # connect common neighbour faces until all faces are connected
        while len(connections) < 24:
            connections = self.connect_common_neighbours(connections)

        self.face_connections = connections

    def connect_common_neighbours(self, connections: dict) -> dict:
        """Resolve connection from common neighbours.
        If face a is touching face b, a & b must shares two common neighbours.
        Find those indirect connections and return as a dict"""
        new_connections = {}

        for key, value in connections.items():
            (face_a, a_to_b_direction), (face_b, b_to_a_direction) = key, value

            a_b_direction_diff = (b_to_a_direction - a_to_b_direction) + 2
            # rotate +2 will be in opposite direction of a -> b, so only try +1 and +3
            for addition_rotation in (+1, +3):

                a_to_c_direction = a_to_b_direction.turn_clockwise(addition_rotation)
                # return early if already got a -> c
                if (face_a, a_to_c_direction) in connections:
                    continue

                b_to_c_direction = a_to_b_direction.turn_clockwise(
                    a_b_direction_diff + addition_rotation
                )
                # skip if b -> c is not established yet
                if (face_b, b_to_c_direction) not in connections:
                    continue

                face_c, c_to_b_direction = connections[face_b, b_to_c_direction]
                a_c_direction_diff = b_to_c_direction - b_to_a_direction
                c_to_a_direction = c_to_b_direction.turn_clockwise(a_c_direction_diff)
                new_connections[face_a, a_to_c_direction] = (face_c, c_to_a_direction)

        return {**connections, **new_connections}

    def get_neighbour_face(
        self, from_face: int, direction: Facing
    ) -> tuple[int, Facing]:
        return self.face_connections[(from_face, direction)]

    @functools.cache
    def get_face_index(self, x: int, y: int) -> int:
        for face_index, face in enumerate(self.faces):
            x_range, y_range = face
            if x in x_range and y in y_range:
                return face_index

        raise ValueError(f"cannot find position {x, y} on any face")

    def relative_position_on_face(self, x: int, y: int) -> tuple[int, int]:
        face_index = self.get_face_index(x=x, y=y)
        x_range, y_range = self.faces[face_index]
        rel_x = x - x_range.start
        rel_y = y - y_range.start

        return (rel_x, rel_y)

    def face_position_to_absolute_position(
        self, face_index: int, rel_x: int, rel_y: int
    ) -> tuple[int, int]:
        if rel_x > self.side_width or rel_y > self.side_width:
            raise ValueError("Got invalid relative position")
        x_range, y_range = self.faces[face_index]
        x, y = x_range.start + rel_x, y_range.start + rel_y
        return x, y

    def next_tile(self, state: State) -> State:
        x, y, facing = state

        delta = {
            Facing.Right: (1, 0),
            Facing.Down: (0, 1),
            Facing.Left: (-1, 0),
            Facing.Up: (0, -1),
        }
        dx, dy = delta[facing]

        x1 = (x + dx) % self.map_width
        y1 = (y + dy) % self.map_height

        # handle special case if facing a void tile, or next tile is on another face
        # fmt: off
        if (self.get_tile(x=x1, y=y1) == Tile.Void) or self.get_face_index(x, y) != self.get_face_index(x1, y1):
        # fmt: on
            rel_x, rel_y = self.relative_position_on_face(x, y)
            rel_x1, rel_y1 = (rel_x + dx) % self.side_width, (rel_y + dy) % self.side_width

            current_face = self.get_face_index(x, y)
            dest_face_index, dest_facing = self.get_neighbour_face(current_face, facing)
            rotation = (dest_facing - facing + 2) % 4
            for _ in range(rotation):
                rel_x1, rel_y1 = (self.side_width - rel_y1 - 1, rel_x1)

            x1, y1 = self.face_position_to_absolute_position(dest_face_index, rel_x1, rel_y1)
            facing = facing.turn_clockwise(rotation)

        return (x1, y1, facing)


def parse_raw(raw: str, as_cube: bool = False) -> MonkeyMap | MonkeyMapCube:
    raw_map, raw_path = raw.split("\n\n")
    max_y = max(len(line) for line in raw_map.splitlines())
    input_map = [line.ljust(max_y) for line in raw_map.splitlines()]

    path = parse_path(raw_path)

    if not as_cube:
        return MonkeyMap(input_map, path)
    else:
        return MonkeyMapCube(input_map, path)


def parse_path(raw_path: str) -> Path:
    path_in_string: list[str] = re.findall(pattern=r"(\d+|L|R)", string=raw_path)
    parsed_path = [
        int(step) if step.isnumeric() else TurnDirection(step)
        for step in path_in_string
    ]
    return parsed_path


def part_one(monkey_map: MonkeyMap) -> int:
    path = monkey_map.path
    final_state = monkey_map.follow_path(path)

    return monkey_map.calc_password(state=final_state)


if __name__ == "__main__":

    day = 22

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()

    parsed_data = parse_raw(raw_data)
    print(f"part one solution: {part_one(parsed_data)}")

    parsed_data_part_two = parse_raw(raw_data, as_cube=True)
    print(f"part two solution: {part_one(parsed_data_part_two)}")
