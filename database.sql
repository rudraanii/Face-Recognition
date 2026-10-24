-- ========================================================
-- Database Schema for Face Recognition Attendance System
-- Target: MySQL 5.7+ / 8.0+ / MariaDB
-- ========================================================

CREATE DATABASE IF NOT EXISTS face_recognizer1;
USE face_recognizer1;

-- 1. Teacher / Admin Registration Table
CREATE TABLE IF NOT EXISTS regteach (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    cnum VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL PRIMARY KEY,
    ss_que VARCHAR(100) NOT NULL,
    s_ans VARCHAR(100) NOT NULL,
    pwd VARCHAR(50) NOT NULL
);

-- 2. Student Records Table
CREATE TABLE IF NOT EXISTS student (
    Student_ID VARCHAR(50) NOT NULL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Department VARCHAR(50) NOT NULL,
    Course VARCHAR(50) NOT NULL,
    Year VARCHAR(50) NOT NULL,
    Semester VARCHAR(50) NOT NULL,
    Division VARCHAR(50) NOT NULL,
    Gender VARCHAR(50) NOT NULL,
    DOB VARCHAR(50) NOT NULL,
    Mobile_No VARCHAR(50) NOT NULL,
    Address VARCHAR(200) NOT NULL,
    Roll_No VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Teacher_Name VARCHAR(100) NOT NULL,
    PhotoSample VARCHAR(50) NOT NULL
);

-- 3. Student Attendance Log Table
CREATE TABLE IF NOT EXISTS stdattendance (
    std_id VARCHAR(50) NOT NULL,
    std_roll_no VARCHAR(50) NOT NULL,
    std_name VARCHAR(100) NOT NULL,
    std_time VARCHAR(50) NOT NULL,
    std_date VARCHAR(50) NOT NULL,
    std_attendance VARCHAR(50) NOT NULL
);

-- Seed an initial admin user (Optional, email: admin@admin.com, password: admin)
INSERT IGNORE INTO regteach (fname, lname, cnum, email, ss_que, s_ans, pwd)
VALUES ('Admin', 'User', '0000000000', 'admin@admin.com', 'Your Nick Name', 'admin', 'admin');
