import cv2
import sqlite3
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "attendance.db"
MODEL_FILE = BASE_DIR / "trainer" / "trainer.yml"


def get_student(student_id):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute(
        "SELECT id, name FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()
    conn.close()
    return row


def mark_attendance(student_id, name):
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    conn = sqlite3.connect(DB_FILE)

    existing = conn.execute(
        "SELECT 1 FROM attendance WHERE student_id = ? AND date = ?",
        (student_id, today)
    ).fetchone()

    if existing is None:
        conn.execute(
            """
            INSERT INTO attendance(student_id, name, date, time)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, name, today, now)
        )
        conn.commit()
        result = True
    else:
        result = False

    conn.close()
    return result


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def start_attendance():
    init_db()

    if not MODEL_FILE.exists():
        raise RuntimeError(
            "Trained model not found. Register a student and train the model first."
        )

    if not hasattr(cv2, "face"):
        raise RuntimeError(
            "cv2.face is unavailable. Install opencv-contrib-python."
        )

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(MODEL_FILE))

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise RuntimeError("Could not open webcam.")

    recognized_name = "Unknown"
    recognized_id = None
    attendance_message = ""

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
            student_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            # LBPH confidence is a distance: lower means more similar.
            if confidence < 70:
                student = get_student(student_id)

                if student:
                    recognized_id, recognized_name = student
                    mark_attendance(recognized_id, recognized_name)

                    label = f"{recognized_name} ({recognized_id})"
                    color = (0, 255, 0)
                else:
                    label = "Unknown Student"
                    color = (0, 0, 255)
            else:
                recognized_id = None
                recognized_name = "Unknown"
                label = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                color,
                2
            )

            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        cv2.putText(
            frame,
            "Press Q to exit",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.imshow("Face Attendance", frame)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


def main():
    root = tk.Tk()
    root.withdraw()

    try:
        start_attendance()
    except Exception as e:
        messagebox.showerror("Attendance Error", str(e))


if __name__ == "__main__":
    main()
