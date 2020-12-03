
"""Defines the Snowflake queries"""

from util.snowflake import SnowflakeDatabase

def get_viewers(sample_size, viewer_condition, content_condition, onDemand):
    with SnowflakeDatabase() as sno:
        schema = f"engagement{'_ondemand' if onDemand else ''}"
        query = f"""
            WITH viewers as (
            SELECT v.personkey, age, gender, person_education, countysize, householdincome
            FROM {schema}.viewers v
              join {schema}.engagement e on v.personkey = e.personkey
              join {schema}.content c on e.contentsk = c.contentsk
            WHERE TRUE {viewer_condition} {content_condition}
            ) SELECT * FROM viewers SAMPLE({sample_size} rows);
        """
        return sno.query(query)

def get_viewers2(sample_size, viewer_condition, content_condition, onDemand):
    with SnowflakeDatabase() as sno:
        schema = f"engagement{'_ondemand' if onDemand else ''}"
        query = f"""
            WITH viewers as (
            SELECT v.personkey, age, gender, person_education, countysize, householdincome
            FROM {schema}.viewers v
              join {schema}.engagement e on v.personkey = e.personkey
              join {schema}.content c on e.contentsk = c.contentsk
            WHERE TRUE {viewer_condition} {content_condition} AND e.ENGAGEMENT > 50
            ) SELECT * FROM viewers SAMPLE({sample_size} rows);
        """
        return sno.query(query)


def get_content(viewers, content_condition, onDemand):
    with SnowflakeDatabase() as sno:
        schema = f"engagement{'_ondemand' if onDemand else ''}"
        query = f"""
            select distinct c.contentsk, c.programname, c.nhiprogramtype, c.programtypesummary, c.primarynetwork
            from {schema}.engagement e
            join {schema}.content c on e.contentsk = c.contentsk
            where e.personkey in ('{"','".join([v['PERSONKEY'] for v in viewers])}') {content_condition}
        """
        return sno.query(query)

def get_content2(viewers, content_condition, onDemand):
    with SnowflakeDatabase() as sno:
        schema = f"engagement{'_ondemand' if onDemand else ''}"
        query = f"""
            select distinct c.contentsk, c.programname, c.nhiprogramtype, c.programtypesummary, c.primarynetwork
            from {schema}.engagement e
            join {schema}.content c on e.contentsk = c.contentsk
            where e.personkey in ('{"','".join([v['PERSONKEY'] for v in viewers])}') AND programcategory = 'SERIES' AND e.ENGAGEMENT > 50
        """
        return sno.query(query)

def get_engagement(viewers, content_condition, onDemand):
    with SnowflakeDatabase() as sno:
        schema = f"engagement{'_ondemand' if onDemand else ''}"
        query = f"""
            select e.personkey, e.engagement, e.contentsk
            from {schema}.engagement e
            join {schema}.content c on e.contentsk = c.contentsk
            where personkey in ('{"','".join([v['PERSONKEY'] for v in viewers])}') {content_condition}
        """
        return sno.query(query)

def get_engagement2(viewers, content_condition, onDemand):
    with SnowflakeDatabase() as sno:
        schema = f"engagement{'_ondemand' if onDemand else ''}"
        query = f"""
            select e.personkey, e.engagement, e.contentsk
            from {schema}.engagement e
            join {schema}.content c on e.contentsk = c.contentsk
            where personkey in ('{"','".join([v['PERSONKEY'] for v in viewers])}') AND programcategory = 'SERIES' AND e.ENGAGEMENT > 50
        """
        return sno.query(query)