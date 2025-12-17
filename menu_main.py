import tkinter as tk
from points import open_points_panel

def open_menu_main(root):
    from member_menu import open_member_menu
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Dashboard")
    tk.Label(root, text="The Brew Corner", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Member", width=20,
              command=lambda: open_member_menu(root)).pack(pady=10)

    tk.Button(root, text="Points", width=20,
              command=lambda: open_points_panel(root)).pack(pady=10)

    tk.Button(root, text="Logout", width=20,
              command=lambda: root.destroy()).pack(pady=10)
