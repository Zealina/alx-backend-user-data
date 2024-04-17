#!/usr/bin/env python3
"""Authentification module for Basic Auth"""

from flask import request
from typing import List, TypeVar
from os import getenv
import re


class Auth:
    """Contains all authentification parameters"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentification is required"""
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        for ex_path in excluded_paths:
            ex_path_regex = ex_path.replace('*', '.*')
            ex_path_regex = '^' + ex_path_regex + '$'
            if re.match(ex_path_regex, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks the authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user"""
        return None

    def session_cookie(self, request=None):
        """Returns the value of the cookie"""
        if not request:
            return
        name = getenv('SESSION_NAME')
        return request.cookies.get(name)
