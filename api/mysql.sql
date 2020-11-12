-- mysqld stop
-- mysql.server start

create database content_engagement;
use content_engagement;

create TABLE ENGAGEMENT (
    CONTENTSK INT,
    PERSONKEY VARCHAR(20),
    ENGAGEMENT INT
);

create TABLE VIEWERS (
	PERSONKEY VARCHAR(20),
	FIRST_RESPONDENTWEIGHTREPORTDATE INT,
	LAST_RESPONDENTWEIGHTREPORTDATE INT,
	INTABWEIGHT INT,
	AGE INT,
	GENDER VARCHAR(1),
	RACE VARCHAR(30),
	PERSON_EDUCATION VARCHAR(44),
	PERSON_EDUCATION_LEVEL INT,
	COUNTYSIZE VARCHAR(100),
	COUNTY_SIZE_LEVEL INT,
	HOUSEHOLDINCOME INT,
	LANGUAGEOFHOUSEHOLD VARCHAR(100),
	HEADOFHOUSHOLD_EDUCATION_LEVEL INT,
	HOUSEHOLDSIZE VARCHAR(100),
	NUMBEROFCHILDREN INT,
	NUMBEROFADULTS INT,
	NUMBEROFINCOMES VARCHAR(100),
	HASCAT BOOLEAN,
	HASDOG BOOLEAN,
	HASSVODSUBSCRIPTION BOOLEAN,
	HASNETFLIXSUBSCRIPTION BOOLEAN,
	HASHULUSUBSCRIPTION BOOLEAN,
	HASAMAZONPRIMESUBSCRIPTION BOOLEAN,
	ISNEWCARPROSPECTLAST3YEARS BOOLEAN,
	ISNEWTRUCKPROSPECTLAST3YEARS BOOLEAN,
	HASMAC BOOLEAN,
	HASPC BOOLEAN,
	WEEKLY_VIEWING_MINUTES FLOAT
);

create TABLE CONTENT (
	CONTENTSK INT,
	PROGRAMCATEGORY VARCHAR(25),
	PROGRAMNAME VARCHAR(66),
	PROGRAMTYPESUMMARY VARCHAR(25),
	NHIPROGRAMTYPE VARCHAR(30),
	EPISODES INT,
	DURATION FLOAT,
	PIDS TEXT,
	PRIMARYNETWORK VARCHAR(5)
);

LOAD DATA INFILE '/Users/sletkeman/practicum/table.csv' INTO TABLE content
 FIELDS TERMINATED BY ','
 ENCLOSED BY '"'
 IGNORE 1 LINES
(@dummy, CONTENTSK, PROGRAMCATEGORY, PROGRAMNAME, PROGRAMTYPESUMMARY, NHIPROGRAMTYPE, EPISODES, DURATION, PIDS, PRIMARYNETWORK );
 

SHOW VARIABLES LIKE "secure_file_priv";

SHOW GLOBAL VARIABLES LIKE 'secure_file_priv';


LOAD DATA INFILE '/Users/sletkeman/practicum/table.csv' INTO TABLE content;

grant file on *.* to python@localhost;