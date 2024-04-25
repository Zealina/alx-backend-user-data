#!/usr/bin/env python3
"""Auth module"""

from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password and return bytes"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """Intialize the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user and return said user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound as e:
            return self._db.add_user(email, _hash_password(password))
