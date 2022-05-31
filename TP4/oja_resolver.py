import sys

from sklearn.decomposition import PCA

from algorithms.oja import Oja
from config import Config
from parser import parse_csv
import numpy as np


def ej1b(config_file: str):
    config: Config = Config(config_file)
    dataset,countries = parse_csv(config.dataset)
    variables = ["Area","GDP", "Inflation", "Life.expect", "Military","Pop.growth","Unemployment"]
    results = []
    #entrenamos N veces y hacemos promedio de resultados
    l_rates = [0.1, 0.01, 0.001, 0.0001,0.00001]
    l_rates_tags = ["0.1", "0.01", "0.001", "0.0001","0.00001"]
    results_l_rates = []
    for t in range(len(l_rates)):
        oja = Oja(dataset, l_rates[t])
        for i in range(50):
            results.append(oja.algorithm()[-1])
        results = np.array(results).mean(axis=0)
        # oja.plot(variables,results,"Valores","Variables","Primer componente principal",(14,6),'%.4f')
        results_l_rates.append(results)
        results = []
        oja.reset()

    countries_results = []

    # for country in range(len(countries)):
    #     sum = 0
    #     for v in range(len(variables)):
    #         sum += dataset[country][v] * results[v]
    #     countries_results.append(sum)
    # oja.plot(countries,np.array(countries_results),"Valores","Países","Primer componente principal por país con Oja",(14,10),'%.4f')

    pca = PCA()
    principal_components = pca.fit_transform(dataset)

    oja.plot(variables,pca.components_.T[:,0],"Valores","Variables","Primer componente principal",(14,6),'%.4f')

    # ska_results = np.array(principal_components[:,0])
    # oja.plot(countries, ska_results, "Valores", "Países", "Primer componente principal por país con Sklearn", (14, 10), '%.4f')
    #
    errors = []
    for t in range(len(l_rates)):
        sum = 0
        for v in range(len(variables)):
            sum += abs(results_l_rates[t][v] - pca.components_.T[:,0][v])
        print(sum/7)
        errors.append(sum/len(variables))
    errors = np.array(errors)
    print(errors)
    print(l_rates)
    oja.plot_errors(l_rates_tags,errors,"Tasa de aprendizaje","Error","Errores según la tasa de aprendizaje",(14,6),'%.4f')


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