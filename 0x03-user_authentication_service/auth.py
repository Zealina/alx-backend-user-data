#!/usr/bin/env python3
"""Auth module"""

from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password and return bytes"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def _generate_uuid() -> str:
    """Return a string representation of a new uuid"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login details are valid"""
        if not email or not password:
            return False
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode("utf-8"),
                user.hashed_password)
        except NoResultFound as e:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session"""
        if not email:
            return
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound as e:
            return

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user based on session id"""
        if not session_id:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound as e:
            return

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session on logout"""
        if not user_id:
            return
        try:
            self._db.update_user(user.id, session_id=None)
        except NoResultFound as e:
            return
