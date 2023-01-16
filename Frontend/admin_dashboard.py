import tkinter as tk
import datetime
import pymysql
from tkinter import messagebox
from tkcalendar import *
from Backend.CustomerInfo import add, delinfo, search_by_name
from Backend.LoginInfo import update
from Backend.ProductInfo import addprod, delprod, show_by_retail
from Backend.billing import getstocks, updatestocks, getinfo, getprod, insertd, view_recent, delorder
from Backend.popup import mobilepop, emailpop, emailmob, emptyDB
from Backend.validation import check
from LoginForm import user_name


Font = ("Verdana", 10, "bold")
now = datetime.datetime.now()
selected_user = 0
selected_item = 0
global cursor, connection


def connect():
    global cursor, connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="e-store")
    cursor = connection.cursor()


class Dashboard(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.username = user_name.get()
        self.geometry("1320x540+100+120")
        self.title("ADMIN DASHBOARD")
        self.resizable(False, False)

        # ========================================DASHBOARD DESIGN============================================#

        # =============================================LABELS===============================================#

        tk.Label(self, width=1320, bg="#09e31f", font=('Verdana', 25)).pack()
        tk.Label(self, text="DASHBOARD", fg="white", bg="#09e31f", font=('Verdana', 25, "bold")).place(x=10)
        tk.Label(self, text="Date:\nTime:", fg="white", bg="#09e31f", font='Verdana 12 bold').place(x=300, y=3)
        tk.Label(self, text=(now.strftime("%Y-%m-%d\n%H:%M:%S")), bg="#09e31f", fg='white', font="Verdana 12").place(
            x=350, y=3)
        tk.Label(self, text=f"Current User:   {str(self.username)}",
                 bg="#09e31f", fg='white', font="Verdana 12 bold").place(x=1050, y=10)

        # ===================================================BUTTONS==========================================================#
        tk.Frame(self, bg="#9e5fc2", width=100, height=500).place(x=0, y=46)
        tk.Button(self, text="Home", height=4, width=10, relief="ridge", command=lambda: self.switch_frame(Home)).place(
            x=10, y=60)
        tk.Button(self, text="Manage\nCustomers", height=4, width=10, relief="groove",
                  command=lambda: self.switch_frame(ManageCustomer)).place(x=10, y=140)
        tk.Button(self, text="Manage\nProducts", height=4, width=10, relief="ridge",
                  command=lambda: self.switch_frame(ManageProduct)).place(x=10, y=220)
        tk.Button(self, text="Purchases\n&\nBills", height=4, width=10, relief="groove",
                  command=lambda: self.switch_frame(PurchaseBill)).place(x=10, y=300)
        tk.Button(self, text="Manage\nAccount", height=4, width=10, relief="ridge",
                  command=lambda: self.switch_frame(ManageAccount)).place(x=10, y=380)
        tk.Button(self, text="LOGOUT", height=4, width=10, relief="groove", command=lambda: self.call()).place(x=10,
                                                                                                               y=460)

        # ========================INITIAL FRAME==========================#
        self._frame = None
        self.switch_frame(Home)

    # ======================FUNCTION THAT SWITCHES FRAME==========================#
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=100, y=46)
        self._frame.config(height=500, width=1500)

    def call(self):
        res = messagebox.askquestion('Logout & Exit', 'Do you really want to Logout?')
        if res == 'yes':
            self.destroy()
        else:
            messagebox.showinfo('Return', 'Returning to main application')


class Home(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Home/About")
        tk.Label(self, text="ABOUT", bg="#e610de", width=10, font=("Verdana", 22, "bold")).place(x=10, y=10)
        tk.Label(self, text="==========================").place(x=10, y=55)
        tk.Label(self, text="Hello User,", font='Verdana 15 bold').place(x=10, y=80)
        tk.Label(self, text="Welcome To E-Store Management System", font='Verdana 15 bold').place(x=10, y=120)
        tk.Label(self, text="======================================================"
                            "======").place(x=10, y=160)
        tk.Label(self, text="WHAT IS E-STORE?", bg="#05f599", fg="white", font='Verdana 18 bold').place(x=10, y=190)
        tk.Label(self, text="Electronic Store is a process of storing the products which is"
                            "\ncapable of maintaining storage of large number of products.",
                 font='Verdana 18 bold', fg="white", bg="#6fd2e3").place(x=10, y=240)
        tk.Label(self, text="E-Store Management System is a desktop application that keeps"
                            " track\nof all the transactions and generates a bill for all the purchased goods.",
                 font='Verdana 18 bold', bg="#89e36b", fg="white").place(x=10, y=320)
        tk.Label(self, text="======================================================"
                            "======================================================"
                            "===========").place(x=10, y=390)
        tk.Label(self,
                 text="Use the side panel to navigate through out the App",
                 font=('Verdana', 18, "bold"),
                 bg="red").place(x=10, y=450)


class ManageCustomer(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # tk.Frame.config(self,height=500,width=600)
        self.master.title("Manage Customers")
        tk.Label(self, text="Customer Information", bg="#e68609", width=20, font=("Verdana", 22, "bold")).place(x=10,
                                                                                                                y=20)
        tk.Label(self, text="FullName", font=Font).place(x=55, y=100)
        name_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        name_entry.focus()
        name_entry.place(x=170, y=100)

        tk.Label(self, text="Email", font=Font).place(x=55, y=150)
        email_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        email_entry.place(x=170, y=150)

        tk.Label(self, text="Gender", font=Font).place(x=55, y=200)
        gen = tk.IntVar()
        tk.Radiobutton(self, text="Male", padx=5, variable=gen, value=1).place(x=160, y=200)
        tk.Radiobutton(self, text="Female", padx=20, variable=gen, value=2).place(x=220, y=200)

        tk.Label(self, text="Age", font=Font).place(x=55, y=250)
        age_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        age_entry.place(x=170, y=250)

        tk.Label(self, text="Mobile", font=Font).place(x=55, y=300)
        mobile_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        mobile_entry.place(x=170, y=300)

        tk.Button(self, text='ADD', width=10, bg='brown', fg='white', command=lambda: submit()).place(x=55, y=360)
        tk.Button(self, text='UPDATE', width=10, bg='brown', fg='white', command=lambda: edit()).place(x=150, y=360)
        tk.Button(self, text='DELETE', width=10, bg='brown', fg='white', command=lambda: delete()).place(x=245, y=360)
        tk.Button(self, text="SEARCH", width=10, bg='brown', fg='white', command=lambda: search()).place(x=850, y=2)
        tk.Button(self, text="REFRESH", width=10, bg='brown', fg='white', command=lambda: refresh()).place(x=950, y=2)

        # ====================================FUNCTIONS=====================================#
        def refresh():
            master.switch_frame(ManageCustomer)

        def search():
            def ssubmit2():
                name = sname_entry.get()
                if name == "":
                    messagebox.showinfo(message="This field is required")
                else:
                    name = sname_entry.get()
                    search_by_name(name)
                    sname_entry.delete(0, tk.END)
                    screen.destroy()

            screen = tk.Tk()
            screen.title("Search Customer By Name")
            screen.geometry("400x200")
            screen.config(bg="#acc926")
            tk.Label(screen, text="SEARCH THE CUSTOMERS", width=20, bg="green", font=("Verdana", 20, "bold")).pack(
                pady=10)
            tk.Label(screen, text="Enter Full Name", width=20, font=("bold", 15)).pack(pady=10)
            sname_entry = tk.Entry(screen, width=25, bd=2)
            sname_entry.pack(pady=10)

            tk.Button(screen, text='SEARCH', width=10, bg='brown', fg='white', command=lambda: ssubmit2()).pack(pady=10)

        def submit():
            name = name_entry.get()
            age = age_entry.get()
            email = email_entry.get()
            if gen.get() == 1:
                gender = "Male"
            elif gen.get() == 2:
                gender = "Female"
            else:
                gender = "Others"
            mobile = mobile_entry.get()
            valid = check(mobile, email)
            if not valid[0] and valid[1]:
                mobilepop()
            elif valid[0] and not valid[1]:
                emailpop()
            elif not valid[0] and not valid[1]:
                emailmob()
            elif name == "" or email == "" or age == "" or mobile == "":
                messagebox.showinfo(message="All fields are required")
            else:
                add(name, age, email, gender, mobile)
                name_entry.delete(0, tk.END)
                age_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                mobile_entry.delete(0, tk.END)
                master.switch_frame(ManageCustomer)

        def edit():
            from Backend.update_user import CustomerUpdate
            root = tk.Tk()
            app = CustomerUpdate(master=root)
            app.mainloop()

        def delete():
            def submit2():
                name = delname_entry.get()
                if name == "":
                    messagebox.showinfo(message="This field is required")
                else:
                    name = delname_entry.get()
                    delinfo(name)
                    delname_entry.delete(0, tk.END)
                    screen.destroy()

            screen = tk.Tk()
            screen.title("Enter Name To Delete Information")
            screen.geometry("350x200")
            screen.config(bg="#ADD8E6")
            tk.Label(screen, text="Delete Customer Data", width=20, bg="green", font=("Verdana", 20, "bold")).pack(
                pady=10)
            tk.Label(screen, text="Enter Full Name", width=20, font=("bold", 15)).pack(pady=10)
            delname_entry = tk.Entry(screen, width=25, bd=2)
            delname_entry.pack(pady=10)

            tk.Button(screen, text='DELETE', width=10, bg='brown', fg='white', command=lambda: submit2()).pack(pady=10)

            # ========================================SHOW TABLE======================================#

        tk.Label(self, text="LIST OF AVAILABLE CUSTOMERS", font=("Verdana", 15, "bold")).place(x=450, y=0)

        self.table = tk.Frame(self)
        self.table.config(height=500, width=600)
        self.table.place(x=450, y=30)

        connect()
        display = "Select * from customerd;"
        cursor.execute(display)
        data = cursor.fetchall()
        row = len(data)

        tk.Label(self.table, text="ID", fg='white', bg='orange', width=17, bd=2).grid(row=0, column=0, padx=1, pady=1)
        tk.Label(self.table, text="Name", fg='white', bg='orange', width=17, bd=2).grid(row=0, column=1, padx=1, pady=1)
        tk.Label(self.table, text="Email", fg='white', bg='orange', width=17, bd=2).grid(row=0, column=2, padx=1,
                                                                                         pady=1)
        tk.Label(self.table, text="Age", fg='white', bg='orange', width=17, bd=2).grid(row=0, column=3, padx=1, pady=1)
        tk.Label(self.table, text="Gender", fg='white', bg='orange', width=17, bd=2).grid(row=0, column=4, padx=1,
                                                                                          pady=1)
        tk.Label(self.table, text="Mobile", fg='white', bg='orange', width=17, bd=2).grid(row=0, column=5, padx=1,
                                                                                          pady=1)

        if row > 0:
            for i in range(row):
                for j in range(6):
                    tab = tk.Text(self.table, bg='white', width=15, height=2, bd=2, font=("Verdana", 8, "bold"))
                    tab.insert(tk.INSERT, data[i][j])
                    tab.grid(row=i + 1, column=j, padx=1, pady=1)
        else:
            emptyDB()


class ManageProduct(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Manage Products")

        tk.Label(self, text="Product Information", width=20, bg="#981ed9", font=("Verdana", 22, "bold")).place(x=10,
                                                                                                               y=20)

        tk.Label(self, text="Product ID", font=Font).place(x=55, y=100)
        ProductID_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        ProductID_entry.focus()
        ProductID_entry.place(x=170, y=100)

        tk.Label(self, text="Product Name", font=Font).place(x=55, y=150)
        ProductName_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        ProductName_entry.place(x=170, y=150)

        tk.Label(self, text="Product Price", font=Font).place(x=55, y=200)
        ProductPrice_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        ProductPrice_entry.place(x=170, y=200)

        tk.Label(self, text="Product Type", font=Font).place(x=55, y=250)
        ProductType_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        ProductType_entry.place(x=170, y=250)

        tk.Label(self, text="Retailer", font=Font).place(x=55, y=300)
        Retailer_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        Retailer_entry.place(x=170, y=300)

        tk.Label(self, text="Product Stock", font=Font).place(x=55, y=350)
        ProductStock_entry = tk.Entry(self, width=19, bd=3, font=("Verdana", 8, "bold"))
        ProductStock_entry.place(x=170, y=350)

        tk.Button(self, text='ADD', width=10, bg='brown', fg='white', command=lambda: submit()).place(x=55, y=410)
        tk.Button(self, text='UPDATE', width=10, bg='brown', fg='white', command=lambda: edit()).place(x=150, y=410)
        tk.Button(self, text='DELETE', width=10, bg='brown', fg='white', command=lambda: delete()).place(x=245, y=410)
        tk.Button(self, text="SEARCH", width=10, bg='brown', fg='white', command=lambda: search()).place(x=850, y=2)
        tk.Button(self, text="REFRESH", width=10, bg='brown', fg='white', command=lambda: refresh()).place(x=950, y=2)

        def refresh():
            master.switch_frame(ManageProduct)

        def search():
            def submit2():
                retail = r_entry.get()
                if retail == "":
                    messagebox.showinfo(message="This field is required")
                else:
                    show_by_retail(retail)
                    r_entry.delete(0, tk.END)
                    screen.destroy()

            screen = tk.Tk()
            screen.title("Search Customer By ID")
            screen.geometry("350x200")
            screen.config(bg="#27dbae")
            tk.Label(screen, text="SEARCH PRODUCTS", width=20, bg="green", font=("Verdana", 20, "bold")).pack(pady=10)
            tk.Label(screen, text="Enter Retailer", width=20, font=("bold", 15)).pack(pady=10)
            r_entry = tk.Entry(screen, width=25, bd=2)
            r_entry.pack(pady=10)
            tk.Button(screen, text='SEARCH', width=10, bg='brown', fg='white', command=lambda: submit2()).pack(pady=10)

        def delete():
            def submit2():
                ID = delID_entry.get()
                if ID == "":
                    messagebox.showinfo(message="This field is required")
                else:
                    delprod(ID)
                    delID_entry.delete(0, tk.END)
                    screen.destroy()

            screen = tk.Tk()
            screen.title("Delete Product")
            screen.geometry("350x200")
            screen.config(bg="#ADD8E6")
            tk.Label(screen, text="Delete Product Data", width=20, bg="green", font=("bold", 20)).pack(pady=10)
            tk.Label(screen, text="Enter Product ID", width=20, font=("bold", 15)).pack(pady=10)
            delID_entry = tk.Entry(screen, width=25, bd=2)
            delID_entry.pack(pady=10)

            tk.Button(screen, text='DELETE', width=10, bg='brown', fg='white', command=lambda: submit2()).pack(pady=10)

        def edit():
            from Backend.update_product import ProdUpdate
            root = tk.Tk()
            app = ProdUpdate(master=root)
            app.mainloop()

        def submit():
            ProductID = ProductID_entry.get()
            ProductName = ProductName_entry.get()
            ProductPrice = ProductPrice_entry.get()
            ProductType = ProductType_entry.get()
            Retailer = Retailer_entry.get()
            ProductStock = ProductStock_entry.get()

            if ProductID == "" or ProductName == "" or ProductPrice == "" or ProductType == "" or Retailer == "" or ProductStock == "":
                messagebox.showinfo(message="All fields are required")
            else:
                addprod(ProductID, ProductName, ProductPrice, ProductType, Retailer, ProductStock)
                ProductID_entry.delete(0, tk.END)
                ProductName_entry.delete(0, tk.END)
                ProductPrice_entry.delete(0, tk.END)
                ProductType_entry.delete(0, tk.END)
                Retailer_entry.delete(0, tk.END)
                ProductStock_entry.delete(0, tk.END)
                master.switch_frame(ManageProduct)

        # ====================================SHOW TABLE============================================#
        tk.Label(self, text="LIST OF AVAILABLE PRODUCTS", font=("Verdana", 15, "bold")).place(x=450, y=0)
        self.table = tk.Frame(self)
        self.table.config(height=500, width=600)
        self.table.place(x=450, y=30)
        connect()
        display = "Select * from prod_info;"
        cursor.execute(display)
        data = cursor.fetchall()
        row = len(data)

        tk.Label(self.table, text="Product_ID", fg='white', bg='#4da3ff', width=17, bd=2).grid(row=0, column=0, padx=1,
                                                                                               pady=1)
        tk.Label(self.table, text="Product_Name", fg='white', bg='#4da3ff', width=17, bd=2).grid(row=0, column=1,
                                                                                                 padx=1, pady=1)
        tk.Label(self.table, text="Product_Price", fg='white', bg='#4da3ff', width=17, bd=2).grid(row=0, column=2,
                                                                                                  padx=1, pady=1)
        tk.Label(self.table, text="Product_Type", fg='white', bg='#4da3ff', width=17, bd=2).grid(row=0, column=3,
                                                                                                 padx=1, pady=1)
        tk.Label(self.table, text="Retailer", fg='white', bg='#4da3ff', width=17, bd=2).grid(row=0, column=4, padx=1,
                                                                                             pady=1)
        tk.Label(self.table, text="Product_Stock", fg='white', bg='#4da3ff', width=17, bd=2).grid(row=0, column=5,
                                                                                                  padx=1, pady=1)

        if row > 0:
            for i in range(row):
                for j in range(6):
                    tab = tk.Text(self.table, bg='white', width=15, height=2, bd=2, font=("Verdana", 8, "bold"))
                    tab.insert(tk.INSERT, data[i][j])
                    tab.grid(row=i + 1, column=j, padx=1, pady=1)
        else:
            emptyDB()


class PurchaseBill(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Purchases & Bills")

        # ==========FILLER=============#
        tk.Label(self, text="How-To,", font=("Verdana", 15, "bold")).place(x=650, y=0)
        tk.Label(self, text="1. Enter the customer details or select the customer"
                            "\nfrom the given listbox on the right.", fg="white", bg="red",
                 font=("Verdana", 10, "bold")).place(x=650, y=50)
        tk.Label(self, text="2. Choose the product from the listbox given below", fg="white", bg="red",
                 font=("Verdana", 10, "bold")).place(x=650, y=100)
        tk.Label(self, text="3. Enter Quantity and Press ADD to add it to the ORDER INFO", fg="white", bg="red",
                 font=("Verdana", 10, "bold")).place(x=650, y=135)
        tk.Label(self, text="4. Enter Random Order ID then Press 'Save Order'\n"
                            "Button to save the Order in the Database", fg="white", bg="red",
                 font=("Verdana", 10, "bold")).place(x=650, y=165)

        # =======================================WIDGETS===============================================#

        tk.Label(self, text="Purchases & Bill", bg="#27dbae", width=15, font=("Verdana", 25, "bold")).place(x=0, y=0)
        tk.Label(self, text="Enter Customer Details Or Select From The List", font=("Verdana", 12, "bold")).place(x=40,
                                                                                                                  y=60)
        tk.Label(self, text="Customer Name", font=("Verdana", 10, "bold")).place(x=40, y=90)

        cust_name = tk.Entry(self, bd=3, font=("Verdana", 10, "bold"), textvariable=tk.StringVar)
        cust_name.place(x=180, y=90)

        tk.Label(self, text="Mobile Number", font=("Verdana", 10, "bold")).place(x=40, y=120)
        mobile_no = tk.Entry(self, bd=3, font=("Verdana", 10, "bold"))
        mobile_no.place(x=180, y=120)

        tk.Label(self, text="Choose Product From List Below", font=("Verdana", 12, "bold")).place(x=40, y=180)

        tk.Label(self, text="Enter Quantity", font=("Verdana", 10, "bold")).place(x=40, y=300)
        quantity = tk.Entry(self, bd=3, font=("Verdana", 10, "bold"))
        quantity.place(x=180, y=300)

        # =====================================Order Table Layout=========================================#

        tk.Label(self, text="==================================================================================").place(
            x=40, y=330)
        tk.Label(self, text="Order Info", font=("Verdana", 12, "bold")).place(x=40, y=350)
        LabelFont = ("Verdana", 9, "bold")
        EntryFont = ("Verdana", 8, "bold")
        tk.Label(self, text="ID", bg="red", width=5, font=LabelFont).place(x=40, y=380)
        tk.Label(self, text="Date", bg="red", width=5, font=LabelFont).place(x=90, y=380)
        tk.Label(self, text="Customer Name", bg="red", width=15, font=LabelFont).place(x=140, y=380)
        tk.Label(self, text="Product Name", bg="red", width=15, font=LabelFont).place(x=270, y=380)
        tk.Label(self, text="P_Price", bg="red", width=10, font=LabelFont).place(x=400, y=380)
        tk.Label(self, text="P_Type", bg="red", width=10, font=LabelFont).place(x=490, y=380)
        tk.Label(self, text="Quantity", bg="red", width=8, font=LabelFont).place(x=580, y=380)
        tk.Label(self, text="Total", bg="red", width=8, font=LabelFont).place(x=655, y=380)

        # ===========Entry Part==================#
        i_d = tk.Entry(self, width=5, bd=3, font=EntryFont)
        i_d.place(x=40, y=420)
        Date = DateEntry(self, width=4, background="#00254d")
        Date.place(x=90, y=420)
        cust_name1 = tk.Entry(self, width=15, bd=3, font=EntryFont)
        cust_name1.place(x=140, y=420)
        prod_name = tk.Entry(self, width=15, bd=3, font=EntryFont)
        prod_name.place(x=270, y=420)
        prod_type = tk.Entry(self, width=10, bd=3, font=EntryFont)
        prod_type.place(x=400, y=420)
        prod_price = tk.Entry(self, width=10, bd=3, font=EntryFont)
        prod_price.place(x=490, y=420)
        quantity1 = tk.Entry(self, width=8, bd=3, font=EntryFont)
        quantity1.place(x=580, y=420)
        total = tk.Entry(self, width=8, bd=3, font=EntryFont)
        total.place(x=655, y=420)

        tk.Button(self, text="ADD", width=5, bg="brown", fg='white', font=("Verdana", 10, "bold"),
                  command=lambda: addquantity()).place(x=400, y=300)
        tk.Button(self, text="CLEAR", width=5, bg="brown", fg='white', font=("Verdana", 10, "bold"),
                  command=lambda: clear()).place(x=480, y=300)
        tk.Button(self, text="SAVE ORDER", width=10, bg="brown", fg='white', font=("Verdana", 10, "bold"),
                  command=lambda: submitdata()).place(x=40, y=460)
        tk.Button(self, text="VIEW ALL ORDERS", width=15, bg="brown", fg='white', font=("Verdana", 10, "bold"),
                  command=lambda: view_recent()).place(x=180, y=460)
        tk.Button(self, text="DELETE ORDER", width=15, bg="brown", fg="white", font=("Verdana", 10, "bold"),
                  command=lambda: delete_order()).place(x=370, y=460)

        # ============================USER LISTBOX===================================#
        # SETTING SCROLLBAR SETTINGS
        user_list = tk.Listbox(self, height=5, width=30, border=0)
        user_list.place(x=400, y=90)

        scrollbar = tk.Scrollbar(self)
        scrollbar.place(x=581, y=90)

        user_list.configure(yscrollcommand=scrollbar.set)
        user_list.configure(yscrollcommand=user_list.yview)

        def select_user(event):
            try:
                index = user_list.curselection()[0]

                selected_user = user_list.get(index)

                cust_name.delete(0, tk.END)
                cust_name.insert(tk.END, selected_user[0])
                cust_name1.delete(0, tk.END)
                cust_name1.insert(tk.END, selected_user[0])
                mobile_no.delete(0, tk.END)
                mobile_no.insert(tk.END, selected_user[1])
            except IndexError:
                pass

        user_list.bind('<<ListboxSelect>>', select_user)

        def populate_user_list():
            user_list.delete(0, tk.END)
            for row in getinfo():
                user_list.insert(tk.END, row)

        # =================================USER LIST END=============================#

        # =================================PRODUCT LIST==============================#
        # SETTING SCROLLBAR SETTINGS
        prod_list = tk.Listbox(self, height=5, width=48, border=0)
        prod_list.place(x=50, y=210)

        scrollbar2 = tk.Scrollbar(self)
        scrollbar2.place(x=340, y=210)

        prod_list.configure(yscrollcommand=scrollbar2.set)
        prod_list.configure(yscrollcommand=prod_list.yview)

        def select_item(event):
            try:
                index = prod_list.curselection()[0]

                selected_item = prod_list.get(index)

                prod_name.delete(0, tk.END)
                prod_name.insert(tk.END, selected_item[0])
                prod_price.delete(0, tk.END)
                prod_price.insert(tk.END, selected_item[1])
                prod_type.delete(0, tk.END)
                prod_type.insert(tk.END, selected_item[2])

            except IndexError:
                pass

        prod_list.bind('<<ListboxSelect>>', select_item)

        def populate_prod_list():
            user_list.delete(0, tk.END)
            for row in getprod():
                prod_list.insert(tk.END, row)

        populate_prod_list()
        populate_user_list()

        # ========================================PRODUCT LIST END===================================#

        # ===================================DEFINING FUNCTIONS TO SUBMIT DATA====================================#

        def submitdata():
            if quantity1.get() == " " or i_d == " ":
                messagebox.showinfo("Check whether all the fields are filled")
            else:
                insertd(i_d.get(), Date.get_date(), cust_name.get(), prod_name.get(), prod_type.get(), prod_price.get(),
                        quantity1.get(), total.get())

                for row in getstocks(prod_name.get()):
                    stocks = row
                stocks = int(stocks) - int(quantity1.get())

                updatestocks(prod_name.get(), stocks)
                master.switch_frame(PurchaseBill)
                i_d.delete(0, tk.END)
                Date.delete(0, tk.END)
                cust_name.delete(0, tk.END)
                prod_name.delete(0, tk.END)
                prod_type.delete(0, tk.END)
                prod_price.delete(0, tk.END)
                quantity.delete(0, tk.END)
                total.delete(0, tk.END)

        def delete_order():
            def submit2():
                ID = order_entry.get()
                if ID == "":
                    messagebox.showinfo(message="This field is required")
                else:
                    delorder(ID)
                    order_entry.delete(0, tk.END)
                    screen.destroy()

            screen = tk.Tk()
            screen.title("Delete Order")
            screen.geometry("350x200")
            screen.config(bg="#ADD8E6")
            tk.Label(screen, text="Delete Order", width=20, bg="green", font=("bold", 20)).pack(pady=10)
            tk.Label(screen, text="Enter Order ID", width=20, font=("bold", 15)).pack(pady=10)
            order_entry = tk.Entry(screen, width=25, bd=2)
            order_entry.pack(pady=10)

            tk.Button(screen, text='DELETE', width=10, bg='brown', fg='white', command=lambda: submit2()).pack(pady=10)

        def addquantity():
            Total_Cost = int(quantity.get()) * int(prod_price.get())
            if quantity1 != "":
                quantity1.insert(0, quantity.get())
                quantity.delete(0, tk.END)
                total.insert(0, Total_Cost)
            else:
                quantity1.delete(0, tk.END)

        def clear():
            quantity1.delete(0, tk.END)
            i_d.delete(0, tk.END)
            Date.delete(0, tk.END)
            cust_name.delete(0, tk.END)
            prod_name.delete(0, tk.END)
            prod_type.delete(0, tk.END)
            prod_price.delete(0, tk.END)
            quantity.delete(0, tk.END)
            total.delete(0, tk.END)


class ManageAccount(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Manage Account")
        tk.Label(self, text="Manage Account", bg="Yellow", width=20, font=("Verdana", 20, "bold")).place(x=10, y=20)
        tk.Label(self, text="Change Password", font=("Verdana", 20, "bold")).place(x=10, y=80)
        tk.Label(self, text="Enter Username", font=("Verdana", 12, "bold")).place(x=10, y=140)
        tk.Label(self, text="Enter New Password", font=("Verdana", 12, "bold")).place(x=10, y=200)
        tk.Label(self, text="Re-Enter Password", font=("Verdana", 12, "bold")).place(x=10, y=260)
        tk.Button(self, text="Change\nPassword", bg="brown", fg="white", font=("Verdana", 10, "bold"),
                  command=lambda: updateinfo()).place(x=30, y=310)
        tk.Button(self, text="Clear", height=2, width=8, bg="brown", fg="white", font=("Verdana", 10, "bold"),
                  command=lambda: clearform()).place(x=150, y=310)

        username = tk.Entry(self, bd=3, font=("Verdana", 10, "bold"))
        username.place(x=250, y=140)
        username.focus()
        password = tk.Entry(self, bd=3, font=("Verdana", 10, "bold"))
        password.place(x=250, y=200)
        ver_pass = tk.Entry(self, bd=3, font=("Verdana", 10, "bold"), show="*")
        ver_pass.place(x=250, y=260)

        def updateinfo():
            if username.get() == "" or password.get() == "" or ver_pass.get() == ():
                messagebox.showinfo(message="All fields are required")
            elif password.get() != ver_pass.get():
                messagebox.showinfo(message="Passwords DO NOT MATCH !")
            else:
                update(username.get(), password.get())

        def clearform():
            username.delete(0, tk.END)
            password.delete(0, tk.END)
            ver_pass.delete(0, tk.END)

# if __name__ == "__main__":
# app = Dashboard()
# app.mainloop()
