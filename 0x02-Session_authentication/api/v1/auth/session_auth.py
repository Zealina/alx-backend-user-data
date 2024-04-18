#!/usr/bin/env python3
"""Session based Auth module"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
import os


class SessionAuth(Auth):
    """Session Authentification class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create all parameters for a session"""
        if not user_id or type(user_id) is not str:
            return
        sess_id = str(uuid4())
        self.__class__.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user_id based on sess_id"""
        if not session_id or type(session_id) is not str:
            return
        return self.__class__.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns the current user"""
        cookie = self.session_cookie(request)
        if not cookie:
            return
        user_id = self.user_id_for_session_id(cookie)
        if not user_id:
            return
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Remove a session from storage"""
        if request is None:
            return False
        cookie_name = os.getenv('SESSION_NAME')
        cookie = request.cookies.get(cookie_name)
        if not cookie:
            return False
        user_id = self.user_id_for_session_id(cookie)
        if not user_id:
            return False
        self.__class__.user_id_by_session_id.pop(cookie)
        return True
