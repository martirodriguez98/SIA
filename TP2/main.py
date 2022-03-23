import sys

from Items import Items
from config_loader import Config


def main(config_file: str):
    config: Config = Config(config_file)
    items: Items = Items(config.items_file)
    for i in range(len(items.items)):
        print(items.items[i])


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


