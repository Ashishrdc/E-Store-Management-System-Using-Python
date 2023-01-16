import pymysql
from tkinter import messagebox
from Backend.popup import changed


# Connection To Database
def connect():
    global cursor, connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="e-store")
    cursor = connection.cursor()


def add(username, passw, email):
    connect()
    insertd = "INSERT INTO accountd(USER, PASS, EMAIL) VALUES(%s, %s, %s);"
    val = (username, passw, email)
    cursor.execute(insertd, val)
    connection.commit()
    connection.close()


def update(username, password):
    connect()
    cursor.execute("SELECT USERNAME FROM accountd WHERE USERNAME = %s", username)
    data = cursor.fetchall()
    user = len(data)
    if user > 0:
        try:
            cursor.execute("UPDATE accountd SET PASSWORD = %s WHERE USERNAME = %s", (password, username))
            connection.commit()
            changed()
            connection.close()
        except Exception as es:
            messagebox.showerror(es)
    else:
        messagebox.showerror("Error",message="Username does not exist !")