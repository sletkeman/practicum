
"""Defines the Snowflake queries"""

from util.snowflake import SnowflakeDatabase

def get_viewers(sample_size, viewer_condition, content_condition):
    """Gets the prospects"""
    with SnowflakeDatabase() as sno:
        query = f"""
            WITH viewers AS (
                SELECT v.personkey, age, gender, person_education, countysize, householdincome
                FROM engagement.viewers v
                    JOIN engagement.ENGAGEMENT e ON e.personkey = v.personkey
                    JOIN engagement.CONTENT c ON e.contentsk = c.contentsk
                WHERE {viewer_condition} AND {content_condition}
            )
            SELECT personkey, age, gender, person_education, countysize, householdincome
            FROM viewers SAMPLE({sample_size} rows)
        """
        print(query)
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