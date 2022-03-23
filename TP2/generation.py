from Items import Items
from bag import Bag


class Generation:

    @staticmethod
    def create_first_generation(items: Items, population_size: int) -> 'Generation':
        return Generation(items.generate_random_set(population_size), 0)

    def __init__(self, bag: Bag, gen_count: int):
        self.bag: Bag = bag
        self.generation_size: int = gen_count
