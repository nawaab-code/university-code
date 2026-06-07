import pandas as pd

data = {
    'Name':   ['Alice', 'Bob', None],
    'Age':    [25, None, 28],
    'Salary': [50000, 60000, None]
}

df = pd.DataFrame(data)
print(df)
print(df.describe())
print(df.isnull().sum())