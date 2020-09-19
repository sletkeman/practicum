"""Snowflake Utils: Provides a wrapper for the snowflake connector"""

from os import environ
from snowflake.connector import DictCursor, connect


class SnowflakeDatabase(object):
    '''Wrapper for handling Snowflake connection setup and teardown.
    This wrapper class is designed to handle the connection to Snowflake and
    common setup/teardown code.
    '''
    def __init__(
            self,
            warehouse,
            database,
            schema='Public',
            user=None,
            password=None,
            account=None,
        ):

        # default to
        if not (user or password or account):
            user = environ['SNOWFLAKE_USER']
            password = environ['SNOWFLAKE_PASS']
            account = environ['SNOWFLAKE_ACCT']

        self.connection = connect(
            user=user,
            password=password,
            account=account,
        )

        self.execute(f'USE WAREHOUSE {warehouse}')
        self.execute(f'USE {database}')
        self.execute(f'USE SCHEMA {schema}')

    def __enter__(self):
        return self

    def __exit__(self, exctype, excinst, exctb):
        self.commit()
        self.connection.close()

    def commit(self):
        """executes a commit"""
        return self.execute('commit')

    def cursor(self, cursor_class=DictCursor):
        """gets a cursor"""
        return cursor_class(self.connection)

    def execute(self, query):
        '''Executes a Snowflake sql query
        Args:
            query (str): Snowflake sql query
        Returns:
            Snowflake cursor object
        '''
        return self.cursor().execute(query)

    def query(self, query):
        '''Executes a Snowflake sql query and returns the results
        Args:
            query (str): Snowflake sql query
        Returns:
            all results from query
        '''
        return self.execute(query).fetchall()
