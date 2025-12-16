import tkinter as tk
from tkinter import messagebox
import sqlite3

def login():
    user = entry_user.get()
    pwd = entry_pass.get()

    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user, pwd)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Login", "Success")
        open_dashboard()
    else:
        messagebox.showerror("Login", "Invalid login")

def open_dashboard():
    dash = tk.Toplevel(root)
    dash.title("CRM Dashboard")
    tk.Label(dash, text="Welcome to CRM").pack(padx=20, pady=20)

root = tk.Tk()
root.title("CRM Login")

tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password").pack()
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
