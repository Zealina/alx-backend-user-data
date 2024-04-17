#!/usr/bin/env python3
"""Session based Auth module"""

from api.v1.auth.auth import Auth
from uuid import uuid4


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
