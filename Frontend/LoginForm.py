import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql


def clear():
    userentry.delete(0, END)
    passentry.delete(0, END)


def close():
    window.destroy()


def login():
    # ================================LOGIN WHEN BUTTON IS CLICKED========================================#
    if user_name.get() == "" or password.get() == "":
        messagebox.showerror("Error", "Enter User Name And Password", parent=window)
    else:
        try:
            connection = pymysql.connect(host="localhost", user="root", password="", database="e-store")
            cursor = connection.cursor()
            cursor.execute("select * from accountd where USERNAME = %s and PASSWORD = %s",
                           (user_name.get(), password.get()))
            row = cursor.fetchone()

            if not row:
                messagebox.showerror("Error", "Invalid User Name And Password", parent=window)

            else:
                messagebox.showinfo("Success", "Successfully Logged-In", parent=window)
                close()

                from Frontend.admin_dashboard import Dashboard
                app = Dashboard()
                app.mainloop()
            connection.close()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due to : {str(es)}", parent=window)


# ========================================SIGNUP PAGE WINDOW============================================== #
def signup():
    # signup database connect
    def action():
        if first_name_entry.get() == "" or last_name_entry.get() == "" or email.get() == "" or user_name_entry.get() == "" or password_entry.get() == "" or ver_pass_entry.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=winsignup)
        elif password_entry.get() != ver_pass_entry.get():
            messagebox.showerror("Error", "Password & Confirm Password Should Be Same", parent=winsignup)
        else:
            try:
                connection = pymysql.connect(host="localhost", user="root", password="", database="e-store")
                cursor = connection.cursor()
                cursor.execute("select * from accountd where USERNAME=%s", user_name.get())
                row = cursor.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "User Name Already Exits!", parent=winsignup)
                else:
                    cursor.execute(
                        "insert into accountd(FIRSTNAME,LASTNAME,EMAIL,USERNAME,PASSWORD) values(%s,%s,%s,%s,%s)",
                        (
                            first_name_entry.get(),
                            last_name_entry.get(),
                            email.get(),
                            user_name_entry.get(),
                            password_entry.get()
                        ))
                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Success", "Account Created", parent=winsignup)
                    clear()
                    switch()

            except Exception as es:
                messagebox.showerror("Error", f"Error Due to : {str(es)}", parent=winsignup)

    def switch():
        winsignup.destroy()

    def clear():
        first_name_entry.delete(0, END)
        last_name_entry.delete(0, END)
        email.delete(0, END)
        user_name_entry.delete(0, END)
        password_entry.delete(0, END)
        ver_pass_entry.delete(0, END)

    winsignup = Tk()
    winsignup.title("Create a New Account")
    winsignup.geometry("500x500+500+150")
    winsignup.maxsize(width=500, height=500)
    winsignup.minsize(width=500, height=500)

    # heading label
    heading = Label(winsignup, text="Signup,", font='Verdana 20 bold')
    heading.place(x=75, y=60)

    # form data label
    first_name = Label(winsignup, text="First Name :", font='Verdana 11 bold')
    first_name.place(x=75, y=130)

    last_name = Label(winsignup, text="Last Name :", font='Verdana 11 bold')
    last_name.place(x=75, y=160)

    email_label = Label(winsignup, text="Email :", font='Verdana 11 bold')
    email_label.place(x=75, y=190)

    usname = Label(winsignup, text="User Name :", font='Verdana 11 bold')
    usname.place(x=75, y=220)

    pass_word = Label(winsignup, text="Password :", font='Verdana 11 bold')
    pass_word.place(x=75, y=250)

    ver_pass = Label(winsignup, text="Verify Pass :", font='Verdana 11 bold')
    ver_pass.place(x=75, y=280)

    first_name = StringVar()
    last_name = StringVar()
    email = StringVar()
    user_n = StringVar()
    passw = StringVar()
    ver_pass = StringVar()

    first_name_entry = Entry(winsignup, width=25, bd=3, font='Verdana 10 bold', textvariable=first_name)
    first_name_entry.place(x=200, y=133)

    last_name_entry = Entry(winsignup, width=25, bd=3, font='Verdana 10 bold', textvariable=last_name)
    last_name_entry.place(x=200, y=163)

    email = Entry(winsignup, width=25, bd=3, font='Verdana 10 bold', textvariable=email)
    email.place(x=200, y=193)

    user_name_entry = Entry(winsignup, width=25, bd=3, font='Verdana 10 bold', textvariable=user_n)
    user_name_entry.place(x=200, y=223)

    password_entry = Entry(winsignup, width=25, bd=3, font='Verdana 10 bold', textvariable=passw)
    password_entry.place(x=200, y=253)

    ver_pass_entry = Entry(winsignup, width=25, bd=3, font='Verdana 10 bold', show="*", textvariable=ver_pass)
    ver_pass_entry.place(x=200, y=283)

    # button login and clear

    btn_signup = Button(winsignup, text="Signup", font='Verdana 12 bold', command=action)
    btn_signup.place(x=170, y=320)

    btn_login = Button(winsignup, text="Clear", font='Verdana 12 bold', command=clear)
    btn_login.place(x=260, y=320)

    sign_up_btn = Button(winsignup, text="Switch To Login", command=switch, font='Verdana 10 bold')
    sign_up_btn.place(x=320, y=20)

    winsignup.mainloop()


# =============================================Start Up LOGIN Window====================================== #
window = Tk()

# app title
window.title("E-Store Management System")

# window size
window.geometry("500x500+500+150")
window.maxsize(width=500, height=500)
window.minsize(width=500, height=500)

# heading label
heading = Label(window, text="Login,", font='Verdana 25 bold')
heading.place(x=80, y=150)

username = Label(window, text="Username :", font='Verdana 11 bold')
username.place(x=80, y=222)

userpass = Label(window, text="Password :", font='Verdana 11 bold')
userpass.place(x=80, y=262)

# Entry Box
user_name = StringVar()
password = StringVar()

userentry = Entry(window, width=25, bd=3, font='Verdana 10 bold', textvariable=user_name)
userentry.focus()
userentry.place(x=200, y=223)

passentry = Entry(window, width=25, bd=3, show="*", font='Verdana 10 bold', textvariable=password)
passentry.place(x=200, y=260)

# button login and clear

btn_login = Button(window, text="Login", font='Verdana 12 bold', command=login)
btn_login.place(x=180, y=300)

btn_login = Button(window, text="Clear", font='Verdana 12 bold', command=clear)
btn_login.place(x=260, y=300)

# signup button

sign_up_btn = Button(window, text="Switch To Sign up", command=signup, font='Verdana 10 bold')
sign_up_btn.place(x=320, y=20)

window.mainloop()
