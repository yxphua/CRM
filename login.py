import tkinter as tk
from tkinter import messagebox
from database import get_connection
from menu_main import open_menu_main

def open_login_screen(root):
    for w in root.winfo_children():
        w.destroy()

    root.title("Login")

    tk.Label(root, text="Username").pack()
    user = tk.Entry(root)
    user.pack()

    tk.Label(root, text="Password").pack()
    pwd = tk.Entry(root, show="*")
    pwd.pack()

    def login():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user.get(), pwd.get())
        )
        result = cur.fetchone()
        conn.close()

        if result:
            open_menu_main(root)
        else:
            messagebox.showerror("Error", "Invalid login")

    tk.Button(root, text="Login", command=login).pack(pady=10)
