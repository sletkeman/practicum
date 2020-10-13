"""MySql Utils: Provides a wrapper for the mysql connector"""

from mysql import connector

class MySqlDatabase(object):
    '''Wrapper for handling Snowflake connection setup and teardown.
    This wrapper class is designed to handle the connection to Snowflake and
    common setup/teardown code.
    '''
    def __init__(
            self,
            mySql = {
                'user': 'python',
                'password': 'python',
                'host': 'localhost',
                'database': 'content_engagement',
                'auth_plugin': 'mysql_native_password',
                'client_flags': [connector.constants.ClientFlag.LOCAL_FILES]
            }
        ):

        self.connection = connector.connect(**mySql)
        self.cursor = self.connection.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exctype, excinst, exctb):
        self.cursor.close()
        self.connection.close()

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
