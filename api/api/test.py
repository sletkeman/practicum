from flask import abort
from services.mysql import (
    get_viewers
)

def fetch_viewers():
    try:
        viewers = get_viewers(10, "c.PROGRAMNAME = 'BERMUDA TRI: NEW SECRETS'")
        return viewers, 200
    except Exception as ex:
        abort(500, ex.args[0])