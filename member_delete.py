import tkinter as tk
from tkinter import messagebox
from database import get_connection

def open_delete_member(parent):
    win = tk.Toplevel(parent)
    win.title("Delete Member")

    tk.Label(win, text="Member ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    def delete_member():
        member_id = entry_id.get()

        if not member_id:
            messagebox.showerror("Error", "Enter Member ID")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM members WHERE MemberId=?", (member_id,))
        conn.commit()

        # CHECK IF MEMBER EXISTED
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Member ID not found")
        else:
            messagebox.showinfo("Success", "Member removed successfully")

        conn.close()

    tk.Button(win, text="Delete", command=delete_member).pack(pady=10)
