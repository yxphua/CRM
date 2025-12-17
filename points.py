import tkinter as tk
from tkinter import messagebox
from database import get_connection

def open_points_panel(parent):
    win = tk.Toplevel(parent)
    win.title("Points Panel")

    tk.Label(win, text="Member ID").grid(row=0, column=0)
    entry_id = tk.Entry(win)
    entry_id.grid(row=0, column=1)

    tk.Label(win, text="Name:").grid(row=1, column=0)
    label_name = tk.Label(win, text="-")
    label_name.grid(row=1, column=1)

    tk.Label(win, text="Points:").grid(row=2, column=0)
    label_points = tk.Label(win, text="-")
    label_points.grid(row=2, column=1)

    def search():
        member_id = entry_id.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, points FROM members WHERE id=?", (member_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            label_name.config(text=row[0])
            label_points.config(text=row[1])
        else:
            messagebox.showerror("Error", "Member not found")

    tk.Button(win, text="Search", command=search).grid(row=0, column=2, padx=10)

    tk.Label(win, text="Change Points").grid(row=3, column=0)
    entry_change = tk.Entry(win)
    entry_change.grid(row=3, column=1)

    def update(add=True):
        member_id = entry_id.get()
        value = entry_change.get()

        try:
            value = int(value)
        except:
            messagebox.showerror("Error", "Invalid number")
            return

        if not add:
            value = -abs(value)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE members SET points = points + ? WHERE id=?", (value, member_id))
        conn.commit()

        cursor.execute("SELECT name, points FROM members WHERE id=?", (member_id,))
        row = cursor.fetchone()
        conn.close()

        label_name.config(text=row[0])
        label_points.config(text=row[1])

        messagebox.showinfo("Success", "Points updated")

    tk.Button(win, text="Add Points", command=lambda: update(True)).grid(row=4, column=0, pady=5)
    tk.Button(win, text="Deduct Points", command=lambda: update(False)).grid(row=4, column=1, pady=5)
