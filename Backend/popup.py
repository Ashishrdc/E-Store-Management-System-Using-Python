from tkinter import messagebox


def success():
    messagebox.showinfo(message="Data Entered Successfully")


def changed():
    messagebox.showinfo(message="Password was changed successfully !")


def ordersaved():
    messagebox.showinfo(message="Order Saved Succesfully")


def orderdelete():
    messagebox.showinfo(message="Order Deleted Succesfully")


def emptyDB():
    messagebox.showinfo(message="Database is Empty")


def delete():
    messagebox.showinfo(message="Data has been deleted successfully!")


def connected():
    messagebox.showinfo(message="Connection to Database was successful")


def emailpop():
    messagebox.showinfo(message='Enter valid Email ID!')


def mobilepop():
    messagebox.showinfo(message='Enter valid Mobile Number!')


def emailmob():
    messagebox.showinfo(message='Check whether the Email ID or Mobile is correct!')
