import sys

from sklearn.decomposition import PCA

from algorithms.oja import Oja
from config import Config
from parser import parse_csv


def ej1b(config_file: str):
    config: Config = Config(config_file)
    dataset = parse_csv(config.dataset)
    oja = Oja(dataset,config.learning_rate)
    results = oja.algorithm()
    print(results[-1])

    pca = PCA()
    principal_components = pca.fit_transform(dataset)
    print(pca.components_.T[:,0])
    print(principal_components[:,0])

if __name__ == '__main__':
    argv = sys.argv
    config_file: str = 'config.yaml'
    if len(argv) > 1:
        config_file = argv[1]

    try:
        ej1b(config_file)

    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Optimization ended incomplete.')