from tkinter import *
from tkinter import messagebox
import pymysql

from Backend.popup import success, delete, emptyDB


# Connection To Database
def connect():
    global cursor, connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="e-store")
    cursor = connection.cursor()


def addprod(ProductID, ProductName, ProductPrice, ProductType, Retailer, ProductStock):
    try:
        connect()
        insertd = "INSERT INTO prod_info(Product_ID, Product_Name, Product_Price, Product_Type, Retailer, Product_Stock) VALUES(%s, %s, %s, %s, %s, %s);"
        val = (ProductID, ProductName, ProductPrice, ProductType, Retailer, ProductStock)
        cursor.execute(insertd, val)
        connection.commit()
        success()
        connection.close()
    except Exception as es:
        messagebox.showinfo(message=es)

def show_by_retail(retail):
    connect()
    cursor.execute("Select * from prod_info WHERE Retailer = %s", retail)
    data = cursor.fetchall()
    row = len(data)
    window = Tk()
    window.title("List Of Available Product")
    window.resizable(False, False)
    window.config(bg="orange")
    Label(window, text="Product_ID", fg='white', bg='#4da3ff', width=17).grid(row=0, column=0, padx=1, pady=1)
    Label(window, text="Product_Name", fg='white', bg='#4da3ff', width=17).grid(row=0, column=1, padx=1, pady=1)
    Label(window, text="Product_Price", fg='white', bg='#4da3ff', width=17).grid(row=0, column=2, padx=1, pady=1)
    Label(window, text="Product_Type", fg='white', bg='#4da3ff', width=17).grid(row=0, column=3, padx=1, pady=1)
    Label(window, text="Retailer", fg='white', bg='#4da3ff', width=17).grid(row=0, column=4, padx=1, pady=1)
    Label(window, text="Product_Stock", fg='white', bg='#4da3ff', width=17).grid(row=0, column=5, padx=1, pady=1)

    if row > 0:
        for i in range(row):
            for j in range(6):
                tab = Text(window, bg='white', width=15, height=2, bd=2, font=("Verdana", 8, "bold"))
                tab.insert(INSERT, data[i][j])
                tab.grid(row=i + 1, column=j, padx=1, pady=1)
    else:
        emptyDB()


def delprod(ID):
    connect()
    cursor.execute("DELETE FROM prod_info WHERE Product_ID = %s", ID)
    connection.commit()
    delete()
    connection.close()
