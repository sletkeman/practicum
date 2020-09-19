
"""Defines the Snowflake queries"""

from util.snowflake import SnowflakeDatabase

def get_viewers(sample_size, condition):
    """Gets the prospects"""
    with SnowflakeDatabase(warehouse='adds_dw', database='CONTENT_ENGAGEMENT') as sno:
        return sno.query("""

        """)

def get_content(viewers):
    """Gets the prospects"""
    with SnowflakeDatabase(warehouse='adds_dw', database='CONTENT_ENGAGEMENT') as sno:
        return sno.query("""
            
        """)

def get_engagement(viewers):
    """Gets the prospects"""
    with SnowflakeDatabase(warehouse='adds_dw', database='CONTENT_ENGAGEMENT') as sno:
        return sno.query("""
            
        """)