import tkinter as tk
from tkinter import ttk
from database import get_connection

def open_view_member(parent):
    win = tk.Toplevel(parent)
    win.title("View All Members")

    tk.Label(win, text="All Members", font=("Arial", 16)).pack(pady=10)

    # Frame to hold table + scrollbar
    frame = tk.Frame(win)
    frame.pack(pady=10, fill="both", expand=True)

    # Create Treeview with columns
    columns = ("MemberId", "Name", "Phone")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Define headings
    tree.heading("MemberId", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")

    # Set column widths
    tree.column("MemberId", width=50, anchor="center")
    tree.column("Name", width=150, anchor="w")
    tree.column("Phone", width=120, anchor="center")

    # Attach vertical scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # Pack table and scrollbar side by side
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load data from database
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MemberId, name, phone FROM members")
            rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)
    except Exception as e:
        tk.Label(win, text=f"Error loading members: {e}", fg="red").pack()
