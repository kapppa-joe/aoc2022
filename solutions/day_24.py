import numpy as np
import functools
from enum import Enum
from typing import NamedTuple


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: tuple[int, int]) -> "Coord":
        """helper method for easy vector summing
        >>> Coord(1, 3) + Coord(2, 3)
        Coord(3, 6)
        """
        if isinstance(other, tuple) and len(other) == 2:
            dx, dy = other
            return Coord(self.x + dx, self.y + dy)
        else:
            raise ValueError("Can only add a coordinate to a pair of int")

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"


class Tile(Enum):
    Empty = 0
    Wall = 1
    BlizzardUp = 2
    BlizzardRight = 4
    BlizzardDown = 8
    BlizzardLeft = 16

    @classmethod
    @functools.cache
    def string_representations(cls) -> dict["Tile", str]:
        all_tiles = ".#^>v<"
        return {tile: all_tiles[i] for i, tile in enumerate(cls)}

    @classmethod
    @functools.cache
    def from_str(cls, tile_string: str) -> "Tile":
        reverse_dict = {
            value: key for key, value in cls.string_representations().items()
        }
        return reverse_dict[tile_string]

    @classmethod
    @functools.cache
    def to_str(cls, tile_value: int) -> str:
        dict = cls.string_representations()
        all_tile_values = [tile.value for tile in dict]
        if tile_value in all_tile_values:
            return dict[Tile(tile_value)]
        else:
            # if multiple blizzard overlap, count bit and display the digit as tile
            return str(bin(tile_value).count("1"))

    @classmethod
    def blizzards(cls) -> list["Tile"]:
        return [
            cls.BlizzardUp,
            cls.BlizzardRight,
            cls.BlizzardDown,
            cls.BlizzardLeft,
        ]

    @classmethod
    def obstacles(cls) -> list["Tile"]:
        return [cls.Wall] + cls.blizzards()


ObstacleMaps = dict[Tile, np.ndarray]


class BlizzardBasin:
    def __init__(self, input_map: str):
        lines = input_map.splitlines()
        combined_map = np.array(
            [[self.object_index(tile) for tile in line] for line in lines], dtype=int
        )
        self.obstacle_maps = {
            obstacle: (combined_map == obstacle.value) for obstacle in Tile.obstacles()
        }
        self.height, self.width = combined_map.shape
        self.inner_height = self.height - 2
        self.inner_width = self.width - 2

    def object_index(self, tile: str) -> int:
        return Tile.from_str(tile).value

    def obstacle_map_as_string(self, obstacle_maps: ObstacleMaps) -> str:
        combined_map: np.ndarray = sum(
            individual_map * obstacle.value
            for obstacle, individual_map in obstacle_maps.items()
        )  # pyright: ignore

        converted_to_strings = [
            [Tile.to_str(tile_value) for tile_value in row]
            for row in combined_map.tolist()
        ]
        lines = ["".join(row) for row in converted_to_strings]
        return "\n".join(lines)

    def obstacles_for_turn_n(self, n: int) -> ObstacleMaps:
        dy = n % self.inner_height
        dx = n % self.inner_width

        new_maps = {}
        new_maps[Tile.Wall] = self.obstacle_maps[Tile.Wall]

        for blizzard_type in Tile.blizzards():
            base_map = self.obstacle_maps[blizzard_type]
            inner_area = base_map[1:-1, 1:-1]

            match blizzard_type:
                case Tile.BlizzardUp:
                    new_inner_area = np.concatenate(
                        [inner_area[dy:, :], inner_area[:dy, :]], axis=0
                    )
                case Tile.BlizzardRight:
                    new_inner_area = np.concatenate(
                        [inner_area[:, (-1 * dx) :], inner_area[:, : (-1 * dx)]], axis=1
                    )
                case Tile.BlizzardDown:
                    new_inner_area = np.concatenate(
                        [inner_area[(-1 * dy) :, :], inner_area[: (-1 * dy), :]], axis=0
                    )
                case Tile.BlizzardLeft:
                    new_inner_area = np.concatenate(
                        [inner_area[:, dx:], inner_area[:, :dx]], axis=1
                    )
                case _:
                    raise RuntimeError("Unexpected case. Possibly a bug")

            new_map = np.zeros(shape=base_map.shape, dtype=bool)
            new_map[1:-1, 1:-1] = new_inner_area

            new_maps[blizzard_type] = new_map

        return new_maps


def parse_raw(raw: str) -> BlizzardBasin:
    return BlizzardBasin(input_map=raw)


def part_one(data):
    ...


def part_two(data):
    ...


if __name__ == "__main__":

    day = 24

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
