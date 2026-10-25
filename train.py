from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
from tkinter import messagebox
from utils import get_asset_path, LANCZOS_RESAMPLE

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Train Dataset Panel")

        # Header image  
        img = Image.open(get_asset_path("banner.jpg"))
        img = img.resize((1366, 130), LANCZOS_RESAMPLE)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # Background image 
        bg1 = Image.open(get_asset_path("t_bg1.jpg"))
        bg1 = bg1.resize((1366, 768), LANCZOS_RESAMPLE)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # Title section
        title_lb1 = Label(bg_img, text="Face Recognition Model Training",
                          font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Training button
        std_img_btn = Image.open(get_asset_path("t_btn1.png"))
        std_img_btn = std_img_btn.resize((180, 180), LANCZOS_RESAMPLE)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.train_classifier, image=self.std_img1, cursor="hand2")
        std_b1.place(x=600, y=170, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.train_classifier, text="Train Dataset", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=600, y=350, width=180, height=45)

    # ================== Function for Training ===================
    def train_classifier(self):
        data_dir = "data_img"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)

        valid_extensions = (".jpg", ".jpeg", ".png")
        image_files = [
            os.path.join(data_dir, f) for f in os.listdir(data_dir)
            if f.lower().endswith(valid_extensions)
        ]

        if not image_files:
            messagebox.showwarning(
                "No Data Found",
                "No training image samples found in 'data_img' directory!\nPlease use 'Take Pic' in the Student Panel to capture sample images first.",
                parent=self.root
            )
            return

        # Get currently enrolled students from database
        enrolled_ids = set()
        try:
            import db
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Student_ID FROM student")
            for row in cur.fetchall():
                sid_str = str(row[0]).strip()
                if sid_str.isdigit():
                    enrolled_ids.add(int(sid_str))
            conn.close()
        except Exception as e:
            print("[WARN] Could not retrieve enrolled student list:", e)

        faces = []
        ids = []

        for image_path in image_files:
            try:
                filename = os.path.basename(image_path)
                parts = filename.split(".")
                
                # Check for format: student.<id>.<sample>.ext or stdudent.<id>.<sample>.ext
                if len(parts) >= 3 and parts[1].isdigit():
                    student_id = int(parts[1])
                    # Only train on samples of students currently enrolled in the database
                    if enrolled_ids and student_id not in enrolled_ids:
                        continue
                else:
                    continue

                pil_img = Image.open(image_path).convert("L")  # Convert to grayscale
                image_np = np.array(pil_img, "uint8")
                image_np = cv2.resize(image_np, (200, 200))
                image_np = cv2.equalizeHist(image_np)

                faces.append(image_np)
                ids.append(student_id)

                if self.root:
                    cv2.imshow("Training Dataset in Progress... (Press ESC to skip)", image_np)
                    if cv2.waitKey(1) == 27:
                        break
            except Exception as e:
                print(f"[WARN] Skipping corrupted image file {image_path}: {e}")
                continue

        cv2.destroyAllWindows()

        if not faces:
            msg = "No valid sample images found for enrolled students in 'data_img'!\nPlease enroll students and capture sample photos first."
            if self.root:
                messagebox.showerror("Training Error", msg, parent=self.root)
            else:
                print("[ERROR]", msg)
            return

        try:
            ids_np = np.array(ids, dtype=np.int32)
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids_np)
            clf.write("clf.xml")

            msg = f"LBPH Classifier trained successfully on {len(faces)} images across {len(set(ids))} enrolled student(s)!\nModel saved to clf.xml."
            if self.root:
                messagebox.showinfo("Training Completed", msg, parent=self.root)
            else:
                print("[SUCCESS]", msg)
        except Exception as es:
            if self.root:
                messagebox.showerror("Training Failed", f"Could not train classifier model:\n{str(es)}", parent=self.root)
            else:
                print("[ERROR] Training failed:", es)

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()