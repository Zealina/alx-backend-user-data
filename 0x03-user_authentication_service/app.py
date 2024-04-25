#!/usr/bin/env python3
"""Flask app"""

from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """Index page return"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """Create user if not exists"""
    email = request.form["email"]
    password = request.form["password"]
    if not email or not password:
        abort(400)
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def create_sessh():
    """Create new session on login"""
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    out = jsonify({"email": email, "message": "logged in"})
    out.set_cookie("session_id", session_id)
    return out


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")