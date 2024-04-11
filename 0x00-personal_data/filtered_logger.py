#!/usr/bin/env python3
"""Filtered logging module"""

import logging
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str,
                 separator: str) -> str:
    """Return the log messages obfuscate
    """
    for field in fields:
        substitute = f'{field}={redaction};'
        message = re.sub(f'{field}=.+?;', substitute, message)
    return message
