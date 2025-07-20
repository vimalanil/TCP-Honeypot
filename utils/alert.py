# utils/alert.py
import threading
import tkinter as tk
from PIL import Image, ImageTk

def system_notification(title, message, image_path="dashboard/static/alert.png"):
    def show_popup():
        root = tk.Tk()
        root.title(title)
        root.geometry("450x400")
        root.configure(bg='black')
        root.resizable(False, False)

        try:
            img = Image.open(image_path)
            img = img.resize((150, 150))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(root, image=photo, bg='black')
            img_label.image = photo
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Image error: {e}")

        tk.Label(root, text=message, fg='red', bg='black',
                 font=("Helvetica", 14), wraplength=400, justify="center").pack(pady=10)
        tk.Button(root, text="OK", command=root.destroy, font=("Helvetica", 12),
                  bg='gray', fg='white').pack(pady=10)
        root.mainloop()

    threading.Thread(target=show_popup).start()
