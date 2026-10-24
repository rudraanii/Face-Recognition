#!/usr/bin/env python3
"""
Launcher script for Face Recognition Attendance System
"""
import os
import sys

def check_environment():
    missing = []
    try:
        import PIL
    except ImportError:
        missing.append("Pillow")
    try:
        import cv2
    except ImportError:
        missing.append("opencv-contrib-python")
    try:
        import numpy
    except ImportError:
        missing.append("numpy")

    if missing:
        print("=" * 60)
        print("[WARNING] Missing required Python packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nPlease install the required packages using:")
        print("  pip install -r requirements.txt")
        print("=" * 60)
        return False
    return True

def initialize_workspace():
    # Ensure data_img directory exists
    os.makedirs("data_img", exist_ok=True)

    # Ensure attendance.csv exists with headers
    if not os.path.exists("attendance.csv"):
        with open("attendance.csv", "w", newline="\n") as f:
            f.write("Std_ID,Roll_No,Name,Time,Date,Attendance\n")
        print("[INIT] Created attendance.csv with header.")

    # Initialize database tables
    try:
        import db
        db.init_database()
    except Exception as e:
        print("[WARN] Database auto-initialization message:", e)

def main():
    print("=" * 60)
    print("  Starting Face Recognition Attendance Management System")
    print("=" * 60)

    if not check_environment():
        sys.exit(1)

    initialize_workspace()

    # Launch Login window
    import tkinter as tk
    from login import Login

    root = tk.Tk()
    app = Login(root)
    root.mainloop()

if __name__ == "__main__":
    main()
