from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from register import Register
from main import Face_Recognition_System
from utils import get_asset_path, LANCZOS_RESAMPLE
import db

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Face Recognition Attendance System")
        self.root.geometry("1366x768+0+0")

        # Variables 
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()

        self.bg = ImageTk.PhotoImage(file=get_asset_path("loginBg1.jpg"))
        
        lb1_bg = Label(self.root, image=self.bg)
        lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame1 = Frame(self.root, bg="#002B53")
        frame1.place(x=560, y=170, width=340, height=450)

        img1 = Image.open(get_asset_path("log1.png"))
        img1 = img1.resize((100, 100), LANCZOS_RESAMPLE)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lb1img1 = Label(image=self.photoimage1, bg="#002B53")
        lb1img1.place(x=690, y=175, width=100, height=100)

        get_str = Label(frame1, text="Login", font=("times new roman", 20, "bold"), fg="white", bg="#002B53")
        get_str.place(x=140, y=100)

        # Username label & entry
        username = Label(frame1, text="Username / Email:", font=("times new roman", 15, "bold"), fg="white", bg="#002B53")
        username.place(x=30, y=160)

        self.txtuser = ttk.Entry(frame1, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=33, y=190, width=270)

        # Password label & entry
        pwd = Label(frame1, text="Password:", font=("times new roman", 15, "bold"), fg="white", bg="#002B53")
        pwd.place(x=30, y=230)

        self.txtpwd = ttk.Entry(frame1, font=("times new roman", 15, "bold"), show="*")
        self.txtpwd.place(x=33, y=260, width=270)

        # Login button
        loginbtn = Button(frame1, command=self.login, text="Login", font=("times new roman", 15, "bold"),
                          bd=0, relief=RIDGE, fg="#002B53", bg="white", activeforeground="white", activebackground="#007ACC")
        loginbtn.place(x=33, y=320, width=270, height=35)

        # Register button
        regbtn = Button(frame1, command=self.reg, text="Register", font=("times new roman", 10, "bold"),
                        bd=0, relief=RIDGE, fg="white", bg="#002B53", activeforeground="orange", activebackground="#002B53")
        regbtn.place(x=33, y=370, width=70, height=20)

        # Forgot Password button
        forbtn = Button(frame1, command=self.forget_pwd, text="Forgot Password", font=("times new roman", 10, "bold"),
                        bd=0, relief=RIDGE, fg="white", bg="#002B53", activeforeground="orange", activebackground="#002B53")
        forbtn.place(x=120, y=370, width=120, height=20)

    # Open registration window
    def reg(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)

    def login(self):
        username = self.txtuser.get().strip()
        password = self.txtpwd.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "All Fields are Required!")
            return

        # Built-in Admin bypass
        if username == "admin" and password == "admin":
            messagebox.showinfo("Success", "Welcome to Attendance Management System Using Facial Recognition")
            self.new_window = Toplevel(self.root)
            self.app = Face_Recognition_System(self.new_window)
            return

        try:
            conn = db.get_connection()
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM regteach WHERE email=%s AND pwd=%s", (username, password))
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Username or Password!")
            else:
                messagebox.showinfo("Success", f"Welcome {row[0]} {row[1]}!")
                self.new_window = Toplevel(self.root)
                self.app = Face_Recognition_System(self.new_window)
            conn.close()
        except Exception as es:
            messagebox.showerror("Database Error", f"Error connecting to database:\n{str(es)}")

    # ======================= Reset Password Function =============================
    def reset_pass(self):
        if self.var_ssq.get() == "Select":
            messagebox.showerror("Error", "Select the Security Question!", parent=self.root2)
        elif self.var_sa.get().strip() == "":
            messagebox.showerror("Error", "Please Enter the Answer!", parent=self.root2)
        elif self.var_pwd.get().strip() == "":
            messagebox.showerror("Error", "Please Enter the New Password!", parent=self.root2)
        else:
            try:
                conn = db.get_connection()
                mycursor = conn.cursor()
                query = "SELECT * FROM regteach WHERE email=%s AND ss_que=%s AND s_ans=%s"
                value = (self.txtuser.get().strip(), self.var_ssq.get(), self.var_sa.get().strip())
                mycursor.execute(query, value)
                row = mycursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please Enter the Correct Answer!", parent=self.root2)
                else:
                    query = "UPDATE regteach SET pwd=%s WHERE email=%s"
                    value = (self.var_pwd.get().strip(), self.txtuser.get().strip())
                    mycursor.execute(query, value)
                    conn.commit()
                    messagebox.showinfo("Info", "Successfully reset your password. Please login with your new Password!", parent=self.root2)
                    self.root2.destroy()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root2)

    # ===================== Forgot Password Window =========================================
    def forget_pwd(self):
        email_val = self.txtuser.get().strip()
        if email_val == "":
            messagebox.showerror("Error", "Please Enter the Email ID in Username field to reset Password!")
            return

        try:
            conn = db.get_connection()
            mycursor = conn.cursor()
            query = "SELECT * FROM regteach WHERE email=%s"
            mycursor.execute(query, (email_val,))
            row = mycursor.fetchone()
            conn.close()

            if row is None:
                messagebox.showerror("Error", "Email ID not found in database!")
                return
        except Exception as es:
            messagebox.showerror("Database Error", f"Due to: {str(es)}")
            return

        self.root2 = Toplevel()
        self.root2.title("Forget Password")
        self.root2.geometry("400x400+610+170")
        
        l = Label(self.root2, text="Forgot Password", font=("times new roman", 24, "bold"), fg="#002B53", bg="#fff")
        l.place(x=0, y=10, relwidth=1)

        ssq = Label(self.root2, text="Select Security Question:", font=("times new roman", 14, "bold"), fg="#002B53")
        ssq.place(x=65, y=70)

        self.combo_security = ttk.Combobox(self.root2, textvariable=self.var_ssq, font=("times new roman", 13), state="readonly")
        self.combo_security["values"] = ("Select", "Your Date of Birth", "Your Nick Name", "Your Favorite Book")
        self.combo_security.current(0)
        self.combo_security.place(x=65, y=100, width=270)

        sa = Label(self.root2, text="Security Answer:", font=("times new roman", 14, "bold"), fg="#002B53")
        sa.place(x=65, y=140)

        self.txtsa = ttk.Entry(self.root2, textvariable=self.var_sa, font=("times new roman", 13))
        self.txtsa.place(x=65, y=170, width=270)

        new_pwd = Label(self.root2, text="New Password:", font=("times new roman", 14, "bold"), fg="#002B53")
        new_pwd.place(x=65, y=210)

        self.new_pwd_entry = ttk.Entry(self.root2, textvariable=self.var_pwd, font=("times new roman", 13), show="*")
        self.new_pwd_entry.place(x=65, y=240, width=270)

        resetbtn = Button(self.root2, command=self.reset_pass, text="Reset Password", font=("times new roman", 14, "bold"),
                          bd=0, relief=RIDGE, fg="#fff", bg="#002B53", activeforeground="white", activebackground="#007ACC")
        resetbtn.place(x=65, y=300, width=270, height=35)

if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()