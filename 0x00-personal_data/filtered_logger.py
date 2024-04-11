#!/usr/bin/env python3
"""Filtered logging module"""

import logging
import re
from typing import List


def filter_datum(fields: List, red: str, message: str, sep: str) -> str:
    """Return the log messages obfuscate"""
    for field in fields:
        message = re.sub(f'{field}=.+?;', f'{field}={red};', message)
    return message
