from logging import root
import tkinter as tk
from tkinter import messagebox
from database import get_connection
from menu_main import open_menu_main
import sqlite3

def open_add_member(parent):
    win = tk.Toplevel(parent)
    win.title("Add Member")

    tk.Label(win, text="Name").grid(row=0, column=0)
    entry_name = tk.Entry(win)
    entry_name.grid(row=0, column=1)

    tk.Label(win, text="Phone Number").grid(row=1, column=0)
    entry_phone = tk.Entry(win)
    entry_phone.grid(row=1, column=1)

    def add():
        # Strip whitespace
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()

        if not name or not phone:
            messagebox.showwarning("Error", "All fields required")
            return

        if not phone.isdigit():
            messagebox.showerror("Error", "Phone must contain only digits")
            return
        
        if len(phone) < 9 or len(phone) > 11:
            messagebox.showerror("Error", "Phone must be 9-11 digits long")
            return

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO members (name, phone) VALUES (?, ?)",
                    (name, phone)
                )
                messagebox.showinfo("Success", "Member Successfully Added")
                load_member()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Member already exists"
            )

    # Button to add member
    tk.Button(win, text="Add Member", command=add).grid(row=2, column=0, columnspan=2, pady=10)

    # Listbox for member list
    listbox = tk.Listbox(win, width=40)
    listbox.grid(row=3, column=0, columnspan=2, pady=10)

    def load_member():
        listbox.delete(0, tk.END)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MemberId, name, phone FROM members")
            rows = cursor.fetchall()

        for r in rows:
            listbox.insert(tk.END, f"ID {r[0]} | {r[1]} | {r[2]}")

    load_member()
