import sys
from random import random

from algorithms.hopfield import Hopfield
from config import Config
from parser import parse_csv, parse_letters


def ej2(config_file: str):
    config: Config = Config(config_file)
    dataset = parse_letters(config.dataset)
    letters = []
    letters.append(dataset[0])
    letters.append(dataset[1])
    letters.append(dataset[2])
    letters.append(dataset[3])
    hopfield = Hopfield(letters)

    testing_letter = letters[2]
    for i in range(len(testing_letter)):
        r = random()
        if r < 0.05:
            if testing_letter[i] == 1:
                testing_letter[i] = -1
            else:
                testing_letter[i] = 1

    results = hopfield.algorithm(testing_letter)
    print(results[-1])
    print(testing_letter)

if __name__ == '__main__':
    argv = sys.argv
    config_file: str = 'config.yaml'
    if len(argv) > 1:
        config_file = argv[1]

    try:
        ej2(config_file)

    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Optimization ended incomplete.')