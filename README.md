# Attendance Management System Using Facial Recognition

A high-performance Desktop Attendance Management System powered by Computer Vision (OpenCV Haar Cascades and LBPH Face Recognizer) and Tkinter, featuring integrated student registration, real-time facial recognition attendance marking, CSV import/export, and seamless dual-database support (MySQL and SQLite).

---

## Key Features

- **Teacher / Admin Authentication**: Secure login and registration with security-question password recovery.
- **Student Profile Management**: Full CRUD operations for student records (department, course, semester, roll number, contact details).
- **Webcam Dataset Capture**: Automated face cropping and sample generation (100 grayscale face samples per student).
- **LBPH Model Training**: Real-time training of Local Binary Patterns Histograms (LBPH) classifier, generating `clf.xml`.
- **Facial Recognition Attendance**: Real-time webcam face detection and recognition with high-confidence matching and duplicate-prevention logging.
- **Dual Database Architecture**: Zero-setup standalone mode using SQLite (`face_recognizer.db`) with automatic MySQL support (`face_recognizer1`) when a MySQL server is configured.
- **CSV Import & Export**: Direct integration with spreadsheet-compatible attendance records.
- **Cross-Platform Compatibility**: Fully compatible with macOS, Windows, and Linux.

---

## Project Structure

```
Face-Recognition-main/
├── attendance.py              # Attendance panel with CSV and database synchronization
├── build_desktop.py           # Automated PyInstaller packaging script
├── clf.xml                    # Pre-trained LBPH face recognition model
├── data_img/                  # Dataset directory containing facial training samples
├── database.sql               # MySQL DDL schema script
├── databaseTest.py            # Database health-check utility
├── db.py                      # Unified database manager (MySQL + SQLite fallback)
├── developer.py               # Developer team attribution panel
├── face_recognition.py        # Real-time webcam face recognition and attendance engine
├── haarcascade_frontalface_default.xml # OpenCV Haar Cascade model for frontal face detection
├── helpsupport.py             # Help, support, and community links
├── Image_GUI/                 # UI assets and graphics
├── login.py                   # Authentication and password recovery interface
├── main.py                    # Main system dashboard
├── register.py                # New user / teacher registration window
├── requirements.txt           # Project dependencies
├── run.py                     # One-click system launcher and environment validator
├── student.py                 # Student management and dataset generation interface
├── train.py                   # LBPH model training interface
└── utils.py                   # Cross-platform asset resolvers and Pillow helpers
```

---

## Getting Started

### 1. Prerequisites
- **Python 3.8+**
- **Webcam** (for dataset capture and face recognition)
- *(Optional)* **MySQL Server** (if you prefer MySQL over the built-in SQLite engine)

### 2. Environment Setup

Clone or open the repository directory:
```bash
cd Face-Recognition-main
```

Create and activate a virtual environment:
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

---

## Database Configuration

The application automatically defaults to a portable, zero-setup **SQLite database** (`face_recognizer.db`). No configuration or database installation is required to start using the system immediately.

### Using MySQL (Optional)
If you wish to connect to a MySQL server:
1. Import the schema script:
   ```bash
   mysql -u root -p < database.sql
   ```
2. Copy `.env.example` to `.env` and set your credentials:
   ```env
   DB_ENGINE=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=face_recognizer1
   ```

Verify database connectivity at any time:
```bash
python databaseTest.py
```

---

## Running the Application

Launch the application using the master launcher:
```bash
python run.py
```

Alternatively, launch the login screen directly:
```bash
python login.py
```

### Default Credentials
- **Username**: `admin`
- **Password**: `admin`

---

## Workflow Guide

1. **User Registration / Login**:
   - Register a new account or log in using `admin` / `admin`.
2. **Add Students**:
   - Navigate to **Student Panel**.
   - Fill in student details and click **Save**.
3. **Capture Face Samples**:
   - Select the student from the table and click **Take Pic**.
   - Position the student in front of the webcam until 100 face samples are saved into `data_img/`.
4. **Train Classifier**:
   - Open **Data Train** from the main dashboard.
   - Click **Train Dataset** to fit the LBPH classifier.
5. **Mark Attendance**:
   - Open **Face Detector**.
   - When a student's face is recognized with confidence > 77%, their attendance is logged to `attendance.csv` and the database.
   - Press `Enter`, `Q`, or `Esc` to close the webcam feed.
6. **Review & Export Attendance**:
   - Open **Attendance** panel to view, update, import, or export logs to CSV.

---

## Packaging as Desktop Application

To create a standalone executable (`.exe` on Windows or `.app` on macOS):
```bash
pip install pyinstaller
python build_desktop.py
```
The compiled application will be generated in the `dist/` directory.

---

## License & Credits
Developed by the Face Recognition System Team. Distributed for educational and administrative attendance tracking purposes.
