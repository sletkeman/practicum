"""
    basic ReST actions.
"""

from flask import abort
from services.snowflake import get_viewers

def get_allergens():
    """gets the allergens"""
    try:
        viewer_condition = "v.hascat and v.age > 60 and v.gender = 'F'"
        viewers = get_viewers(20, viewer_condition)
        return viewers
    except RuntimeError as ex:
        abort(500, ex.args[1])
