import numpy as np


def matrix_multiplication(size, result):
    a = np.random.rand(size, size)
    b = np.random.rand(size, size)

    result["a"] = np.array2string(a)
    result["b"] = np.array2string(b)
    result["c"] = np.array2string(a @ b)

    return 0
