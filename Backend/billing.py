from tkinter import *

import pymysql

from Backend.popup import emptyDB, ordersaved, orderdelete

global cursor, connection


def connect():
    global cursor, connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="e-store")
    cursor = connection.cursor()


def getinfo():
    connect()
    cursor.execute("SELECT Name, Mobile FROM customerd")
    row = cursor.fetchall()
    return row


def getprod():
    connect()
    cursor.execute("SELECT Product_Name, Product_Price, Product_Type, Product_Stock FROM prod_info")
    row = cursor.fetchall()
    return row


def getstocks(prod_name):
    connect()
    cursor.execute("SELECT Product_Stock FROM prod_info WHERE Product_Name = %s", prod_name)
    stocks = cursor.fetchone()
    return stocks


def updatestocks(prod_name, stocks):
    connect()
    cursor.execute("UPDATE prod_info SET Product_Stock = %s WHERE Product_Name = %s", (stocks, prod_name))
    connection.commit()
    connection.close()


def insertd(i_d, Date, cust_name, prod_name, prod_type, prod_price, quantity, total):
    connect()
    cursor.execute(
        "INSERT INTO transaction (ID, Date, Customer_Name, Product_Name, Product_Type, Product_Price, Quantity, Total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
        (i_d, Date, cust_name, prod_name, prod_type, prod_price, quantity, total))
    connection.commit()
    ordersaved()
    connection.close()


def view_recent():
    connect()
    cursor.execute("SELECT * FROM transaction")
    data = cursor.fetchall()
    row = len(data)
    screen = Tk()
    screen.title("LIST OF RECENT ORDERS")
    Label(screen, text="Order ID", fg='white', bg="red", width=17, bd=2, font=("Verdana", 10, "bold")).grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=1,
                                                                                                            pady=1)
    Label(screen, text="Date", fg='white', bg="red", width=17, bd=2, font=("Verdana", 10, "bold")).grid(row=0, column=1,
                                                                                                        padx=1, pady=1)
    Label(screen, text="Customer_Name", fg='white', bg="red", width=17, bd=2, font=("Verdana", 10, "bold")).grid(row=0,
                                                                                                                 column=2,
                                                                                                                 padx=1,
                                                                                                                 pady=1)
    Label(screen, text="Product_Name", fg='white', bg="red", width=17, bd=2, font=("Verdana", 10, "bold")).grid(row=0,
                                                                                                                column=3,
                                                                                                                padx=1,
                                                                                                                pady=1)
    Label(screen, text="Product_Type", fg='white', bg="red", width=17, bd=2, font=("Verdana", 10, "bold")).grid(row=0,
                                                                                                                column=4,
                                                                                                                padx=1,
                                                                                                                pady=1)
    Label(screen, text="Product_Price", fg='white', bg="red", width=17, bd=2, font=("Verdana", 10, "bold")).grid(row=0,
                                                                                                                 column=5,
                                                                                                                 padx=1,
                                                                                                                 pady=1)
    Label(screen, text="Quantity", fg='white', bg="red", width=17, bd=2, font=("Verdana", 10, "bold")).grid(row=0,
                                                                                                            column=6,
                                                                                                            padx=1,
                                                                                                            pady=1)
    Label(screen, text="Total", fg='white', bg="red", width=17, bd=2, font=("Verdana", 10, "bold")).grid(row=0,
                                                                                                         column=7,
                                                                                                         padx=1, pady=1)

    if row > 0:
        for i in range(row):
            for j in range(8):
                tab = Text(screen, bg='white', width=19, height=2, bd=2, font=("Verdana", 8, "bold"))
                tab.insert(INSERT, data[i][j])
                tab.grid(row=i + 1, column=j, padx=1, pady=1)
    else:
        emptyDB()


def delorder(ID):
    connect()
    cursor.execute("DELETE FROM transaction WHERE ID = %s", ID)
    connection.commit()
    orderdelete()
    connection.close()
