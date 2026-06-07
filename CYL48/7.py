import pandas as pd
import matplotlib.pyplot as plt

dates = pd.date_range('2024-01-01', periods=6, freq='ME')
sales = [100, 200, 150, 300, 250, 400]

df = pd.DataFrame({'Sales': sales}, index=dates)
plt.plot(df.index, df['Sales'])
plt.show()