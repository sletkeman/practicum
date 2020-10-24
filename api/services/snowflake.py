
"""Defines the Snowflake queries"""

from util.snowflake import SnowflakeDatabase

def get_viewers(sample_size, viewer_condition):
    with SnowflakeDatabase() as sno:
        query = f"""
            SELECT personkey, age, gender, person_education, countysize, householdincome
            FROM engagement.viewers v SAMPLE({sample_size} rows)
            WHERE TRUE {viewer_condition}
        """
        return sno.query(query)

def get_content(viewers, content_condition):
    with SnowflakeDatabase() as sno:
        query = f"""
            select distinct c.contentsk, c.programname, c.nhiprogramtype, c.programtypesummary
            from engagement.engagement e
            join engagement.content c on e.contentsk = c.contentsk
            where e.personkey in ('{"','".join([v['PERSONKEY'] for v in viewers])}') {content_condition}
        """
        return sno.query(query)

def get_engagement(viewers, content_condition):
    with SnowflakeDatabase() as sno:
        query = f"""
            select e.personkey, e.engagement, e.contentsk
            from engagement.engagement e
            join engagement.content c on e.contentsk = c.contentsk
            where personkey in ('{"','".join([v['PERSONKEY'] for v in viewers])}') {content_condition}
        """
        return sno.query(query)
