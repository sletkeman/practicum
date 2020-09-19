"""
    basic ReST actions.
"""

from flask import abort


def get_allergens():
    try:
        result = [
            { "group": "group 1", "ingredients": 1 },
            { "group": "group 2", "ingredients": 2 },
            { "group": "group 3", "ingredients": 3 },
            { "group": "group 4", "ingredients": 4 }
        ]
        return result
    except RuntimeError as ex:
        abort(500, ex.args[1])
