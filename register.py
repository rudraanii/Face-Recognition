from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from utils import get_asset_path, LANCZOS_RESAMPLE
import db

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher / Admin Registration")
        self.root.geometry("1366x768+0+0")

        # Variables
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_cnum = StringVar()
        self.var_email = StringVar()
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()
        self.var_cpwd = StringVar()
        self.var_check = IntVar()

        self.bg = ImageTk.PhotoImage(file=get_asset_path("bgReg.jpg"))
        
        lb1_bg = Label(self.root, image=self.bg)
        lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame = Frame(self.root, bg="#F2F2F2")
        frame.place(x=100, y=80, width=900, height=580)

        get_str = Label(frame, text="User Registration", font=("times new roman", 28, "bold"), fg="#002B53", bg="#F2F2F2")
        get_str.place(x=320, y=50)

        # First Name
        Label(frame, text="First Name:", font=("times new roman", 14, "bold"), fg="#002B53", bg="#F2F2F2").place(x=100, y=130)
        self.txtfname = ttk.Entry(frame, textvariable=self.var_fname, font=("times new roman", 14))
        self.txtfname.place(x=100, y=160, width=270)

        # Last Name
        Label(frame, text="Last Name:", font=("times new roman", 14, "bold"), fg="#002B53", bg="#F2F2F2").place(x=100, y=200)
        self.txtlname = ttk.Entry(frame, textvariable=self.var_lname, font=("times new roman", 14))
        self.txtlname.place(x=100, y=230, width=270)

        # Contact Number
        Label(frame, text="Contact No:", font=("times new roman", 14, "bold"), fg="#002B53", bg="#F2F2F2").place(x=500, y=130)
        self.txtcnum = ttk.Entry(frame, textvariable=self.var_cnum, font=("times new roman", 14))
        self.txtcnum.place(x=500, y=160, width=270)

        # Email
        Label(frame, text="Email Address:", font=("times new roman", 14, "bold"), fg="#002B53", bg="#F2F2F2").place(x=500, y=200)
        self.txtemail = ttk.Entry(frame, textvariable=self.var_email, font=("times new roman", 14))
        self.txtemail.place(x=500, y=230, width=270)

        # Security Question
        Label(frame, text="Security Question:", font=("times new roman", 14, "bold"), fg="#002B53", bg="#F2F2F2").place(x=100, y=270)
        self.combo_security = ttk.Combobox(frame, textvariable=self.var_ssq, font=("times new roman", 13), state="readonly")
        self.combo_security["values"] = ("Select", "Your Date of Birth", "Your Nick Name", "Your Favorite Book")
        self.combo_security.current(0)
        self.combo_security.place(x=100, y=300, width=270)

        # Security Answer
        Label(frame, text="Security Answer:", font=("times new roman", 14, "bold"), fg="#002B53", bg="#F2F2F2").place(x=100, y=340)
        self.txtsa = ttk.Entry(frame, textvariable=self.var_sa, font=("times new roman", 14))
        self.txtsa.place(x=100, y=370, width=270)

        # Password
        Label(frame, text="Password:", font=("times new roman", 14, "bold"), fg="#002B53", bg="#F2F2F2").place(x=500, y=270)
        self.txtpwd = ttk.Entry(frame, textvariable=self.var_pwd, font=("times new roman", 14), show="*")
        self.txtpwd.place(x=500, y=300, width=270)

        # Confirm Password
        Label(frame, text="Confirm Password:", font=("times new roman", 14, "bold"), fg="#002B53", bg="#F2F2F2").place(x=500, y=340)
        self.txtcpwd = ttk.Entry(frame, textvariable=self.var_cpwd, font=("times new roman", 14), show="*")
        self.txtcpwd.place(x=500, y=370, width=270)

        # Terms Checkbox
        Checkbutton(frame, variable=self.var_check, text="I Agree to the Terms & Conditions",
                    font=("times new roman", 13, "bold"), fg="#002B53", bg="#F2F2F2").place(x=100, y=420)

        # Register Button
        Button(frame, command=self.reg, text="Register", font=("times new roman", 15, "bold"),
               bd=0, relief=RIDGE, fg="#fff", bg="#002B53", activeforeground="white", activebackground="#007ACC").place(x=100, y=460, width=270, height=40)

        # Return to Login Button
        Button(frame, command=self.root.destroy, text="Back to Login", font=("times new roman", 15, "bold"),
               bd=0, relief=RIDGE, fg="#fff", bg="#555", activeforeground="white", activebackground="#333").place(x=500, y=460, width=270, height=40)

    def reg(self):
        fname = self.var_fname.get().strip()
        lname = self.var_lname.get().strip()
        cnum = self.var_cnum.get().strip()
        email = self.var_email.get().strip()
        ssq = self.var_ssq.get()
        sa = self.var_sa.get().strip()
        pwd = self.var_pwd.get().strip()
        cpwd = self.var_cpwd.get().strip()

        if not all([fname, lname, cnum, email, sa, pwd, cpwd]) or ssq == "Select":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        if pwd != cpwd:
            messagebox.showerror("Error", "Password and Confirm Password must match!", parent=self.root)
            return

        if self.var_check.get() == 0:
            messagebox.showerror("Error", "Please agree to the Terms & Conditions to proceed!", parent=self.root)
            return

        try:
            conn = db.get_connection()
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM regteach WHERE email=%s", (email,))
            row = mycursor.fetchone()
            if row is not None:
                messagebox.showerror("Error", "A user with this Email ID already exists. Please login or use a different email.", parent=self.root)
                conn.close()
                return

            mycursor.execute(
                "INSERT INTO regteach (fname, lname, cnum, email, ss_que, s_ans, pwd) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (fname, lname, cnum, email, ssq, sa, pwd)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration Successful! You may now log in.", parent=self.root)
            self.root.destroy()
        except Exception as es:
            messagebox.showerror("Error", f"Could not complete registration:\n{str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    app = Register(root)
    root.mainloop()