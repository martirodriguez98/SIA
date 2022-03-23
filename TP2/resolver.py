from typing import Set, Tuple

from Items import Items, Item
from config_loader import Config
from generation import Generation


class Resolver:
    def __init__(self, config: Config, items: Items):
        self.items: Items = items
        self.population_size: int = config.population_size

    def bag_packer(self) -> Tuple[int, Set[Item]]:
        current_generation: Generation = Generation.create_first_generation(self.items, self.population_size)
        return 0, current_generation.bag.bag
