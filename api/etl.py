from snowflake import connector
from dotenv import load_dotenv
from os import environ
import mysql.connector

load_dotenv(dotenv_path="../.env")

user = environ['SNOWFLAKE_USER']
password = environ['SNOWFLAKE_PASS']
account = environ['SNOWFLAKE_ACCT']
warehouse='ADDS_DW'
database='CONTENT_ENGAGEMENT'
schema='ENGAGEMENT'

mySql = {
  'user': 'python',
  'password': 'python',
  'host': '127.0.0.1',
  'database': 'content_engagement'
}

def extract(tableName):
    conn = connector.connect(user=user, password=password, account=account)
    conn.cursor().execute(f"USE WAREHOUSE {warehouse}")
    conn.cursor().execute(f"USE {database}")
    conn.cursor().execute(f"USE SCHEMA {schema}")
    query_output = conn.cursor().execute(f"""
        select top 100 * from engagement.{tableName};
    """)
    query_output.fetch_pandas_all().to_csv(f"/Users/sletkeman/mysql/{tableName}.csv")
    conn.close()

def load(tableName):
    cnx = mysql.connector.connect(**mySql)
    cursor = cnx.cursor()
    query = ("""
        LOAD DATA INFILE '/Users/sletkeman/mysql/{tableName}.csv' INTO TABLE content
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        IGNORE 1 LINES
        (@dummy, CONTENTSK, PROGRAMCATEGORY, PROGRAMNAME, PROGRAMTYPESUMMARY, NHIPROGRAMTYPE, EPISODES, DURATION, PIDS, PRIMARYNETWORK );
    """)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

try:
    tableName = 'content'
    extract(tableName)
    # load(tableName)
except Exception as error:
    print(error)