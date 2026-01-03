import tkinter as tk
from tkinter import messagebox
from database import get_connection
from datetime import datetime

def open_pos_system(parent):
    win = tk.Toplevel(parent)
    win.title("POS System")

    tk.Label(win, text="Customer Name").grid(row=0, column=0)
    entry_name = tk.Entry(win)
    entry_name.grid(row=0, column=1)

    tk.Label(win, text="Phone").grid(row=1, column=0)
    entry_phone = tk.Entry(win)
    entry_phone.grid(row=1, column=1)

    tk.Label(win, text="Amount (RM)").grid(row=2, column=0)
    entry_amount = tk.Entry(win)
    entry_amount.grid(row=2, column=1)

    def submit():
        name = entry_name.get()
        phone = entry_phone.get()

        try:
            amt = float(entry_amount.get())
        except:
            messagebox.showerror("Error", "Invalid amount")
            return

        if not name or not phone:
            messagebox.showerror("Error", "All fields required")
            return

        conn = get_connection()
        cur = conn.cursor()

        # Find member by phone
        cur.execute("SELECT MemberId FROM members WHERE phone=?", (phone,))
        member = cur.fetchone()

        if not member:
            cur.execute(
                "INSERT INTO members (name, phone, points) VALUES (?, ?, ?)",
                (name, phone, int(amt))
            )
            member_id = cur.lastrowid
        else:
            member_id = member[0]
            cur.execute(
                "UPDATE members SET points = points + ? WHERE MemberId=?",
                (int(amt), member_id)
            )

        # Save transaction using MemberId
        cur.execute(
            "INSERT INTO transactions (MemberId, amount, datetime) VALUES (?, ?, ?)",
            (member_id, amt, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Transaction saved")

    tk.Button(win, text="Submit", command=submit)\
        .grid(row=3, column=0, columnspan=2, pady=10)
