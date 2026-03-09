# 1. IMPORT LIBRARIES
# Core
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


# 2. LOAD DATASET
df_fixed = pd.read_csv("processed_fixed_dataset.csv")

df_fixed.head()


# 3. BASIC CLEANING
# Remove duplicates
df_fixed = df_fixed.drop_duplicates()

# Handle missing values
df_fixed = df_fixed.dropna()

df_fixed.info()


# 4. DEFINE TARGET VARIABLE
df_fixed.columns
target_column = "waiting_time"


# 5. FEATURE AND TARGET SPLIT
target_column = "waiting_time"

X = df_fixed.drop(columns=[
    target_column,
    "vehicle_id",
    "system_type",
    "congestion"
])

y = df_fixed[target_column]


# 6. TRAIN/TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. FEATURE SCALING
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 8. TRAIN MODELS
# Model 1 - Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

y_pred_lr = lr_model.predict(X_test_scaled)

# Model 2 - Random Forest
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)


# 9. EVALUATION FUNCTION
def evaluate_model(y_true, y_pred, model_name):

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print(f"\n{model_name} Performance:")
    print("MAE :", round(mae, 3))
    print("RMSE:", round(rmse, 3))
    print("R²  :", round(r2, 3))

    return mae, rmse, r2

# 10. EVALUATE BOTH MODELS
mae_lr, rmse_lr, r2_lr = evaluate_model(y_test, y_pred_lr, "Linear Regression")
mae_rf, rmse_rf, r2_rf = evaluate_model(y_test, y_pred_rf, "Random Forest")


# 11. PREDICTION VS ACTUAL PLOT
plt.figure()
plt.scatter(y_test, y_pred_rf)
plt.xlabel("Actual Flow")
plt.ylabel("Predicted Flow")
plt.title("Random Forest - Actual vs Predicted")
plt.show()

# 11.1 RESIDUAL PLOT
residuals = y_test - y_pred_rf

plt.figure()
plt.scatter(y_pred_rf, residuals)
plt.axhline(y=0, color='red')
plt.xlabel("Predicted Waiting Time")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()


# 12. FEATURE IMPORTANCE
importances = rf_model.feature_importances_

feature_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

feature_importance_df.head(10)

plt.figure()
sns.barplot(data=feature_importance_df.head(10),
            x="Importance",
            y="Feature")
plt.title("Top 10 Important Features")
plt.show()


# 13. STORE RESULTS
results = pd.DataFrame({
    "System": ["Fixed"],
    "Model": ["Random Forest"],
    "MAE": [mae_rf],
    "RMSE": [rmse_rf],
    "R2": [r2_rf]
})

print(results)

# ------------------------------
# SAVE MODEL
# ------------------------------

joblib.dump(rf_model, "fixed_throughput_prediction.pkl")
joblib.dump(scaler, "throughput_scaler.pkl")

print("\nThroughput prediction model saved successfully!")








