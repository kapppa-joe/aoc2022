import re
import itertools
import functools
from typing import Iterable, NamedTuple

import aoc_helper

class Blueprint(NamedTuple):
    ore_bot_ore_cost: int
    clay_bot_ore_cost: int
    obsidian_bot_ore_cost: int
    obsidian_bot_clay_cost: int
    geode_bot_ore_cost: int
    geode_bot_obsidian_cost: int

class State(NamedTuple):
    geode_bot: int = 0
    obsidian_bot: int = 0
    clay_bot: int = 0
    ore_bot: int = 0
    geode: int = 0
    obsidian: int = 0
    clay: int = 0
    ore: int = 0

    def __add__(self, other: "State") -> "State":
        if isinstance(other, self.__class__):
            return State(*map(sum, zip(self, other)))
        raise ValueError('can only add state to state')

    def __sub__(self, other: "State") -> "State":
        deduction = [value * -1 for value in other]
        if isinstance(other, self.__class__):
            return State(*map(sum, zip(self, deduction)))
        raise ValueError('can only subtract state from state')

    def __repr__(self) -> str:
        fmt = (f"{name}={qty}" for name, qty in self._asdict().items() if qty > 0)
        return self.__class__.__name__ + f"({', '.join(fmt)})"

    def can_afford(self, other: "State") -> bool:
        if not isinstance(other, self.__class__):
            raise ValueError('can only compare state with state')  

        self_resources = self[4:]
        resources_cost = other[4:]
        
        return all(has_got >= cost for has_got, cost in zip(self_resources, resources_cost))

    def better_than(self, other: "State") -> bool:
        return all(self_qty >= other_qty for self_qty, other_qty in zip(self, other))

BotTypes = State._fields[:4]
ResourceTypes = State._fields[4:]


class RobotFactory():
    def __init__(self, blueprints:list[Blueprint]):
        self.blueprints = blueprints

    @functools.cache
    def get_bot_cost(self, blueprint_num:int, bot_type:str) -> State:
        blueprint = self.blueprints[blueprint_num - 1]
        recipe_dict = {}

        for recipe, qty in blueprint._asdict().items():
            if recipe.startswith(bot_type):
                resource_type = recipe.replace(f'{bot_type}_', '').replace('_cost', '')
                recipe_dict[resource_type] = qty

        return State(**recipe_dict)

    def can_make_bot(self, blueprint_num:int, input_state: State) -> list[str]:
        result = []
        for bot_type in BotTypes:
            cost = self.get_bot_cost(blueprint_num=blueprint_num, bot_type=bot_type)
            if input_state.can_afford(cost):
                result.append(bot_type)

        return result

    @functools.cache
    def run_blueprint(self, blueprint_num: int, input_state: State) -> list[State]:
        bots_at_start = input_state[:4]
        resources_gathered = State(0, 0, 0, 0, *bots_at_start)

        output_states = []

        bot_choices = self.can_make_bot(blueprint_num=blueprint_num, input_state=input_state)
        for bot_type in bot_choices:
            cost = self.get_bot_cost(blueprint_num=blueprint_num, bot_type=bot_type)
            new_state = input_state - cost + State(**{bot_type: 1})
            output_states.append(new_state)

            if bot_type == 'geode_bot':
                # if can make geode_bot, rush for it!
                break


        # if some type of bot can't be made now, add the choice of withholding resource.
        if len(bot_choices) != len(BotTypes) and ('geode_bot' not in bot_choices):
            output_states.append(input_state)
        
        # add collected resource at turn end
        output_states = [state + resources_gathered for state in output_states]
        
        return output_states

    def trim_inferior_state(self, states: set[State]) -> set[State]:
        if len(states) < 2:
            return states 

        results = set()
        sorted_states = sorted(states, reverse=True)
        current = sorted_states[0]

        for state in sorted_states[1:]:
            if current.better_than(state):
                continue
            else:
                results.add(current)
                current = state
        results.add(current)

        return results

    def run_n_turns(self, turn_count: int, blueprint_num: int, initial_state: State) -> set[State]:
        all_states = set([initial_state])
        for _ in range(turn_count):
            all_states = set(output 
                for state in all_states
                for output in self.run_blueprint(blueprint_num=blueprint_num, input_state=state) 
            )
            all_states = self.trim_inferior_state(all_states)
        return all_states

    def best_geode_for_blueprint(self, blueprint_num: int, minutes=24) -> int:
        initial_state = State(ore_bot=1)
        all_states_collected = self.run_n_turns(turn_count=minutes, blueprint_num=blueprint_num, initial_state=initial_state)
        return max(state.geode for state in all_states_collected)


def parse_raw(raw: str) -> RobotFactory:
    numbers_each_line = (list(map(int, re.findall(r'\d+', line))) for line in raw.splitlines())
    blueprint_params = (numbers[1:] for numbers in numbers_each_line)
    blueprints = [Blueprint(*params) for params in blueprint_params]

    return RobotFactory(blueprints=blueprints)



def part_one(factory: RobotFactory) -> int:
    return sum(
        blueprint_num * factory.best_geode_for_blueprint(blueprint_num)
        for blueprint_num in range(1, len(factory.blueprints) + 1)
    )


def part_two(data):
    ...


if __name__ == "__main__":

    day = 19

    raw_data = aoc_helper.fetch(day, 2022)
    parsed_data = parse_raw(raw_data)

    print(f"part one solution: {part_one(parsed_data)}")
    print(f"part two solution: {part_two(parsed_data)}")
