import pymysql

# Connection To Database
global cursor, connection

#Test Connection

def connect():
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="e-store")
    cursor = connection.cursor()
    connection.close()
