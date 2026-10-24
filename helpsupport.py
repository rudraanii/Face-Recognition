from tkinter import *
from PIL import Image, ImageTk
import webbrowser
from utils import get_asset_path, LANCZOS_RESAMPLE

class Helpsupport:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Help & Support Panel")

        # Header image  
        img = Image.open(get_asset_path("banner.jpg"))
        img = img.resize((1366, 130), LANCZOS_RESAMPLE)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # Background image 
        bg1 = Image.open(get_asset_path("bg4.png"))
        bg1 = bg1.resize((1366, 768), LANCZOS_RESAMPLE)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # Title section
        title_lb1 = Label(bg_img, text="Help & Support Resources", font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # 1. Website button
        std_img_btn = Image.open(get_asset_path("web.png"))
        std_img_btn = std_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.website, image=self.std_img1, cursor="hand2")
        std_b1.place(x=250, y=180, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.website, text="Official Website", cursor="hand2", font=("tahoma", 14, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=250, y=360, width=180, height=45)

        # 2. Facebook button
        det_img_btn = Image.open(get_asset_path("fb.png"))
        det_img_btn = det_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img, command=self.facebook, image=self.det_img1, cursor="hand2")
        det_b1.place(x=480, y=180, width=180, height=180)

        det_b1_1 = Button(bg_img, command=self.facebook, text="Community", cursor="hand2", font=("tahoma", 14, "bold"), bg="white", fg="navyblue")
        det_b1_1.place(x=480, y=360, width=180, height=45)

        # 3. Youtube button
        att_img_btn = Image.open(get_asset_path("yt.png"))
        att_img_btn = att_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img, command=self.youtube, image=self.att_img1, cursor="hand2")
        att_b1.place(x=710, y=180, width=180, height=180)

        att_b1_1 = Button(bg_img, command=self.youtube, text="Tutorials / YouTube", cursor="hand2", font=("tahoma", 13, "bold"), bg="white", fg="navyblue")
        att_b1_1.place(x=710, y=360, width=180, height=45)

        # 4. Gmail button
        hlp_img_btn = Image.open(get_asset_path("gmail.png"))
        hlp_img_btn = hlp_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.hlp_img1 = ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(bg_img, command=self.gmail, image=self.hlp_img1, cursor="hand2")
        hlp_b1.place(x=940, y=180, width=180, height=180)

        hlp_b1_1 = Button(bg_img, command=self.gmail, text="Email Support", cursor="hand2", font=("tahoma", 14, "bold"), bg="white", fg="navyblue")
        hlp_b1_1.place(x=940, y=360, width=180, height=45)

    def website(self):
        webbrowser.open("https://github.com/rudraanii/Face-Recognition", new=1)

    def facebook(self):
        webbrowser.open("https://www.facebook.com/", new=1)

    def youtube(self):
        webbrowser.open("https://www.youtube.com/", new=1)

    def gmail(self):
        webbrowser.open("mailto:support@example.com", new=1)

if __name__ == "__main__":
    root = Tk()
    obj = Helpsupport(root)
    root.mainloop()