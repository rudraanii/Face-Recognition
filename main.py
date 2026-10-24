from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from utils import get_asset_path, LANCZOS_RESAMPLE, open_directory
from train import Train
from student import Student
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
from helpsupport import Helpsupport

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face_Recognition_System")

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
        title_lb1 = Label(bg_img, text="Attendance Management System Using Facial Recognition",
                          font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # ---------------- Create buttons ----------------
        # 1. Student button
        std_img_btn = Image.open(get_asset_path("std1.jpg"))
        std_img_btn = std_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.student_pannels, image=self.std_img1, cursor="hand2")
        std_b1.place(x=250, y=100, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.student_pannels, text="Student Panel", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=250, y=280, width=180, height=45)

        # 2. Detect Face button
        det_img_btn = Image.open(get_asset_path("det1.jpg"))
        det_img_btn = det_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img, command=self.face_rec, image=self.det_img1, cursor="hand2")
        det_b1.place(x=480, y=100, width=180, height=180)

        det_b1_1 = Button(bg_img, command=self.face_rec, text="Face Detector", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        det_b1_1.place(x=480, y=280, width=180, height=45)

        # 3. Attendance System button
        att_img_btn = Image.open(get_asset_path("att.jpg"))
        att_img_btn = att_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img, command=self.attendance_pannel, image=self.att_img1, cursor="hand2")
        att_b1.place(x=710, y=100, width=180, height=180)

        att_b1_1 = Button(bg_img, command=self.attendance_pannel, text="Attendance", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        att_b1_1.place(x=710, y=280, width=180, height=45)

        # 4. Help Support button
        hlp_img_btn = Image.open(get_asset_path("hlp.jpg"))
        hlp_img_btn = hlp_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.hlp_img1 = ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(bg_img, command=self.helpSupport, image=self.hlp_img1, cursor="hand2")
        hlp_b1.place(x=940, y=100, width=180, height=180)

        hlp_b1_1 = Button(bg_img, command=self.helpSupport, text="Help Support", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        hlp_b1_1.place(x=940, y=280, width=180, height=45)

        # 5. Train button
        tra_img_btn = Image.open(get_asset_path("tra1.jpg"))
        tra_img_btn = tra_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.tra_img1 = ImageTk.PhotoImage(tra_img_btn)

        tra_b1 = Button(bg_img, command=self.train_pannels, image=self.tra_img1, cursor="hand2")
        tra_b1.place(x=250, y=330, width=180, height=180)

        tra_b1_1 = Button(bg_img, command=self.train_pannels, text="Data Train", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        tra_b1_1.place(x=250, y=510, width=180, height=45)

        # 6. Photo / Dataset button
        pho_img_btn = Image.open(get_asset_path("t_bg1.jpg"))
        pho_img_btn = pho_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.pho_img1 = ImageTk.PhotoImage(pho_img_btn)

        pho_b1 = Button(bg_img, command=self.open_img, image=self.pho_img1, cursor="hand2")
        pho_b1.place(x=480, y=330, width=180, height=180)

        pho_b1_1 = Button(bg_img, command=self.open_img, text="Dataset", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        pho_b1_1.place(x=480, y=510, width=180, height=45)

        # 7. Developers button
        dev_img_btn = Image.open(get_asset_path("dev.jpg"))
        dev_img_btn = dev_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.dev_img1 = ImageTk.PhotoImage(dev_img_btn)

        dev_b1 = Button(bg_img, command=self.developr, image=self.dev_img1, cursor="hand2")
        dev_b1.place(x=710, y=330, width=180, height=180)

        dev_b1_1 = Button(bg_img, command=self.developr, text="Developers", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        dev_b1_1.place(x=710, y=510, width=180, height=45)

        # 8. Exit button
        exi_img_btn = Image.open(get_asset_path("exi.jpg"))
        exi_img_btn = exi_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.exi_img1 = ImageTk.PhotoImage(exi_img_btn)

        exi_b1 = Button(bg_img, command=self.Close, image=self.exi_img1, cursor="hand2")
        exi_b1.place(x=940, y=330, width=180, height=180)

        exi_b1_1 = Button(bg_img, command=self.Close, text="Exit", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        exi_b1_1.place(x=940, y=510, width=180, height=45)

    # ================== Function for Open Images Folder ==================
    def open_img(self):
        open_directory("data_img")

    # ================== Button Actions =====================
    def student_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_rec(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance_pannel(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def developr(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)

    def helpSupport(self):
        self.new_window = Toplevel(self.root)
        self.app = Helpsupport(self.new_window)

    def Close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
