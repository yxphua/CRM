

import tkinter as tk
from tkinter import ttk

from member_add import open_add_member
from member_edit import open_edit_member
from member_delete import open_delete_member
from member_view import open_view_member

from ui_theme import apply_global_style, make_header, make_center_card

def open_member_menu(parent: tk.Tk):
    # Import inside function to avoid circular import issues
    from menu_main import open_menu_main

    # Clear and rebuild page
    for w in parent.winfo_children():
        w.destroy()

    parent.title("Member Menu")
    apply_global_style(parent)
    make_header(parent, "Members")

    card = make_center_card(parent, width=600)

    ttk.Label(card, text="Manage members", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 8)
    )
    ttk.Label(card, text="Add, edit, delete, or view all members.",
              style="Subheading.TLabel").pack(
        anchor="w", padx=24, pady=(0, 16)
    )

    grid = ttk.Frame(card, style="Card.TFrame")
    grid.pack(fill="x", padx=24, pady=(8, 16))

    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)

    def show_page(page_func):
        """Render a subpage full-screen, with a small back button under the header."""
        for w in parent.winfo_children():
            w.destroy()
        page_func(parent)
        # Small sticky back button below the header on the left
        back_bar = ttk.Frame(parent)
        back_bar.place(x=16, y=64)
        ttk.Button(back_bar, text="← Back to Member Menu",
                   command=lambda: open_member_menu(parent)).pack()

    ttk.Button(
        grid, text="➕ Add Member", style="Accent.TButton",
        command=lambda: show_page(open_add_member)
    ).grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=(0, 12))

    ttk.Button(
        grid, text="✏️ Edit Member",
        command=lambda: show_page(open_edit_member)
    ).grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 12))

    ttk.Button(
        grid, text="🗑️ Delete Member", style="Danger.TButton",
        command=lambda: show_page(open_delete_member)
    ).grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(0, 12))

    ttk.Button(
        grid, text="👀 View All Members",
        command=lambda: show_page(open_view_member)
    ).grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 12))

    # ===== New: Back to Dashboard button =====
    ttk.Button(
        card, text="← Back to Dashboard",
        command=lambda: open_menu_main(parent)
    ).pack(padx=24, pady=(8, 24), anchor="w")
