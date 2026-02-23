
import tkinter as tk
from tkinter import ttk

# --- Design tokens ---
PRIMARY = "#2563EB"
BG = "#F3F4F6"
TEXT = "#111827"
MUTED = "#6B7280"
ERROR = "#EF4444"

def apply_global_style(root: tk.Tk | tk.Toplevel):
    """Apply a consistent light theme across the app."""
    root.configure(bg=BG)
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Base font & label colors
    style.configure(".", font=("Segoe UI", 11))
    style.configure("TLabel", background="white", foreground=TEXT)

    # Buttons
    style.configure("TButton", padding=8)
    style.configure("Accent.TButton", foreground="white", background=PRIMARY)
    style.map(
        "Accent.TButton",
        foreground=[("disabled", "#dddddd"), ("!disabled", "white")],
        background=[("active", "#1D4ED8"), ("!active", PRIMARY)],
    )
    style.configure("Danger.TButton", foreground="white", background=ERROR, padding=8)
    style.map(
        "Danger.TButton",
        background=[("active", "#DC2626"), ("!active", ERROR)],
    )

    # Cards & headings
    style.configure("Card.TFrame", background="white", relief="flat")
    style.configure("Heading.TLabel", font=("Segoe UI", 18, "bold"), background="white", foreground=TEXT)
    style.configure("Subheading.TLabel", font=("Segoe UI", 12), background="white", foreground=MUTED)

    # Tables (Treeview)
    style.configure(
        "Treeview",
        background="white",
        fieldbackground="white",
        foreground=TEXT,
        borderwidth=0,
        rowheight=26,
    )
    style.configure(
        "Treeview.Heading",
        background="white",
        foreground=TEXT,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
    )
    style.map("Treeview", background=[("selected", "#E5F0FF")], foreground=[("selected", "#0F172A")])
    style.map("Treeview.Heading", relief=[("active", "flat"), ("pressed", "flat")])

    # Scrollbar (subtle)
    style.configure("Vertical.TScrollbar", background="white")

def make_header(root, title: str):
    """Top bar header with app title."""
    header = tk.Frame(root, bg="white", height=56)
    header.pack(side="top", fill="x")
    tk.Label(
        header,
        text=title,
        bg="white",
        fg=TEXT,
        font=("Segoe UI", 16, "bold"),
    ).pack(side="left", padx=16, pady=8)
    return header

def make_center_card(root, width=520):
    """Create a centered 'card' container with fixed content width."""
    container = tk.Frame(root, bg=BG)
    container.pack(fill="both", expand=True)

    card_wrap = tk.Frame(container, bg=BG)
    card_wrap.pack(expand=True)

    card = ttk.Frame(card_wrap, style="Card.TFrame")
    card.pack(padx=24, pady=24)

    # Spacer ensures a consistent content width
    spacer = tk.Frame(card, width=width, height=0, bg="white")
    spacer.pack()
    return card