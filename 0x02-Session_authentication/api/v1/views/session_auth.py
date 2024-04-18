#!/usr/bin/env python3
"""View for session authentication module"""

from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """Login, session auth"""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    pwd = request.form.get('password')
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(pwd):
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)
            out = jsonify(user.to_json())
            cookie_name = os.getenv('SESSION_NAME')
            out.set_cookie(cookie_name, sess_id)
            return out
    return jsonify({"error": "wrong password"}), 401
