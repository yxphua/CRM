
import tkinter as tk
from tkinter import ttk
from database import get_connection
from ui_theme import apply_global_style, make_header, make_center_card


def open_view_member(parent: tk.Tk):
    # Rebuild page
    for w in parent.winfo_children():
        w.destroy()

    parent.title("View All Members")
    apply_global_style(parent)
    make_header(parent, "All Members")

    card = make_center_card(parent, width=800)

    ttk.Label(card, text="Member directory", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 8)
    )
    ttk.Label(
        card,
        text="Search by name or phone. Click column headers to sort.",
        style="Subheading.TLabel",
    ).pack(anchor="w", padx=24, pady=(0, 16))

    # Search bar
    search_row = ttk.Frame(card, style="Card.TFrame")
    search_row.pack(fill="x", padx=24, pady=(8, 12))

    ttk.Label(search_row, text="Search").pack(side="left")
    search_var = tk.StringVar()
    ttk.Entry(search_row, textvariable=search_var, width=30).pack(
        side="left", padx=(8, 12)
    )
    ttk.Button(
        search_row, text="Clear", command=lambda: (search_var.set(""), load_members())
    ).pack(side="left")

    # Table
    table_wrap = ttk.Frame(card, style="Card.TFrame")
    table_wrap.pack(fill="both", expand=True, padx=24, pady=(8, 24))

    columns = ("MemberId", "Name", "Phone", "Email")
    tree = ttk.Treeview(table_wrap, columns=columns, show="headings")

    tree.heading("MemberId", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Email", text="Email") 

    tree.column("MemberId", width=80, anchor="center")
    tree.column("Name", width=360, anchor="w")
    tree.column("Phone", width=200, anchor="center")
    tree.column("Email", width=260, anchor="w") 

    vs = ttk.Scrollbar(table_wrap, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vs.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vs.grid(row=0, column=1, sticky="ns")

    table_wrap.columnconfigure(0, weight=1)
    table_wrap.rowconfigure(0, weight=1)

    info_label = ttk.Label(card, text="-", style="Subheading.TLabel")
    info_label.pack(anchor="w", padx=24, pady=(0, 8))

    # Data cache (for search + sort)
    data = []
    sort_state = {"MemberId": True, "Name": True, "Phone": True, "Email": True}

    def load_members(filter_text=""):
        tree.delete(*tree.get_children())
        nonlocal data

        with get_connection() as conn:
            cur = conn.cursor()

            if filter_text:
                cur.execute(
                    "SELECT MemberId, name, phone, email FROM members "
                    "WHERE TRIM(name) LIKE ? OR phone LIKE ?",
                    (f"%{filter_text}%", f"%{filter_text}%"),
                )
            else:
                cur.execute("SELECT MemberId, name, phone, email FROM members")

            data = cur.fetchall()

            if not data:
                info_label.config(text="No members found")
                return

            for row in data:
                tree.insert("", tk.END, values=row)  # now 4 fields

            info_label.config(text=f"Total members: {len(data)}")

    def apply_filter(*_):
        load_members(search_var.get().strip())

    def sort_by(col):
        key_funcs = {
            "MemberId": lambda r: int(r[0]),
            "Name": lambda r: r[1].lower(),
            "Phone": lambda r: r[2],
            "Email": lambda r: [3].lower(),
        }

        reverse = sort_state[col]
        sort_state[col] = not reverse

        sorted_rows = sorted(data, key=key_funcs[col], reverse=reverse)

        tree.delete(*tree.get_children())

        for r in sorted_rows:
            if (
                not search_var.get().strip()
                or search_var.get().strip().lower() in r[1].lower()
                or search_var.get().strip() in r[2]
                or (r[3] and search_var.get().strip().lower() in r[3].lower())
            ):
                tree.insert("", tk.END, values=r)

    tree.heading("MemberId", text="ID", command=lambda: sort_by("MemberId"))
    tree.heading("Name", text="Name", command=lambda: sort_by("Name"))
    tree.heading("Phone", text="Phone", command=lambda: sort_by("Phone"))
    tree.heading("Email",    text="Email",command=lambda: sort_by("Email"))

    search_var.trace_add("write", apply_filter)
