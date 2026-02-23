
import tkinter as tk
from database import setup_database
from login import open_login_screen

APP_TITLE = "The Brew Corner — POS CRM"

def center_window(root: tk.Tk, w=960, h=600):
    root.update_idletasks()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

def main():
    root = tk.Tk()
    root.title(APP_TITLE)
    center_window(root, 960, 600)

    setup_database()
    open_login_screen(root)

    root.mainloop()

if __name__ == "__main__":
    main()
