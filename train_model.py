import cv2
import numpy as np
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
TRAINER_DIR = BASE_DIR / "trainer"
MODEL_FILE = TRAINER_DIR / "trainer.yml"


def train():
    if not hasattr(cv2, "face"):
        raise RuntimeError(
            "cv2.face is unavailable. Install opencv-contrib-python "
            "instead of opencv-python."
        )

    TRAINER_DIR.mkdir(exist_ok=True)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    image_paths = list(DATASET_DIR.glob("User.*.*.jpg"))

    if not image_paths:
        raise RuntimeError(
            "No face samples found. Register at least one student first."
        )

    face_samples = []
    ids = []

    for image_path in image_paths:
        try:
            gray_img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            student_id = int(image_path.name.split(".")[1])

            faces = detector.detectMultiScale(
                gray_img,
                scaleFactor=1.1,
                minNeighbors=5
            )

            if len(faces) == 0:
                face_samples.append(gray_img)
                ids.append(student_id)
            else:
                for (x, y, w, h) in faces:
                    face_samples.append(gray_img[y:y+h, x:x+w])
                    ids.append(student_id)

        except Exception:
            continue

    if not face_samples:
        raise RuntimeError("Could not read any training images.")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(face_samples, np.array(ids))
    recognizer.write(str(MODEL_FILE))

    return len(face_samples)


def main():
    root = tk.Tk()
    root.withdraw()

    try:
        count = train()
        messagebox.showinfo(
            "Training Complete",
            f"Face model trained successfully.\n"
            f"Training samples: {count}\n\n"
            f"Model saved to:\n{MODEL_FILE}"
        )
    except Exception as e:
        messagebox.showerror("Training Error", str(e))


if __name__ == "__main__":
    main()
