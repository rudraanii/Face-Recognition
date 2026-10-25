from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
from tkinter import messagebox
from datetime import datetime
from utils import get_asset_path, LANCZOS_RESAMPLE
import db

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Panel")

        # Header image  
        img = Image.open(get_asset_path("banner.jpg"))
        img = img.resize((1366, 130), LANCZOS_RESAMPLE)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # Background image 
        bg1 = Image.open(get_asset_path("bg2.jpg"))
        bg1 = bg1.resize((1366, 768), LANCZOS_RESAMPLE)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # Title section
        title_lb1 = Label(bg_img, text="Face Recognition Attendance Panel",
                          font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Face detector button
        std_img_btn = Image.open(get_asset_path("f_det.jpg"))
        std_img_btn = std_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.face_recog, image=self.std_img1, cursor="hand2")
        std_b1.place(x=600, y=170, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.face_recog, text="Launch Face Detector", cursor="hand2",
                          font=("tahoma", 14, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=590, y=350, width=200, height=45)

    # ===================== Attendance Logging ===================
    def mark_attendance(self, i, r, n):
        # Strictly verify student exists in the enrolled student database
        enrolled = False
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Student_ID, Roll_No, Name FROM student WHERE Student_ID=%s", (str(i),))
            row = cur.fetchone()
            if row:
                enrolled = True
                r = str(row[1]) if row[1] else r
                n = str(row[2]) if row[2] else n
            conn.close()
        except Exception as e:
            print("[WARN] Error checking student enrollment for attendance:", e)

        if not enrolled:
            print(f"[REJECT] Attendance not marked: Student ID {i} is not enrolled in database.")
            return

        csv_file = "attendance.csv"
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M:%S")

        # Initialize CSV if not present
        if not os.path.exists(csv_file):
            with open(csv_file, "w", newline="\n") as f:
                f.write("Std_ID,Roll_No,Name,Time,Date,Attendance\n")

        # Read existing attendance records from CSV to prevent duplicates on same date
        existing_keys = set()
        with open(csv_file, "r", newline="\n") as f:
            for line in f.readlines()[1:]:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 5:
                    existing_keys.add((parts[0], parts[4]))  # (ID, Date)

        # Check existing attendance in database table stdattendance
        db_has_record = False
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT std_id FROM stdattendance WHERE std_id=%s AND std_date=%s", (str(i), date_str))
            if cur.fetchone():
                db_has_record = True
            conn.close()
        except Exception:
            pass

        if (str(i), date_str) not in existing_keys:
            with open(csv_file, "a", newline="\n") as f:
                f.write(f"{i},{r},{n},{time_str},{date_str},Present\n")

        if not db_has_record:
            try:
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO stdattendance (std_id, std_roll_no, std_name, std_time, std_date, std_attendance) VALUES (%s,%s,%s,%s,%s,%s)",
                            (str(i), str(r), str(n), time_str, date_str, "Present"))
                conn.commit()
                conn.close()
            except Exception as e:
                print("[WARN] Could not save to stdattendance:", e)

    # ==================== Face Recognition Execution ==================
    def face_recog(self):
        cascade_file = get_asset_path("haarcascade_frontalface_default.xml")
        if not os.path.exists(cascade_file):
            cascade_file = "haarcascade_frontalface_default.xml"

        if not os.path.exists(cascade_file):
            messagebox.showerror("Error", "Face Cascade XML file not found!")
            return

        clf_file = "clf.xml"
        if not os.path.exists(clf_file):
            messagebox.showerror("Error", "Trained Classifier model (clf.xml) not found!\nPlease train the dataset first in the 'Data Train' panel.", parent=self.root)
            return

        # Pre-cache enrolled student records from database
        student_cache = {}
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Student_ID, Roll_No, Name FROM student")
            for row in cur.fetchall():
                sid_str = str(row[0]).strip()
                s_info = (str(row[1]).strip() if row[1] else "", str(row[2]).strip() if row[2] else "")
                student_cache[sid_str] = s_info
                if sid_str.isdigit():
                    student_cache[str(int(sid_str))] = s_info
            conn.close()
        except Exception as es:
            print("[WARN] Could not preload student database cache:", es)

        faceCascade = cv2.CascadeClassifier(cascade_file)
        try:
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read(clf_file)
        except Exception as e:
            messagebox.showerror("Model Error", f"Error loading trained model:\n{str(e)}")
            return

        videoCap = cv2.VideoCapture(0)
        if not videoCap.isOpened():
            videoCap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        if not videoCap.isOpened():
            messagebox.showerror("Camera Error", "Could not open webcam. Please check your camera permissions and device connection.")
            return

        while True:
            ret, img = videoCap.read()
            if not ret or img is None:
                break

            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10)

            for (x, y, w, h) in features:
                face_crop = gray_image[y:y+h, x:x+w]
                face_crop = cv2.resize(face_crop, (200, 200))
                face_crop = cv2.equalizeHist(face_crop)
                predicted_id, predict_conf = clf.predict(face_crop)
                confidence = int(100 * (1 - predict_conf / 300))

                std_id_str = str(predicted_id)
                student_info = student_cache.get(std_id_str) or student_cache.get(str(int(predicted_id)) if std_id_str.isdigit() else std_id_str)

                # Strict requirement: confidence >= 65% AND must be a verified enrolled student in database
                if confidence >= 65 and student_info is not None:
                    roll_no, name = student_info
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, f"ID: {std_id_str}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(img, f"Name: {name}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(img, f"Roll: {roll_no} ({confidence}%)", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                    self.mark_attendance(std_id_str, roll_no, name)
                else:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(img, "Unknown Face", (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)

            cv2.imshow("Face Detector - Press ENTER or Q to exit", img)

            key = cv2.waitKey(1) & 0xFF
            if key in (13, ord('q'), ord('Q'), 27):  # Enter, Q, or Esc to exit
                break

        videoCap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()