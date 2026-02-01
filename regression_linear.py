import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#Load dataset

df = pd.read_csv("component1_merged.csv")

#encode system type

df["system_encoded"] = df["system_type"].map({
    "fixed": 0,
    "adaptive": 1
})