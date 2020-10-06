from snowflake import connector
from dotenv import load_dotenv
from os import environ
load_dotenv(dotenv_path="../.env")

user = environ['SNOWFLAKE_USER']
password = environ['SNOWFLAKE_PASS']
account = environ['SNOWFLAKE_ACCT']
warehouse='ADDS_DW'
database='CONTENT_ENGAGEMENT'
schema='ENGAGEMENT'

def extract(tableName):
    conn = connector.connect(user=user, password=password, account=account)
    conn.cursor().execute(f"USE WAREHOUSE {warehouse}")
    conn.cursor().execute(f"USE {database}")
    conn.cursor().execute(f"USE SCHEMA {schema}")

    query_output = conn.cursor().execute(f"""
        select top 100 * from engagement.{tableName};
    """)
    conn.close()

    query_output.fetch_pandas_all().to_csv(f"{tableName}.csv")