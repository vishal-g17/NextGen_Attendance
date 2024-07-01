# import face_recognition
# import cv2
# import numpy as np
# import csv
# from datetime import datetime

# # Initialize video capture
# video_capture = cv2.VideoCapture(0)

# # Load known faces
# vishal_image = face_recognition.load_image_file("faces/vishal.jpg")
# vishal_encoding = face_recognition.face_encodings(vishal_image)[0]
# # vishal_encoding = face_recognition.face_encodings(vishal_image)

# known_face_encodings = [vishal_encoding]
# known_face_names = ["vishal"]

# # List of expected students
# students = known_face_names.copy()

# # Initialize face locations and encodings
# face_locations = []
# face_encodings = []

# # Get the current date for the CSV filename
# now = datetime.now()
# current_date = now.strftime("%Y-%m-%d")

# # Open CSV file for writing attendance
# f = open(f"{current_date}.csv", "w+", newline="")
# lnwriter = csv.writer(f)

# while True:
#     # Capture a single frame of video
#     ret, frame = video_capture.read()
#     if not ret:
#         break

#     # Resize frame for faster processing
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

#     # Find all face locations and face encodings in the current frame
#     face_locations = face_recognition.face_locations(rgb_small_frame)
#     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

#     for face_encoding in face_encodings:
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#         face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
#         best_match_index = np.argmin(face_distance)

#         name = "Unknown"
#         if matches[best_match_index]:
#             name = known_face_names[best_match_index]

#         # Display the name if a known person is recognized
#         if name in known_face_names:
#             font = cv2.FONT_HERSHEY_SIMPLEX
#             bottom_left_corner_of_text = (10, 100)
#             font_scale = 1.5
#             font_color = (255, 0, 10)
#             thickness = 3
#             line_type = 2
#             cv2.putText(frame, name + " Present", bottom_left_corner_of_text, font, font_scale, font_color, thickness, line_type)

#             if name in students:
#                 students.remove(name)
#                 current_time = now.strftime("%H-%M-%S")
#                 lnwriter.writerow([name, current_time])

#     # Display the resulting frame
#     cv2.imshow("Attendance", frame)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# # Release the capture and close windows
# video_capture.release()
# cv2.destroyAllWindows()
# f.close()

# ****************************************************************************************************************************************************

# for many student just un sbki seperate pic with name face folder me daalni h

import face_recognition
import cv2
import numpy as np
from datetime import datetime
import os
from db import init_db, insert_attendance

# Path to the directory containing images of students
students_images_path = "faces"

def initialize_webcam():
    video_capture = cv2.VideoCapture(0)  # 0 means default Open webcam
    return video_capture

def initialize_droidcam():
    droidcam_index = 1  # Adjust this index based on DroidCam's camera index
    video_capture = cv2.VideoCapture(droidcam_index)  # Open DroidCam-connected camera
    return video_capture

def capture_attendance(video_capture):
    # Load known faces
    known_face_encodings = []
    known_face_names = []
    for image_name in os.listdir(students_images_path):
        if image_name.endswith(('.jpg', '.jpeg', '.png')):
            student_image = face_recognition.load_image_file(f"{students_images_path}/{image_name}")
            student_encoding = face_recognition.face_encodings(student_image)[0]
            known_face_encodings.append(student_encoding)
            known_face_names.append(os.path.splitext(image_name)[0])

    # Initialize list of expected students
    students = known_face_names.copy()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)

            name = "Unknown"
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            if name in known_face_names:
                cv2.putText(frame, name + " Present", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 10), 3, 2)

                if name in students:
                    students.remove(name)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    insert_attendance(name, now.strftime("%Y-%m-%d"), current_time)

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Example: Select webcam or DroidCam (uncomment one)
    # video_capture = initialize_webcam()
    video_capture = initialize_droidcam()

    capture_attendance(video_capture)



