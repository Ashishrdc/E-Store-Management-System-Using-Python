import tkinter as tk

import pymysql

Font = ("Verdana", 10, "bold")


def connect():
    global cursor, connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="e-store")
    cursor = connection.cursor()


def fetch():
    connect()
    cursor.execute("SELECT * FROM prod_info")
    rows = cursor.fetchall()
    return rows


def update(i_d, n_ame, p_rice, t_ype, r_etailer, s_tock):
    connect()
    cursor.execute(
        "UPDATE prod_info SET Product_Name = %s, Product_Price = %s, Product_Type = %s, Retailer = %s, Product_Stock = %s WHERE Product_ID = %s",
        (n_ame, p_rice, t_ype, r_etailer, s_tock, i_d))
    connection.commit()


class ProdUpdate(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('UPDATE PRODUCT INFORMATION')
        # Width height
        master.geometry("710x300")
        master.resizable(False, False)
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()

    def create_widgets(self):
        # Creating Widgets
        tk.Label(self.master, text="Select Product From The List To Update", bg="#FFFF00",
                 font=("Verdana", 20, "bold")).place(x=5)
        tk.Label(self.master, text="Product ID", width=10, font=Font).grid(row=1, column=0)
        tk.Label(self.master, text="Product Name", font=Font).grid(row=2, column=0)
        tk.Label(self.master, text="Product Price", font=Font).grid(row=3, column=0)
        tk.Label(self.master, text="Product Type", font=Font).grid(row=4, column=0)
        tk.Label(self.master, text="Retailer", font=Font).grid(row=5, column=0)
        tk.Label(self.master, text="Product Stock", font=Font).grid(row=6, column=0)

        self.i_d = tk.Entry(self.master, font=Font)
        self.i_d.grid(row=1, column=1)
        self.n_ame = tk.Entry(self.master, font=Font)
        self.n_ame.grid(row=2, column=1)
        self.p_rice = tk.Entry(self.master, font=Font)
        self.p_rice.grid(row=3, column=1)
        self.t_ype = tk.Entry(self.master, font=Font)
        self.t_ype.grid(row=4, column=1)
        self.r_etailer = tk.Entry(self.master, font=Font)
        self.r_etailer.grid(row=5, column=1)
        self.s_tock = tk.Entry(self.master, font=Font)
        self.s_tock.grid(row=6, column=1)

        # Listbox
        self.prod_list = tk.Listbox(self.master, height=10, width=61, border=0)
        self.prod_list.grid(row=1, column=5, columnspan=3,
                            rowspan=6, padx=5)

        # scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=0, column=8)

        # setscrollbar
        self.prod_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.prod_list.yview)

        # Bind select
        self.prod_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        tk.Button(self.master, text="UPDATE", height=2, width=12, bg='brown', fg='white',
                  command=self.update_item).grid(row=7, column=0, padx=20, pady=20)
        tk.Button(self.master, text="CLEAR", height=2, width=12, bg='brown', fg='white', command=self.clear_text).grid(
            row=7, column=1)

    def populate_list(self):
        self.prod_list.delete(0, tk.END)
        for row in fetch():
            self.prod_list.insert(tk.END, row)

    def select_item(self, event):
        try:
            index = self.prod_list.curselection()[0]

            self.selected_item = self.prod_list.get(index)

            self.i_d.delete(0, tk.END)
            self.i_d.insert(tk.END, self.selected_item[0])
            self.n_ame.delete(0, tk.END)
            self.n_ame.insert(tk.END, self.selected_item[1])
            self.p_rice.delete(0, tk.END)
            self.p_rice.insert(tk.END, self.selected_item[2])
            self.t_ype.delete(0, tk.END)
            self.t_ype.insert(tk.END, self.selected_item[3])
            self.r_etailer.delete(0, tk.END)
            self.r_etailer.insert(tk.END, self.selected_item[4])
            self.s_tock.delete(0, tk.END)
            self.s_tock.insert(tk.END, self.selected_item[5])
        except IndexError:
            pass

    def update_item(self):
        update(self.selected_item[0],
               self.n_ame.get(), self.p_rice.get(), self.t_ype.get(), self.r_etailer.get(),
               self.s_tock.get())
        self.populate_list()

    def clear_text(self):
        self.i_d.delete(0, tk.END)
        self.n_ame.delete(0, tk.END)
        self.p_rice.delete(0, tk.END)
        self.t_ype.delete(0, tk.END)
        self.r_etailer.delete(0, tk.END)
        self.s_tock.delete(0, tk.END)
