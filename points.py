import tkinter as tk
from tkinter import messagebox
from database import get_connection

def open_points_panel(parent):
    win = tk.Toplevel(parent)
    win.title("Points Panel")

    # Phone input
    tk.Label(win, text="Phone Number").grid(row=0, column=0)
    entry_phone = tk.Entry(win)
    entry_phone.grid(row=0, column=1)

    # Display name
    tk.Label(win, text="Name").grid(row=1, column=0)
    label_name = tk.Label(win, text="-")
    label_name.grid(row=1, column=1)

    # Display points
    tk.Label(win, text="Points").grid(row=2, column=0)
    label_points = tk.Label(win, text="-")
    label_points.grid(row=2, column=1)

    def search():
        phone = entry_phone.get()

        if not phone:
            messagebox.showerror("Error", "Enter phone number")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, points FROM members WHERE phone=?",
            (phone,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            label_name.config(text=row[0])
            label_points.config(text=row[1])
        else:
            messagebox.showerror("Error", "Member not found")

    tk.Button(win, text="Search", command=search).grid(row=0, column=2, padx=10)

    # Change points
    tk.Label(win, text="Change Points").grid(row=3, column=0)
    entry_change = tk.Entry(win)
    entry_change.grid(row=3, column=1)

    def update(add=True):
        phone = entry_phone.get()
        value = entry_change.get()

        if not phone:
            messagebox.showerror("Error", "Search member first")
            return

        try:
            value = int(value)
        except:
            messagebox.showerror("Error", "Invalid number")
            return

        if not add:
            value = -abs(value)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE members SET points = points + ? WHERE phone=?",
            (value, phone)
        )
        conn.commit()

        cursor.execute(
            "SELECT name, points FROM members WHERE phone=?",
            (phone,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            label_name.config(text=row[0])
            label_points.config(text=row[1])
            messagebox.showinfo("Success", "Points updated")
        else:
            messagebox.showerror("Error", "Member not found")

    tk.Button(win, text="Add Points", command=lambda: update(True)).grid(row=4, column=0, pady=5)
    tk.Button(win, text="Deduct Points", command=lambda: update(False)).grid(row=4, column=1, pady=5)
