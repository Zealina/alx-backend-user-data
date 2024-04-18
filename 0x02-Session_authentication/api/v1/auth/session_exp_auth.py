#!/usr/bin/env python3
"""Expiration of Session Authentication"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Extend session auth to allow exporation"""
    def __init__(self):
        """Overload the init method"""
        super().__init__()
        time = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(time)
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ extend the super method"""
        if not user_id:
            return
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        self.__class__.user_id_by_session_id[sess_id] = {
                'user_id': user_id,
                'created_at': datetime.now()}
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user id another way"""
        if not session_id:
            return
        user_date = self.__class__.user_id_by_session_id.get(session_id)
        if not user_date:
            return
        if self.session_duration <= 0:
            return user_date['user_id']
        creation = user_date.get('created_at')
        if not creation:
            return None
        seconds = self.session_duration
        if creation + timedelta(seconds=seconds) < datetime.now():
            return None
        return user_date['user_id']
