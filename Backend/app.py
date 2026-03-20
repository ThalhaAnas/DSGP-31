from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np

app = Flask(__name__)

# -----------------------------
# LOGIN USERS
# -----------------------------
USERS = {
    "admin": "admin123"
}

#Load models

# Congestion
adaptive_cong = joblib.load("adaptive_congestion_prediction.pkl")
fixed_cong = joblib.load("fixed_congestion_prediction.pkl")
manual_cong = joblib.load("manual_congestion_prediction.pkl")
dynamic_cong = joblib.load("dynamic_congestion_prediction.pkl")

# Waiting
adaptive_wait = joblib.load("adaptive_waiting_time_model.pkl")
fixed_wait = joblib.load("fixed_waiting_time_model.pkl")
manual_wait = joblib.load("manual_waiting_time_model.pkl")
dynamic_wait = joblib.load("dynamic_waiting_time_model.pkl")

# Throughput
adaptive_tp = joblib.load("adaptive_throughput_prediction.pkl")
fixed_tp = joblib.load("fixed_throughput_prediction.pkl")
manual_tp = joblib.load("manual_throughput_prediction.pkl")
dynamic_tp = joblib.load("dynamic_throughput_prediction.pkl")

# Speed
adaptive_speed = joblib.load("speed_prediction_model_adaptive.pkl")
fixed_speed = joblib.load("speed_prediction_model_fixed.pkl")
manual_speed = joblib.load("speed_prediction_model_manual.pkl")
dynamic_speed = joblib.load("speed_prediction_model_dynamic.pkl")

# Login
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":
        if request.form["username"] in USERS and USERS[request.form["username"]] == request.form["password"]:
            return redirect(url_for("dashboard"))

    return render_template("login.html")

# Dashboard

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    results = None

    # Default values
    form_data = {
        "depart_time": 500,
        "arrival_time": 800,
        "duration": 300,
        "route_length": 1500,
        "average_speed": 10,
        "time_loss": 80,
        "waiting_ratio": 0.3,
        "delay_ratio": 0.3
    }


