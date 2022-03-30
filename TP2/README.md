#El problema de la Mochila
En este trabajo se intenta resolver el problema de la mochila utilizando algoritmos genéticos.

### Requisitos
  Tener instalado previamente:

  `numpy`

  `yaml`

  `schema`

  `matplotlib`

## Ejecución

Para la ejecución del programa no es necesario compilarlo, solo se debe ejecutar:

`python3 main.py`

A menos que se indique lo contrario, se utilizará el archivo `config.yaml` provisto en el proyecto.

En caso de querer proveer un archivo de configuración diferente, se debe ejecutar de la siguiente manera:

`python3 main.py <path>`

Una vez finalizado, se imprimirá el beneficio, peso y fitness de la generación final y se mostrarán gráficos de los datos obtenidos en una ventana que se abrirá automáticamente.


## Configuración

Esta se encuentra en el archivo `config.yaml` que contiene:
- **items_file**: aquí se encuentra el archivo `.txt` del cual se obtienen los datos iniciales para resolver el problema. Este parámetro es requerido.
- **population_size**: es requerido, indica el tamaño de la población.
- **selector**: 
  - method: 
    - name: se requiere este parámetro, refiere al nombre del método de selección que se va a implementar, posibles valores:
      - elite
      - roulette
      - rank
      - boltzmann
      - prob_tournament
      - truncate
    - params: indica los parámetros de la selección utilizada, si es que se necesitan
      - initial_temp: utilizada con `boltzmann`, indica la temperatura inicial para la función de temperatura
      - final_temp: utilizada con `boltzmann`, indica la temperatura final para la función de temperatura
      - k: utilizada con `boltzmann`, es una constante mayor a 0 que se utiliza en la función de la temperatura
      - tournament_probability: es utilizada para el método de selección `prob_tournament`, se pide un número del 0 al 1
      - k: utilizada con `truncate`, es un número entero mayor a 0
- **crossover**: 
  - method: 
    - name: los posibles cruzamientos que se pueden realizar son:
      - single_point
      - multiple_point
      - uniform
    - params: en este caso el único que tiene parámetros es el cruzamiento `multiple_point`
      - points_q: cantidad de puntos en el que se va a realizar el cruzamiento, es un número entero positivo
- **mutation_prob**: refiere a la probabilidad de mutación de cada elemento de un individuo
- **stop_condition**: cada uno es opcional, si no está se utiliza la condición de corte por default. Las opciones son:
  - time
  - gen_count
  - percentage
  - gen_count_percentage
  - fitness_gen_count

  
###Ejemplos de configuración
Un ejemplo simple:
```yaml
items_file: Mochila100Elementos.txt
population_size: 12
selector:
  method:
    name: elite
crossover:
  method:
    name: uniform
mutation_prob: 0.005
```
Un ejemplo más completo:
```yaml
items_file: Mochila100Elementos.txt
population_size: 12
selector:
  method:
    name: boltzmann
    params:
      initial_temp: 40
      final_temp: 5
      k: 0.05
crossover:
  method:
    name: multiple_point
    params:
      points_q: 3
mutation_prob: 0.005
stop_condition:
  percentage: 85
  gen_count_percentage: 10
  gen_count: 2000
```

##Resultado
Por la salida estándar se imprime el beneficio, peso y fitness de la generación final. También se mostraran gráficos mostrando los fitness mínimo, máximo y promedio a lo largo de las generaciones.

## Integrantes

- Ana Tarantino Pedrosa 
- Maria Victoria Conca 
- Martina Rodriguez