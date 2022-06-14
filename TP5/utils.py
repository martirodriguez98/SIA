import numpy as np

def transform_input(values: np.ndarray) -> np.ndarray:
    new_values = np.empty((np.size(values, 0), np.size(values, 1) * 5)).astype(int)
    for i in range(np.size(values,0)):
        total_bits: list = []
        for j in range(np.size(values,1)):
            binary_value = bin(values[i][j])[2:].zfill(5)
            total_bits.append(list(binary_value))
        new_values[i] = np.array(total_bits).flatten()
    return new_values





