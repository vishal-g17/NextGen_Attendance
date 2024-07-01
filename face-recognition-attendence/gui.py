import tkinter as tk
from tkinter import messagebox
from main import capture_attendance, initialize_webcam, initialize_droidcam

def start_attendance():
    if var.get() == 1:
        video_capture = initialize_webcam()
    elif var.get() == 2:
        video_capture = initialize_droidcam()
    else:
        messagebox.showerror("Error", "Please select a camera source.")
        return

    capture_attendance(video_capture)
    messagebox.showinfo("Info", "Attendance Captured Successfully!")

root = tk.Tk()
root.title("Face Recognition Attendance System")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Face Recognition Attendance System", font=("Helvetica", 16))
label.pack(pady=10)

var = tk.IntVar()

webcam_radio = tk.Radiobutton(frame, text="Webcam", variable=var, value=1)
webcam_radio.pack(pady=5)

droidcam_radio = tk.Radiobutton(frame, text="DroidCam", variable=var, value=2)
droidcam_radio.pack(pady=5)

start_button = tk.Button(frame, text="Start Attendance", command=start_attendance)
start_button.pack(pady=10)

root.mainloop()
