from math import exp

x = [[4.4793, -4.0765,-4.0765], [-4.1793, -4.9218, 1.6774], [-3.9429, -0.7689, 4.8830]]
y = [0,1,1]

def g(x):
    return exp(x) / (1 + exp(x))

#todo check si range empieza en 0 o 1
def F(W, w, w0, x):
    sum = 0
    for j in range (1,2):
        aux_sum = 0
        for k in range(1,3):
            aux_sum += w[j][k] * x[k]
        aux_sum -= w0[j]
        sum += W[j] * g(aux_sum)
    return g(sum - W[0])

def E(W, w, w0):
    sum = 0
    for u in range(1,3):
        sum += (y[u] - F(W, w, w0, x[u])) ** 2
    return sum

def solver():
    # metodo del gradiente descendiente
    # metodo de gradientes conjugados
    #metodo ADAM


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    solver()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
