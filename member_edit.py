
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import sqlite3
from ui_theme import apply_global_style, make_header, make_center_card

def open_edit_member(parent: tk.Tk):
    for w in parent.winfo_children():
        w.destroy()

    parent.title("Edit Member")
    apply_global_style(parent)
    make_header(parent, "Edit Member")

    card = make_center_card(parent, width=520)

    ttk.Label(card, text="Update member details", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 8)
    )
    ttk.Label(
        card,
        text="Enter the Member ID and new contact info.",
        style="Subheading.TLabel",
    ).pack(anchor="w", padx=24, pady=(0, 16))

    form = ttk.Frame(card, style="Card.TFrame")
    form.pack(fill="x", padx=24, pady=(8, 24))
    form.columnconfigure(1, weight=1)

    ttk.Label(form, text="Member ID").grid(row=0, column=0, sticky="w", pady=(0, 6))
    entry_id = ttk.Entry(form)
    entry_id.grid(row=0, column=1, sticky="ew", pady=(0, 12))

    ttk.Label(form, text="New Name").grid(row=1, column=0, sticky="w", pady=(0, 6))
    entry_name = ttk.Entry(form)
    entry_name.grid(row=1, column=1, sticky="ew", pady=(0, 12))

    ttk.Label(form, text="New Phone").grid(row=2, column=0, sticky="w", pady=(0, 6))
    entry_phone = ttk.Entry(form)
    entry_phone.grid(row=2, column=1, sticky="ew", pady=(0, 12))

    # NEW: Email (optional)
    ttk.Label(form, text="New Email (optional)").grid(row=3, column=0, sticky="w", pady=(0, 6))
    entry_email = ttk.Entry(form)
    entry_email.grid(row=3, column=1, sticky="ew", pady=(0, 12))

    def update_member():
        member_id = entry_id.get().strip()
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        email = entry_email.get().strip()  # 👈 NEW

        if not member_id or not name or not phone:
            messagebox.showerror("Error", "Enter all fields")
            return

        if not member_id.isdigit():
            messagebox.showerror("Error", "Member ID must be a number")
            return

        if not phone.isdigit() or len(phone) < 9 or len(phone) > 11:
            messagebox.showerror(
                "Error", "Phone must be 9–11 digits and contain only numbers"
            )
            return

        # NEW: basic email validation if provided
        if email and "@" not in email:
            messagebox.showerror("Error", "Enter a valid email or leave it blank")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                # NEW: include email (None if blank)
                cur.execute(
                    "UPDATE members SET name=?, phone=?, email=? WHERE MemberId=?",
                    (name, phone, email if email else None, int(member_id)),
                )

                if cur.rowcount == 0:
                    messagebox.showerror("Error", "Member not found")
                else:
                    messagebox.showinfo(
                        "Success", "Member info updated successfully"
                    )
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    ttk.Button(
        card, text="Update", style="Accent.TButton", command=update_member
    ).pack(padx=24, pady=(0, 24), fill="x")

    entry_id.focus_set()
