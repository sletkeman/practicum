"""
    basic ReST actions.
"""

from flask import abort
from services.snowflake import getCount
import numpy as np

def get_allergens():
    """gets the allergens"""
    try:
        r = np.linspace(10, 2000, 200)
        last = 0
        result = {}
        for val in r:
            count = getCount(last, val)
            result[f'{last}-{val}'] = count[0]['NUM']
            last = val
        return result
    except RuntimeError as ex:
        abort(500, ex.args[1])
