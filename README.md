Face Attendance System

This is a web-based facial recognition attendance system built using Python, Flask, and OpenCV.
It allows for the registration of users, captures their facial data, trains a machine learning model for recognition, and automatically records attendance in CSV files.

---

Features

User Registration

Register students or employees with the following details:

- ID
- Name
- Semester
- Year
- Branch
- Subject

---

Face Data Capture

Automatically captures 80 face images using webcam.

---

Model Training

Uses LBPH (Local Binary Pattern Histogram) algorithm to train the face recognition model.

---

Automated Attendance Tracking

Real-time face recognition system:

🟢 Green Box → First attendance

🔵 Blue Box → Duplicate attendance blocked

🔴 Red Box → Unknown person

Attendance is stored automatically in CSV file.

---

Dashboard & Reporting

Teacher dashboard provides:

- Search student by name
- Filter attendance by date
- Filter attendance by branch
- Download filtered Excel report

---

Monthly Report

Shows total attendance count.

---

Requirements

Install required libraries:

pip install Flask opencv-contrib-python numpy Pillow pandas openpyxl

Make sure webcam is working properly.

---

Project Structure

ABC/
│
├── app.py
├── haarcascade_frontalface_default.xml
│
├── employees.csv
│
├── TrainingImage/
│
├── TrainingImageLabel/
│
├── Attendance/
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── register.html
    ├── attendance.html
    ├── login.html
    ├── dashboard.html
    ├── message.html
    └── report.html

---

How to Run

Open terminal in project folder:

python app.py

Open browser:

http://127.0.0.1:5000

---

Steps to Use

Step 1 – Register Student

Go to Register page
Fill student details
Click capture

Camera will capture 80 images automatically.

After capture, training will complete automatically.

---

Step 2 – Start Attendance

Click Start Attendance

Camera will open

System detects face and marks attendance

Press q to close camera

Attendance saved inside:

Attendance folder

---

Step 3 – Teacher Login

Login credentials:

username: admin
password: 1234

Teacher can:

View attendance

Filter by date

Filter by branch

Download Excel file

Check monthly report

---

Advantages

No proxy attendance

Automatic system

Time saving

Accurate data

Easy to use

---

Conclusion

Face Recognition Attendance System provides a smart and secure method to manage attendance using Artificial Intelligence technology.