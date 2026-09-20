import numpy as np

arr = np.array([10, 20, 30, 40, 50, 60, 70])

print("First:",    arr[0])    # 10
print("Last:",     arr[-1])   # 70
print("First 3:",  arr[:3])   # [10 20 30]
print("Mid:",      arr[2:5])  # [30 40 50]
print("Every 2nd:", arr[::2]) # [10 30 50 70]
print("Reversed:", arr[::-1]) # [70 60 50 40 30 20 10]