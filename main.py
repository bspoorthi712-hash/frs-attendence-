import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent


def run_script(script_name):
    try:
        subprocess.Popen([sys.executable, str(BASE_DIR / script_name)])
    except Exception as e:
        messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    root.title("Face Recognition Attendance System")
    root.geometry("520x420")
    root.resizable(False, False)

    title = tk.Label(
        root,
        text="Face Recognition Attendance",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=30)

    subtitle = tk.Label(
        root,
        text="Python + OpenCV + SQLite",
        font=("Arial", 11)
    )
    subtitle.pack(pady=5)

    buttons = [
        ("1. Register New Student", "register_student.py"),
        ("2. Train Face Model", "train_model.py"),
        ("3. Take Attendance", "attendance.py"),
        ("4. View Attendance", "view_attendance.py"),
    ]

    for text, script in buttons:
        tk.Button(
            root,
            text=text,
            width=30,
            height=2,
            font=("Arial", 12),
            command=lambda s=script: run_script(s)
        ).pack(pady=7)

    tk.Label(
        root,
        text="Make sure your webcam is connected.",
        fg="gray"
    ).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
