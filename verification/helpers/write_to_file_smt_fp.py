import numpy as np
from helpers.numpy_float32_to_smt_fp import numpy_float32_to_smt_fp


def write_to_file_smt_fp(filename, array, name):
    array = np.array(array)

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"## {name}:\n")
        f.write(f"```\n{array}\n```\n")
        f.write(f"Shape: {array.shape}, Data type: {array.dtype}\n")

        if array.ndim == 0:
            # scalar
            f.write(f"- {name}={array.item()} = {numpy_float32_to_smt_fp(array.item())}\n")

        elif array.ndim == 1:
            # vector
            for i in range(array.shape[0]):
                f.write(
                    f"- {name}[{i}]={array[i]} = {numpy_float32_to_smt_fp(array[i])}\n"
                )

        elif array.ndim == 2:
            # matrix
            for i in range(array.shape[0]):
                for j in range(array.shape[1]):
                    f.write(
                        f"- {name}[{i},{j}]={array[i, j]} = {numpy_float32_to_smt_fp(array[i, j])}\n"
                    )

        else:
            raise ValueError(f"Unsupported array dimension: {array.ndim}, shape: {array.shape}")