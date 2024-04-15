#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def load_from_file_delayed():
    """Delay the imports"""
    from api.v1.views.index import *
    from api.v1.views.users import *

    User.load_from_file()

load_from_file_delayed()
