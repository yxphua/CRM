import tkinter as tk
from database import get_connection

def open_view_member(parent):
    win = tk.Toplevel(parent)
    win.title("View All Members")

    tk.Label(win, text="All Members", font=("Arial", 16)).pack(pady=10)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM members")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tk.Label(win, text=f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}").pack()
