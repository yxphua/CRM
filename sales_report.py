
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import sqlite3
from datetime import datetime

from ui_theme import apply_global_style, make_header, make_center_card

def open_sales_report(parent: tk.Tk):
    # Rebuild page
    for w in parent.winfo_children():
        w.destroy()

    parent.title("Sales Report")
    apply_global_style(parent)
    make_header(parent, "Sales Report")

    card = make_center_card(parent, width=920)

    ttk.Label(card, text="Filter by date range (YYYY-MM-DD)", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 8)
    )
    ttk.Label(card, text="Leave a field empty for no limit.", style="Subheading.TLabel").pack(
        anchor="w", padx=24, pady=(0, 16)
    )

    # ----- Date inputs: split Y/M/D (kept from your design) -----
    def make_date_inputs(label_text):
        row = ttk.Frame(card, style="Card.TFrame")
        row.pack(padx=24, pady=2, anchor="w")
        ttk.Label(row, text=label_text).pack(side="left", padx=(0, 8))
        y = ttk.Entry(row, width=6); y.pack(side="left")
        ttk.Label(row, text="-").pack(side="left", padx=2)
        m = ttk.Entry(row, width=4); m.pack(side="left")
        ttk.Label(row, text="-").pack(side="left", padx=2)
        d = ttk.Entry(row, width=4); d.pack(side="left")
        return y, m, d

    entry_from_y, entry_from_m, entry_from_d = make_date_inputs("From (YYYY-MM-DD)")
    entry_to_y,   entry_to_m,   entry_to_d   = make_date_inputs("To (YYYY-MM-DD)")

    def build_date(y, m, d):
        y, m, d = y.get().strip(), m.get().strip(), d.get().strip()
        if not (y and m and d):
            return ""  # empty = no bound
        try:
            dt = datetime(int(y), int(m), int(d))
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", f"Invalid date: {y}-{m}-{d}")
            return None

    # Summary
    label_summary = ttk.Label(card, text="-", style="Subheading.TLabel")
    label_summary.pack(anchor="w", padx=24, pady=(8, 8))

    # Table
    table_wrap = ttk.Frame(card, style="Card.TFrame")
    table_wrap.pack(fill="both", expand=True, padx=24, pady=(8, 24))

    columns = ("TransId", "MemberId", "Member Name", "Amount", "DateTime")
    tree = ttk.Treeview(table_wrap, columns=columns, show="headings")
    for col, title, w, anchor in [
        ("TransId", "Trans ID", 100, "center"),
        ("MemberId", "Member ID", 110, "center"),
        ("Member Name", "Member Name", 300, "w"),
        ("Amount", "Amount (RM)", 140, "center"),
        ("DateTime", "Date/Time", 230, "center"),
    ]:
        tree.heading(col, text=title)
        tree.column(col, width=w, anchor=anchor)

    vs = ttk.Scrollbar(table_wrap, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vs.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vs.grid(row=0, column=1, sticky="ns")
    table_wrap.columnconfigure(0, weight=1)
    table_wrap.rowconfigure(0, weight=1)

    def load_sales_report():
        date_from = build_date(entry_from_y, entry_from_m, entry_from_d)
        date_to   = build_date(entry_to_y, entry_to_m, entry_to_d)
        if date_from is None or date_to is None:
            return  # invalid date

        where = []
        params = []
        if date_from:
            where.append("t.datetime >= ?")
            params.append(date_from + " 00:00:00")
        if date_to:
            where.append("t.datetime <= ?")
            params.append(date_to + " 23:59:59")
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                query = f"""
                    SELECT t.TransId, t.MemberId, m.name, t.amount, t.datetime
                    FROM transactions t
                    LEFT JOIN members m ON t.MemberId = m.MemberId
                    {where_sql}
                    ORDER BY t.datetime DESC
                """
                cur.execute(query, tuple(params))
                rows = cur.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
            return

        # Refresh table
        for i in tree.get_children():
            tree.delete(i)

        if not rows:
            label_summary.config(text="No sales found in the specified date range")
            return

        total = 0.0
        for trans_id, member_id, member_name, amount, dt in rows:
            # Format datetime nicely (fallback to raw)
            try:
                dt_obj = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                dt_str = dt_obj.strftime("%d %b %Y, %I:%M %p")
            except Exception:
                dt_str = dt

            # Show Guest when no member
            if member_id is None:
                display_member_id = "-"
                display_member = "Guest"
            else:
                display_member_id = member_id
                display_member = member_name if member_name else f"ID: {member_id}"

            tree.insert(
                "", tk.END,
                values=(trans_id, display_member_id, display_member, f"{amount:.2f}", dt_str)
            )
            total += float(amount)

        label_summary.config(
            text=f"Total Transactions: {len(rows)} • Total Sales: RM{total:.2f}"
        )

    # Action button
    ttk.Button(card, text="Generate Report", style="Accent.TButton",
               command=load_sales_report).pack(padx=24, pady=(0, 24), anchor="e")
