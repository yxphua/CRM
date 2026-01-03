import tkinter as tk
from tkinter import messagebox
from database import get_connection
import sqlite3

def open_edit_member(parent):
    win = tk.Toplevel(parent)
    win.title("Edit Member")

    tk.Label(win, text="Member ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    tk.Label(win, text="New Name").pack()
    entry_name = tk.Entry(win)
    entry_name.pack()

    tk.Label(win, text="New Phone").pack()
    entry_phone = tk.Entry(win)
    entry_phone.pack()

    def update_member():
        member_id = entry_id.get().strip()
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()

        if not member_id or not name or not phone:
            messagebox.showerror("Error", "Enter all fields")
            return
        
        if not member_id.isdigit():
            messagebox.showerror("Error", "Member ID must be a number")
            return
        member_id = int(member_id)

        if not phone.isdigit() or len(phone) < 9 or len(phone) > 11:
            messagebox.showerror("Error", "Phone must be 9-11 digits and contain only numbers")
            return

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE members SET name=?, phone=? WHERE MemberId=?",
                    (name, phone, member_id)
                )

                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Member not found")
                else:
                    messagebox.showinfo("Success", "Member info updated successfully")
        
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    tk.Button(win, text="Update", command=update_member).pack(pady=10)
