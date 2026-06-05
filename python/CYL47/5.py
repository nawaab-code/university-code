import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create a date range
dates = pd.date_range(start="2025-01-01", periods=50, freq="D")

# Generate sample time series data
values = np.random.randn(50).cumsum()

# Create DataFrame
df = pd.DataFrame({
    "Date": dates,
    "Value": values
})

# Set Date as index
df.set_index("Date", inplace=True)

# Plot time series
plt.figure(figsize=(10,5))
plt.plot(df.index, df["Value"], marker='o')
plt.title("Time Series Visualization")
plt.xlabel("Date")
plt.ylabel("Value")
plt.grid(True)

# Display plot
plt.show()
