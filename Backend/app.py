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
    if request.method == "POST":

        for key in form_data:
            form_data[key] = float(request.form[key])

        # CONGESTION
        cong_input = np.array([[
            form_data["depart_time"],
            form_data["time_loss"],
            form_data["route_length"],
            form_data["average_speed"]
        ]])

        congestion = {
            "adaptive": int(adaptive_cong.predict(cong_input)[0]),
            "fixed": int(fixed_cong.predict(cong_input)[0]),
            "manual": int(manual_cong.predict(cong_input)[0]),
            "dynamic": int(dynamic_cong.predict(cong_input)[0])
        }

        # WAITING
        wait_input = np.array([[
            form_data["duration"],
            form_data["route_length"],
            form_data["average_speed"],
            form_data["time_loss"]
        ]])

        waiting = {
            "adaptive": adaptive_wait.predict(wait_input)[0],
            "fixed": fixed_wait.predict(wait_input)[0],
            "manual": manual_wait.predict(wait_input)[0],
            "dynamic": dynamic_wait.predict(wait_input)[0]
        }

        # THROUGHPUT
        tp_input = np.array([[
            form_data["depart_time"],
            form_data["arrival_time"],
            form_data["duration"],
            form_data["time_loss"],
            form_data["route_length"],
            form_data["average_speed"],
            form_data["waiting_ratio"],
            form_data["delay_ratio"]
        ]])

        throughput = {
            "adaptive": adaptive_tp.predict(tp_input)[0],
            "fixed": fixed_tp.predict(tp_input)[0],
            "manual": manual_tp.predict(tp_input)[0],
            "dynamic": dynamic_tp.predict(tp_input)[0]
        }

        # SPEED (uses predicted waiting)
        speed = {}

        for system in ["adaptive", "fixed", "manual", "dynamic"]:

            speed_input = np.array([[
                form_data["depart_time"],
                form_data["arrival_time"],
                form_data["duration"],
                waiting[system],  # KEY PART
                form_data["time_loss"],
                form_data["route_length"]
            ]])

            if system == "adaptive":
                speed[system] = adaptive_speed.predict(speed_input)[0]
            elif system == "fixed":
                speed[system] = fixed_speed.predict(speed_input)[0]
            elif system == "manual":
                speed[system] = manual_speed.predict(speed_input)[0]
            else:
                speed[system] = dynamic_speed.predict(speed_input)[0]

        # BEST SYSTEM
        best_system = min(waiting, key=waiting.get)

        results = {
            "congestion": congestion,
            "waiting": waiting,
            "throughput": throughput,
            "speed": speed,
            "best_system": best_system.capitalize()
        }

    return render_template("dashboard.html", form_data=form_data, results=results)

if __name__ == "__main__":
    app.run(debug=True)