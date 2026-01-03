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
        # Strips whitespace at the edges of the input
        username = user.get().strip()
        password = pwd.get().strip()

        # Checks if either field is empty before querying the database
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return # Stop here if inputs are incomplete
        
        # Hashes the password before checking against the database for better security
        import hashlib 
        hashed_pwd = hashlib.sha256(password.encode()).hexdigest()

        # Context manager for connection handling
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pwd))
            result = cur.fetchone()

        if result:
            open_menu_main(root)
        else:
            messagebox.showerror("Error", "Invalid login")

    tk.Button(root, text="Login", command=login).pack(pady=10)
