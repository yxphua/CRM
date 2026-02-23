
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from datetime import datetime
import sqlite3

from ui_theme import apply_global_style, make_header, make_center_card

def open_pos_system(parent: tk.Tk):
    # Full-page render
    for w in parent.winfo_children():
        w.destroy()

    parent.title("POS System")
    apply_global_style(parent)
    make_header(parent, "POS Checkout")

    card = make_center_card(parent, width=760)

    ttk.Label(card, text="Record a sale", style="Heading.TLabel").pack(
        anchor="w", padx=24, pady=(24, 8)
    )
    ttk.Label(card, text="Enter phone to fetch member (or leave blank for guest). "
                         "Apply points-for-discount, then confirm.",
              style="Subheading.TLabel").pack(
        anchor="w", padx=24, pady=(0, 16)
    )

    # Form grid
    form = ttk.Frame(card, style="Card.TFrame")
    form.pack(fill="x", padx=24, pady=(8, 16))
    for c in range(3):
        form.columnconfigure(c, weight=1)

    ttk.Label(form, text="Phone").grid(row=0, column=0, sticky="w", pady=(0, 6))
    entry_phone = ttk.Entry(form)
    entry_phone.grid(row=0, column=1, sticky="ew", pady=(0, 12))

    ttk.Label(form, text="Amount (RM)").grid(row=1, column=0, sticky="w", pady=(0, 6))
    entry_amount = ttk.Entry(form)
    entry_amount.grid(row=1, column=1, sticky="ew", pady=(0, 12))

    # Member details (read-only labels)
    ttk.Label(form, text="Customer Name").grid(row=2, column=0, sticky="w", pady=(0, 6))
    label_name = ttk.Label(form, text="-")
    label_name.grid(row=2, column=1, sticky="w", pady=(0, 12))

    ttk.Label(form, text="Current Points").grid(row=3, column=0, sticky="w", pady=(0, 6))
    label_points = ttk.Label(form, text="-")
    label_points.grid(row=3, column=1, sticky="w", pady=(0, 12))

    # Discount buttons row
    disc_row = ttk.Frame(card, style="Card.TFrame")
    disc_row.pack(fill="x", padx=24, pady=(0, 12))
    btn_5 = ttk.Button(disc_row, text="100 pts → RM5 off", state="disabled")
    btn_10 = ttk.Button(disc_row, text="200 pts → RM10 off", state="disabled")
    btn_25 = ttk.Button(disc_row, text="400 pts → RM25 off", state="disabled")
    btn_5.pack(side="left")
    btn_10.pack(side="left", padx=8)
    btn_25.pack(side="left")

    # Totals/preview
    preview = ttk.Frame(card, style="Card.TFrame")
    preview.pack(fill="x", padx=24, pady=(0, 24))
    ttk.Label(preview, text="Final Amount (RM)").grid(row=0, column=0, sticky="w", pady=(0, 6))
    label_final = ttk.Label(preview, text="-"); label_final.grid(row=0, column=1, sticky="w", pady=(0, 6))
    ttk.Label(preview, text="Points After Transaction").grid(row=1, column=0, sticky="w")
    label_future_points = ttk.Label(preview, text="-"); label_future_points.grid(row=1, column=1, sticky="w")

    # State
    applied_discount = {"value": 0, "points": 0}
    current_points = 0
    current_member_id = None

    def check_customer():
        """Fetch customer by phone and enable discounts based on points."""
        nonlocal current_points, current_member_id
        phone = entry_phone.get().strip()
        if not phone:
            # Reset when phone removed
            label_name.config(text="-")
            label_points.config(text="-")
            for b in (btn_5, btn_10, btn_25):
                b.state(["disabled"])
            current_points = 0
            current_member_id = None
            update_final_amount()
            return
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT MemberId, name, points FROM members WHERE phone=?", (phone,))
                row = cur.fetchone()
            if row:
                member_id, name, pts = row
                label_name.config(text=name)
                label_points.config(text=str(pts))
                btn_5.state(["!disabled"] if pts >= 100 else ["disabled"])
                btn_10.state(["!disabled"] if pts >= 200 else ["disabled"])
                btn_25.state(["!disabled"] if pts >= 400 else ["disabled"])
                current_points = pts
                current_member_id = member_id
                update_final_amount()
            else:
                label_name.config(text="Not found")
                label_points.config(text="-")
                for b in (btn_5, btn_10, btn_25):
                    b.state(["disabled"])
                current_member_id = None
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def update_final_amount(*_):
        """Update final amount (after discount) and future points preview."""
        try:
            amt = float(entry_amount.get().strip())
        except ValueError:
            label_final.config(text="-")
            label_future_points.config(text="-")
            return

        final_amt = amt - applied_discount["value"]
        if final_amt < 0:
            final_amt = 0.0
        label_final.config(text=f"{final_amt:.2f}")

        if current_member_id is None:
            label_future_points.config(text="-")
        else:
            future_pts = current_points - applied_discount["points"] + int(final_amt)
            if future_pts < 0:
                future_pts = 0
            label_future_points.config(text=str(future_pts))

    def set_discount(value, points, buttons, clicked):
        """Toggle a single discount; only one active at a time."""
        if applied_discount["value"] == value and applied_discount["points"] == points:
            applied_discount["value"] = 0
            applied_discount["points"] = 0
        else:
            applied_discount["value"] = value
            applied_discount["points"] = points
        # Visual feedback (pressed/unpressed) - simulate by state
        for b in buttons:
            b.state(["!pressed"])
        clicked.state(["pressed"])
        update_final_amount()

    # Bind discount buttons
    btn_5.configure(command=lambda: set_discount(5, 100, (btn_5, btn_10, btn_25), btn_5))
    btn_10.configure(command=lambda: set_discount(10, 200, (btn_5, btn_10, btn_25), btn_10))
    btn_25.configure(command=lambda: set_discount(25, 400, (btn_5, btn_10, btn_25), btn_25))

    def confirm():
        """Save transaction and update points if member present (guest allowed)."""
        phone = entry_phone.get().strip()
        try:
            amt = float(entry_amount.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                member_id = None
                current_points_db = 0

                if phone:
                    cur.execute("SELECT MemberId, points FROM members WHERE phone=?", (phone,))
                    member = cur.fetchone()
                    if not member:
                        if not messagebox.askyesno("Member Not Found", "Member not found. Continue as guest?"):
                            return
                    else:
                        member_id, current_points_db = member

                final_amt = amt - applied_discount["value"]
                if final_amt < 0:
                    final_amt = 0.0

                if member_id is not None:
                    # Update points: burn discount points, add int(final_amt)
                    new_points = current_points_db - applied_discount["points"] + int(final_amt)
                    if new_points < 0:
                        new_points = 0
                    cur.execute("UPDATE members SET points=? WHERE MemberId=?", (new_points, member_id))

                # Insert transaction (MemberId can be NULL for guest)
                cur.execute(
                    "INSERT INTO transactions (MemberId, amount, datetime) VALUES (?, ?, ?)",
                    (member_id, final_amt, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()

            messagebox.showinfo("Transaction Complete", f"Final amount RM{final_amt:.2f}")
            # Reset inputs
            entry_amount.delete(0, tk.END)
            # keep phone field for quick repeated use
            applied_discount["value"] = 0
            applied_discount["points"] = 0
            update_final_amount()
            check_customer()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Events
    entry_phone.bind("<FocusOut>", lambda e: check_customer())
    entry_amount.bind("<KeyRelease>", lambda e: update_final_amount())

    ttk.Button(card, text="Confirm", style="Accent.TButton", command=confirm).pack(
        padx=24, pady=(0, 24), anchor="e"
    )
