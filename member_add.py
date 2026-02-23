
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import sqlite3
from ui_theme import apply_global_style, make_header, make_center_card

def open_add_member(parent: tk.Tk):
    # Clear and rebuild page inside parent window
    for w in parent.winfo_children():
        w.destroy()

    parent.title("Add Member")
    apply_global_style(parent)
    make_header(parent, "Add Member")

    card = make_center_card(parent, width=640)

    ttk.Label(card, text="Create a new member", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 4)
    )
    ttk.Label(
        card,
        text="Fill in name and phone number (9–11 digits).",
        style="Subheading.TLabel",
    ).pack(anchor="w", padx=24, pady=(0, 16))

    # Form
    form = ttk.Frame(card, style="Card.TFrame")
    form.pack(fill="x", padx=24, pady=(8, 16))
    form.columnconfigure(1, weight=1)

    ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w", pady=(0, 6))
    entry_name = ttk.Entry(form)
    entry_name.grid(row=0, column=1, sticky="ew", pady=(0, 12))

    ttk.Label(form, text="Phone Number").grid(row=1, column=0, sticky="w", pady=(0, 6))
    entry_phone = ttk.Entry(form)
    entry_phone.grid(row=1, column=1, sticky="ew", pady=(0, 12))

    # Email (optional) — added
    ttk.Label(form, text="Email (optional)").grid(row=2, column=0, sticky="w", pady=(0, 6))
    entry_email = ttk.Entry(form)
    entry_email.grid(row=2, column=1, sticky="ew", pady=(0, 12))

    # Actions
    actions = ttk.Frame(card, style="Card.TFrame")
    actions.pack(fill="x", padx=24, pady=(0, 8))

    add_btn = ttk.Button(actions, text="Add Member", style="Accent.TButton")
    add_btn.pack(anchor="e")

    # Member list (Treeview) — now includes Email column
    table_wrap = ttk.Frame(card, style="Card.TFrame")
    table_wrap.pack(fill="both", expand=True, padx=24, pady=(8, 24))

    cols = ("MemberId", "Name", "Phone", "Email")  # ← Email added
    table = ttk.Treeview(table_wrap, columns=cols, show="headings", height=10)

    table.heading("MemberId", text="ID")
    table.heading("Name", text="Name")
    table.heading("Phone", text="Phone")
    table.heading("Email", text="Email")  # ← Email header

    table.column("MemberId", width=90, anchor="center")
    table.column("Name", width=260, anchor="w")
    table.column("Phone", width=200, anchor="center")
    table.column("Email", width=260, anchor="w")  # ← Email width

    vs = ttk.Scrollbar(table_wrap, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=vs.set)

    table.grid(row=0, column=0, sticky="nsew")
    vs.grid(row=0, column=1, sticky="ns")

    table_wrap.columnconfigure(0, weight=1)
    table_wrap.rowconfigure(0, weight=1)

    def load_members():
        table.delete(*table.get_children())
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                # ← SELECT now pulls email
                cur.execute(
                    "SELECT MemberId, name, phone, email FROM members ORDER BY MemberId DESC"
                )
                for mid, name, phone, email in cur.fetchall():
                    table.insert("", "end", values=(mid, name, phone, email))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def add():
        # Strip whitespace
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        email = entry_email.get().strip()

        if not name or not phone:
            messagebox.showwarning("Error", "All fields required")
            return

        if not phone.isdigit():
            messagebox.showerror("Error", "Phone must contain only digits")
            return

        if len(phone) < 9 or len(phone) > 11:
            messagebox.showerror("Error", "Phone must be 9–11 digits long")
            return

        # basic email validation if provided
        if email and "@" not in email:
            messagebox.showerror("Error", "Enter a valid email or leave it blank")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                # ← INSERT now includes email (None when blank)
                cur.execute(
                    "INSERT INTO members (name, phone, email) VALUES (?, ?, ?)",
                    (name, phone, email if email else None)
                )
                messagebox.showinfo("Success", "Member successfully added")

                entry_name.delete(0, tk.END)
                entry_phone.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_name.focus_set()

                load_members()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Member already exists (phone in use)")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    add_btn.configure(command=add)
    entry_name.focus_set()
    load_members()
