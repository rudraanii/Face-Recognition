from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import csv
from tkinter import messagebox, filedialog
from utils import get_asset_path, LANCZOS_RESAMPLE
import db

mydata = []

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Attendance Management Panel")

        # ----------- Variables -------------------
        self.var_id = StringVar()
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_dep = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_attend = StringVar()

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
        title_lb1 = Label(bg_img, text="Student Attendance Panel", font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Main frame
        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=5, y=55, width=1355, height=510)

        # Left Label Frame (CSV Attendance)
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="CSV Attendance Details",
                                font=("verdana", 12, "bold"), fg="navyblue")
        left_frame.place(x=10, y=10, width=660, height=480)

        # Text boxes for Attendance Entry
        Label(left_frame, text="Std-ID:", font=("verdana", 11, "bold"), fg="navyblue", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_id, width=15, font=("verdana", 11)).grid(row=0, column=1, padx=5, pady=5, sticky=W)

        Label(left_frame, text="Roll-No:", font=("verdana", 11, "bold"), fg="navyblue", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_roll, width=15, font=("verdana", 11)).grid(row=0, column=3, padx=5, pady=5, sticky=W)

        Label(left_frame, text="Std-Name:", font=("verdana", 11, "bold"), fg="navyblue", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_name, width=15, font=("verdana", 11)).grid(row=1, column=1, padx=5, pady=5, sticky=W)

        Label(left_frame, text="Time:", font=("verdana", 11, "bold"), fg="navyblue", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_time, width=15, font=("verdana", 11)).grid(row=1, column=3, padx=5, pady=5, sticky=W)

        Label(left_frame, text="Date:", font=("verdana", 11, "bold"), fg="navyblue", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_date, width=15, font=("verdana", 11)).grid(row=2, column=1, padx=5, pady=5, sticky=W)

        Label(left_frame, text="Status:", font=("verdana", 11, "bold"), fg="navyblue", bg="white").grid(row=2, column=2, padx=5, pady=5, sticky=W)
        self.var_attend.set("Present")
        attend_combo = ttk.Combobox(left_frame, textvariable=self.var_attend, width=13, font=("verdana", 11), state="readonly")
        attend_combo["values"] = ("Status", "Present", "Absent")
        attend_combo.current(1)
        attend_combo.grid(row=2, column=3, padx=5, pady=5, sticky=W)

        # Left Table Frame (CSV Viewer)
        table_frame_left = Frame(left_frame, bd=2, bg="white", relief=RIDGE)
        table_frame_left.place(x=10, y=105, width=635, height=275)

        scroll_x_left = ttk.Scrollbar(table_frame_left, orient=HORIZONTAL)
        scroll_y_left = ttk.Scrollbar(table_frame_left, orient=VERTICAL)

        self.attendanceReport_left = ttk.Treeview(table_frame_left, column=("ID", "Roll_No", "Name", "Time", "Date", "Attend"),
                                                 xscrollcommand=scroll_x_left.set, yscrollcommand=scroll_y_left.set)

        scroll_x_left.pack(side=BOTTOM, fill=X)
        scroll_y_left.pack(side=RIGHT, fill=Y)
        scroll_x_left.config(command=self.attendanceReport_left.xview)
        scroll_y_left.config(command=self.attendanceReport_left.yview)

        for col, title, width in [("ID", "Std-ID", 80), ("Roll_No", "Roll.No", 90), ("Name", "Std-Name", 120),
                                  ("Time", "Time", 90), ("Date", "Date", 90), ("Attend", "Status", 80)]:
            self.attendanceReport_left.heading(col, text=title)
            self.attendanceReport_left.column(col, width=width)

        self.attendanceReport_left["show"] = "headings"
        self.attendanceReport_left.pack(fill=BOTH, expand=1)
        self.attendanceReport_left.bind("<ButtonRelease>", self.get_cursor_left)

        # Button Frame (Left)
        btn_frame_left = Frame(left_frame, bd=2, bg="white", relief=RIDGE)
        btn_frame_left.place(x=10, y=390, width=635, height=60)

        Button(btn_frame_left, command=self.importCsv, text="Import CSV", width=12, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=0, padx=6, pady=10)
        Button(btn_frame_left, command=self.exportCsv, text="Export CSV", width=12, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=1, padx=6, pady=10)
        Button(btn_frame_left, command=self.save_to_db, text="Save to DB", width=12, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=2, padx=6, pady=10)
        Button(btn_frame_left, command=self.reset_data, text="Reset", width=12, font=("verdana", 11, "bold"), fg="white", bg="navyblue").grid(row=0, column=3, padx=6, pady=10)

        # Right Label Frame (Database Attendance)
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Database Attendance Records",
                                 font=("verdana", 12, "bold"), fg="navyblue")
        right_frame.place(x=680, y=10, width=660, height=480)

        # Right Action Buttons
        Button(right_frame, command=self.update_data, text="Update Record", width=14, font=("verdana", 10, "bold"), fg="white", bg="navyblue").grid(row=0, column=0, padx=10, pady=8, sticky=W)
        Button(right_frame, command=self.delete_data, text="Delete Record", width=14, font=("verdana", 10, "bold"), fg="white", bg="navyblue").grid(row=0, column=1, padx=10, pady=8, sticky=W)
        Button(right_frame, command=self.fetch_data, text="Refresh", width=12, font=("verdana", 10, "bold"), fg="white", bg="navyblue").grid(row=0, column=2, padx=10, pady=8, sticky=W)

        # Right Table Frame (Database Records)
        table_frame_right = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame_right.place(x=10, y=50, width=635, height=400)

        scroll_x_right = ttk.Scrollbar(table_frame_right, orient=HORIZONTAL)
        scroll_y_right = ttk.Scrollbar(table_frame_right, orient=VERTICAL)

        self.attendanceReport = ttk.Treeview(table_frame_right, column=("ID", "Roll_No", "Name", "Time", "Date", "Attend"),
                                             xscrollcommand=scroll_x_right.set, yscrollcommand=scroll_y_right.set)

        scroll_x_right.pack(side=BOTTOM, fill=X)
        scroll_y_right.pack(side=RIGHT, fill=Y)
        scroll_x_right.config(command=self.attendanceReport.xview)
        scroll_y_right.config(command=self.attendanceReport.yview)

        for col, title, width in [("ID", "Std-ID", 80), ("Roll_No", "Roll.No", 90), ("Name", "Std-Name", 120),
                                  ("Time", "Time", 90), ("Date", "Date", 90), ("Attend", "Status", 80)]:
            self.attendanceReport.heading(col, text=title)
            self.attendanceReport.column(col, width=width)

        self.attendanceReport["show"] = "headings"
        self.attendanceReport.pack(fill=BOTH, expand=1)
        self.attendanceReport.bind("<ButtonRelease>", self.get_cursor_right)

        self.fetch_data()

        # Load local attendance.csv if present
        if os.path.exists("attendance.csv"):
            self.load_default_csv()

    # =============================== Database Operations =================
    def fetch_data(self):
        try:
            conn = db.get_connection()
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM stdattendance")
            data = mycursor.fetchall()
            self.attendanceReport.delete(*self.attendanceReport.get_children())
            for row in data:
                self.attendanceReport.insert("", END, values=row)
            conn.close()
        except Exception as es:
            print("[WARN] Error loading attendance records:", es)

    def update_data(self):
        if (self.var_id.get().strip() == "" or self.var_roll.get().strip() == "" or
            self.var_name.get().strip() == "" or self.var_attend.get() == "Status"):
            messagebox.showerror("Error", "Please fill all required fields before updating!", parent=self.root)
            return

        try:
            confirm = messagebox.askyesno("Update", "Do you want to update this attendance record?", parent=self.root)
            if confirm:
                conn = db.get_connection()
                mycursor = conn.cursor()
                mycursor.execute(
                    "UPDATE stdattendance SET std_roll_no=%s, std_name=%s, std_time=%s, std_date=%s, std_attendance=%s "
                    "WHERE std_id=%s AND std_date=%s",
                    (
                        self.var_roll.get().strip(),
                        self.var_name.get().strip(),
                        self.var_time.get().strip(),
                        self.var_date.get().strip(),
                        self.var_attend.get(),
                        self.var_id.get().strip(),
                        self.var_date.get().strip()
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Attendance record updated successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_id.get().strip() == "":
            messagebox.showerror("Error", "Student ID is required to delete record!", parent=self.root)
            return

        try:
            confirm = messagebox.askyesno("Delete", f"Do you want to delete attendance record for ID {self.var_id.get()}?", parent=self.root)
            if confirm:
                conn = db.get_connection()
                mycursor = conn.cursor()
                mycursor.execute("DELETE FROM stdattendance WHERE std_id=%s", (self.var_id.get().strip(),))
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Record deleted successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def save_to_db(self):
        if (self.var_id.get().strip() == "" or self.var_roll.get().strip() == "" or
            self.var_name.get().strip() == "" or self.var_attend.get() == "Status"):
            messagebox.showerror("Error", "Please select or enter an attendance row first!", parent=self.root)
            return

        try:
            conn = db.get_connection()
            mycursor = conn.cursor()
            mycursor.execute(
                "INSERT INTO stdattendance (std_id, std_roll_no, std_name, std_time, std_date, std_attendance) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (
                    self.var_id.get().strip(),
                    self.var_roll.get().strip(),
                    self.var_name.get().strip(),
                    self.var_time.get().strip(),
                    self.var_date.get().strip(),
                    self.var_attend.get()
                )
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Attendance record saved into database!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Could not save record: {str(es)}", parent=self.root)

    # ============================ CSV Functions ===========================
    def reset_data(self):
        self.var_id.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attend.set("Present")

    def load_default_csv(self):
        global mydata
        mydata = []
        try:
            with open("attendance.csv", "r", newline="\n") as f:
                reader = csv.reader(f)
                header = next(reader, None)  # skip header
                for row in reader:
                    if row and any(row):
                        mydata.append(row)
            self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
            for row in mydata:
                self.attendanceReport_left.insert("", END, values=row)
        except Exception as e:
            print("[WARN] Could not load default attendance.csv:", e)

    def importCsv(self):
        global mydata
        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Open Attendance CSV",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
            parent=self.root
        )
        if not fln:
            return

        mydata = []
        try:
            with open(fln, "r", newline="\n") as myfile:
                csvread = csv.reader(myfile)
                header = next(csvread, None)  # Skip header
                for row in csvread:
                    if row and any(row):
                        mydata.append(row)

            self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
            for row in mydata:
                self.attendanceReport_left.insert("", END, values=row)
            messagebox.showinfo("Success", f"Imported {len(mydata)} attendance record(s).", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Could not read CSV file:\n{str(es)}", parent=self.root)

    def exportCsv(self):
        try:
            items = self.attendanceReport_left.get_children()
            if not items:
                messagebox.showerror("Error", "No attendance records available to export!", parent=self.root)
                return

            fln = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Export Attendance to CSV",
                defaultextension=".csv",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
                parent=self.root
            )
            if not fln:
                return

            with open(fln, mode="w", newline="\n") as myfile:
                exp_write = csv.writer(myfile)
                exp_write.writerow(["Std_ID", "Roll_No", "Name", "Time", "Date", "Attendance"])
                for item in items:
                    exp_write.writerow(self.attendanceReport_left.item(item)["values"])

            messagebox.showinfo("Success", f"Data exported successfully to:\n{fln}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Could not export CSV:\n{str(es)}", parent=self.root)

    def get_cursor_left(self, event=""):
        cursor_focus = self.attendanceReport_left.focus()
        content = self.attendanceReport_left.item(cursor_focus)
        data = content.get("values", [])
        if len(data) >= 6:
            self.var_id.set(data[0])
            self.var_roll.set(data[1])
            self.var_name.set(data[2])
            self.var_time.set(data[3])
            self.var_date.set(data[4])
            self.var_attend.set(data[5])

    def get_cursor_right(self, event=""):
        cursor_focus = self.attendanceReport.focus()
        content = self.attendanceReport.item(cursor_focus)
        data = content.get("values", [])
        if len(data) >= 6:
            self.var_id.set(data[0])
            self.var_roll.set(data[1])
            self.var_name.set(data[2])
            self.var_time.set(data[3])
            self.var_date.set(data[4])
            self.var_attend.set(data[5])

if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()