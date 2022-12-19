import re
import itertools
import functools
from typing import NamedTuple

import aoc_helper

class Blueprint(NamedTuple):
    ore_bot_ore_cost: int
    clay_bot_ore_cost: int
    obsidian_bot_ore_cost: int
    obsidian_bot_clay_cost: int
    geode_bot_ore_cost: int
    geode_bot_obsidian_cost: int

class State(NamedTuple):
    ore_bot: int = 1
    clay_bot: int = 0
    obsidian_bot: int = 0
    geode_bot: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other: "State"):
        if isinstance(other, self.__class__):
            return State(*map(sum, zip(self, other)))
        raise ValueError('can only add state to state')



class RobotFactory():
    def __init__(self, blueprints:list[Blueprint]):
        self.blueprints = blueprints

    # @functools.cache
    def run_blueprint(self, blueprint_number: int, input_state: State) -> list[State]:
        bots_at_start = input_state[:4]
        resources_gathered = State(0, 0, 0, 0, *bots_at_start)

        blueprint = self.blueprints[blueprint_number - 1]
        recipe = ''.join(blueprint._fields)

        output_states = []

        if input_state.ore >= blueprint.clay_bot_ore_cost:
            new_state = input_state._replace(
                ore=input_state.ore - blueprint.clay_bot_ore_cost,
                clay_bot=input_state.clay_bot + 1
            )
            output_states.append(new_state)

        # if don't make any bot
        output_states.append(input_state)
        
        output_states = [state + resources_gathered for state in output_states]
        
        return output_states

    def bot_cost(self, blueprint_number:int, bot_name:str) -> State:
        blueprint = self.blueprints[blueprint_number - 1]
        recipe = ''.join(blueprint._fields)
        
    
        return State()

    def can_make_bot(self, blueprint_number:int, input_state: State) -> list[str]:
        return []

def parse_raw(raw: str) -> RobotFactory:
    numbers_each_line = (list(map(int, re.findall(r'\d+', line))) for line in raw.splitlines())
    blueprint_params = (numbers[1:] for numbers in numbers_each_line)
    blueprints = [Blueprint(*params) for params in blueprint_params]

    return RobotFactory(blueprints=blueprints)



def part_one(data):
    ...


def part_two(data):
    ...


if __name__ == "__main__":

    day = None

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
