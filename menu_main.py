
import tkinter as tk
from tkinter import ttk, messagebox

# If files are in the same folder:
from points import open_points_panel
from pos_system import open_pos_system
from member_menu import open_member_menu
from purchase_history import open_purchase_history
from sales_report import open_sales_report  

from ui_theme import apply_global_style, make_header, make_center_card

def open_menu_main(root: tk.Tk):
    # Clear existing UI
    for w in root.winfo_children():
        w.destroy()

    root.title("Dashboard")
    apply_global_style(root)
    make_header(root, "The Brew Corner — Dashboard")

    card = make_center_card(root, width=680)

    ttk.Label(card, text="Quick actions", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 8)
    )
    ttk.Label(
        card,
        text="Manage members, view points, perform checkout, and run reports.",
        style="Subheading.TLabel",
    ).pack(anchor="w", padx=24, pady=(0, 16))

    grid = ttk.Frame(card, style="Card.TFrame")
    grid.pack(fill="x", padx=24, pady=(8, 24))

    # 2-column layout
    for c in (0, 1):
        grid.columnconfigure(c, weight=1)

    def show_page(page_func):
        """Render a subpage full-screen, with a small back button under the header."""
        for w in root.winfo_children():
            w.destroy()
        page_func(root)
        back_bar = ttk.Frame(root)
        back_bar.place(x=16, y=64)  # just under header
        ttk.Button(back_bar, text="← Back to Dashboard",
                   command=lambda: open_menu_main(root)).pack()

    # Row 0
    ttk.Button(
        grid,
        text="👥 Members",
        style="Accent.TButton",
        command=lambda: open_member_menu(root),
    ).grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=(0, 12))

    ttk.Button(
        grid,
        text="💳 Points",
        command=lambda: show_page(open_points_panel),
    ).grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 12))

    # Row 1
    ttk.Button(
        grid,
        text="🧾 POS System",
        command=lambda: show_page(open_pos_system),
    ).grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(0, 12))

    ttk.Button(
        grid,
        text="📜 Purchase History",
        command=lambda: show_page(open_purchase_history),
    ).grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 12))

    # Row 2
    ttk.Button(
        grid,
        text="📈 Sales Report",
        command=lambda: show_page(open_sales_report),
    ).grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 12))

    # Logout
    def confirm_logout():
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            root.destroy()

    ttk.Button(
        card, text="⏻ Logout", style="Danger.TButton", command=confirm_logout
    ).pack(padx=24, pady=(0, 24), anchor="w")
