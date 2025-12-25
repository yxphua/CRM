import tkinter as tk
from tkinter import messagebox
from database import get_connection

def open_purchase_history(parent):
    win = tk.Toplevel(parent)
    win.title("Purchase History")

    tk.Label(win, text="Member ID").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    label_info = tk.Label(win, text="")
    label_info.pack(pady=5)

    listbox = tk.Listbox(win, width=50)
    listbox.pack(pady=10)

    def load_history():
        member_id = entry_id.get()

        if not member_id:
            messagebox.showerror("Error", "Enter Member ID")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM members WHERE MemberId=?",
            (member_id,)
        )
        member = cursor.fetchone()

        if not member:
            conn.close()
            messagebox.showerror("Error", "Member not found")
            return

        cursor.execute(
            """
            SELECT amount, datetime
            FROM transactions
            WHERE MemberId=?
            ORDER BY datetime DESC
            """,
            (member_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        listbox.delete(0, tk.END)

        if not rows:
            label_info.config(text=f"{member[0]} | No purchases")
            return

        for amt, dt in rows:
            listbox.insert(tk.END, f"RM {amt:.2f} | {dt}")

        label_info.config(
            text=f"{member[0]} | Total Purchases: {len(rows)}"
        )

    tk.Button(win, text="Search", command=load_history).pack(pady=5)
