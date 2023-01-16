from tkinter import *

import pymysql

from Backend.popup import success, delete, emptyDB


# Connection To Database
def connect():
    global cursor, connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="e-store")
    cursor = connection.cursor()


def add(Name, Age, Email, Gender, Mobile):
    connect()
    insertd = "INSERT INTO customerd(Name, Age, Email, Gender, Mobile) VALUES(%s, %s, %s, %s, %s);"
    val = (Name, Age, Email, Gender, Mobile)
    cursor.execute(insertd, val)
    connection.commit()
    success()
    connection.close()


def show():
    connect()
    display = "Select * from customerd;"
    cursor.execute(display)
    data = cursor.fetchall()
    row = len(data)

    if row > 0:
        window = Tk()
        window.config(bg="orange")
        window.title("List Of Available Customers")
        window.resizable(False, False)
        Label(window, text="ID", fg='white', bg='#4da3ff', width=19).grid(row=0, column=0, padx=1, pady=1)
        Label(window, text="Name", fg='white', bg='#4da3ff', width=19).grid(row=0, column=1, padx=1, pady=1)
        Label(window, text="Age", fg='white', bg='#4da3ff', width=19).grid(row=0, column=2, padx=1, pady=1)
        Label(window, text="Email", fg='white', bg='#4da3ff', width=19).grid(row=0, column=3, padx=1, pady=1)
        Label(window, text="Gender", fg='white', bg='#4da3ff', width=19).grid(row=0, column=4, padx=1, pady=1)
        Label(window, text="Mobile", fg='white', bg='#4da3ff', width=19).grid(row=0, column=5, padx=1, pady=1)
        if row > 0:
            for i in range(row):
                for j in range(6):
                    tab = Text(window, bg='white', width=17, height=2)
                    tab.insert(INSERT, data[i][j])
                    tab.grid(row=i + 1, column=j, padx=1, pady=1)
        else:
            emptyDB()


def search_by_name(name):
    connect()
    cursor.execute("Select * from customerd WHERE name = %s", name)
    data = cursor.fetchall()
    row = len(data)

    if row > 0:
        window = Tk()
        window.config(bg="orange")
        window.title("List Of Available Customers")
        window.resizable(False, False)
        Label(window, text="ID", fg='white', bg='#4da3ff', width=17).grid(row=0, column=0, padx=1, pady=1)
        Label(window, text="Name", fg='white', bg='#4da3ff', width=17).grid(row=0, column=1, padx=1, pady=1)
        Label(window, text="Age", fg='white', bg='#4da3ff', width=17).grid(row=0, column=2, padx=1, pady=1)
        Label(window, text="Email", fg='white', bg='#4da3ff', width=17).grid(row=0, column=3, padx=1, pady=1)
        Label(window, text="Gender", fg='white', bg='#4da3ff', width=17).grid(row=0, column=4, padx=1, pady=1)
        Label(window, text="Mobile", fg='white', bg='#4da3ff', width=17).grid(row=0, column=5, padx=1, pady=1)
        if row > 0:
            for i in range(row):
                for j in range(6):
                    tab = Text(window,bg='white', width=15, height=2, bd=2, font=("Verdana", 8, "bold"))
                    tab.insert(INSERT, data[i][j])
                    tab.grid(row=i + 1, column=j, padx=1, pady=1)
        else:
            emptyDB()


def delinfo(name):
    connect()
    cursor.execute("DELETE FROM customerd WHERE Name = %s", name)
    connection.commit()
    delete()
    connection.close()
