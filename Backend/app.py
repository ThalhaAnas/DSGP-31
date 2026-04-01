from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np
import json

app = Flask(__name__)

# -----------------------------
# LOGIN USERS
# -----------------------------
USERS = {"admin": "admin123"}

# -----------------------------
# LOAD MODELS
# -----------------------------
adaptive_cong = joblib.load("adaptive_congestion_prediction.pkl")
fixed_cong = joblib.load("fixed_congestion_prediction.pkl")
manual_cong = joblib.load("manual_congestion_prediction.pkl")
dynamic_cong = joblib.load("dynamic_congestion_prediction.pkl")

adaptive_wait = joblib.load("adaptive_waiting_time_model.pkl")
fixed_wait = joblib.load("fixed_waiting_time_model.pkl")
manual_wait = joblib.load("manual_waiting_time_model.pkl")
dynamic_wait = joblib.load("dynamic_waiting_time_model.pkl")

adaptive_tp = joblib.load("adaptive_throughput_prediction.pkl")
fixed_tp = joblib.load("fixed_throughput_prediction.pkl")
manual_tp = joblib.load("manual_throughput_prediction.pkl")
dynamic_tp = joblib.load("dynamic_throughput_prediction.pkl")

adaptive_speed = joblib.load("speed_prediction_model_adaptive.pkl")
fixed_speed = joblib.load("speed_prediction_model_fixed.pkl")
manual_speed = joblib.load("speed_prediction_model_manual.pkl")
dynamic_speed = joblib.load("speed_prediction_model_dynamic.pkl")


# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# -----------------------------
# DASHBOARD (SIMPLIFIED INPUT)
# -----------------------------
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():

    results = None

    # ONLY USER INPUTS
    form_data = {
        "depart_time": 500,
        "route_length": 1500,
        "traffic_level": "medium"
    }

    if request.method == "POST":

        # -------------------------
        # USER INPUTS
        # -------------------------
        depart_time = float(request.form["depart_time"])
        route_length = float(request.form["route_length"])
        traffic = request.form["traffic_level"]

        # -------------------------
        # AUTO-GENERATED FEATURES
        # -------------------------
        if traffic == "low":
            avg_speed = 15
            time_loss = 20
            waiting_ratio = 0.1
            delay_ratio = 0.1

        elif traffic == "medium":
            avg_speed = 10
            time_loss = 80
            waiting_ratio = 0.3
            delay_ratio = 0.3

        else:  # high traffic
            avg_speed = 6
            time_loss = 200
            waiting_ratio = 0.6
            delay_ratio = 0.6

        # Derived values
        duration = route_length / avg_speed
        arrival_time = depart_time + duration

        # -------------------------
        # CONGESTION PREDICTION
        # -------------------------
        cong_input = np.array([[depart_time, time_loss, route_length, avg_speed]])

        congestion = {
            "adaptive": int(adaptive_cong.predict(cong_input)[0]),
            "fixed": int(fixed_cong.predict(cong_input)[0]),
            "manual": int(manual_cong.predict(cong_input)[0]),
            "dynamic": int(dynamic_cong.predict(cong_input)[0])
        }

        # -------------------------
        # WAITING TIME
        # -------------------------
        wait_input = np.array([[duration, route_length, avg_speed, time_loss]])

        waiting = {
            "adaptive": float(adaptive_wait.predict(wait_input)[0]),
            "fixed": float(fixed_wait.predict(wait_input)[0]),
            "manual": float(manual_wait.predict(wait_input)[0]),
            "dynamic": float(dynamic_wait.predict(wait_input)[0])
        }

        # -------------------------
        # THROUGHPUT
        # -------------------------
        tp_input = np.array([[depart_time, arrival_time, duration, time_loss, route_length, avg_speed, waiting_ratio, delay_ratio]])

        throughput = {
            "adaptive": float(adaptive_tp.predict(tp_input)[0]),
            "fixed": float(fixed_tp.predict(tp_input)[0]),
            "manual": float(manual_tp.predict(tp_input)[0]),
            "dynamic": float(dynamic_tp.predict(tp_input)[0])
        }

        # -------------------------
        # SPEED (uses waiting output)
        # -------------------------
        speed = {}

        for system in ["adaptive","fixed","manual","dynamic"]:

            speed_input = np.array([[depart_time, arrival_time, duration, waiting[system], time_loss, route_length]])

            if system == "adaptive":
                speed[system] = float(adaptive_speed.predict(speed_input)[0])
            elif system == "fixed":
                speed[system] = float(fixed_speed.predict(speed_input)[0])
            elif system == "manual":
                speed[system] = float(manual_speed.predict(speed_input)[0])
            else:
                speed[system] = float(dynamic_speed.predict(speed_input)[0])

        # -------------------------
        # BEST SYSTEM
        # -------------------------
        best_system = min(waiting, key=waiting.get)

        results = {
            "congestion": congestion,
            "waiting": waiting,
            "throughput": throughput,
            "speed": speed,
            "best_system": best_system.capitalize()
        }

        # Keep values in UI
        form_data["depart_time"] = depart_time
        form_data["route_length"] = route_length
        form_data["traffic_level"] = traffic

    return render_template("dashboard.html", form_data=form_data, results=results)


# -----------------------------
# REPORT PAGE
# -----------------------------
@app.route("/report", methods=["POST"])
def report():

    data = json.loads(request.form["data"])

    ranking = sorted(data["waiting"].items(), key=lambda x: x[1])

    return render_template("report.html", data=data, ranking=ranking)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)