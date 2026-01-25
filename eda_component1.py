import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv("component1_merged.csv")

df.head()
df.info()
df.describe()

#Count the edges per system

sns.countplot(data=df, x="system_type")
plt.title("Number of edge records per system")
plt.show()

#missing values heatmap

sns.heatmap(df.isna(), cbar=False)
plt.title("Missing values overview")
plt.show()

