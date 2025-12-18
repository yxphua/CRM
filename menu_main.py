import tkinter as tk

from points import open_points_panel
from pos_system import open_pos_system

def open_menu_main(root):
    from member_menu import open_member_menu
    for w in root.winfo_children():
        w.destroy()

    root.title("Dashboard")

    tk.Label(root, text="The Brew Corner", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Members", width=25,
              command=lambda: open_member_menu(root)).pack(pady=5)

    tk.Button(root, text="Points", width=25,
              command=lambda: open_points_panel(root)).pack(pady=5)

    tk.Button(root, text="POS System", width=25,
              command=lambda: open_pos_system(root)).pack(pady=5)

    tk.Button(root, text="Logout", width=25,
              command=root.destroy).pack(pady=10)
