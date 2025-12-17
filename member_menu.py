import tkinter as tk
from member_add import open_add_member
from member_edit import open_edit_member
from member_delete import open_delete_member
from member_view import open_view_member

def open_member_menu(root):
    from menu_main import open_menu_main
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Member Menu")

    tk.Label(root, text="Member Menu", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Add Member", width=20,
              command=lambda: open_add_member(root)).pack(pady=10)

    tk.Button(root, text="Edit Member", width=20,
              command=lambda: open_edit_member(root)).pack(pady=10)

    tk.Button(root, text="Delete Member", width=20,
              command=lambda: open_delete_member(root)).pack(pady=10)

    tk.Button(root, text="View All Members", width=20,
              command=lambda: open_view_member(root)).pack(pady=10)

    tk.Button(root, text="Back", width=20,
              command=lambda: open_menu_main(root)).pack(pady=20)
