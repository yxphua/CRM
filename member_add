from logging import root
import tkinter as tk
from tkinter import messagebox
from database import get_connection
from menu_main import open_menu_main

def open_add_member(parent):
    win = tk.Toplevel(parent)
    win.title("Add Member")

    tk.Label(win, text="Name").grid(row=0, column=0)
    entry_name = tk.Entry(win)
    entry_name.grid(row=0, column=1)

    tk.Label(win, text="Phone").grid(row=1, column=0)
    entry_phone = tk.Entry(win)
    entry_phone.grid(row=1, column=1)

    def add():
        name = entry_name.get()
        phone = entry_phone.get()

        if not name or not phone:
            messagebox.showwarning("Error", "All fields required")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Member Added")
        load_member()

    tk.Button(win, text="Add Member", command=add).grid(row=2, column=0, columnspan=2, pady=10)

    # Listbox for member list
    listbox = tk.Listbox(win, width=40)
    listbox.grid(row=3, column=0, columnspan=2, pady=10)

    def load_member():
        listbox.delete(0, tk.END)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone FROM members")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            listbox.insert(tk.END, f"ID {r[0]} | {r[1]} | {r[2]}")

    load_member()
