import tkinter as tk
from tkinter import messagebox
from database import get_connection
from menu_main import open_menu_main

def open_login_screen(root):
    for w in root.winfo_children():
        w.destroy()

    root.title("Login")

    tk.Label(root, text="Username").pack(pady=5)
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Password").pack(pady=5)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    def login_action():
        user = entry_user.get()
        pwd = entry_pass.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Logged in")
            open_menu_main(root)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(root, text="Login", command=login_action).pack(pady=10)

