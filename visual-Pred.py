import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("--- STEP 3: VISUAL PREDICTIVE ANALYSIS ---")

# 1. Load Data
predictions = pd.read_csv('model_predictions.csv')
fixed_df = pd.read_csv('component3_control_fixed_runtime.csv')
adaptive_df = pd.read_csv('component3_control_adaptive_runtime.csv')

# --- VISUAL 1: PREDICTIVE TRAFFIC FLOW (Fixed vs. Adaptive) ---
# Shows how the AI predicts and changes duration dynamically vs the static fixed line
target_id = adaptive_df['traffic_light_id'].unique()[0] 
f_data = fixed_df[fixed_df['traffic_light_id'] == target_id].iloc[:50] # First 50 cycles
a_data = adaptive_df[adaptive_df['traffic_light_id'] == target_id].iloc[:50]

plt.figure(figsize=(12, 6))
plt.plot(f_data['time'], f_data['phase_duration'], label='Fixed Control (Static)', color='red', linestyle='--', linewidth=2)
plt.plot(a_data['time'], a_data['phase_duration'], label='Adaptive AI Prediction (Dynamic)', color='green', linewidth=2)
plt.xlabel('Simulation Time')
plt.ylabel('Signal Duration (seconds)')
plt.title('Predictive Traffic Flow: AI vs Fixed Control')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- VISUAL 2: MODEL ACCURACY (Actual vs Predicted) ---
# Shows how close the AI predictions are to the ideal values
plt.figure(figsize=(8, 6))
sns.scatterplot(x=predictions['Actual_Duration'], y=predictions['Predicted_Duration'], alpha=0.6, color='blue')
# Ideal line
plt.plot([predictions.Actual_Duration.min(), predictions.Actual_Duration.max()], 
         [predictions.Actual_Duration.min(), predictions.Actual_Duration.max()], 
         'r--', lw=2, label='Perfect Prediction')
plt.xlabel('Actual Duration')
plt.ylabel('Predicted Duration')
plt.title('Model Accuracy: Random Forest')
plt.legend()
plt.grid(True)
plt.show()