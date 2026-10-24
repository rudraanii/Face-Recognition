import db

def test_database():
    print("[TEST] Testing database connectivity and table schemas...")
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Test regteach
        cursor.execute("SELECT COUNT(*) FROM regteach")
        teachers_count = cursor.fetchone()[0]
        print(f"[OK] regteach table: {teachers_count} record(s)")

        # Test student
        cursor.execute("SELECT COUNT(*) FROM student")
        students_count = cursor.fetchone()[0]
        print(f"[OK] student table: {students_count} record(s)")

        # Test stdattendance
        cursor.execute("SELECT COUNT(*) FROM stdattendance")
        attendance_count = cursor.fetchone()[0]
        print(f"[OK] stdattendance table: {attendance_count} record(s)")

        conn.close()
        print("[SUCCESS] All database tables are accessible and ready for use!")
    except Exception as e:
        print(f"[ERROR] Database test encountered an issue: {e}")

if __name__ == "__main__":
    test_database()