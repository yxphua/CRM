
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import sqlite3
from datetime import datetime

from ui_theme import apply_global_style, make_header, make_center_card

def open_purchase_history(parent: tk.Tk):
    # Rebuild page
    for w in parent.winfo_children():
        w.destroy()

    parent.title("Purchase History")
    apply_global_style(parent)
    make_header(parent, "Purchase History")

    card = make_center_card(parent, width=820)

    # Heading + helper
    ttk.Label(card, text="Find a member’s transactions", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 8)
    )
    ttk.Label(card, text="Enter Member ID and (optionally) a From/To date (YYYY-MM-DD).",
              style="Subheading.TLabel").pack(
        anchor="w", padx=24, pady=(0, 16)
    )

    # Member ID input
    id_row = ttk.Frame(card, style="Card.TFrame")
    id_row.pack(fill="x", padx=24, pady=(8, 8))
    ttk.Label(id_row, text="Member ID").pack(side="left")
    member_id_var = tk.StringVar()
    entry_id = ttk.Entry(id_row, textvariable=member_id_var, width=12)
    entry_id.pack(side="left", padx=(8, 12))

    # Live preview of member (name, points)
    member_preview = ttk.Label(card, text="-", style="Subheading.TLabel")
    member_preview.pack(anchor="w", padx=24, pady=(0, 8))

    # ---- Split date inputs (YYYY-MM-DD) ----
    def make_date_inputs(label_text):
        row = ttk.Frame(card, style="Card.TFrame")
        row.pack(padx=24, pady=2, anchor="w")
        ttk.Label(row, text=label_text).pack(side="left", padx=(0, 8))
        y = ttk.Entry(row, width=6);  y.pack(side="left")
        ttk.Label(row, text="-").pack(side="left", padx=2)
        m = ttk.Entry(row, width=4);  m.pack(side="left")
        ttk.Label(row, text="-").pack(side="left", padx=2)
        d = ttk.Entry(row, width=4);  d.pack(side="left")
        return y, m, d

    entry_from_y, entry_from_m, entry_from_d = make_date_inputs("From (YYYY-MM-DD)")
    entry_to_y,   entry_to_m,   entry_to_d   = make_date_inputs("To (YYYY-MM-DD)")

    def build_date(y, m, d):
        y, m, d = y.get().strip(), m.get().strip(), d.get().strip()
        if not (y and m and d):
            return ""  # empty = no limit
        try:
            dt = datetime(int(y), int(m), int(d))
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", f"Invalid date: {y}-{m}-{d}")
            return None

    # Info label (summary / errors)
    label_info = ttk.Label(card, text="-", style="Subheading.TLabel")
    label_info.pack(anchor="w", padx=24, pady=(6, 8))

    # Table
    table_wrap = ttk.Frame(card, style="Card.TFrame")
    table_wrap.pack(fill="both", expand=True, padx=24, pady=(8, 24))

    columns = ("Amount", "DateTime")
    tree = ttk.Treeview(table_wrap, columns=columns, show="headings")
    tree.heading("Amount", text="Amount (RM)")
    tree.heading("DateTime", text="Date/Time")

    tree.column("Amount", width=140, anchor="center")
    tree.column("DateTime", width=300, anchor="center")

    vs = ttk.Scrollbar(table_wrap, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vs.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vs.grid(row=0, column=1, sticky="ns")
    table_wrap.columnconfigure(0, weight=1)
    table_wrap.rowconfigure(0, weight=1)

    def preview_member():
        """Show name + points when Member ID looks valid."""
        raw = member_id_var.get().strip()
        if not raw.isdigit():
            member_preview.config(text="-")
            return
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT name, points FROM members WHERE MemberId=?", (int(raw),))
                row = cur.fetchone()
            if row:
                member_preview.config(text=f"{row[0]} • Points: {row[1]}")
            else:
                member_preview.config(text="Member not found")
        except sqlite3.Error:
            member_preview.config(text="Database error")

    def load_history():
        raw_id = member_id_var.get().strip()
        if not raw_id.isdigit():
            messagebox.showerror("Error", "Enter a valid numeric Member ID")
            return
        member_id = int(raw_id)

        date_from = build_date(entry_from_y, entry_from_m, entry_from_d)
        date_to   = build_date(entry_to_y, entry_to_m, entry_to_d)
        if date_from is None or date_to is None:
            return  # invalid date input

        clause = []
        params = [member_id]
        if date_from:
            clause.append("datetime >= ?")
            params.append(date_from + " 00:00:00")
        if date_to:
            clause.append("datetime <= ?")
            params.append(date_to + " 23:59:59")
        where_extra = (" AND " + " AND ".join(clause)) if clause else ""

        try:
            with get_connection() as conn:
                cur = conn.cursor()

                # Confirm member exists (and get points for summary)
                cur.execute("SELECT name, points FROM members WHERE MemberId=?", (member_id,))
                member = cur.fetchone()
                if not member:
                    messagebox.showerror("Error", "Member not found")
                    return

                # Fetch transactions in range (latest first)
                cur.execute(
                    f"""
                    SELECT amount, datetime
                    FROM transactions
                    WHERE MemberId=? {where_extra}
                    ORDER BY datetime DESC
                    """,
                    tuple(params)
                )
                rows = cur.fetchall()

            # Refresh table
            for i in tree.get_children():
                tree.delete(i)

            if not rows:
                label_info.config(text=f"{member[0]} — No purchases in range • Points: {member[1]}")
                return

            total = 0.0
            for amt, dt_str in rows:
                try:
                    dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                    dt_fmt = dt_obj.strftime("%d %b %Y, %I:%M %p")
                except Exception:
                    dt_fmt = dt_str
                tree.insert("", tk.END, values=(f"RM {amt:.2f}", dt_fmt))
                total += float(amt)

            label_info.config(
                text=f"{member[0]} — Purchases: {len(rows)} • Total Spent: RM{total:.2f} • Points: {member[1]}"
            )
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Actions
    actions = ttk.Frame(card, style="Card.TFrame")
    actions.pack(fill="x", padx=24, pady=(0, 24))
    ttk.Button(actions, text="Search", style="Accent.TButton", command=load_history).pack(side="right")

    # Events
    entry_id.bind("<Return>", lambda e: preview_member())
    entry_id.bind("<FocusOut>", lambda e: preview_member())
    entry_id.focus_set()
