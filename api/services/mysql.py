from util.mysql import MySqlDatabase

def get_viewers(sample_size, viewer_condition, content_condition):
    with MySqlDatabase() as mysql:
        query = f"""
            WITH content as (
	            select c.contentsk, e.personkey
                FROM content_engagement.CONTENT c
                  JOIN content_engagement.ENGAGEMENT e ON e.contentsk = c.contentsk
                WHERE {content_condition}
            ), viewers AS (
                SELECT personkey, age, gender, person_education, countysize, householdincome
                FROM content_engagement.viewers v
                WHERE {viewer_condition}
            )
            SELECT v.personkey, v.age, v.gender, v.person_education, v.countysize, v.householdincome
            FROM viewers v
                JOIN content c on v.personkey = c.personkey
            ORDER BY RAND() LIMIT {sample_size}
        """
        print(query)
        return mysql.query(query)

def get_content(viewers):
    with MySqlDatabase() as mysql:
        query = f"""
            select distinct c.contentsk, c.programname, c.nhiprogramtype, c.programtypesummary
            from content_engagement.engagement e
            join content_engagement.content c on e.contentsk = c.contentsk
            where e.personkey in ('{"','".join([v.get('personkey') for v in viewers])}') and c.programcategory = 'SERIES'
        """
        return mysql.query(query)

def get_engagement(viewers):
    with MySqlDatabase() as mysql:
        query = f"""
            select e.personkey, e.engagement, e.contentsk
            from content_engagement.engagement e
            join content_engagement.content c on e.contentsk = c.contentsk
            where personkey in ('{"','".join([v.get('personkey') for v in viewers])}') and c.programcategory = 'SERIES'
        """
        return mysql.query(query)
