#!/usr/bin/env python3
"""Authentification module for Basic Auth"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Contains all authentification parameters"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentification is required"""
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        return not path in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Checks the authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user"""
        return None
