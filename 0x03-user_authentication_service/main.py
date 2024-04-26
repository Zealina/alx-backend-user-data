#!/usr/bin/env python3
"""End to end integration test"""

import requests


url = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test register_user end point"""
    data = {"email": email, "password": password}
    r = requests.post(url + "/users", data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}
    r = requests.post(url + "/users", data=data)
    assert r.status_code == 400
    assert r.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Login with wrong password"""
    data = {"email": email, "password": password}
    r = requests.post(url + "/sessions", data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """Login successfully"""
    data = {"email": email, "password": password}
    r = requests.post(url + "/sessions", data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    assert r.cookies.get("session_id") is not None
    return r.cookies.get("session_id")


def profile_unlogged() -> None:
    """unlloged profile test"""
    r = requests.get(url + "/profile")
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test session id"""
    cookies = {"session_id": session_id}
    r = requests.get(url + "/profile", cookies=cookies)
    assert r.status_code == 200
    assert r.json().get("email") == EMAIL


def log_out(session_id: str) -> None:
    """Test logout sesh"""
    cookies = {"session_id": session_id}
    r = requests.delete(
            url + "/sessions",
            cookies=cookies,
            allow_redirects=False)
    assert r.is_redirect
    assert r.status_code == 302
    assert r.headers.get("Location") == '/'


def reset_password_token(email: str) -> str:
    """Reset password token"""
    data = {"email": email}
    r = requests.post(url + "/reset_password", data=data)
    assert r.status_code == 200
    assert r.json().get("reset_token")
    assert r.json().get("email") == email
    return r.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update password"""
    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    r = requests.put(url + "/reset_password", data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
