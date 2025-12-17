import tkinter as tk
from database import setup_database
from login import open_login_screen

root = tk.Tk()

setup_database()
open_login_screen(root)

root.mainloop()
