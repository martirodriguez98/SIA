import numpy as np

def transform_input(values: np.ndarray) -> np.ndarray:
    new_values = np.empty((np.size(values, 0), np.size(values, 1) * 5))
    print(f'size(values,0) = {np.size(values,0)}')
    print(f'size(values,1) = {np.size(values,1)}')
#
#     # for i in range(np.size(values,0)):
#     #     bits = ""
#     #     for j in range(np.size(values,1)):
#     #         binary_value = str(str(bin(values[i][j]))[2:].zfill(5))
#     #         bits += binary_value
#     #         print(binary_value)
#     #         print(f'bits: {bits}')
#     #     np.append(new_values[i], int(bits))
#     #     print(new_values[i])
    print(np.array("001"))
    for i in range(np.size(values,0)):
        for j in range(np.size(values,1)):
            binary_value = bin(values[i][j])[2:].zfill(5)
            binary_array: np.array = np.array([binary_value])
            for k in range(np.size(binary_array)):
                np.append(new_values[i], binary_array[k])
        # print(new_values[i])
    return new_values





