import tkinter as tk
from tkinter import messagebox
from database import get_connection

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
        member_id = entry_id.get()
        name = entry_name.get()
        phone = entry_phone.get()

        if not member_id or not name or not phone:
            messagebox.showerror("Error", "Enter all fields")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE members SET name=?, phone=? WHERE MemberId=?",
            (name, phone, member_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Member not found")
        else:
            messagebox.showinfo("Success", "Member updated")

        conn.close()

    tk.Button(win, text="Update", command=update_member).pack(pady=10)
