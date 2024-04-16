#!/usr/bin/env python3
"""Create Basic Authentication"""

from api.v1.auth.auth import Auth


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
