import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

print("--- STEP 2: MODELING (Random Forest) ---")

# Load Processed Data
df = pd.read_csv('traffic_training_data.csv')

X = df[['green_count', 'red_count', 'junction_pressure', 'average_network_pressure']]
y = df['phase_duration']

# Split: 80% Training, 20% Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model: Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation metrics
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"Model Accuracy (R2 Score): {r2:.4f}")
print(f"Mean Absolute Error: {mae:.2f} seconds")

# Save predictions for visualization step
results = pd.DataFrame({'Actual_Duration': y_test, 'Predicted_Duration': y_pred})
results.to_csv('model_predictions.csv', index=False)

print("Predictions saved to: model_predictions.csv")