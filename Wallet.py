import tkinter as tk
from tkinter import *
import sqlite3
from tkinter import messagebox
import logging
from datetime import datetime

conn = sqlite3.connect('ksupay.db')


class Wallet:
    def __init__(self, user_id):
        self.window = tk.Tk()
        self.window.title("Student Wallet")
        self.window.geometry('600x400')
        self.window.iconbitmap('logo.ico')
        bg = PhotoImage(file="Background.png")
        my_label = Label(image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.window.resizable(False, False)

        print(user_id)
        self.buttonBack = tk.Button(self.window, text='Logout', command=self.logout, bg='#00f', fg='#0084bd',
                                    font=10).grid(row=1, column=1, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.balance, self.wallet_no = self.getData(user_id)
        print(self.wallet_no)
        self.walletNoLabel = tk.Label(self.window, text="Wallet number :  ", bg='#0084bd', fg='#00f', font=8).grid(
            row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.walletNoText = tk.Label(self.window, text=self.wallet_no, bg='#00f', fg='#0084bd', font=8).grid(row=3,
                                                                                                             column=1,
                                                                                                             sticky=tk.E,
                                                                                                             padx=5,
                                                                                                             pady=5)
        self.balanceLabel = tk.Label(self.window, text="Account Balance :  ", bg='#0084bd', fg='#00f', font=8).grid(
            row=3, column=3, sticky=tk.E, padx=5, pady=5)
        self.balanceText = tk.Label(self.window, text=self.balance, bg='#00f', fg='#0084bd', font=8)
        self.balanceText.grid(row=3, column=4, sticky=tk.E, padx=5, pady=5)

        self.toWalletLabel = tk.Label(self.window, text="Target Wallet number :  ", bg='#0084bd').grid(row=5, column=0,
                                                                                                       sticky=tk.E,
                                                                                                       padx=5, pady=5)
        self.toWalletEntry = tk.Entry(self.window)
        self.toWalletEntry.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)

        self.amountLabel = tk.Label(self.window, text="Amount to Pay :  ", bg='#0084bd').grid(row=5, column=3,
                                                                                              sticky=tk.E, padx=5,
                                                                                              pady=5)
        self.amountEntry = tk.Entry(self.window)
        self.amountEntry.grid(row=5, column=4, sticky=tk.E, padx=5, pady=5)
        self.buttonPay = tk.Button(self.window, text='Pay', command=self.payKSU, bg='#0f0', fg='#0084bd', font=10).grid(
            row=7, column=1, pady=5, sticky='w' + 'e' + 'n' + 's')

        self.window.mainloop()

    def getData(self, user_id):
        val = (user_id,)

        cursor = conn.execute("SELECT * FROM users where id=?", val)
        for row in cursor:
            balance = row[9]
            wallet_no = row[7]
        return balance, wallet_no

    def logout(self):
        self.window.destroy()
        import Signup
        Signup.Signup()

    def payKSU(self):
        targetWallet = self.toWalletEntry.get()
        if targetWallet.strip() == "":
            self.toWalletEntry.focus()
            messagebox.showerror(title="Input Error", message="Please Provide Target Wallet number")
            return

        try:
            targetWallet = int(targetWallet)

        except:
            self.toWalletEntry.focus()
            messagebox.showerror(title="Input Error", message="Please Provide Target Wallet as number")
            return

        if len(str(targetWallet)) != 10:
            self.toWalletEntry.focus()
            messagebox.showerror(title="Input Error", message="Please Provide Target Wallet number as 10 digits number")
            return

        amount = self.amountEntry.get()
        if amount.strip() == "":
            self.amountEntry.focus()
            messagebox.showerror(title="Input Error", message="Please Provide teh amount of pay")
            return

        try:
            amount = int(amount)

        except:
            self.amountEntry.focus()
            messagebox.showerror(title="Input Error", message="Please Provide amount as number")
            return
        if amount > self.balance:
            self.amountEntry.focus()
            messagebox.showerror(title="Input Error", message="Insufficient funds")
            return
        if targetWallet == self.wallet_no:
            self.toWalletEntry.focus()
            messagebox.showerror(title="Input Error", message="You can not transfer to your wallet")
            return

        val = (targetWallet,)
        cursor = conn.execute("SELECT * FROM users where wallet_number=? ", val)
        validWallet = "none"
        for row in cursor:
            validWallet = "yes"

        if validWallet != 'yes':
            self.toWalletEntry.focus()
            messagebox.showerror(title="Input Error", message="Invalid target Wallet")
            return

        logging.basicConfig(filename="KSU.log", format='', filemode='a')

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        val = (amount, targetWallet,)
        conn.execute("UPDATE users SET wallet_balance=wallet_balance+? WHERE wallet_number=?", val)
        conn.commit()

        val = (amount, self.wallet_no,)
        conn.execute("UPDATE users SET wallet_balance=wallet_balance-? WHERE wallet_number=?", val)
        conn.commit()

        logger.info(
            "Time of transaction : {}  Amount sent : {} SR  Sender's wallet number : {}    Receiver's wallet_number : {}  ".format(
                dt, amount, self.wallet_no, targetWallet))
        messagebox.showinfo(message='Payment Transaction was created successfully')
        self.balance = self.balance - amount
        self.balanceText.config(text=self.balance)
