import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv("component1_merged.csv")

df.head()
df.info()
df.describe()

df["system_encoded"] = df["system_type"].map({
    "fixed": 0,
    "adaptive": 1
})

#Count the edges per system

sns.countplot(data=df, x="system_type")
plt.title("Number of edge records per system")
plt.show()

#comparison for mean waiting time

mean_wait = df.groupby("system_type")["avg_waiting_time"].mean()

mean_wait.plot(kind="bar")
plt.ylabel("Average waiting time")
plt.title("Average waiting time by system")
plt.show()

# Distribution comparison (one KDE, not multiple boxes)

sns.kdeplot(
    data=df,
    x="avg_waiting_time",
    hue="system_type",
    fill=True,
    common_norm=False,
    alpha=0.4
)
plt.title("Waiting time distribution: Fixed vs Adaptive")
plt.show()

# Proportion of high-traffic edges per system
########check why equal#####################
high_traffic_rate = (
    df.groupby("system_type")["is_high_traffic"].mean()
)

high_traffic_rate.plot(kind="bar")
plt.ylabel("Proportion of high-traffic edges")
plt.title("High-traffic edge proportion by system")
plt.show()

# Traffic score vs vehicle count (relationship plot)
sns.scatterplot(
    data=df,
    x="vehicle_count",
    y="traffic_score",
    hue="system_type",
    alpha=0.6
)
plt.title("Traffic score vs vehicle count")
plt.show()


# Correlation heatmap (SELECTIVE COLUMNS)

cols = [
    "vehicle_count",
    "avg_waiting_time",
    "avg_time_loss",
    "traffic_score",
    "system_encoded"
]

corr = df[cols].corr()

sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Feature correlation matrix")
plt.show()


# Traffic score difference by system

sns.boxplot(
    data=df,
    x="system_type",
    y="traffic_score"
)
plt.title("Traffic score comparison by system")
plt.show()

