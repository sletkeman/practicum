
"""Defines the Snowflake queries"""

from util.mysql import MySqlDatabase

def get_viewers(sample_size, condition):
    """Gets the prospects"""
    with MySqlDatabase() as mysql:
        query = f"""
            SELECT v.personkey
            FROM content_engagement.viewers v
            --    JOIN content_engagement.ENGAGEMENT e on v.PERSONKEY = e.PERSONKEY
            --    JOIN content_engagement.CONTENT c on e.CONTENTSK = c.CONTENTSK
            where {condition}
            ORDER BY RAND() LIMIT {sample_size}
        """
        print(query)
        return mysql.query(query)

def get_content(viewers):
    """Gets the prospects"""
    with MySqlDatabase() as mysql:
        query = f"""
            select distinct c.contentsk, c.programname, c.NHIPROGRAMTYPE, c.PROGRAMTYPESUMMARY
            from content_engagement.engagement e
            join content_engagement.content c on e.contentsk = c.contentsk
            where e.personkey in ('{"','".join([v.get('personkey') for v in viewers])}') and c.programcategory = 'SERIES'
        """
        return mysql.query(query)

def get_engagement(viewers):
    """Gets the prospects"""
    with MySqlDatabase() as mysql:
        query = f"""
            select e.personkey, e.engagement, e.contentsk
            from content_engagement.engagement e
            join content_engagement.content c on e.contentsk = c.contentsk
            where personkey in ('{"','".join([v.get('personkey') for v in viewers])}') and c.programcategory = 'SERIES'
        """
        return mysql.query(query)

def getCount(minimum, maximum):
    with MySqlDatabase() as mysql:
        query = f"""
            select count(engagement) as num
            from engagement.engagement
            where engagement >= {minimum} and engagement < {maximum}
        """
        return mysql.query(query)