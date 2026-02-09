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

#features and target

features = [ "vehicle_count", "avg_time_loss", "system_encoded"]

X = df[features]
y = df["avg_waiting_time"]

#Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

#scale features

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#Train linear regression model

lr = LinearRegression()
lr.fit(X_train_scaled, y_train)

#prediction
y_pred = lr.predict(X_test_scaled)

#evaluation
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Linear Regression results:")
print(f"RMSE: {rmse:.2f}")
print(f"R2: {r2:.3f}")

#Coefficients

coef_df = pd.DataFrame(
    {
        "feature": features,
        "coefficient": lr.coef_,
    }
)

print("\nCoefficients:")
print(coef_df)