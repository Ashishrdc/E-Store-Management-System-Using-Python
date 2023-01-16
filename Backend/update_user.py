import tkinter as tk

import pymysql

Font = ("Verdana", 10, "bold")


def connect():
    global cursor, connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="e-store")
    cursor = connection.cursor()


def fetch():
    connect()
    cursor.execute("SELECT * FROM customerd")
    rows = cursor.fetchall()
    return rows


def update(i_d, n_ame, e_mail, a_ge, g_ender, m_obile):
    connect()
    cursor.execute("UPDATE customerd SET Name = %s, Email = %s, Age = %s, Gender = %s, Mobile = %s WHERE ID = %s",
                   (n_ame, e_mail, a_ge, g_ender, m_obile, i_d))
    connection.commit()


class CustomerUpdate(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('UPDATE USER INFORMATION')
        # Width height
        master.geometry("710x280")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()

    def create_widgets(self):
        # Creating Widgets
        tk.Label(self.master, text="Select Customer From The List To Update", bg="#E0FFFF",
                 font=("Verdana", 20, "bold")).place(x=5)
        tk.Label(self.master, text="ID", width=10, font=Font).grid(row=1, column=0)
        tk.Label(self.master, text="Name", font=Font).grid(row=2, column=0)
        tk.Label(self.master, text="Email", font=Font).grid(row=3, column=0)
        tk.Label(self.master, text="Age", font=Font).grid(row=4, column=0)
        tk.Label(self.master, text="Gender", font=Font).grid(row=5, column=0)
        tk.Label(self.master, text="Mobile", font=Font).grid(row=6, column=0)

        self.i_d = tk.Entry(self.master, font=Font)
        self.i_d.grid(row=1, column=1)
        self.n_ame = tk.Entry(self.master, font=Font)
        self.n_ame.grid(row=2, column=1)
        self.e_mail = tk.Entry(self.master, font=Font)
        self.e_mail.grid(row=3, column=1)
        self.a_ge = tk.Entry(self.master, font=Font)
        self.a_ge.grid(row=4, column=1)
        self.g_ender = tk.Entry(self.master, font=Font)
        self.g_ender.grid(row=5, column=1)
        self.m_obile = tk.Entry(self.master, font=Font)
        self.m_obile.grid(row=6, column=1)

        # Listbox
        self.user_list = tk.Listbox(self.master, height=10, width=60, border=0)
        self.user_list.grid(row=1, column=5, columnspan=3,
                            rowspan=6, padx=5)

        # scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=0, column=8)

        # setscrollbar
        self.user_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.user_list.yview)

        # Bind select
        self.user_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        tk.Button(self.master, text="UPDATE", height=2, width=12, bg='brown', fg='white',
                  command=self.update_item).grid(row=7, column=0, padx=20, pady=20)
        tk.Button(self.master, text="CLEAR", height=2, width=12, bg='brown', fg='white', command=self.clear_text).grid(
            row=7, column=1)

    def populate_list(self):
        self.user_list.delete(0, tk.END)
        for row in fetch():
            self.user_list.insert(tk.END, row)

    def select_item(self, event):
        try:
            index = self.user_list.curselection()[0]

            self.selected_item = self.user_list.get(index)

            self.i_d.delete(0, tk.END)
            self.i_d.insert(tk.END, self.selected_item[0])
            self.n_ame.delete(0, tk.END)
            self.n_ame.insert(tk.END, self.selected_item[1])
            self.e_mail.delete(0, tk.END)
            self.e_mail.insert(tk.END, self.selected_item[2])
            self.a_ge.delete(0, tk.END)
            self.a_ge.insert(tk.END, self.selected_item[3])
            self.g_ender.delete(0, tk.END)
            self.g_ender.insert(tk.END, self.selected_item[4])
            self.m_obile.delete(0, tk.END)
            self.m_obile.insert(tk.END, self.selected_item[5])
        except IndexError:
            pass

    def update_item(self):
        update(self.selected_item[0],
               self.n_ame.get(), self.e_mail.get(), self.a_ge.get(), self.g_ender.get(),
               self.m_obile.get())
        self.populate_list()

    def clear_text(self):
        self.i_d.delete(0, tk.END)
        self.n_ame.delete(0, tk.END)
        self.e_mail.delete(0, tk.END)
        self.a_ge.delete(0, tk.END)
        self.g_ender.delete(0, tk.END)
        self.m_obile.delete(0, tk.END)
