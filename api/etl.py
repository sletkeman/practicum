from snowflake import connector
from dotenv import load_dotenv
from os import environ
import mysql.connector
from mysql.connector.constants import ClientFlag

load_dotenv(dotenv_path="../.env")

ondemand = '_ondemand'
# ondemand = ''

tables = [
    #'content',
    'viewers',
    #'engagement'
]
column_names = [
    #'(@dummy, CONTENTSK, PROGRAMCATEGORY, PROGRAMNAME, PROGRAMTYPESUMMARY, NHIPROGRAMTYPE, EPISODES, DURATION, PIDS, PRIMARYNETWORK)',
    '(@dummy, PERSONKEY,FIRST_RESPONDENTWEIGHTREPORTDATE,LAST_RESPONDENTWEIGHTREPORTDATE,INTABWEIGHT,AGE,GENDER,RACE,PERSON_EDUCATION,PERSON_EDUCATION_LEVEL,COUNTYSIZE,COUNTY_SIZE_LEVEL,HOUSEHOLDINCOME,LANGUAGEOFHOUSEHOLD,HEADOFHOUSHOLD_EDUCATION_LEVEL,HOUSEHOLDSIZE,NUMBEROFCHILDREN,NUMBEROFADULTS,NUMBEROFINCOMES,HASCAT,HASDOG,HASSVODSUBSCRIPTION,HASNETFLIXSUBSCRIPTION,HASHULUSUBSCRIPTION,HASAMAZONPRIMESUBSCRIPTION,ISNEWCARPROSPECTLAST3YEARS,ISNEWTRUCKPROSPECTLAST3YEARS,HASMAC,HASPC,WEEKLY_VIEWING_MINUTES)',
    #'(@dummy, CONTENTSK,PERSONKEY,ENGAGEMENT)'
]

user = environ['SNOWFLAKE_USER']
password = environ['SNOWFLAKE_PASS']
account = environ['SNOWFLAKE_ACCT']
warehouse='ADDS_DW'
database='CONTENT_ENGAGEMENT'
schema='ENGAGEMENT_ONDEMAND'

mySql = {
  'user': 'python',
  'password': 'python',
  'host': 'localhost',
  'database': 'content_engagement',
  'auth_plugin': 'mysql_native_password',
  'client_flags': [ClientFlag.LOCAL_FILES]
}

def extract(table_name):
    conn = connector.connect(user=user, password=password, account=account)
    conn.cursor().execute(f"USE WAREHOUSE {warehouse}")
    conn.cursor().execute(f"USE {database}")
    conn.cursor().execute(f"USE SCHEMA {schema}")
    query_output = conn.cursor().execute(f"""
        select * from {table_name};
    """)
    query_output.fetch_pandas_all().to_csv(f"{table_name}{ondemand}.csv")
    conn.close()

def load(table_name, columns):
    cnx = mysql.connector.connect(**mySql)
    cursor = cnx.cursor()
    query = (f"""
        LOAD DATA INFILE '/Users/sletkeman/practicum/{table_name}{ondemand}.csv' INTO TABLE {table_name}{ondemand}
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        IGNORE 1 LINES
        {columns}
        SET HASCAT = (@HASCAT = 'True'),
            HASDOG = (@HASDOG = 'True'),
            HASSVODSUBSCRIPTION = (@HASSVODSUBSCRIPTION = 'True'),
            HASNETFLIXSUBSCRIPTION = (@HASNETFLIXSUBSCRIPTION = 'True'),
            HASHULUSUBSCRIPTION = (@HASHULUSUBSCRIPTION = 'True'), 
            HASAMAZONPRIMESUBSCRIPTION = (@HASAMAZONPRIMESUBSCRIPTION = 'True'),
            ISNEWCARPROSPECTLAST3YEARS = (@ISNEWCARPROSPECTLAST3YEARS = 'True'),
	        ISNEWTRUCKPROSPECTLAST3YEARS = (@ISNEWTRUCKPROSPECTLAST3YEARS = 'True'),
	        HASMAC = (@HASMAC = 'True'),
	        HASPC = (@HASPC = 'True'),
            WEEKLY_VIEWING_MINUTES = IF(@WEEKLY_VIEWING_MINUTES = '', 0.0, @WEEKLY_VIEWING_MINUTES)
    """)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

try:
    for i, name in enumerate(tables):
        print(f"{i}: {name}")
        # extract(name)
        load(name, column_names[i])
except Exception as error:
    print(error)
