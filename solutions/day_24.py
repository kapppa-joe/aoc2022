import functools
from enum import Enum

import numpy as np


class Tile(Enum):
    Empty = 0
    Wall = 1
    BlizzardUp = 2
    BlizzardRight = 4
    BlizzardDown = 8
    BlizzardLeft = 16
    Expedition = 32

    @classmethod
    @functools.cache
    def string_representations(cls) -> dict["Tile", str]:
        all_tiles = ".#^>v<E"
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
    def __init__(self, raw_string: str):
        combined_map = self.string_to_combined_map(raw_string)
        self.height, self.width = combined_map.shape
        self.inner_height = self.height - 2
        self.inner_width = self.width - 2

        empty_tiles = np.argwhere(combined_map == Tile.Empty.value)
        self.start = tuple(empty_tiles[0])
        self.goal = tuple(empty_tiles[-1])

        self.obstacle_maps = {
            obstacle: (combined_map == obstacle.value) for obstacle in Tile.obstacles()
        }

    def string_to_combined_map(self, raw_string: str) -> np.ndarray:
        """Convert the string representation as in AoC official site example to a combined map of np.array .
        Seperate this from __init__ for reuse in tests."""
        lines = raw_string.splitlines()
        return np.array(
            [[Tile.from_str(tile).value for tile in line] for line in lines], dtype=int
        )

    def combine_map_to_string(self, combined_map: np.ndarray) -> str:
        """Convert a combined map to the string representation as in AoC official site example. Mostly for testing purpose."""
        converted_to_strings = [
            [Tile.to_str(tile_value) for tile_value in row]
            for row in combined_map.tolist()
        ]
        lines = ["".join(row) for row in converted_to_strings]
        return "\n".join(lines)

    def obstacle_map_as_string(self, obstacle_maps: ObstacleMaps) -> str:
        """Convert obstacle_maps to the string representation as in AoC official site example. Mostly for testing purpose."""
        combined_map: np.ndarray = sum(
            individual_map * obstacle.value
            for obstacle, individual_map in obstacle_maps.items()
        )  # pyright: ignore

        return self.combine_map_to_string(combined_map)

    @functools.cache
    def forecast_blizzard_for_turn_n(self, n: int, blizzard_type: Tile) -> np.ndarray:
        """Return the locations of certain blizzard on turn N.
        If we only consider the inner area (those cells within the walls),
        for blizzard moving left/right, it is just slicing the 0:n columns and concat it to the left or right side of the n: columns.
        Similar for blizzard moving up/down.

        As the pattern repeats in vertical directions when n >= inner_height and in horizontal directions for n >= inner_width,
        use functools cache to memoize patterns that already computed before.

        Args:
            n (int): turn number
            blizzard_type (Tile): blizzard type

        Returns:
            np.ndarray: A numpy array of boolean value. True denotes that blizzard exist on that tile.
        """
        # fmt: off
        if n >= self.inner_height and blizzard_type in (Tile.BlizzardUp, Tile.BlizzardDown):
            return self.forecast_blizzard_for_turn_n(n % self.inner_height, blizzard_type)
        elif n >= self.inner_width and blizzard_type in (Tile.BlizzardLeft, Tile.BlizzardRight):
            return self.forecast_blizzard_for_turn_n(n % self.inner_width, blizzard_type)
        
        base_map = self.obstacle_maps[blizzard_type]
        inner_area = base_map[1:-1, 1:-1]

  
        match blizzard_type:
            case Tile.BlizzardUp:
                new_inner_area = np.concatenate([inner_area[n:, :], inner_area[:n, :]], axis=0)
            case Tile.BlizzardRight:
                new_inner_area = np.concatenate([inner_area[:, (-1 * n) :], inner_area[:, : (-1 * n)]], axis=1)
            case Tile.BlizzardDown:
                new_inner_area = np.concatenate([inner_area[(-1 * n) :, :], inner_area[: (-1 * n), :]], axis=0)
            case Tile.BlizzardLeft:
                new_inner_area = np.concatenate([inner_area[:, n:], inner_area[:, :n]], axis=1)
            case _:
                raise RuntimeError("Unexpected case. Possibly a bug")
        # fmt: on

        new_map = np.zeros(shape=base_map.shape, dtype=bool)
        new_map[1:-1, 1:-1] = new_inner_area

        return new_map

    def make_obstacle_maps_for_turn_n(self, n: int) -> ObstacleMaps:
        """Return a dict that contains the map of each type of obstacle in turn N

        Args:
            n (int): turn number

        Returns:
            ObstacleMaps: A dict that represent the locations of each type of obstacle.
            Keys are Tile and values are numpy arrays (in bool)
        """
        new_maps = {}
        new_maps[Tile.Wall] = self.obstacle_maps[Tile.Wall]

        for blizzard_type in Tile.blizzards():
            new_maps[blizzard_type] = self.forecast_blizzard_for_turn_n(
                n=n, blizzard_type=blizzard_type
            )

        return new_maps

    def four_directions(self, coord: tuple[int, int]) -> list[tuple[int, int]]:
        output = []
        y0, x0 = coord
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            y1, x1 = y0 + dy, x0 + dx
            if 0 <= y1 < self.height and 0 <= x1 < self.width:
                output.append((y1, x1))

        return output

    def next_turn_moves(self, current_locations: np.ndarray) -> np.ndarray:
        """Simulate all possible moves that Expedition can take in next turn.
        Ignore any obstacles. Only consider boundries and the diffusion to four directions.

        Args:
            current_locations (np.ndarray): An np.array in bool that denote all possible current location of Expedition in this turn.

        Returns:
            np.ndarray: An np.array in bool that denote all possible moves for the Expedition to take in next turn.
        """
        new_state = np.zeros(shape=current_locations.shape, dtype=bool)

        for coord in np.argwhere(current_locations == True):
            four_neighbour_tiles = self.four_directions(coord)
            for y, x in [coord, *four_neighbour_tiles]:
                new_state[y, x] = True

        return new_state

    def simulate_next_turn(
        self, current_locations: np.ndarray, next_turn_obstacles: ObstacleMaps
    ) -> np.ndarray:
        """Simulate all possible moves that Expedition can take in next turn.
        This one take account of obstacles.
        Tiles that the Expedition can exist in are denoted as True
        """
        all_moves = self.next_turn_moves(current_locations)
        obstacles = sum(next_turn_obstacles.values()).astype(bool)  # pyright: ignore
        all_possible_moves = all_moves & ~obstacles

        return all_possible_moves

    def bfs(
        self, start: tuple[int, int], goal: tuple[int, int], starting_turn: int = 0
    ) -> int:
        initial_state = np.zeros(shape=(self.height, self.width), dtype=bool)
        initial_state[start] = True

        locations = initial_state
        turn_number = starting_turn

        while not locations[goal]:
            next_turn_obstacles = self.make_obstacle_maps_for_turn_n(n=turn_number + 1)
            locations = self.simulate_next_turn(locations, next_turn_obstacles)
            turn_number += 1

        return turn_number


def parse_raw(raw: str) -> BlizzardBasin:
    return BlizzardBasin(raw_string=raw)


def part_one(basin: BlizzardBasin) -> int:
    start = basin.start
    goal = basin.goal
    starting_turn = 0
    return basin.bfs(start=start, goal=goal, starting_turn=starting_turn)


def part_two(basin: BlizzardBasin) -> int:
    start = basin.start
    goal = basin.goal

    first_trip = basin.bfs(start=start, goal=goal, starting_turn=0)
    return_trip = basin.bfs(start=goal, goal=start, starting_turn=first_trip)
    third_trip = basin.bfs(start=start, goal=goal, starting_turn=return_trip)

    return third_trip


if __name__ == "__main__":

    day = 24

    raw_data = open(f"puzzle/day_{day}.txt", "r").read()
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
