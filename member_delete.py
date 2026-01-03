import tkinter as tk
from tkinter import messagebox
from database import get_connection
import sqlite3

def open_delete_member(parent):
    win = tk.Toplevel(parent)
    win.title("Delete Member")

    tk.Label(win, text="Member ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    def delete_member():
        member_id = entry_id.get().strip()

        if not member_id:
            messagebox.showerror("Error", "Enter Member ID")
            return

        if not member_id.isdigit():
            messagebox.showerror("Error", "Member ID must be a number")
            return
        
        member_id = int(member_id)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM members WHERE MemberId=?", (member_id,))

                # CHECK IF MEMBER EXISTED
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Member ID not found")
                else:
                    messagebox.showinfo("Success", "Member Deleted Successfully")
        
        # Shows database errors that are not integrity errors instead of crashing Pythonx
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    tk.Button(win, text="Delete", command=delete_member).pack(pady=10)
