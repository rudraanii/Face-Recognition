import os
import io
import csv
import base64
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import db
from utils import get_asset_path

app = Flask(__name__)

# Ensure required directories and files exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_IMG_DIR = os.path.join(BASE_DIR, "data_img")
os.makedirs(DATA_IMG_DIR, exist_ok=True)

CSV_FILE = os.path.join(BASE_DIR, "attendance.csv")
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="\n") as f:
        f.write("Std_ID,Roll_No,Name,Time,Date,Attendance\n")

# Load Face Cascade
CASCADE_PATH = get_asset_path("haarcascade_frontalface_default.xml")
if not os.path.exists(CASCADE_PATH):
    CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Global model state
clf_model = None

def train_model_internal():
    global clf_model
    valid_exts = ('.jpg', '.jpeg', '.png')
    if not os.path.exists(DATA_IMG_DIR):
        return False, "Dataset directory does not exist."

    image_paths = [os.path.join(DATA_IMG_DIR, f) for f in os.listdir(DATA_IMG_DIR) if f.lower().endswith(valid_exts)]
    if not image_paths:
        return False, "No face samples found."

    faces = []
    ids = []
    for p in image_paths:
        parts = os.path.basename(p).split(".")
        if len(parts) >= 3 and parts[1].isdigit():
            sid = int(parts[1])
            try:
                pil_img = Image.open(p).convert("L")
                img_np = np.array(pil_img, "uint8")
                img_np = cv2.resize(img_np, (200, 200))
                faces.append(img_np)
                ids.append(sid)
            except Exception:
                continue

    if not faces:
        return False, "No valid face samples with numeric IDs could be loaded."

    try:
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, np.array(ids, dtype=np.int32))
        clf_file = os.path.join(BASE_DIR, "clf.xml")
        clf.write(clf_file)
        clf_model = clf
        print(f"[INFO] LBPH model successfully trained on {len(faces)} images across {len(set(ids))} student(s).")
        return True, f"Trained on {len(faces)} images across {len(set(ids))} student(s)."
    except Exception as e:
        print("[WARN] Model training failed:", e)
        return False, str(e)

def load_model():
    global clf_model
    clf_path = os.path.join(BASE_DIR, "clf.xml")
    if os.path.exists(clf_path):
        try:
            model = cv2.face.LBPHFaceRecognizer_create()
            model.read(clf_path)
            clf_model = model
            print("[INFO] LBPH model successfully loaded from clf.xml")
            return True
        except Exception as e:
            print("[WARN] Could not load clf.xml:", e)
    # If clf.xml not loaded, try training from existing data_img
    success, _ = train_model_internal()
    return success

load_model()

def mark_attendance_record(std_id, roll_no, name):
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")

    # Read existing entries to prevent duplicate logs on the same day
    existing_keys = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="\n") as f:
            for line in f.readlines()[1:]:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 5:
                    existing_keys.add((parts[0], parts[4]))

    if (str(std_id), date_str) not in existing_keys:
        with open(CSV_FILE, "a", newline="\n") as f:
            f.write(f"{std_id},{roll_no},{name},{time_str},{date_str},Present\n")

        # Also insert into database
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO stdattendance (std_id, std_roll_no, std_name, std_time, std_date, std_attendance) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (str(std_id), str(roll_no), str(name), time_str, date_str, "Present")
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print("[WARN] Could not save to stdattendance table:", e)
        return True, time_str, date_str
    return False, time_str, date_str

# ----------------- Routes -----------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    global clf_model
    if clf_model is None:
        load_model()

    total_students = 0
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM student")
        row = cur.fetchone()
        if row:
            total_students = row[0]
        conn.close()
    except Exception:
        pass

    total_samples = 0
    if os.path.exists(DATA_IMG_DIR):
        total_samples = len([f for f in os.listdir(DATA_IMG_DIR) if f.lower().endswith(('.jpg', '.png'))])

    today_str = datetime.now().strftime("%d/%m/%Y")
    present_today = 0
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="\n") as f:
            for line in f.readlines()[1:]:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 5 and parts[4] == today_str:
                    present_today += 1

    attendance_rate = round((present_today / total_students) * 100, 1) if total_students > 0 else 0

    dept_counts = {}
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Department, COUNT(*) FROM student GROUP BY Department")
        for r in cur.fetchall():
            if r[0]:
                dept_counts[str(r[0])] = r[1]
        conn.close()
    except Exception:
        pass

    clf_path = os.path.join(BASE_DIR, "clf.xml")
    model_last_trained = None
    if os.path.exists(clf_path):
        try:
            mtime = os.path.getmtime(clf_path)
            model_last_trained = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y %H:%M")
        except Exception:
            pass

    return jsonify({
        "model_loaded": clf_model is not None,
        "total_students": total_students,
        "total_samples": total_samples,
        "present_today": present_today,
        "attendance_rate": attendance_rate,
        "department_counts": dept_counts,
        "model_last_trained": model_last_trained,
        "server_time": datetime.now().strftime("%H:%M:%S"),
        "server_date": datetime.now().strftime("%A, %d %B %Y"),
        "db_engine": db.DB_ENGINE
    })

@app.route("/api/recognize", methods=["POST"])
def recognize():
    global clf_model
    data = request.get_json(force=True)
    image_b64 = data.get("image", "")

    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    try:
        if "," in image_b64:
            image_b64 = image_b64.split(",")[1]
        image_bytes = base64.b64decode(image_b64)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({"error": f"Failed to decode image: {str(e)}"}), 400

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60))

    if len(faces) == 0:
        return jsonify({"faces": [], "message": "No face detected"})

    if clf_model is None:
        load_model()

    # Pre-cache student dictionary
    student_cache = {}
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Student_ID, Roll_No, Name, Department FROM student")
        for row in cur.fetchall():
            sid_raw = str(row[0]).strip()
            sinfo = {
                "roll_no": str(row[1]).strip() if row[1] else "",
                "name": str(row[2]).strip() if row[2] else f"Student #{sid_raw}",
                "department": str(row[3]).strip() if row[3] else "General"
            }
            student_cache[sid_raw] = sinfo
            if sid_raw.isdigit():
                student_cache[str(int(sid_raw))] = sinfo
        conn.close()
    except Exception as es:
        print("[WARN] student_cache error:", es)

    results = []
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_res = {
            "box": [int(x), int(y), int(w), int(h)],
            "recognized": False,
            "name": "Unknown Face",
            "roll_no": "",
            "student_id": "",
            "confidence": 0,
            "new_attendance_marked": False
        }

        if clf_model is not None:
            try:
                # Resize and equalize histogram to match 200x200 LBPH training resolution
                face_norm = cv2.resize(face_roi, (200, 200))
                face_norm = cv2.equalizeHist(face_norm)

                pred_id, conf_val = clf_model.predict(face_norm)
                # conf_val is the Chi-Square distance (lower = closer match)
                confidence = int(100 * (1 - conf_val / 300))
                face_res["confidence"] = max(0, min(100, confidence))

                std_id_str = str(pred_id)
                student = student_cache.get(std_id_str) or student_cache.get(str(int(pred_id)) if std_id_str.isdigit() else std_id_str)

                # Robust threshold: confidence >= 65% indicates a verified facial match
                if confidence >= 65:
                    face_res["recognized"] = True
                    face_res["student_id"] = std_id_str

                    if student is not None:
                        face_res["name"] = student["name"]
                        face_res["roll_no"] = student["roll_no"]
                        face_res["department"] = student["department"]
                    else:
                        face_res["name"] = f"Student #{std_id_str}"
                        face_res["roll_no"] = f"ID-{std_id_str}"
                        face_res["department"] = "General"

                    # Mark attendance
                    is_new, t_str, d_str = mark_attendance_record(std_id_str, face_res["roll_no"], face_res["name"])
                    face_res["new_attendance_marked"] = is_new
                    face_res["time"] = t_str
                    face_res["date"] = d_str
            except Exception as e:
                print("[WARN] Prediction error:", e)

        results.append(face_res)

    return jsonify({"faces": results})

@app.route("/api/students", methods=["GET", "POST"])
def handle_students():
    if request.method == "GET":
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Student_ID, Name, Department, Course, Year, Semester, Division, Gender, Roll_No, Email, Mobile_No, PhotoSample FROM student ORDER BY Student_ID ASC")
            rows = cur.fetchall()
            students = []
            for r in rows:
                students.append({
                    "id": r[0], "name": r[1], "department": r[2], "course": r[3],
                    "year": r[4], "semester": r[5], "division": r[6], "gender": r[7],
                    "roll_no": r[8], "email": r[9], "mobile": r[10], "photo_sample": r[11]
                })
            conn.close()
            return jsonify(students)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "POST":
        data = request.get_json(force=True)
        std_id = data.get("id", "").strip()
        name = data.get("name", "").strip()
        roll_no = data.get("roll_no", "").strip()
        department = data.get("department", "SCSE")
        course = data.get("course", "Btech")
        year = data.get("year", "2021-25")
        semester = data.get("semester", "Semester-1")
        division = data.get("division", "Morning")
        gender = data.get("gender", "Female")
        email = data.get("email", "").strip()
        mobile = data.get("mobile", "").strip()

        if not std_id or not name or not roll_no:
            return jsonify({"error": "Student ID, Name, and Roll Number are required"}), 400

        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Student_ID FROM student WHERE Student_ID=%s", (std_id,))
            if cur.fetchone():
                conn.close()
                return jsonify({"error": f"Student with ID {std_id} already exists"}), 400

            cur.execute(
                "INSERT INTO student (Student_ID, Name, Department, Course, Year, Semester, Division, Gender, DOB, Mobile_No, Address, Roll_No, Email, Teacher_Name, PhotoSample) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (std_id, name, department, course, year, semester, division, gender, "", mobile, "", roll_no, email, "", "No")
            )
            conn.commit()
            conn.close()
            return jsonify({"success": True, "message": f"Student {name} registered successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/api/students/<std_id>", methods=["DELETE"])
def delete_student(std_id):
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE Student_ID=%s", (std_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"Student {std_id} deleted."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/capture_sample", methods=["POST"])
def capture_sample():
    data = request.get_json(force=True)
    std_id = data.get("id", "").strip()
    image_b64 = data.get("image", "")

    if not std_id or not image_b64:
        return jsonify({"error": "Student ID and image are required"}), 400

    try:
        if "," in image_b64:
            image_b64 = image_b64.split(",")[1]
        image_bytes = base64.b64decode(image_b64)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        if len(faces) == 0:
            return jsonify({"error": "No face detected in capture. Please look directly at the camera."}), 400

        # Crop the largest face
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        (x, y, w, h) = faces[0]
        face_crop = cv2.resize(gray[y:y+h, x:x+w], (200, 200))

        # Count existing samples for this student
        existing = [f for f in os.listdir(DATA_IMG_DIR) if f.startswith(f"student.{std_id}.") or f.startswith(f"stdudent.{std_id}.")]
        sample_num = len(existing) + 1

        filename = f"student.{std_id}.{sample_num}.jpg"
        cv2.imwrite(os.path.join(DATA_IMG_DIR, filename), face_crop)

        # Update PhotoSample flag in database
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE student SET PhotoSample='Yes' WHERE Student_ID=%s", (std_id,))
            conn.commit()
            conn.close()
        except Exception:
            pass

        # Auto-retrain model in real-time so scanner immediately recognizes new faces
        train_model_internal()

        return jsonify({
            "success": True,
            "sample_num": sample_num,
            "message": f"Sample {sample_num} saved for Student ID {std_id}! Model automatically updated."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/train", methods=["POST"])
def train_model():
    success, msg = train_model_internal()
    if success:
        return jsonify({
            "success": True,
            "message": f"Model successfully retrained: {msg}"
        })
    return jsonify({"error": f"Training failed: {msg}"}), 400

@app.route("/api/attendance", methods=["GET"])
def get_attendance():
    records = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="\n") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if row and len(row) >= 6:
                    records.append({
                        "id": row[0].strip(),
                        "roll_no": row[1].strip(),
                        "name": row[2].strip(),
                        "time": row[3].strip(),
                        "date": row[4].strip(),
                        "status": row[5].strip()
                    })
    records.reverse()  # Show most recent first
    return jsonify(records)

@app.route("/api/export_csv", methods=["GET"])
def export_csv():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True, download_name="attendance_records.csv", mimetype="text/csv")
    return jsonify({"error": "Attendance CSV not found"}), 404

@app.route("/api/samples/<filename>", methods=["GET"])
def get_sample_image(filename):
    if "/" in filename or "\\" in filename or ".." in filename:
        return jsonify({"error": "Invalid filename"}), 400
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        return jsonify({"error": "Invalid file extension"}), 400
    file_path = os.path.join(DATA_IMG_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="image/jpeg")
    return jsonify({"error": "Sample image not found"}), 404

@app.route("/api/students/<std_id>/samples", methods=["GET"])
def get_student_samples(std_id):
    if not os.path.exists(DATA_IMG_DIR):
        return jsonify({"student_id": std_id, "total_samples": 0, "samples": []})
    all_files = os.listdir(DATA_IMG_DIR)
    matched = [f for f in all_files if (f.startswith(f"student.{std_id}.") or f.startswith(f"stdudent.{std_id}.")) and f.lower().endswith(('.jpg', '.png'))]
    def extract_sample_num(name):
        parts = name.split(".")
        if len(parts) >= 3 and parts[2].isdigit():
            return int(parts[2])
        return 0
    matched.sort(key=extract_sample_num, reverse=True)
    return jsonify({
        "student_id": std_id,
        "total_samples": len(matched),
        "samples": matched[:12]
    })

@app.route("/api/attendance/manual", methods=["POST"])
def mark_manual_attendance():
    data = request.get_json(force=True)
    std_id = data.get("id", "").strip()
    roll_no = data.get("roll_no", "").strip()
    name = data.get("name", "").strip()
    if not std_id or not name:
        return jsonify({"error": "Student ID and Name are required"}), 400
    is_new, time_str, date_str = mark_attendance_record(std_id, roll_no, name)
    if is_new:
        return jsonify({"success": True, "message": f"Attendance successfully marked for {name} ({time_str})"})
    return jsonify({"success": True, "message": f"{name} is already marked Present for today ({time_str})"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
