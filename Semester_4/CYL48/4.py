import pandas as pd

df = pd.read_csv("file.csv")
print(df)
print(df.describe())
print(df.isnull().sum())