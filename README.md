# Face Recognition Attendance System

A simple mini project built with **Python, OpenCV, Tkinter and SQLite** that uses face detection and face recognition to mark student attendance automatically.

## Features

- Register students with a unique Student ID
- Capture 30 face samples using a webcam
- Train an LBPH face-recognition model
- Recognize registered students
- Automatically mark attendance once per day
- Store attendance in SQLite
- View attendance records using a GUI
- Simple Tkinter menu

## Technologies

- Python 3.10+
- OpenCV
- OpenCV Contrib
- NumPy
- Tkinter
- SQLite

## Project Structure

```text
Face_Attendance_System/
│
├── main.py
├── register_student.py
├── train_model.py
├── attendance.py
├── view_attendance.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── dataset/
│   └── .gitkeep
│
└── trainer/
    └── .gitkeep
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Face_Attendance_System.git
cd Face_Attendance_System
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Important: `opencv-contrib-python` is required because the project uses `cv2.face.LBPHFaceRecognizer`.

## Run

```bash
python main.py
```

### Workflow

1. Click **Register New Student**
2. Enter a unique Student ID and name
3. Look at the webcam until 30 samples are captured
4. Click **Train Face Model**
5. Click **Take Attendance**
6. The system recognizes registered students and records attendance
7. Click **View Attendance** to see records

## Database

SQLite creates `attendance.db` automatically.

It contains:

### students

| Column | Description |
|---|---|
| id | Unique student ID |
| name | Student name |

### attendance

| Column | Description |
|---|---|
| id | Attendance record ID |
| student_id | Student ID |
| name | Student name |
| date | Attendance date |
| time | Attendance time |

## How It Works

The project uses a Haar Cascade classifier to detect faces.

For recognition, it uses the **LBPH (Local Binary Patterns Histograms) Face Recognizer** provided by OpenCV Contrib.

The basic flow is:

```text
Webcam
   ↓
Face Detection
   ↓
Face Samples
   ↓
LBPH Training
   ↓
Face Recognition
   ↓
Student ID + Name
   ↓
SQLite Attendance Record
```

## GitHub Push

After creating your GitHub repository:

```bash
git init
git add .
git commit -m "Initial commit - Face Recognition Attendance System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Face_Attendance_System.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Important Notes

- Use the system only with the knowledge and consent of the people whose faces are registered.
- The default recognition threshold may need adjustment depending on lighting and camera quality.
- This is an educational mini project, not a production-grade biometric security system.
