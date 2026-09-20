import numpy as np

# Define two matrices
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix Addition
print("Addition:\n", A + B)

# Matrix Multiplication
print("Multiplication:\n", np.dot(A, B))

# Transpose
print("Transpose of A:\n", A.T)

# Determinant
print("Determinant of A:", np.linalg.det(A))