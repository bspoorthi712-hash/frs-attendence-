import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "attendance.db"


def view_records():
    conn = sqlite3.connect(DB_FILE)

    try:
        rows = conn.execute(
            """
            SELECT student_id, name, date, time
            FROM attendance
            ORDER BY date DESC, time DESC
            """
        ).fetchall()
    except sqlite3.OperationalError:
        rows = []

    conn.close()

    root = tk.Tk()
    root.title("Attendance Records")
    root.geometry("700x450")

    columns = ("student_id", "name", "date", "time")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    headings = {
        "student_id": "Student ID",
        "name": "Name",
        "date": "Date",
        "time": "Time"
    }

    widths = {
        "student_id": 120,
        "name": 230,
        "date": 150,
        "time": 120
    }

    for column in columns:
        tree.heading(column, text=headings[column])
        tree.column(column, width=widths[column], anchor="center")

    for row in rows:
        tree.insert("", "end", values=row)

    tree.pack(fill="both", expand=True, padx=15, pady=15)

    if not rows:
        messagebox.showinfo(
            "Attendance",
            "No attendance records found."
        )

    root.mainloop()


if __name__ == "__main__":
    view_records()
