import sys
from random import random

from algorithms.hopfield import Hopfield
from config import Config
from parser import parse_csv, parse_letters


def ej2(config_file: str):
    config: Config = Config(config_file)
    mutations = 2
    dataset = parse_letters(config.dataset)
    letters = []
    # orthogonals
    # letters.append(dataset[9])
    # letters.append(dataset[4])
    # letters.append(dataset[10])
    # letters.append(dataset[22])
    # #non-orthogonals
    letters.append(dataset[15])
    letters.append(dataset[17])
    letters.append(dataset[1])
    letters.append(dataset[5])

    hopfield = Hopfield(letters, dataset)

    for l in letters:
        print(hopfield.letter_is(l))
        hopfield.print_pattern(l,5)

    mutated_letters = letters
    for m in range(mutations):
        for l in range(len(letters)):
            mutated_letters[l] = add_noise(mutated_letters[l])

    for l in range(len(mutated_letters)):
        print(f'mutated letter: {hopfield.letter_is(letters[l])}')
        hopfield.print_pattern(mutated_letters[l],5)
        results = hopfield.algorithm(mutated_letters[l])
    # print(results[-1])
    # print(testing_letter)

def add_noise(pattern):
    testing_letter = pattern
    for i in range(len(testing_letter)):
        r = random()
        if r < 0.05:
            if testing_letter[i] == 1:
                testing_letter[i] = -1
            else:
                testing_letter[i] = 1
    return testing_letter



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