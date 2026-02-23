
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import sqlite3

from ui_theme import apply_global_style, make_header, make_center_card

def open_delete_member(parent: tk.Tk):
    # full-page render
    for w in parent.winfo_children():
        w.destroy()

    parent.title("Delete Member")
    apply_global_style(parent)
    make_header(parent, "Delete Member")

    card = make_center_card(parent, width=520)

    ttk.Label(card, text="Remove a member by ID", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 8)
    )
    ttk.Label(card, text="This action cannot be undone.", style="Subheading.TLabel").pack(
        anchor="w", padx=24, pady=(0, 16)
    )

    form = ttk.Frame(card, style="Card.TFrame")
    form.pack(fill="x", padx=24, pady=(8, 24))
    form.columnconfigure(1, weight=1)

    ttk.Label(form, text="Member ID").grid(row=0, column=0, sticky="w", pady=(0, 6))
    entry_id = ttk.Entry(form)                # <-- defined here
    entry_id.grid(row=0, column=1, sticky="ew", pady=(0, 12))

    def delete_member():                      # <-- nested; sees entry_id
        raw = entry_id.get().strip()
        if not raw:
            messagebox.showerror("Error", "Enter Member ID")
            return
        if not raw.isdigit():
            messagebox.showerror("Error", "Member ID must be a number")
            return

        member_id = int(raw)

        try:
            # 1) fetch for confirmation
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT name, phone FROM members WHERE MemberId=?", (member_id,))
                row = cur.fetchone()

            if not row:
                messagebox.showerror("Error", "Member ID not found")
                return

            name, phone = row
            if not messagebox.askyesno(
                "Confirm Deletion",
                f"Delete Member?\n\nID: {member_id}\nName: {name}\nPhone: {phone}"
            ):
                return

            # 2) delete
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM members WHERE MemberId=?", (member_id,))
                conn.commit()

            messagebox.showinfo("Success", "Member deleted successfully")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    ttk.Button(card, text="Delete", style="Danger.TButton", command=delete_member).pack(
        padx=24, pady=(0, 24), fill="x"
    )
    entry_id.focus_set()
