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