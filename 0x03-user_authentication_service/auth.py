#!/usr/bin/env python3
"""Auth module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password and return bytes"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)
