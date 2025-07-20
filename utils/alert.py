import tkinter as tk
from tkinter import ttk

def system_notification(ip, port):
    root = tk.Tk()
    root.title("Honeypot Alert")
    root.configure(bg="#1e1e1e")
    root.geometry("420x160")
    root.resizable(False, False)

    # Center the window on screen
    x = (root.winfo_screenwidth() // 2) - (420 // 2)
    y = (root.winfo_screenheight() // 2) - (160 // 2)
    root.geometry(f"+{x}+{y}")

    # Keep the window on top
    root.attributes("-topmost", True)

    # Optional: Remove default icon (but not entire border)
    try:
        root.iconbitmap('')  # No icon
    except:
        pass

    # Message Frame
    message = f"⚠ Connection detected from:\n{ip}:{port}"
    label = tk.Label(
        root,
        text=message,
        font=("Segoe UI", 13, "bold"),
        fg="#f54242",
        bg="#1e1e1e",
        justify="center"
    )
    label.pack(pady=25)

    # Button Styling
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Alert.TButton",
                    foreground="#ffffff",
                    background="#2d89ef",
                    font=("Segoe UI", 11),
                    padding=6)
    style.map("Alert.TButton",
              background=[('active', '#1e70bf')])

    # OK Button
    ok_button = ttk.Button(root, text="OK", style="Alert.TButton", command=root.destroy)
    ok_button.pack()

    root.mainloop()

