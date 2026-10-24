#!/usr/bin/env python3
"""
Comprehensive automated system validation test suite.
"""
import os
import sys
import numpy as np

def run_tests():
    print("=" * 70)
    print("  RUNNING SYSTEM VALIDATION TEST SUITE")
    print("=" * 70)

    errors = []

    # 1. Dependency checks
    print("\n[TEST 1] Checking Core Libraries...")
    try:
        import PIL
        from PIL import Image
        print(f"  [PASS] Pillow {PIL.__version__} is working.")
    except Exception as e:
        errors.append(f"Pillow import error: {e}")
        print(f"  [FAIL] Pillow: {e}")

    try:
        import cv2
        print(f"  [PASS] OpenCV {cv2.__version__} is working.")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        print("  [PASS] cv2.face.LBPHFaceRecognizer_create is available.")
    except Exception as e:
        errors.append(f"OpenCV error: {e}")
        print(f"  [FAIL] OpenCV face recognizer: {e}")

    # 2. Asset loading & Pillow resampling
    print("\n[TEST 2] Verifying GUI Assets and Resampling...")
    from utils import get_asset_path, LANCZOS_RESAMPLE
    required_assets = [
        "banner.jpg", "bg2.jpg", "bg3.jpg", "bg4.png", "bgReg.jpg",
        "loginBg1.jpg", "log1.png", "std1.jpg", "det1.jpg", "att.jpg",
        "hlp.jpg", "tra1.jpg", "t_bg1.jpg", "t_btn1.png", "dev.jpg",
        "exi.jpg", "f_det.jpg", "web.png", "fb.png", "yt.png",
        "gmail.png", "i5.png", "haarcascade_frontalface_default.xml"
    ]
    for asset in required_assets:
        path = get_asset_path(asset)
        if not os.path.exists(path):
            errors.append(f"Missing asset: {asset} at {path}")
            print(f"  [FAIL] Asset missing: {asset}")
        else:
            if asset.endswith(('.jpg', '.png')):
                try:
                    img = Image.open(path)
                    _ = img.resize((100, 100), LANCZOS_RESAMPLE)
                    # print(f"  [PASS] Loaded & resampled {asset}")
                except Exception as e:
                    errors.append(f"Resampling failed for {asset}: {e}")
                    print(f"  [FAIL] Resampling failed for {asset}: {e}")
    print(f"  [PASS] All {len(required_assets)} essential assets resolved and verified.")

    # 3. Database CRUD Operations
    print("\n[TEST 3] Verifying Database CRUD Operations...")
    import db
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        
        # Test regteach
        cur.execute("DELETE FROM regteach WHERE email=%s", ("test_verify@test.com",))
        cur.execute("INSERT INTO regteach (fname, lname, cnum, email, ss_que, s_ans, pwd) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    ("Test", "User", "1234567890", "test_verify@test.com", "Nick", "tester", "pass123"))
        conn.commit()

        cur.execute("SELECT * FROM regteach WHERE email=%s", ("test_verify@test.com",))
        row = cur.fetchone()
        assert row is not None, "Failed to retrieve inserted teacher"
        print("  [PASS] regteach table: Insert, Query OK.")

        # Test student
        cur.execute("DELETE FROM student WHERE Student_ID=%s", ("TEST999",))
        cur.execute(
            "INSERT INTO student (Student_ID, Name, Department, Course, Year, Semester, Division, Gender, DOB, Mobile_No, Address, Roll_No, Email, Teacher_Name, PhotoSample) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ("TEST999", "Validation Student", "SCSE", "Btech", "2021-25", "Semester-5", "Morning", "Male", "01/01/2000", "9876543210", "Campus", "R999", "std@test.com", "Prof X", "No")
        )
        conn.commit()

        cur.execute("SELECT Name, Roll_No FROM student WHERE Student_ID=%s", ("TEST999",))
        s_row = cur.fetchone()
        assert s_row is not None and s_row[0] == "Validation Student", "Failed to retrieve inserted student"
        print("  [PASS] student table: Insert, Query OK.")

        # Test stdattendance
        cur.execute("INSERT INTO stdattendance (std_id, std_roll_no, std_name, std_time, std_date, std_attendance) VALUES (%s,%s,%s,%s,%s,%s)",
                    ("TEST999", "R999", "Validation Student", "12:00:00", "24/10/2026", "Present"))
        conn.commit()
        cur.execute("SELECT * FROM stdattendance WHERE std_id=%s", ("TEST999",))
        att_row = cur.fetchone()
        assert att_row is not None, "Failed to retrieve attendance record"
        print("  [PASS] stdattendance table: Insert, Query OK.")

        # Clean up
        cur.execute("DELETE FROM regteach WHERE email=%s", ("test_verify@test.com",))
        cur.execute("DELETE FROM student WHERE Student_ID=%s", ("TEST999",))
        cur.execute("DELETE FROM stdattendance WHERE std_id=%s", ("TEST999",))
        conn.commit()
        conn.close()
        print("  [PASS] Database cleanup OK.")
    except Exception as e:
        errors.append(f"Database operation failed: {e}")
        print(f"  [FAIL] Database test: {e}")

    # 4. Model Training & XML Model Validation
    print("\n[TEST 4] Testing LBPH Model Training and Haar Cascade...")
    try:
        cascade_path = get_asset_path("haarcascade_frontalface_default.xml")
        face_cascade = cv2.CascadeClassifier(cascade_path)
        assert not face_cascade.empty(), "Cascade classifier failed to load!"
        print("  [PASS] Haar Cascade Classifier loaded successfully.")

        data_dir = "data_img"
        images = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.lower().endswith(('.jpg', '.png'))]
        print(f"  [INFO] Found {len(images)} sample images in data_img.")
        
        faces = []
        ids = []
        for img_p in images:
            parts = os.path.basename(img_p).split(".")
            if len(parts) >= 3 and parts[1].isdigit():
                sid = int(parts[1])
                pil_img = Image.open(img_p).convert("L")
                faces.append(np.array(pil_img, "uint8"))
                ids.append(sid)

        assert len(faces) > 0, "No valid faces loaded for training"
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, np.array(ids, dtype=np.int32))
        clf.write("clf.xml")
        print(f"  [PASS] LBPH Face Recognizer successfully trained on {len(faces)} images and clf.xml written.")

        # Re-read clf.xml to confirm valid XML
        test_clf = cv2.face.LBPHFaceRecognizer_create()
        test_clf.read("clf.xml")
        print("  [PASS] clf.xml reloaded and validated.")
    except Exception as e:
        errors.append(f"Model training/loading error: {e}")
        print(f"  [FAIL] Training/Model: {e}")

    # 5. UI compilation and import verification
    print("\n[TEST 5] Verifying GUI Class Imports...")
    ui_modules = ["main", "login", "register", "student", "attendance", "developer", "helpsupport", "train", "face_recognition"]
    for mod in ui_modules:
        try:
            __import__(mod)
            print(f"  [PASS] Module '{mod}' imported successfully.")
        except Exception as e:
            errors.append(f"Module '{mod}' import failed: {e}")
            print(f"  [FAIL] Module '{mod}': {e}")

    print("\n" + "=" * 70)
    if not errors:
        print("  ALL TESTS PASSED PERFECTLY! (0 ERRORS)")
        print("=" * 70)
        return 0
    else:
        print(f"  TESTS FINISHED WITH {len(errors)} ERROR(S):")
        for err in errors:
            print(f"   - {err}")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
