
# login.py (ttk styled, full-page)
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from menu_main import open_menu_main
import hashlib

from ui_theme import apply_global_style, make_header, make_center_card

def open_login_screen(parent: tk.Tk):
    # Clear current content and rebuild page
    for w in parent.winfo_children():
        w.destroy()

    parent.title("Login")
    apply_global_style(parent)

    # Header
    make_header(parent, "The Brew Corner — Login")

    # Card
    card = make_center_card(parent, width=420)

    ttk.Label(card, text="Welcome back 👋", style="Heading.TLabel").pack(anchor="w", padx=24, pady=(24, 4))
    ttk.Label(card, text="Sign in to access the POS CRM.", style="Subheading.TLabel").pack(anchor="w", padx=24, pady=(0, 16))

    form = ttk.Frame(card, style="Card.TFrame")
    form.pack(fill="x", padx=24, pady=(8, 24))
    form.columnconfigure(0, weight=1)

    ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", pady=(0, 6))
    user = ttk.Entry(form)
    user.grid(row=1, column=0, sticky="ew", pady=(0, 12))

    ttk.Label(form, text="Password").grid(row=2, column=0, sticky="w", pady=(0, 6))
    pwd = ttk.Entry(form, show="*")
    pwd.grid(row=3, column=0, sticky="ew", pady=(0, 12))

    def login():
        username = user.get().strip()
        password = pwd.get().strip()
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return
        hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM users WHERE username=? AND password=?", (username, hashed_pwd))
                ok = cur.fetchone() is not None
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
            return

        if ok:
            # Navigate to main menu (reuses parent)
            open_menu_main(parent)
        else:
            messagebox.showerror("Error", "Invalid login")

    ttk.Button(card, text="Login", style="Accent.TButton", command=login).pack(padx=24, pady=(0, 24), fill="x")
    parent.bind("<Return>", lambda e: login())
    user.focus_set()
