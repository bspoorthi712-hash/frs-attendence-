import cv2
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
DB_FILE = BASE_DIR / "attendance.db"
CASCADE_FILE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def register_student():
    init_db()

    root = tk.Tk()
    root.withdraw()

    student_id = simpledialog.askinteger(
        "Student ID",
        "Enter a unique numeric Student ID:"
    )

    if student_id is None:
        return

    name = simpledialog.askstring(
        "Student Name",
        "Enter student's full name:"
    )

    if not name or not name.strip():
        messagebox.showerror("Error", "Name is required.")
        return

    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute(
            "INSERT INTO students (id, name) VALUES (?, ?)",
            (student_id, name.strip())
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        messagebox.showerror("Error", "That Student ID already exists.")
        return
    conn.close()

    DATASET_DIR.mkdir(exist_ok=True)

    detector = cv2.CascadeClassifier(CASCADE_FILE)
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        messagebox.showerror("Camera Error", "Could not open webcam.")
        return

    count = 0
    messagebox.showinfo(
        "Instructions",
        "Look at the camera. The system will capture 30 face samples.\n"
        "Press Q to stop early."
    )

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]

            filename = DATASET_DIR / f"User.{student_id}.{count}.jpg"
            cv2.imwrite(str(filename), face_img)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(
                frame,
                f"Samples: {count}/30",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow("Register Student - Press Q to stop", frame)

        key = cv2.waitKey(100) & 0xff
        if key == ord("q") or count >= 30:
            break

    cam.release()
    cv2.destroyAllWindows()

    messagebox.showinfo(
        "Success",
        f"Registration completed for {name.strip()}.\n"
        f"Captured {count} face samples."
    )


if __name__ == "__main__":
    register_student()
