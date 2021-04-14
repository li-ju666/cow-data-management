import mysql.connector

def checkDatabase(dbName, database):
    cursor = database.cursor()
    statement = "CREATE DATABASE IF NOT EXISTS "+dbName
    cursor.execute(statement)
    database.commit()
    cursor.close()

# create new table:
def checkPositionTables(database):
    FAstatement = "CREATE TABLE IF NOT EXISTS FA " \
                  "(tag_id INT UNSIGNED, " \
                  "tag_str VARCHAR(10), " \
                  "measure_time TIMESTAMP(3), " \
                  "posX SMALLINT UNSIGNED, " \
                  "posY SMALLINT UNSIGNED, " \
                  "posZ SMALLINT UNSIGNED, " \
                  "PRIMARY KEY (tag_str, measure_time))"
    PAstatement = "CREATE TABLE IF NOT EXISTS PA " \
                  "(tag_id INT UNSIGNED, " \
                  "tag_str VARCHAR(10), " \
                  "start_time TIMESTAMP(3), " \
                  "end_time TIMESTAMP(3), " \
                  "posX SMALLINT UNSIGNED, " \
                  "posY SMALLINT UNSIGNED, " \
                  "posZ SMALLINT UNSIGNED, " \
                  "activity_type SMALLINT, " \
                  "distance SMALLINT, " \
                  "PRIMARY KEY (tag_str, start_time, end_time))"
    PAAstatement ="CREATE TABLE IF NOT EXISTS PAA " \
                  "(tag_id INT UNSIGNED, " \
                  "tag_str VARCHAR(10), " \
                  "measure_time TIMESTAMP(3), " \
                  "interv INT , " \
                  "activity_type SMALLINT UNSIGNED, " \
                  "distance SMALLINT UNSIGNED, " \
                  "period SMALLINT UNSIGNED, " \
                  "duration INT, " \
                  "PRIMARY KEY (tag_str, measure_time, activity_type))"
    PCstatement = "CREATE TABLE IF NOT EXISTS PC " \
                  "(tag_id INT UNSIGNED, " \
                  "tag_str VARCHAR(10), " \
                  "start_time TIMESTAMP(3), " \
                  "end_time TIMESTAMP(3), " \
                  "posX SMALLINT UNSIGNED, " \
                  "posY SMALLINT UNSIGNED, " \
                  "posZ SMALLINT UNSIGNED, " \
                  "PRIMARY KEY (tag_str, start_time, end_time))"

    statements = [FAstatement, PAstatement, PAAstatement, PCstatement]
    for statement in statements:
        cursor = database.cursor()
        cursor.execute(statement)
        database.commit()
        cursor.close()


def checkInfoTables_se(database):
    Mapstatement = "CREATE TABLE IF NOT EXISTS Mapping " \
                   "(cowID SMALLINT, " \
                   " tagStr VARCHAR(10)," \
                   " startDate DATE, " \
                   " endDate DATE, " \
                   " PRIMARY KEY (cowID, startDate, endDate))"

    Infostatement = "CREATE TABLE IF NOT EXISTS CowInfo " \
                    "(cowID SMALLINT, " \
                    " insertDate DATE, " \
                    " resp INT, " \
                    " grp SMALLINT, " \
                    " stat VARCHAR(10), " \
                    " lakt SMALLINT, " \
                    " kalvn_date DATE, "\
                    " PRIMARY KEY (cowID, insertDate))"

    Driedstatement = "CREATE TABLE IF NOT EXISTS InsemInfo " \
                   "(cowID SMALLINT, " \
                   " insertDate DATE, " \
                   " gp SMALLINT, " \
                   " avsinad DATE, " \
                   " insem_date DATE, " \
                   " sedan_insem SMALLINT, " \
                   " insem_tjur VARCHAR(50), " \
                   " forv_kalvn DATE, " \
                   " tid_ins SMALLINT, " \
                   " tid_mellan SMALLINT, " \
                   " PRIMARY KEY (cowID, insertDate))"

    Healthstatement = "CREATE TABLE IF NOT EXISTS HealthInfo " \
                      "(cowID SMALLINT, " \
                      " insertDate Date, " \
                      " 7dag FLOAT, " \
                      " 100dag INT, " \
                      " handelse_day SMALLINT, " \
                      " comments VARCHAR(500), " \
                      " PRIMARY KEY (cowID, insertDate))"

    # MilkPstatement = "CREATE TABLE IF NOT EXISTS MilkProduction " \
    #                 "(cowID SMALLINT," \
    #                 " insert_date Date," \
    #                 " record VARCHAR," \
    #                 " PRIMARY KEY (cowID, insert_date))"

    Milkstatement = "CREATE TABLE IF NOT EXISTS MilkInfo " \
                    "(cowID SMALLINT," \
                    " insertDate Date," \
                    " recordType VARCHAR(15)," \
                    " record VARCHAR(1000)," \
                    " PRIMARY KEY (cowID, insertDate, recordType))"

    statements = [Milkstatement, Infostatement, Driedstatement, Healthstatement, Mapstatement]
    for statement in statements:
        # print(statement)
        cursor = database.cursor()
        cursor.execute(statement)
        database.commit()
        cursor.close()

# We are gonna have to change the primary keys for these tables due to the data properties. 
# Suggestion: iso and levnr in Mapstatement and Milkstatement, werknr in Driedstatement.

def checkInfoTables_nl(database):
    Mapstatement = 'CREATE TABLE IF NOT EXISTS Mapping ' \
                   '(diernr SMALLINT, ' \
                   ' ISO INT, ' \
                   ' tagStr VARCHAR(10),' \
                   ' startDate DATE, ' \
                   ' endDate DATE, ' \
                   ' PRIMARY KEY (ISO, startDate))'


    Milkstatement = 'CREATE TABLE IF NOT EXISTS MilkInfo ' \
                    '(diernr SMALLINT, ' \
                    ' insertdate DATE, ' \
                    ' naam VARCHAR(30), ' \
                    ' levnr VARCHAR(15), ' \
                    ' kgmelk FLOAT, ' \
                    ' isk FLOAT, ' \
                    ' percentv FLOAT, ' \
                    ' eiw FLOAT, ' \
                    ' lact FLOAT, ' \
                    ' ur SMALLINT, ' \
                    ' celget INT, ' \
                    ' klfdat DATE, ' \
                    ' lftafk FLOAT, ' \
                    ' mprlft FLOAT, ' \
                    ' lactnr SMALLINT, ' \
                    ' lactatiedagen INT, ' \
                    ' kgmelklact INT, ' \
                    ' kgmelk305 INT, ' \
                    ' vetlact FLOAT, ' \
                    ' vet305 FLOAT, ' \
                    ' eiwlact FLOAT, ' \
                    ' eiw305 FLOAT, ' \
                    ' kgvetlact FLOAT, ' \
                    ' kgvet305 FLOAT, ' \
                    ' kgeiwlact FLOAT, ' \
                    ' kgeiw305 FLOAT, ' \
                    ' lw SMALLINT, ' \
                    ' PRIMARY KEY (levnr, insertdate))'

    statements = [Milkstatement, Mapstatement]
    for statement in statements:
        # print(statement, flush=True)
        cursor = database.cursor()
        cursor.execute(statement)
        database.commit()
        cursor.close()


def connect_se():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example"
    )
    # make sure database position exists: if not, create it
    checkDatabase("se_cow", db)
    # connect to position database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example",
        database="se_cow"
    )
    checkPositionTables(db)
    checkInfoTables_se(db)
    return db


def connect_nl():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example"
    )
    # make sure database position exists: if not, create it
    checkDatabase("nl_cow", db)
    # connect to position database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example",
        database="nl_cow"
    )
    checkPositionTables(db)
    checkInfoTables_nl(db)
    return db

