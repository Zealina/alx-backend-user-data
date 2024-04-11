#!/usr/bin/env python3
"""Filtered logging module"""

import logging
import re
from typing import List


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    """Return the log messages obfuscate"""
    for f in fields:
        message = re.sub(f'{f}=.+?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message
