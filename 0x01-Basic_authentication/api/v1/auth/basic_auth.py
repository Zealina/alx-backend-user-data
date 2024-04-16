#!/usr/bin/env python3
"""Create Basic Authentication"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """Basic  authentication class """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extract base64 authorization header"""
        if not authorization_header:
            return
        if type(authorization_header) is not str:
            return
        split = authorization_header.split()
        if split[0] != 'Basic':
            return
        return split[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """decode base64 authorization header"""
        if not base64_authorization_header:
            return
        if type(base64_authorization_header) is not str:
            return
        try:
            header = base64_authorization_header
            header = base64.b64decode(header)
            header = header.decode('utf-8')
        except base64.binascii.Error:
            return
        return header

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """Extract the users credentials"""
        if not decoded_base64_authorization_header:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        temp = decoded_base64_authorization_header.split(':')
        if len(temp) != 2:
            return (None, None)
        return (temp[0], temp[1])

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """Get user object based on credentials"""
        if not user_email or type(user_email) is not str:
            return
        if not user_pwd or type(user_pwd) is not str:
            return
        try:
            users = User.search({'email': user_email})
        except Exception:
            return
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the user object based on request"""
        header = self.authorization_header(request)
        if not header:
            return
        token = self.extract_base64_authorization_header(header)
        if not token:
            return
        decode = self.decode_base64_authorization_header(token)
        if not decode:
            return
        cred = self.extract_user_credentials(decode)
        if not cred:
            return
        obj = self.user_object_from_credentials(*cred)
        if not obj:
            return
        return obj
