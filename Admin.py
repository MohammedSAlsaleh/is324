import tkinter as tk
from tkinter import *
import sqlite3
from tkinter import messagebox
import logging
from datetime import datetime
import random

conn = sqlite3.connect('ksupay.db')


class Admin:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Admin")
        self.window.geometry('600x400')
        self.window.iconbitmap('logo.ico')
        bg = PhotoImage(file="Background.png")
        my_label = Label(image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.window.resizable(False, False)

        self.buttonBack = tk.Button(self.window, text='Logout', command=self.logout, bg='#00f', fg='#fff',
                                    font=10).grid(row=1, column=1, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.balanceLabel = tk.Label(self.window, text="KSU entities Balance :  ", bg='#0084bd', fg='#00f',
                                     font=8).grid(row=3, column=3, sticky=tk.E, padx=5, pady=5)
        self.balanceText = tk.Label(self.window, text="", bg='#00f', fg='#fff', font=8)
        self.balanceText.grid(row=3, column=4, sticky=tk.E, padx=5, pady=5)
        self.getTotalBalance()
        self.entityLabel = tk.Label(self.window, text="KSU Entity Name :  ", bg='#0084bd').grid(row=5, column=0,
                                                                                                sticky=tk.E, padx=5,
                                                                                                pady=5)
        self.entityEntry = tk.Entry(self.window)
        self.entityEntry.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)

        self.buttonAddEntity = tk.Button(self.window, text='Add KSU entity', command=self.addEntity, bg='#65A8E1',
                                         font=8).grid(row=5, column=3, pady=5, sticky='w' + 'e' + 'n' + 's')

        self.buttonPayStipends = tk.Button(self.window, text='Pay Stipends', command=self.payStipends, bg='#f00',
                                           fg='#fff', font=8).grid(row=7, column=1, pady=5, padx=5,
                                                                   sticky='w' + 'e' + 'n' + 's')
        self.buttonCashOut = tk.Button(self.window, text='Cash Out', command=self.cashOut, bg='#0f0', fg='#fff',
                                       font=8).grid(row=7, column=2, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.buttonBackup = tk.Button(self.window, text='Backup database', command=self.backup, bg='#00f', fg='#fff',
                                      font=8).grid(row=7, column=3, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')

        self.window.mainloop()

    def logout(self):
        self.window.destroy()
        import Signup
        Signup.Signup()

    def getTotalBalance(self):
        cursor = conn.execute("SELECT sum(wallet_balance) FROM users WHERE wallet_type='KSU'")
        for balance in cursor:
            self.balanceText.config(text=str(balance[0]) + " SR")

    def addEntity(self):
        entity_name = self.entityEntry.get()
        if entity_name.strip() == "":
            self.entityEntry.focus()

            messagebox.showerror(title="Input Error", message="Please Provide entity name")
            return

        now = datetime.now()
        formated_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        wallet_type = "KSU"
        wallet_balance = 0.0

        range_start = 10 ** (10 - 1)
        range_end = (10 ** 10) - 1
        Wallet_no = random.randint(range_start, range_end)
        SQL = """ INSERT INTO users(entity_name, user_id, wallet_number,wallet_type, wallet_balance,  date_time) VALUES ( ?, ?, ?, ?, ?,?)"""
        SQL_VALUES = (entity_name, Wallet_no, Wallet_no, wallet_type, wallet_balance, formated_date_time)
        conn.execute(SQL, SQL_VALUES)
        conn.commit()
        messagebox.showinfo(message='KSU entity was created successfully')

    def payStipends(self):
        amount = 1000
        val = (amount,)
        conn.execute("UPDATE users SET wallet_balance=wallet_balance+? WHERE wallet_type='STUDENT'", val)
        conn.commit()
        messagebox.showinfo(message='Pay Stipends operation was completed')

    def cashOut(self):
        conn.execute("UPDATE users SET wallet_balance=0 WHERE wallet_type='KSU'")
        conn.commit()
        messagebox.showinfo(message='Cash out operation was completed')
        self.balanceText.config(text="0 SAR")

    def backup(self):
        cursor = conn.execute("SELECT * FROM users")
        file_operation = open("KSUbackup.csv", "w+")
        for data in cursor:
            values = (str(data[0]), str(data[1]), str(data[2]), str(data[3]), str(data[4]), str(data[5]), str(data[6]),
                      str(data[7]), str(data[8]), str(data[9]), str(data[10]), str(data[11]))

            file_operation.write(values[0])
            file_operation.write(",")

            file_operation.write(values[1])
            file_operation.write(",")

            file_operation.write(values[2])
            file_operation.write(",")

            file_operation.write(values[3])
            file_operation.write(",")

            file_operation.write(values[4])
            file_operation.write(",")

            file_operation.write(values[5])
            file_operation.write(",")

            file_operation.write(values[6])
            file_operation.write(",")

            file_operation.write(values[7])
            file_operation.write(",")

            file_operation.write(values[8])
            file_operation.write(",")

            file_operation.write(values[9])
            file_operation.write(",")

            file_operation.write(values[10])
            file_operation.write(",")

            file_operation.write(values[11])

            file_operation.write("\n")
        file_operation.close()
        messagebox.showinfo(message='Backup operation was completed')
