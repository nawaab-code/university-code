import matplotlib.pyplot as plt
import numpy as np

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
sales  = [150, 200, 170, 220, 190]

# Line Chart
plt.plot(months, sales)
plt.show()

# Bar Chart
plt.bar(months, sales)
plt.show()

# Pie Chart
plt.pie(sales, labels=months)
plt.show()

# 3D Plot
ax = plt.axes(projection='3d')
x = np.linspace(0, 5, 100)
ax.plot(x, np.sin(x), np.cos(x))
plt.show()