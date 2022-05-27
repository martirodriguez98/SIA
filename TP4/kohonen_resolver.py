import sys

from config import Config
from algorithms.kohonen import Kohonen
from parser import parse_csv


def ej1(config_file: str):
    config: Config = Config(config_file)
    dataset = parse_csv(config.dataset)
    kohonen = Kohonen(config.k,dataset,config.learning_rate,1)
    kohonen.algorithm()

if __name__ == '__main__':
    argv = sys.argv
    config_file: str = 'config.yaml'
    if len(argv) > 1:
        config_file = argv[1]

    try:
        ej1(config_file)

    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Optimization ended incomplete.')