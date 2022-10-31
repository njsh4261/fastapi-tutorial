import numpy as np


def matrix_multiplication(size):
    a = np.random.rand(size, size)
    b = np.random.rand(size, size)
    return {
        "a": np.array2string(a),
        "b": np.array2string(b),
        "c": np.array2string(a @ b)
    }
