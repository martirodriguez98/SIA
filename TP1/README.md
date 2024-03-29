#Rompecabezas de números
En este trabajo se implementa un programa que resuelve problemas de rompecabezas de 8 números utilizando diferentes métodos de búsqueda. 
- **Métodos de búsqueda desinformados:**
  - BPA : Búsqueda Primero a lo Ancho
  - BPP: Búsqueda Primero en Profundidad 
  - BPPV: Búsqueda en Profundidad Variable 
- **Métodos de búsqueda informados:**
  - Búsqueda heuristica local
  - Búsqueda heuristica global
  - A*

## Ejecución

Para la ejecución del programa no es necesario compilarlo, solo se debe ejecutar:

`python3 puzzle_solver.py`

A menos que se indique lo contrario, se utilizará el archivo `config.yaml` provisto en el proyecto.

En caso de querer proveer un archivo de configuración diferente, se debe ejecutar de la siguiente manera:

`python3 puzzle_solver.py <path>`

Una vez finalizado, se imprimirán las estadísticas por salida estándar.

### Requisitos
  Tener instalado previamente:

  `numpy`

  `yaml`

## Configuración

Esta se encuentra en el archivo `config.yaml` que contiene:
- **strategy**
  - name: hace referencia al nombre del método de búsqueda a implementar, las posibles opciones son:

    - BPA 
    - BPP
    - BPPV
    - LOCAL_H
    - GLOBAL_H
    - A_STAR
  - params: se utiliza solo con las búsquedas informadas
  
    - heuristic: refiere a las funciones heurísticas para los métodos de búsqueda informados, sus valores posibles son los siguientes:
    
      - manhattan_distance: Suma de las distancias desde la posición actual de cada ficha hasta su posición correcta. Sin contar la casilla vacía.
      - hamming_distance: Suma de las piezas que se encuentran fuera de lugar. Sin contar la casilla vacía.
      - manhattan_hamming: Suma de las dos anteriores y además se cuenta la distancia de la casilla vacía.
  
###Ejemplos de configuración
```yaml
strategy: 
  name: BPA
```

```yaml
strategy: 
  name: GLOBAL_H
  params:
    heuristic: manhattan_distance
```

##Resultado
Por la salida estándar se imprimen las estadísticas una vez finalizada la ejecución. Las mismas informan:

- `Profundidad`: Cantidad de pasos que tiene la solución.
- `Costo`: Para los algoritmos informados, se muestra el costo de la solución
- `Cantidad de nodos frontera`: Cantidad de nodos frontera al finalizar el algoritmo.
- `Cantidad de nodos expandidos`: Cantidad de nodos que fueron analizados y expandidos.
- `Tiempo de procesamiento`: Tiempo que se tardó en ejecutar el algoritmo.
- `Estados`: Se imprimen todos los estados de la solución encontrada.

## Integrantes

- Ana Tarantino Pedrosa 
- Maria Victoria Conca 
- Martina Rodriguez