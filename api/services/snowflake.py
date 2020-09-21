
"""Defines the Snowflake queries"""

from util.snowflake import SnowflakeDatabase

def get_viewers(sample_size, condition):
    """Gets the prospects"""
    with SnowflakeDatabase() as sno:
        query = f"""
            select personkey, gender, age, race
            from engagement.viewers v sample ({sample_size} rows)
            where {condition}
        """
        return sno.query(query)

def get_content(viewers):
    """Gets the prospects"""
    with SnowflakeDatabase() as sno:
        query = f"""
            select distinct c.contentsk, c.programname, c.NHIPROGRAMTYPE, c.PROGRAMTYPESUMMARY
            from engagement.engagement e
            join engagement.content c on e.contentsk = c.contentsk
            where e.personkey in ('{"','".join([v['PERSONKEY'] for v in viewers])}') and c.programcategory = 'SERIES'
        """
        return sno.query(query)

def get_engagement(viewers):
    """Gets the prospects"""
    with SnowflakeDatabase() as sno:
        query = f"""
            select e.personkey, e.engagement, e.contentsk
            from engagement.engagement e
            join engagement.content c on e.contentsk = c.contentsk
            where personkey in ('{"','".join([v['PERSONKEY'] for v in viewers])}') and c.programcategory = 'SERIES'
        """
        return sno.query(query)

def getCount(minimum, maximum):
    with SnowflakeDatabase() as sno:
        query = f"""
            select count(engagement) as num
            from engagement.engagement
            where engagement >= {minimum} and engagement < {maximum}
        """
        return sno.query(query)