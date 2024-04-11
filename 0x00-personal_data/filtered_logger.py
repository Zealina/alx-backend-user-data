#!/usr/bin/env python3
"""Filtered logging module"""

import logging
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str,
                 separator: str) -> str:
    """Return the log messages obfuscate
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is
        separating all fields in the log line (message)
    Return:
        the obfuscated log message
    """
    for field in fields:
        substitute = f'{field}={redaction};'
        message = re.sub(f'{field}=.+?;', substitute, message)
    return message
