import tkinter as tk
from tkinter import messagebox
from database import get_connection
from datetime import datetime

def open_pos_system(parent):
    win = tk.Toplevel(parent)
    win.title("POS System")

    tk.Label(win, text="Customer Name").grid(row=0, column=0)
    name = tk.Entry(win)
    name.grid(row=0, column=1)

    tk.Label(win, text="Phone").grid(row=1, column=0)
    phone = tk.Entry(win)
    phone.grid(row=1, column=1)

    tk.Label(win, text="Amount (RM)").grid(row=2, column=0)
    amount = tk.Entry(win)
    amount.grid(row=2, column=1)

    def submit():
        if not name.get() or not phone.get() or not amount.get():
            messagebox.showerror("Error", "All fields required")
            return

        try:
            amt = float(amount.get())
        except:
            messagebox.showerror("Error", "Invalid amount")
            return

        conn = get_connection()
        cur = conn.cursor()

        # AUTO CREATE MEMBER IF NOT EXISTS
        cur.execute("SELECT id FROM members WHERE phone=?", (phone.get(),))
        member = cur.fetchone()

        if not member:
            cur.execute(
                "INSERT INTO members (name, phone, points) VALUES (?, ?, ?)",
                (name.get(), phone.get(), int(amt))
            )
        else:
            cur.execute(
                "UPDATE members SET points = points + ? WHERE phone=?",
                (int(amt), phone.get())
            )

        cur.execute(
            "INSERT INTO transactions (phone, amount, datetime) VALUES (?, ?, ?)",
            (phone.get(), amt, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Transaction saved & points updated")

    tk.Button(win, text="Submit Transaction",
              command=submit).grid(row=3, column=0, columnspan=2, pady=10)
