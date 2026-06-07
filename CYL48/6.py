import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("tips")

plt.figure(1)
sns.scatterplot(data=df)

plt.figure(2)
sns.histplot(data=df)

plt.figure(3)
sns.boxplot(data=df)

plt.figure(4)
sns.violinplot(data=df)

plt.show()