from typing import Set, Tuple, List

import bag
from bag import Bag
from config_loader import Config
from data_loader import Item
from generation import Generation, Population


class Resolver:
    def __init__(self, config: Config, bag: Bag):
        self.bag: Bag = bag
        self.population_size: int = config.population_size

    def bag_packer(self) -> Tuple[Population,int]: #bag, generation_count
        current_generation: Generation = Generation.create_first_generation(self.bag, self.population_size)

        return current_generation.population,0
        #TODO change, solo para que no tire errores
