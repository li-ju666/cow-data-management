import mysql.connector

def checkDatabase(dbName, database):
    cursor = database.cursor()
    statement = "CREATE DATABASE IF NOT EXISTS "+dbName
    cursor.execute(statement)
    database.commit()
    cursor.close()

# create new table:
# Side effect: create new table in database
#
def checkPositionTables(database):
    FAstatement = "CREATE TABLE IF NOT EXISTS FA " \
                  "(tag_str VARCHAR(10), " \
                  "measure_time TIMESTAMP(3), " \
                  "posX SMALLINT UNSIGNED, " \
                  "posY SMALLINT UNSIGNED, " \
                  "posZ SMALLINT UNSIGNED, " \
                  "PRIMARY KEY (tag_str, measure_time))"
    PAstatement = "CREATE TABLE IF NOT EXISTS PA " \
                  "(tag_str VARCHAR(10), " \
                  "start_time TIMESTAMP(3), " \
                  "end_time TIMESTAMP(3), " \
                  "posX SMALLINT UNSIGNED, " \
                  "posY SMALLINT UNSIGNED, " \
                  "posZ SMALLINT UNSIGNED, " \
                  "activity_type SMALLINT, " \
                  "distance SMALLINT, " \
                  "PRIMARY KEY (tag_str, start_time, end_time))"
    PAAstatement ="CREATE TABLE IF NOT EXISTS PAA " \
                  "(tag_str VARCHAR(10), " \
                  "measure_time TIMESTAMP(3), " \
                  "interv INT , " \
                  "activity_type SMALLINT UNSIGNED, " \
                  "distance SMALLINT UNSIGNED, " \
                  "period SMALLINT UNSIGNED, " \
                  "duration INT, " \
                  "PRIMARY KEY (tag_str, measure_time, activity_type))"
    PCstatement = "CREATE TABLE IF NOT EXISTS PC " \
                  "(tag_str VARCHAR(10), " \
                  "start_time TIMESTAMP(3), " \
                  "end_time TIMESTAMP(3), " \
                  "posX SMALLINT UNSIGNED, " \
                  "posY SMALLINT UNSIGNED, " \
                  "posZ SMALLINT UNSIGNED, " \
                  "PRIMARY KEY (tag_str, start_time, end_time))"

    statements = [FAstatement, PAstatement, PAAstatement, PCstatement]
    for statement in statements:
        # print(statement)
        cursor = database.cursor()
        cursor.execute(statement)
        database.commit()
        cursor.close()


def checkInfoTables(database):
    Mapstatement = "CREATE TABLE IF NOT EXISTS Reference " \
                   "(cowID SMALLINT, " \
                   " tagStr VARCHAR(10)," \
                   " startDate DATE, " \
                   " endDate DATE, " \
                   " PRIMARY KEY (cowID, startDate))"

    Infostatement = "CREATE TABLE IF NOT EXISTS CowInfo " \
                    "(cowID SMALLINT, " \
                    " insertDate DATE, " \
                    " resp INT, " \
                    " grp SMALLINT, " \
                    " stat VARCHAR(10), " \
                    " lakt SMALLINT, " \
                    " kalvn_date DATE, "\
                    " PRIMARY KEY (cowID, insertDate))"

    Driedstatement = "CREATE TABLE IF NOT EXISTS DriedInfo " \
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

    Milkstatement = "CREATE TABLE IF NOT EXISTS MilkInfo " \
                    "(cowID SMALLINT," \
                    " measure_time TIMESTAMP," \
                    " station SMALLINT," \
                    " volume FLOAT," \
                    " PRIMARY KEY (cowID, measure_time))"

    statements = [Milkstatement, Infostatement, Driedstatement, Healthstatement, Mapstatement]
    for statement in statements:
        # print(statement)
        cursor = database.cursor()
        cursor.execute(statement)
        database.commit()
        cursor.close()


def connect():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example"
    )

    ## make sure database position exists: if not, create it
    checkDatabase("CowData", db)

    ## connect to position database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example",
        database="CowData"
    )
    checkPositionTables(db)
    checkInfoTables(db)
    return db
