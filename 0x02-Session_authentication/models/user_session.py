#!/usr/bin/env python3
"""Create file storage for session id"""

from models.base import Base


class UserSession(Base):
    """user session inhetits from base"""
    def __init__(self, *args: list, **kwargs: dict):
        """Intialize the class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
