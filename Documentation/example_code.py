## before run the script, you need to install the connector using pip: 
# pip3 install mysql-connector-python
import mysql.connector

database = mysql.connector.connect(
        host="srv-cdms",
        user="root",
        password="example",
        database="nl_cow")

cursor = database.cursor()
statement = "select * from MilkInfo"
cursor.execute(statement)
data = cursor.fetchall()

cursor.close()
