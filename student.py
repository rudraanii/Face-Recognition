from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
from utils import get_asset_path, LANCZOS_RESAMPLE
import db

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Student Management Panel")

        # ----------- Variables -------------------
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_mob = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_radio1 = StringVar()
        self.var_searchTX = StringVar()
        self.var_search = StringVar()

        # Header image  
        img = Image.open(get_asset_path("banner.jpg"))
        img = img.resize((1366, 130), LANCZOS_RESAMPLE)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # Background image 
        bg1 = Image.open(get_asset_path("bg3.jpg"))
        bg1 = bg1.resize((1366, 768), LANCZOS_RESAMPLE)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # Title section
        title_lb1 = Label(bg_img, text="Student Management Panel", font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Main frame
        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=5, y=55, width=1355, height=510)

        # Left Frame: Student Details
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details",
                                font=("verdana", 12, "bold"), fg="navyblue")
        left_frame.place(x=10, y=10, width=660, height=480)

        # Current Course Frame
        current_course_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Current Course",
                                          font=("verdana", 11, "bold"), fg="navyblue")
        current_course_frame.place(x=10, y=5, width=635, height=120)

        # Department
        dep_label = Label(current_course_frame, text="Department", font=("verdana", 10, "bold"), bg="white", fg="navyblue")
        dep_label.grid(row=0, column=0, padx=5, pady=8, sticky=W)

        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, width=15, font=("verdana", 10), state="readonly")
        dep_combo["values"] = ("Select Department", "SCSE", "SEEE", "SME", "SA", "SBE")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=5, pady=8, sticky=W)

        # Course
        cou_label = Label(current_course_frame, text="Course", font=("verdana", 10, "bold"), bg="white", fg="navyblue")
        cou_label.grid(row=0, column=2, padx=5, pady=8, sticky=W)

        cou_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, width=15, font=("verdana", 10), state="readonly")
        cou_combo["values"] = ("Select Course", "Btech", "BSC", "MTECH", "MSC", "INT.MTECH")
        cou_combo.current(0)
        cou_combo.grid(row=0, column=3, padx=5, pady=8, sticky=W)

        # Year
        year_label = Label(current_course_frame, text="Year", font=("verdana", 10, "bold"), bg="white", fg="navyblue")
        year_label.grid(row=1, column=0, padx=5, pady=8, sticky=W)

        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, width=15, font=("verdana", 10), state="readonly")
        year_combo["values"] = ("Select Year", "2017-21", "2018-22", "2019-23", "2020-24", "2021-25", "2022-26")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=5, pady=8, sticky=W)

        # Semester
        sem_label = Label(current_course_frame, text="Semester", font=("verdana", 10, "bold"), bg="white", fg="navyblue")
        sem_label.grid(row=1, column=2, padx=5, pady=8, sticky=W)

        sem_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, width=15, font=("verdana", 10), state="readonly")
        sem_combo["values"] = ("Select Semester", "Semester-1", "Semester-2", "Semester-3", "Semester-4",
                               "Semester-5", "Semester-6", "Semester-7", "Semester-8")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=5, pady=8, sticky=W)

        # Class Student Information Frame
        class_student_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Student Information",
                                         font=("verdana", 11, "bold"), fg="navyblue")
        class_student_frame.place(x=10, y=130, width=635, height=250)

        # Std ID
        Label(class_student_frame, text="Std-ID:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=0, column=0, padx=5, pady=4, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_std_id, width=15, font=("verdana", 10)).grid(row=0, column=1, padx=5, pady=4, sticky=W)

        # Std Name
        Label(class_student_frame, text="Std-Name:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=0, column=2, padx=5, pady=4, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_std_name, width=15, font=("verdana", 10)).grid(row=0, column=3, padx=5, pady=4, sticky=W)

        # Division
        Label(class_student_frame, text="Division:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=1, column=0, padx=5, pady=4, sticky=W)
        div_combo = ttk.Combobox(class_student_frame, textvariable=self.var_div, width=13, font=("verdana", 10), state="readonly")
        div_combo["values"] = ("Morning", "Evening")
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=5, pady=4, sticky=W)

        # Roll No
        Label(class_student_frame, text="Roll-No:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=1, column=2, padx=5, pady=4, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_roll, width=15, font=("verdana", 10)).grid(row=1, column=3, padx=5, pady=4, sticky=W)

        # Gender
        Label(class_student_frame, text="Gender:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=2, column=0, padx=5, pady=4, sticky=W)
        gen_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender, width=13, font=("verdana", 10), state="readonly")
        gen_combo["values"] = ("Male", "Female", "Other")
        gen_combo.current(0)
        gen_combo.grid(row=2, column=1, padx=5, pady=4, sticky=W)

        # DOB
        Label(class_student_frame, text="DOB:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=2, column=2, padx=5, pady=4, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_dob, width=15, font=("verdana", 10)).grid(row=2, column=3, padx=5, pady=4, sticky=W)

        # Email
        Label(class_student_frame, text="Email:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=3, column=0, padx=5, pady=4, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_email, width=15, font=("verdana", 10)).grid(row=3, column=1, padx=5, pady=4, sticky=W)

        # Mob-No
        Label(class_student_frame, text="Mob-No:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=3, column=2, padx=5, pady=4, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_mob, width=15, font=("verdana", 10)).grid(row=3, column=3, padx=5, pady=4, sticky=W)

        # Address
        Label(class_student_frame, text="Address:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=4, column=0, padx=5, pady=4, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_address, width=15, font=("verdana", 10)).grid(row=4, column=1, padx=5, pady=4, sticky=W)

        # Teacher Name
        Label(class_student_frame, text="Teacher:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=4, column=2, padx=5, pady=4, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_teacher, width=15, font=("verdana", 10)).grid(row=4, column=3, padx=5, pady=4, sticky=W)

        # Radio Buttons for Photo Sample
        self.var_radio1.set("Yes")
        r1 = ttk.Radiobutton(class_student_frame, text="Take Photo Sample", variable=self.var_radio1, value="Yes")
        r1.grid(row=5, column=0, columnspan=2, padx=5, pady=4, sticky=W)
        r2 = ttk.Radiobutton(class_student_frame, text="No Photo Sample", variable=self.var_radio1, value="No")
        r2.grid(row=5, column=2, columnspan=2, padx=5, pady=4, sticky=W)

        # Button Frame (Bottom of Left Frame)
        btn_frame = Frame(left_frame, bd=2, bg="white", relief=RIDGE)
        btn_frame.place(x=10, y=390, width=635, height=60)

        Button(btn_frame, command=self.add_data, text="Save", width=7, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=0, padx=4, pady=10)
        Button(btn_frame, command=self.update_data, text="Update", width=7, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=1, padx=4, pady=10)
        Button(btn_frame, command=self.delete_data, text="Delete", width=7, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=2, padx=4, pady=10)
        Button(btn_frame, command=self.reset_data, text="Reset", width=7, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=3, padx=4, pady=10)
        Button(btn_frame, command=self.generate_dataset, text="Take Pic", width=9, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=4, padx=4, pady=10)

        # Right Frame: Student Search & Table
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Records",
                                 font=("verdana", 12, "bold"), fg="navyblue")
        right_frame.place(x=680, y=10, width=660, height=480)

        # Search System Frame
        search_frame = LabelFrame(right_frame, bd=2, bg="white", relief=RIDGE, text="Search System",
                                  font=("verdana", 11, "bold"), fg="navyblue")
        search_frame.place(x=10, y=5, width=635, height=75)

        Label(search_frame, text="Search By:", font=("verdana", 10, "bold"), fg="navyblue", bg="white").grid(row=0, column=0, padx=5, pady=8, sticky=W)

        search_combo = ttk.Combobox(search_frame, textvariable=self.var_searchTX, width=12, font=("verdana", 10), state="readonly")
        search_combo["values"] = ("Select", "Roll_No", "Student_ID", "Name")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=5, pady=8, sticky=W)

        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, width=15, font=("verdana", 10))
        search_entry.grid(row=0, column=2, padx=5, pady=8, sticky=W)

        Button(search_frame, command=self.search_data, text="Search", width=8, font=("verdana", 10, "bold"), fg="white", bg="navyblue").grid(row=0, column=3, padx=5, pady=8)
        Button(search_frame, command=self.fetch_data, text="Show All", width=8, font=("verdana", 10, "bold"), fg="white", bg="navyblue").grid(row=0, column=4, padx=5, pady=8)

        # Table Frame
        table_frame = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=10, y=85, width=635, height=365)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame, column=(
            "ID", "Name", "Dep", "Course", "Year", "Sem", "Div", "Gender",
            "DOB", "Mob-No", "Address", "Roll-No", "Email", "Teacher", "Photo"
        ), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        cols = [
            ("ID", "StudentID", 80), ("Name", "Name", 120), ("Dep", "Department", 100),
            ("Course", "Course", 80), ("Year", "Year", 80), ("Sem", "Semester", 90),
            ("Div", "Division", 80), ("Gender", "Gender", 80), ("DOB", "DOB", 90),
            ("Mob-No", "Mob-No", 100), ("Address", "Address", 120), ("Roll-No", "Roll-No", 80),
            ("Email", "Email", 130), ("Teacher", "Teacher", 110), ("Photo", "PhotoSample", 90)
        ]
        for col_id, heading_text, col_width in cols:
            self.student_table.heading(col_id, text=heading_text)
            self.student_table.column(col_id, width=col_width)

        self.student_table["show"] = "headings"
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()

    # ================== Database Functions ==============================
    def validate_inputs(self):
        if (self.var_dep.get() == "Select Department" or
            self.var_course.get() == "Select Course" or
            self.var_year.get() == "Select Year" or
            self.var_semester.get() == "Select Semester" or
            self.var_std_id.get().strip() == "" or
            self.var_std_name.get().strip() == "" or
            self.var_roll.get().strip() == ""):
            messagebox.showerror("Validation Error", "Department, Course, Year, Semester, Student ID, Name, and Roll No are required!", parent=self.root)
            return False
        return True

    def add_data(self):
        if not self.validate_inputs():
            return
        try:
            conn = db.get_connection()
            mycursor = conn.cursor()
            mycursor.execute(
                "INSERT INTO student (Student_ID, Name, Department, Course, Year, Semester, Division, Gender, DOB, Mobile_No, Address, Roll_No, Email, Teacher_Name, PhotoSample) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    self.var_std_id.get().strip(),
                    self.var_std_name.get().strip(),
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_div.get(),
                    self.var_gender.get(),
                    self.var_dob.get().strip(),
                    self.var_mob.get().strip(),
                    self.var_address.get().strip(),
                    self.var_roll.get().strip(),
                    self.var_email.get().strip(),
                    self.var_teacher.get().strip(),
                    self.var_radio1.get()
                )
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Student record successfully saved!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Could not save student:\n{str(es)}", parent=self.root)

    def fetch_data(self):
        try:
            conn = db.get_connection()
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM student")
            data = mycursor.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in data:
                self.student_table.insert("", END, values=row)
            conn.close()
        except Exception as es:
            print("[WARN] Error fetching student data:", es)

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content.get("values", [])
        if len(data) >= 15:
            self.var_std_id.set(data[0])
            self.var_std_name.set(data[1])
            self.var_dep.set(data[2])
            self.var_course.set(data[3])
            self.var_year.set(data[4])
            self.var_semester.set(data[5])
            self.var_div.set(data[6])
            self.var_gender.set(data[7])
            self.var_dob.set(data[8])
            self.var_mob.set(data[9])
            self.var_address.set(data[10])
            self.var_roll.set(data[11])
            self.var_email.set(data[12])
            self.var_teacher.set(data[13])
            self.var_radio1.set(data[14])

    def update_data(self):
        if not self.validate_inputs():
            return
        try:
            update = messagebox.askyesno("Update", "Do you want to update this student's details?", parent=self.root)
            if update:
                conn = db.get_connection()
                mycursor = conn.cursor()
                mycursor.execute(
                    "UPDATE student SET Name=%s, Department=%s, Course=%s, Year=%s, Semester=%s, Division=%s, "
                    "Gender=%s, DOB=%s, Mobile_No=%s, Address=%s, Roll_No=%s, Email=%s, Teacher_Name=%s, PhotoSample=%s "
                    "WHERE Student_ID=%s",
                    (
                        self.var_std_name.get().strip(),
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_div.get(),
                        self.var_gender.get(),
                        self.var_dob.get().strip(),
                        self.var_mob.get().strip(),
                        self.var_address.get().strip(),
                        self.var_roll.get().strip(),
                        self.var_email.get().strip(),
                        self.var_teacher.get().strip(),
                        self.var_radio1.get(),
                        self.var_std_id.get().strip()
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Student details updated successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def delete_data(self):
        std_id = self.var_std_id.get().strip()
        if std_id == "":
            messagebox.showerror("Error", "Student ID is required to delete a record!", parent=self.root)
            return
        try:
            confirm = messagebox.askyesno("Delete Record", f"Are you sure you want to delete student ID {std_id}?", parent=self.root)
            if confirm:
                conn = db.get_connection()
                mycursor = conn.cursor()
                mycursor.execute("DELETE FROM student WHERE Student_ID=%s", (std_id,))
                conn.commit()
                conn.close()
                self.fetch_data()
                self.reset_data()
                messagebox.showinfo("Deleted", "Student record successfully deleted!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def reset_data(self):
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_div.set("Morning")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_mob.set("")
        self.var_address.set("")
        self.var_roll.set("")
        self.var_email.set("")
        self.var_teacher.set("")
        self.var_radio1.set("Yes")

    def search_data(self):
        search_field = self.var_searchTX.get()
        search_val = self.var_search.get().strip()

        if search_field == "Select" or search_val == "":
            messagebox.showerror("Error", "Please select a search column and enter a search value!", parent=self.root)
            return

        try:
            conn = db.get_connection()
            my_cursor = conn.cursor()
            # Map combo value to column name
            col_map = {"Roll_No": "Roll_No", "Student_ID": "Student_ID", "Name": "Name"}
            col_name = col_map.get(search_field, "Roll_No")

            sql = f"SELECT * FROM student WHERE {col_name} LIKE %s"
            my_cursor.execute(sql, (f"%{search_val}%",))
            rows = my_cursor.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert("", END, values=row)
            conn.close()

            if not rows:
                messagebox.showinfo("Search Result", "No matching student records found.", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Search failed:\n{str(es)}", parent=self.root)

    # ===================== OpenCV Dataset Generation =======================
    def generate_dataset(self):
        if not self.validate_inputs():
            return

        std_id_val = self.var_std_id.get().strip()
        cascade_file = get_asset_path("haarcascade_frontalface_default.xml")
        if not os.path.exists(cascade_file):
            cascade_file = "haarcascade_frontalface_default.xml"

        if not os.path.exists(cascade_file):
            messagebox.showerror("Error", "Face Cascade XML file not found!", parent=self.root)
            return

        os.makedirs("data_img", exist_ok=True)
        face_classifier = cv2.CascadeClassifier(cascade_file)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Could not access the webcam.\nPlease ensure your camera is connected and application has camera permissions.", parent=self.root)
            return

        img_id = 0
        messagebox.showinfo("Camera Starting", "Position yourself in front of the camera.\nTaking 100 sample images.\nPress ENTER to stop early.", parent=self.root)

        while True:
            ret, my_frame = cap.read()
            if not ret or my_frame is None:
                break

            gray = cv2.cvtColor(my_frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                img_id += 1
                face_crop = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face_crop, (200, 200))
                file_path = f"data_img/student.{std_id_val}.{img_id}.jpg"
                cv2.imwrite(file_path, face_resized)
                
                cv2.putText(face_resized, f"Sample: {img_id}/100", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 2)
                cv2.imshow("Capturing Face Samples (Press ENTER or Q to cancel)", face_resized)
                break  # capture primary face

            key = cv2.waitKey(1) & 0xFF
            if key in (13, ord('q'), ord('Q'), 27) or img_id >= 100:
                break

        cap.release()
        cv2.destroyAllWindows()

        # Update PhotoSample flag in database
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE student SET PhotoSample='Yes' WHERE Student_ID=%s", (std_id_val,))
            conn.commit()
            conn.close()
            self.fetch_data()
        except Exception:
            pass

        messagebox.showinfo("Completed", f"Face dataset generated successfully!\nCaptured {img_id} samples for Student ID: {std_id_val}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
