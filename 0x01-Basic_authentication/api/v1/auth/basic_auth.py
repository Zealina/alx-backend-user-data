#!/usr/bin/env python3
"""Create Basic Authentication"""

from api.v1.auth.auth import Auth
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
