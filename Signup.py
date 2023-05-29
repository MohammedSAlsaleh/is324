from pickle import TRUE
import tkinter as tk
import sqlite3
from datetime import datetime
import random

from tkinter import messagebox
import re
from tkinter import *

conn = sqlite3.connect('ksupay.db')
create_users_table = """CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(40),
            last_name  VARCHAR(40),
            entity_name VARCHAR(40),
            user_email VARCHAR(150),
            phone_number VARCHAR(10),
            user_id VARCHAR(10) NOT NULL,
            wallet_number BIGINT NOT NULL,
            wallet_type VARCHAR(10) NOT NULL,
            wallet_balance DECIMAL(6,2) NOT NULL,
            user_password VARCHAR(30),
            date_time DATETIME not null
        );"""
conn.execute(create_users_table)


class Signup:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sign up")
        self.window.geometry('600x400')
        self.window.iconbitmap('logo.ico')
        bg = PhotoImage(file="Background.png")
        my_label = Label(image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.window.resizable(False, False)


        self.goLoginLabel = tk.Label(self.window, text="You have an account? press on:", width=10, bg='#0084bd',
                                     fg='#f00').grid(row=1, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.buttonBack = tk.Button(self.window, text='Login', command=self.go_Login, bg='#00f', fg='#0084bd',
                                    font=10).grid(row=1, column=1, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.formLabel = tk.Label(self.window, text="Please Provide the following information", bg='#0084bd', fg='#00f',
                                  font=8).grid(row=2, column=0, pady=5, sticky='w' + 'e' + 'n' + 's')

        self.fnameEntry = tk.Entry(self.window)
        self.fnameLabel = tk.Label(self.window, text="First Name:", bg='#0084bd').grid(row=4, column=0, sticky=tk.E,
                                                                                       padx=5, pady=5)
        self.fnameEntry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.fnameEntry.insert(0, "first name")

        self.lnameEntry = tk.Entry(self.window)
        self.lnameLabel = tk.Label(self.window, text="Last Name:", bg='#0084bd').grid(row=5, column=0, sticky=tk.E,
                                                                                      padx=5,
                                                                                      pady=5)
        self.lnameEntry.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        self.lnameEntry.insert(0, "Last name")

        self.studentIDEntry = tk.Entry(self.window)
        self.studentIDLabel = tk.Label(self.window, text="Student ID No:", bg='#0084bd').grid(row=6, column=0,
                                                                                              sticky=tk.E,
                                                                                              padx=5, pady=5)
        self.studentIDEntry.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        self.studentIDEntry.insert(0, "1234567890")

        self.passwordEntry = tk.Entry(self.window)
        self.passwordLabel = tk.Label(self.window, text="Password:", bg='#0084bd').grid(row=7, column=0, sticky=tk.E,
                                                                                        padx=5, pady=5)
        self.passwordEntry.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)
        self.passwordEntry.insert(0, "*")

        self.emailEntry = tk.Entry(self.window)
        self.emailLabel = tk.Label(self.window, text="Email Address:", bg='#0084bd').grid(row=8, column=0, sticky=tk.E,
                                                                                          padx=5, pady=5)
        self.emailEntry.grid(row=8, column=1, sticky=tk.W, padx=5, pady=5)
        self.emailEntry.insert(0, "xxxxx@ksu.edu.sa")

        self.phoneEntry = tk.Entry(self.window)
        self.phoneLabel = tk.Label(self.window, text="Phone Number:", bg='#0084bd').grid(row=9, column=0, sticky=tk.E,
                                                                                         padx=5, pady=5)
        self.phoneEntry.grid(row=9, column=1, sticky=tk.W, padx=5, pady=5)
        self.phoneEntry.insert(0, "05xxxxxxxx")

        self.buttonRegister = tk.Button(self.window, text='Signup', command=self.validateForm, bg='#f00', fg='#0ff',
                                        font=10).grid(row=10, column=1, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.window.mainloop()

    def checkAvailability(self, student_id):
        sqlQuery = "select user_id from users"
        Cursor = conn.execute(sqlQuery)
        for row in Cursor:
            if int(row[0]) == student_id:
                tk.messagebox.showerror(title="Input Error", message="User already registered")
                return
        return TRUE

    def addUser(self):
        firstname = self.fnameEntry.get()
        lastname = self.lnameEntry.get()
        studentid = self.studentIDEntry.get()
        studentEmail = self.emailEntry.get()
        studentPhone = self.phoneEntry.get()
        studentpassword = self.passwordEntry.get()
        now = datetime.now()
        formated_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        wallet_type = "STUDENT"
        wallet_balance = 1000.0
        entity_name = "student"
        range_start = 10 ** (10 - 1)
        range_end = (10 ** 10) - 1
        Wallet_no = random.randint(range_start, range_end)
        SQL = """ INSERT INTO users(first_name,last_name,entity_name, user_email,phone_number,user_id, wallet_number,wallet_type, wallet_balance, user_password, date_time) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        SQL_VALUES = (
            firstname, lastname, entity_name, studentEmail, studentPhone, studentid, Wallet_no, wallet_type,
            wallet_balance,
            studentpassword, formated_date_time)
        conn.execute(SQL, SQL_VALUES)
        conn.commit()
        messagebox.showinfo(message='Student account was created successfully')

    def go_Login(self):
        self.window.destroy()
        import Login
        Login.Login()

    def validateForm(self):
        firstname = self.fnameEntry.get()

        if firstname.strip() == "":
            self.fnameEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide first name")
            return

        lastname = self.lnameEntry.get()

        if lastname.strip() == "":
            self.lnameEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide Last name")
            return

        studentid = self.studentIDEntry.get()

        if studentid.strip() == "":
            self.studentIDEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide student id")
            return

        try:
            studentid = int(studentid)

        except:
            self.studentIDEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide student id as number")
            return


        if len(str(studentid)) != 10:
            self.studentIDEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide student id as 10 digits number")
            return

        studentEmail = self.emailEntry.get()

        if studentEmail.strip() == "":
            self.emailEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide student Email")
            return

        studentPhone = self.phoneEntry.get()

        if studentPhone.strip() == "":
            self.emailEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide student Phone")
            return

        try:
            studentPhoneint = int(studentPhone)

        except:
            self.phoneEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide student phone as number")
            return


        if len(str(studentPhone)) != 10:
            self.phoneEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Please Provide student phone as 10 digits number")
            return

        studentpassword = self.passwordEntry.get()

        if len(str(studentpassword)) < 6:
            self.passwordEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Password is 6 characters or digits minimum")
            return


        reg = "^[A-Za-z ]*$"
        pat = re.compile(reg)
        x = re.search(pat, firstname)
        if x is None:
            messagebox.showerror(title="Input Error", message="invalid first name")
            return

        reg = "^[A-Za-z ]*$"
        pat = re.compile(reg)
        x = re.search(pat, lastname)
        if x is None:
            messagebox.showerror(title="Input Error", message="invalid last name")
            return

        reg = "^([a-zA-Z0-9\._-]+)(@ksu.edu.sa)$"
        pat = re.compile(reg)
        x = re.search(pat, studentEmail)
        if x is None:
            messagebox.showerror(title="Input Error", message="Invalid KSU email address")
            return
        reg = "^(05)[0-9]{8}$"
        pat = re.compile(reg)
        x = re.search(pat, studentPhone)
        if x is None:
            messagebox.showerror(title="Input Error", message="Invalid Phone number")
            return
        if self.checkAvailability(studentid):
            self.addUser()


Signup()
