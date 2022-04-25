# SIA - EJERCICIO EXTRA

- Conca, María Victoria
- Rodríguez, Martina
- Tarantino Pedrosa, Ana

##Método de optimización no lineal 
Dadas tres mediciones sobre un reactivo, se desea aproximar los valores de salida para otras posibles entradas, por una función ```F(W, w, w0, ξ)```, donde W es un vector de tres coordenadas de nuúmeros reales, w es una matriz de dimensión 2 × 3 de números reales, y w0 = (w01, w02) tambíén de números reales.

Se busca calcular los valores de W, w y w0 que minimizan el error para los datos de entrada ξ1,ξ2,ξ3, utilizando el método del gradiente descendiente, el método de gradientes conjugados y el método ADAM.

##Dependencias

##Ejecución
Dentro de la carpeta ejecutar
```python solver.py```

El programá devolverá el resultado óptimo para los tres métodos.

##Resultados

- Gradiente Descendiente
```
GRADIENT DESCENDENT
total time: 0.03206205368041992
W: [-0.19009174263022566, 0.11161845341943089, 0.11161845341943089]
w: [[-0.04170859359346768, -0.0021241871821122693, 0.03525965947158727], [-0.04170859359346768, -0.0021241871821122693, 0.03525965947158727]]
w0: [-0.002346762939156144, -0.002346762939156144]
```
- Gradientes Conjugados
```
total time: 0.03562021255493164
W: [6.026020383648485, 6.238947748502161, 6.238947748502161]
w: [[-2.7716546241559774, 0.5320342596187484, 2.338427900825127], [-2.7716546241559774, 0.5320342596187484, 2.338427900825127]]
w0: [0.06093933799120939, 0.06093933799120939]
```
- ADAM
```
total time: 4.872428894042969
W: [8.09956276242295, 8.485666170949726, 8.485666170949726]
w: [[-2.2906852007366223, -0.6573042316745252, 2.2036432106100117], [-2.2906852007366223, -0.6573042316745252, 2.2036432106100117]]
w0: [0.8067614440484838, 0.8067614440484838]
```