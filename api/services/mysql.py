from util.mysql import MySqlDatabase

def get_viewers(sample_size, viewer_condition, content_condition):
    with MySqlDatabase() as mysql:
        query = f"""
            with content as (
	            select contentsk 
                from content_engagement.CONTENT
                where {content_condition}
            )
            SELECT v.personkey
            FROM content_engagement.viewers v
                JOIN content_engagement.ENGAGEMENT e on v.PERSONKEY = e.PERSONKEY
                JOIN content c on e.CONTENTSK = c.CONTENTSK
            where {viewer_condition}
            ORDER BY RAND() LIMIT {sample_size}
        """
        print(query)
        return mysql.query(query)

def get_content(viewers):
    with MySqlDatabase() as mysql:
        query = f"""
            select distinct c.contentsk, c.programname, c.NHIPROGRAMTYPE, c.PROGRAMTYPESUMMARY
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
