import numpy as np

def checking_input_matrices(input_dimension, C, A, R, b):
    matrices = [C, A, R]

    # all matrices have the same shape
    check_rows = []
    check_cols = []
    for M in matrices:
        Nrows, Ncolumns = np.shape(M)
        check_rows.append(Nrows)
        check_cols.append(Ncolumns)

    # all columns must equal input_dimension
    if len(set(check_cols)) != 1 or check_cols[0] != input_dimension:
        raise ValueError("Invalid input! Matrices must have shape k × input_dimension.")

    # all rows must be equal (same k for C, A, R)
    if len(set(check_rows)) != 1:
        raise ValueError("Not equal shapes of rows of the matrices (C, A, R).")

    k = check_rows[0]

    #bias shape: must be k × 1
    if np.shape(b)[0] != k:
        raise ValueError("Not equal shapes of rows between matrices and bias.")
    if np.shape(b)[1] != 1:
        raise ValueError("Bias has a wrong column shape; expected (k, 1).")

    return 'fine'