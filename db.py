import os
import sqlite3
from utils import BASE_DIR

# Database configuration with environment variable support
DB_ENGINE = os.getenv("DB_ENGINE", "auto")  # 'mysql', 'sqlite', or 'auto'
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123keshav")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "face_recognizer1")

SQLITE_PATH = os.path.join(BASE_DIR, "face_recognizer.db")

class SQLiteCursorWrapper:
    """Wraps SQLite cursor so %s placeholders match MySQL style syntax."""
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        adapted_query = query.replace("%s", "?")
        if params is not None:
            # Handle single elements passed as non-tuples or booleans
            if not isinstance(params, (tuple, list)):
                params = (params,)
            return self.cursor.execute(adapted_query, params)
        return self.cursor.execute(adapted_query)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def close(self):
        self.cursor.close()

class SQLiteConnectionWrapper:
    """Wraps sqlite3.Connection to provide MySQL-compatible interface."""
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return SQLiteCursorWrapper(self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

def _init_sqlite_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regteach (
            fname TEXT,
            lname TEXT,
            cnum TEXT,
            email TEXT PRIMARY KEY,
            ss_que TEXT,
            s_ans TEXT,
            pwd TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            Student_ID TEXT PRIMARY KEY,
            Name TEXT,
            Department TEXT,
            Course TEXT,
            Year TEXT,
            Semester TEXT,
            Division TEXT,
            Gender TEXT,
            DOB TEXT,
            Mobile_No TEXT,
            Address TEXT,
            Roll_No TEXT,
            Email TEXT,
            Teacher_Name TEXT,
            PhotoSample TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stdattendance (
            std_id TEXT,
            std_roll_no TEXT,
            std_name TEXT,
            std_time TEXT,
            std_date TEXT,
            std_attendance TEXT
        )
    """)
    conn.commit()

def _init_mysql_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regteach (
            fname VARCHAR(50),
            lname VARCHAR(50),
            cnum VARCHAR(50),
            email VARCHAR(100) PRIMARY KEY,
            ss_que VARCHAR(100),
            s_ans VARCHAR(100),
            pwd VARCHAR(50)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            Student_ID VARCHAR(50) PRIMARY KEY,
            Name VARCHAR(100),
            Department VARCHAR(50),
            Course VARCHAR(50),
            Year VARCHAR(50),
            Semester VARCHAR(50),
            Division VARCHAR(50),
            Gender VARCHAR(50),
            DOB VARCHAR(50),
            Mobile_No VARCHAR(50),
            Address VARCHAR(200),
            Roll_No VARCHAR(50),
            Email VARCHAR(100),
            Teacher_Name VARCHAR(100),
            PhotoSample VARCHAR(50)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stdattendance (
            std_id VARCHAR(50),
            std_roll_no VARCHAR(50),
            std_name VARCHAR(100),
            std_time VARCHAR(50),
            std_date VARCHAR(50),
            std_attendance VARCHAR(50)
        )
    """)
    conn.commit()

def get_connection():
    """
    Returns an active database connection.
    Attempts MySQL first if requested or configured, and falls back to SQLite
    to guarantee the app runs standalone without manual database setup.
    """
    global DB_ENGINE
    if DB_ENGINE in ("mysql", "auto"):
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT,
                database=DB_NAME
            )
            return conn
        except Exception as e:
            if DB_ENGINE == "mysql":
                raise e
            # In auto mode, fallback to SQLite
            pass

    # Use SQLite
    raw_conn = sqlite3.connect(SQLITE_PATH)
    conn = SQLiteConnectionWrapper(raw_conn)
    _init_sqlite_tables(conn)
    return conn

def init_database():
    """Initializes tables in whichever database is active."""
    conn = get_connection()
    try:
        if isinstance(conn, SQLiteConnectionWrapper):
            _init_sqlite_tables(conn)
            print("[INFO] Database initialized with SQLite:", SQLITE_PATH)
        else:
            _init_mysql_tables(conn)
            print("[INFO] Database initialized with MySQL:", DB_NAME)
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
