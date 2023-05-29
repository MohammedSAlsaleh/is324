import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import *

conn = sqlite3.connect('ksupay.db')


class Login:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")

        self.window.geometry('600x400')
        self.window.iconbitmap('logo.ico')
        bg = PhotoImage(file="Background.png")
        my_label = Label(image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.window.resizable(False, False)

        self.user_id = 0;
        self.goLoginLabel = tk.Label(self.window, text="You have not an account? press on:", width=10, bg='#0084bd',
                                     fg='#f00').grid(row=1, column=0, padx=5, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.buttonBack = tk.Button(self.window, text='Sign up', command=self.go_signup, bg='#00f', fg='#0084bd',
                                    font=10).grid(row=1, column=1, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.formLabel = tk.Label(self.window, text="Please Provide the following credential to login", bg='#0084bd',
                                  fg='#00f', font=8).grid(row=2, column=0, pady=5, sticky='w' + 'e' + 'n' + 's')

        self.studentIDEntry = tk.Entry(self.window)
        self.studentIDLabel = tk.Label(self.window, text="Student ID No:", bg='#0084bd').grid(row=3, column=0,
                                                                                              sticky=tk.E, padx=5,
                                                                                              pady=5)
        self.studentIDEntry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.studentIDEntry.insert(0, "1234567890")

        self.passwordEntry = tk.Entry(self.window)
        self.passwordLabel = tk.Label(self.window, text="Password:", bg='#0084bd').grid(row=4, column=0, sticky=tk.E,
                                                                                        padx=5, pady=5)
        self.passwordEntry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.passwordEntry.insert(0, "*")

        self.buttonRegister = tk.Button(self.window, text='Login', command=self.validateForm, bg='#f00', fg='#0ff',
                                        font=10).grid(row=5, column=1, pady=5, sticky='w' + 'e' + 'n' + 's')
        self.window.mainloop()

    def go_signup(self):
        self.window.destroy()
        import Signup
        Signup.Signup()

    def login(self):
        studentid = self.studentIDEntry.get()
        studentpassword = self.passwordEntry.get()
        val = (studentid, studentpassword,)

        cursor = conn.execute("SELECT * FROM users where user_id=? and user_password=?", val)
        loginResult = "none"
        for row in cursor:

            loginResult = row[8]
            self.user_id = row[0]

        return loginResult

    def validateForm(self):
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
        studentpassword = self.passwordEntry.get()

        if len(str(studentpassword)) < 6:
            self.passwordEntry.focus()
            tk.messagebox.showerror(title="Input Error", message="Password is 6 characters or digits minimum")
            return

        if self.login() == 'STUDENT':
            import Wallet
            self.window.destroy()
            Wallet.Wallet(self.user_id)
        elif self.login() == 'ADMIN':
            import Admin
            self.window.destroy()
            Admin.Admin()
        else:
            messagebox.showerror(title="Credential Erro", message="Student Id or password error")
