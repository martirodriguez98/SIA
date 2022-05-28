import operator
import sys
from math import sqrt

from config import Config
from algorithms.kohonen import Kohonen
from parser import parse_csv
from numpy import array

grid = {'centers': array([[ 1.5, 0.8660254 ],
                 [ 2.,  0.8660254 ],
                 [ 3.,  0.8660254 ],
                 [ 4.,  0.8660254 ],
                 [ 5.,  0.8660254 ],
                 [ 6.,  0.8660254 ],
                 [ 1.,  1.73205081],
                 [ 2.,  1.73205081],
                 [ 3.,  1.73205081],
                 [ 4.,  1.73205081],
                 [ 5.,  1.73205081],
                 [ 6.,  1.73205081],
                 [ 1.,  2.59807621],
                 [ 2.,  2.59807621],
                 [ 3.,  2.59807621],
                 [ 4.,  2.59807621],
                 [ 5.,  2.59807621],
                 [ 6.,  2.59807621],
                 [ 1.,  3.46410162],
                 [ 2.,  3.46410162],
                 [ 3.,  3.46410162],
                 [ 4.,  3.46410162],
                 [ 5.,  3.46410162],
                 [ 6.,  3.46410162],
                 [ 1.,  4.33012702],
                 [ 2.,  4.33012702],
                 [ 3.,  4.33012702],
                 [ 4.,  4.33012702],
                 [ 5.,  4.33012702],
                 [ 6.,  4.33012702],
                 [ 1.,  5.19615242],
                 [ 2.,  5.19615242],
                 [ 3.,  5.19615242],
                 [ 4.,  5.19615242],
                 [ 5.,  5.19615242],
                 [ 6.,  5.19615242]])}

def ej1(config_file: str):
    config: Config = Config(config_file)
    dataset,countries = parse_csv(config.dataset)
    kohonen = Kohonen(config.k,dataset,config.learning_rate,2)
    last_activations = kohonen.algorithm()
    country_act = []
    for country,act in zip(countries,last_activations):
        country_act.append((country, *act))
    print(country_act)
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