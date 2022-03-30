import sys
from typing import List, Tuple

from bag import Bag
from data_loader import Item, load_data
from resolver import Resolver
from config_loader import Config


def main(config_file: str):
    config: Config = Config(config_file)
    data_loaded: Tuple[int, int, List[Item]] = load_data(config.items_file)
    bag: Bag = Bag(data_loaded[0], data_loaded[1], data_loaded[2])
    resolver: Resolver = Resolver(config, bag)
    resolver.bag_packer()


if __name__ == '__main__':

    argv = sys.argv
    config_file: str = 'config.yaml'

    # if another file is provided
    if len(argv) > 1:
        config_file = argv[1]

    try:
        main(config_file)

    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Optimization ended incomplete.')
