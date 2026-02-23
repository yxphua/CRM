
# points.py (ttk styled, prevents negative totals, full-page)
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import sqlite3

from ui_theme import apply_global_style, make_header, make_center_card

def open_points_panel(parent: tk.Tk):
    # Full-page render
    for w in parent.winfo_children():
        w.destroy()

    parent.title("Points Panel")
    apply_global_style(parent)
    make_header(parent, "Points Panel")

    card = make_center_card(parent, width=640)

    ttk.Label(card, text="Lookup & adjust loyalty points", style="Heading.TLabel").pack(anchor="w", padx=24, pady=(24, 8))
    ttk.Label(card, text="Search by phone, then add or deduct points.", style="Subheading.TLabel").pack(anchor="w", padx=24, pady=(0, 16))

    # Search row
    row_search = ttk.Frame(card, style="Card.TFrame")
    row_search.pack(fill="x", padx=24, pady=(8, 16))
    ttk.Label(row_search, text="Phone Number").pack(side="left")
    phone_var = tk.StringVar()
    entry_phone = ttk.Entry(row_search, textvariable=phone_var, width=22)
    entry_phone.pack(side="left", padx=(8, 12))
    ttk.Button(row_search, text="Search", command=lambda: search()).pack(side="left")

    # Info grid
    info = ttk.Frame(card, style="Card.TFrame")
    info.pack(fill="x", padx=24, pady=(0, 16))
    ttk.Label(info, text="Name").grid(row=0, column=0, sticky="w", pady=(0, 6))
    label_name = ttk.Label(info, text="-"); label_name.grid(row=0, column=1, sticky="w", pady=(0, 6))
    ttk.Label(info, text="Points").grid(row=1, column=0, sticky="w")
    label_points = ttk.Label(info, text="-"); label_points.grid(row=1, column=1, sticky="w")
    info.columnconfigure(1, weight=1)

    # Change points
    changer = ttk.Frame(card, style="Card.TFrame")
    changer.pack(fill="x", padx=24, pady=(0, 24))
    ttk.Label(changer, text="Change Points").grid(row=0, column=0, sticky="w", pady=(0, 6))
    change_var = tk.StringVar()
    entry_change = ttk.Entry(changer, textvariable=change_var, width=12)
    entry_change.grid(row=0, column=1, sticky="w", padx=(8, 12))

    ttk.Button(changer, text="Add Points", style="Accent.TButton", command=lambda: update(True)).grid(row=1, column=0, sticky="w", pady=(8, 0))
    ttk.Button(changer, text="Deduct Points", style="Danger.TButton", command=lambda: update(False)).grid(row=1, column=1, sticky="w", pady=(8, 0))

    def search():
        phone = phone_var.get().strip()
        if not phone:
            messagebox.showerror("Error", "Enter phone number")
            return
        if not phone.isdigit() or len(phone) < 9 or len(phone) > 11:
            messagebox.showerror("Error", "Phone must be 9–11 digits and contain only numbers")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT name, points FROM members WHERE phone=?", (phone,))
                row = cur.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
            return

        if row:
            label_name.config(text=row[0])
            label_points.config(text=str(row[1]))
        else:
            label_name.config(text="Not found")
            label_points.config(text="-")
            messagebox.showerror("Error", "Member not found")

    def update(add=True):
        phone = phone_var.get().strip()
        val = change_var.get().strip()
        if not phone:
            messagebox.showerror("Error", "Search member first")
            return
        try:
            delta = int(val)
            if delta <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a positive integer")
            return
        if not add:
            delta = -delta

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT name, points FROM members WHERE phone=?", (phone,))
                row = cur.fetchone()
                if not row:
                    messagebox.showerror("Error", "Member not found")
                    return
                name, current = row
                new_points = current + delta
                if new_points < 0:
                    messagebox.showerror("Error", "Cannot deduct below 0 points")
                    return
                cur.execute("UPDATE members SET points=? WHERE phone=?", (new_points, phone))
                conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
            return

        label_name.config(text=name)
        label_points.config(text=str(new_points))
        entry_change.delete(0, tk.END)
        messagebox.showinfo("Success", "Points updated")

    entry_phone.focus_set()
