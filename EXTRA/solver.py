import time
import numpy as np
from math import exp
from qiskit.algorithms.optimizers import GradientDescent, ADAM, CG

x = [[4.4793, -4.0765,-4.0765], [-4.1793, -4.9218, 1.6774], [-3.9429, -0.7689, 4.8830]]
y = [0,1,1]

def g(x):
    return exp(x) / (1 + exp(x))

def F(W, w, w0, x):
    sum = 0
    for j in range (1,3):
        aux_sum = 0
        for k in range(0,3):
            aux_sum += w[j-1][k] * x[k]
        aux_sum -= w0[j-1]
        sum += W[j] * g(aux_sum)
    return g(sum - W[0])

def E(initial_point):
    W = [initial_point[i] for i in range(0,3)]
    w = [[],[]]
    w[0] = [initial_point[i] for i in range(3,6)]
    w[1] = [initial_point[i] for i in range(6,9)]
    w0 = [initial_point[i] for i in range(9,11)]
    sum = 0
    for u in range(0,3):
        sum += (y[u] - F(W, w, w0, x[u])) ** 2
    return sum

def print_results(title, total_time, W, w ,w0):
    print('------------------------------')
    print(title)
    print(f'total time: {total_time}')
    print(f'W: {W}')
    print(f'w: {w}')
    print(f'w0: {w0}')

def solver():
    num_vars = 11 #hay 11 variables entre las Ws

    # metodo del gradiente descendiente
    start_time = time.time()
    g_descent_result = GradientDescent().optimize(num_vars, E, initial_point=np.zeros(11,float))
    total_time = time.time() - start_time
    W = [g_descent_result[0][i] for i in range(0,3)]
    w = [[], []]
    w[0] = [g_descent_result[0][i] for i in range(3, 6)]
    w[1] = [g_descent_result[0][i] for i in range(6, 9)]
    w0 = [g_descent_result[0][i] for i in range(9, 11)]
    print_results("GRADIENT DESCENDENT",total_time,W,w,w0)

    # metodo de gradientes conjugados
    start_time = time.time()
    conjugate_g_result = CG().optimize(num_vars, E, initial_point=np.zeros(11, float))
    total_time = time.time() - start_time
    W = [conjugate_g_result[0][i] for i in range(0, 3)]
    w = [[], []]
    w[0] = [conjugate_g_result[0][i] for i in range(3, 6)]
    w[1] = [conjugate_g_result[0][i] for i in range(6, 9)]
    w0 = [conjugate_g_result[0][i] for i in range(9, 11)]
    print_results("CONJUGATE GRADIENT",total_time,W,w,w0)

    #metodo ADAM
    start_time = time.time()
    adam_result = ADAM().optimize(num_vars, E, initial_point=np.zeros(11,float))
    total_time = time.time() - start_time
    W = [adam_result[0][i] for i in range(0, 3)]
    w = [[], []]
    w[0] = [adam_result[0][i] for i in range(3, 6)]
    w[1] = [adam_result[0][i] for i in range(6, 9)]
    w0 = [adam_result[0][i] for i in range(9, 11)]
    print_results("ADAM",total_time,W,w,w0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    solver()
