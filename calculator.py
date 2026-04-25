"""
Matrix Calculator Engine
Pure computation module using NumPy for all matrix operations.
"""

import numpy as np
from numpy.linalg import LinAlgError


def add(a, b):
    """Add two matrices."""
    if a.shape != b.shape:
        raise ValueError(f"Dimension mismatch: A is {a.shape}, B is {b.shape}. Matrices must have the same dimensions for addition.")
    return a + b


def subtract(a, b):
    """Subtract matrix B from matrix A."""
    if a.shape != b.shape:
        raise ValueError(f"Dimension mismatch: A is {a.shape}, B is {b.shape}. Matrices must have the same dimensions for subtraction.")
    return a - b


def multiply(a, b):
    """Multiply two matrices."""
    if a.shape[1] != b.shape[0]:
        raise ValueError(f"Dimension mismatch: A is {a.shape}, B is {b.shape}. A's columns ({a.shape[1]}) must equal B's rows ({b.shape[0]}).")
    return a @ b


def scalar_multiply(a, scalar):
    """Multiply a matrix by a scalar."""
    return scalar * a


def transpose(a):
    """Transpose a matrix."""
    return a.T


def determinant(a):
    """Compute determinant of a square matrix."""
    if a.shape[0] != a.shape[1]:
        raise ValueError(f"Matrix must be square. Got {a.shape[0]}×{a.shape[1]}.")
    return np.linalg.det(a)


def inverse(a):
    """Compute inverse of a square matrix."""
    if a.shape[0] != a.shape[1]:
        raise ValueError(f"Matrix must be square. Got {a.shape[0]}×{a.shape[1]}.")
    det = np.linalg.det(a)
    if np.isclose(det, 0):
        raise ValueError("Matrix is singular (determinant ≈ 0). No inverse exists.")
    return np.linalg.inv(a)


def rank(a):
    """Compute rank of a matrix."""
    return np.linalg.matrix_rank(a)


def trace(a):
    """Compute trace of a square matrix."""
    if a.shape[0] != a.shape[1]:
        raise ValueError(f"Matrix must be square. Got {a.shape[0]}×{a.shape[1]}.")
    return np.trace(a)


def eigenvalues(a):
    """Compute eigenvalues of a square matrix."""
    if a.shape[0] != a.shape[1]:
        raise ValueError(f"Matrix must be square. Got {a.shape[0]}×{a.shape[1]}.")
    vals = np.linalg.eigvals(a)
    return vals


def rref(a):
    """Compute Row Reduced Echelon Form using Gauss-Jordan elimination."""
    mat = a.astype(float).copy()
    rows, cols = mat.shape
    pivot_row = 0

    for col in range(cols):
        if pivot_row >= rows:
            break

        # Find pivot
        max_row = pivot_row
        for row in range(pivot_row + 1, rows):
            if abs(mat[row, col]) > abs(mat[max_row, col]):
                max_row = row

        if np.isclose(mat[max_row, col], 0):
            continue

        # Swap rows
        mat[[pivot_row, max_row]] = mat[[max_row, pivot_row]]

        # Scale pivot row
        mat[pivot_row] = mat[pivot_row] / mat[pivot_row, col]

        # Eliminate column
        for row in range(rows):
            if row != pivot_row and not np.isclose(mat[row, col], 0):
                mat[row] -= mat[row, col] * mat[pivot_row]

        pivot_row += 1

    # Clean up near-zero values
    mat[np.abs(mat) < 1e-10] = 0.0
    return mat


def power(a, n):
    """Raise a square matrix to an integer power."""
    if a.shape[0] != a.shape[1]:
        raise ValueError(f"Matrix must be square. Got {a.shape[0]}×{a.shape[1]}.")
    if not isinstance(n, int) or n < 0:
        raise ValueError("Power must be a non-negative integer.")
    return np.linalg.matrix_power(a, n)
