# ================================
# 1. IMPORT LIBRARIES
# ================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ================================
# 2. DEFINE DATASETS
# ================================

datasets = {
    "fixed": "processed_fixed_dataset.csv",
    "adaptive": "final_dataset_adaptive.csv",
    "dynamic": "final_dataset_dynamic.csv",
    "manual": "final_dataset_manual.csv"
}


# ================================
# 3. THROUGHPUT MODELLING FUNCTION
# ================================

def run_throughput_prediction(system_name, dataset_path):

    print("\n===============================")
    print(f"Running model for: {system_name.upper()}")
    print("===============================")

    # Load dataset
    df = pd.read_csv(dataset_path)

    # Cleaning
    df = df.drop_duplicates()
    df = df.dropna()

    # Target variable
    target_column = "waiting_time"

    # Feature selection
    target_column = "waiting_time"

    X = df.drop(
        columns=[target_column, "vehicle_id", "system_type", "congestion"],
        errors="ignore"
    )

    y = df[target_column]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # Feature scaling
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ================================
    # 4. TRAIN MODEL
    # ================================

    rf_model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    rf_model.fit(X_train, y_train)

    # Predictions
    y_pred = rf_model.predict(X_test)

    # ================================
    # TRAIN / TEST R2 SCORE
    # ================================

    train_r2 = rf_model.score(X_train, y_train)
    test_r2 = rf_model.score(X_test, y_test)

    print("Train R2:", round(train_r2, 3))
    print("Test R2 :", round(test_r2, 3))

    # ================================
    # 5. MODEL EVALUATION
    # ================================

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("MAE :", round(mae, 3))
    print("RMSE:", round(rmse, 3))
    print("R2  :", round(r2, 3))


    # ================================
    # 6. VISUALIZATION
    # ================================

    # Actual vs Predicted
    plt.figure()
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()],
             color='red')
    plt.xlabel("Actual Waiting Time")
    plt.ylabel("Predicted Waiting Time")
    plt.title(f"{system_name.upper()} - Actual vs Predicted")
    plt.show()


    # Residual plot
    residuals = y_test - y_pred

    plt.figure()
    plt.scatter(y_pred, residuals)
    plt.axhline(y=0, color='red')
    plt.xlabel("Predicted Waiting Time")
    plt.ylabel("Residuals")
    plt.title(f"{system_name.upper()} - Residual Plot")
    plt.show()


    # ================================
    # 7. FEATURE IMPORTANCE
    # ================================

    importances = rf_model.feature_importances_

    feature_importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    plt.figure()
    sns.barplot(
        data=feature_importance_df.head(10),
        x="Importance",
        y="Feature"
    )
    plt.title(f"{system_name.upper()} - Feature Importance")
    plt.show()


    # ================================
    # 8. SAVE MODEL
    # ================================

    model_filename = f"{system_name}_throughput_prediction.pkl"
    scaler_filename = f"{system_name}_throughput_scaler.pkl"

    joblib.dump(rf_model, model_filename)
    joblib.dump(scaler, scaler_filename)

    print(f"\nSaved model: {model_filename}")

    # Return evaluation results
    return {
        "System": system_name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }


# ================================
# 9. RUN MODELS FOR ALL DATASETS
# ================================

results_list = []

for system_name, dataset_path in datasets.items():

    result = run_throughput_prediction(system_name, dataset_path)

    results_list.append(result)


# ================================
# 10. FINAL COMPARISON TABLE
# ================================

results_df = pd.DataFrame(results_list)

print("\n===================================")
print("FINAL THROUGHPUT PREDICTION RESULTS")
print("===================================")

print(results_df)