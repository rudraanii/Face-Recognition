"""
PyInstaller build script to bundle Face Recognition Attendance System as a standalone desktop app.
"""
import os
import sys
import subprocess
import platform

def build():
    print("[BUILD] Starting standalone desktop packaging...")

    sep = ";" if platform.system() == "Windows" else ":"

    # Data files to bundle: (source, destination)
    datas = [
        f"Image_GUI{sep}Image_GUI",
        f"haarcascade_frontalface_default.xml{sep}.",
    ]

    if os.path.exists("clf.xml"):
        datas.append(f"clf.xml{sep}.")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=FaceRecognitionAttendance",
        "--onedir",
        "--windowed",
        "--noconfirm",
        "--clean",
    ]

    for data in datas:
        cmd.extend(["--add-data", data])

    cmd.extend([
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=sqlite3",
        "run.py"
    ])

    print("[RUNNING]", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("\n[SUCCESS] Build completed! Check the 'dist/FaceRecognitionAttendance' folder.")
    else:
        print("\n[ERROR] Packaging failed with exit code:", result.returncode)

if __name__ == "__main__":
    build()
