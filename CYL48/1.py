import numpy as np

# Create a 1D array
arr = np.array([10, 20, 30, 40, 50, 60, 70])
print("Array:", arr)

# --- INDEXING ---
print("\n-- Indexing --")
print("First element:", arr[0])       # 10
print("Last element:", arr[-1])       # 70
print("Third element:", arr[2])       # 30

# --- SLICING ---
print("\n-- Slicing --")
print("First 3:", arr[:3])            # [10 20 30]
print("Last 3:", arr[-3:])            # [50 60 70]
print("Middle:", arr[2:5])            # [30 40 50]
print("Every 2nd:", arr[::2])         # [10 30 50 70]
print("Reversed:", arr[::-1])         # [70 60 50 40 30 20 10]