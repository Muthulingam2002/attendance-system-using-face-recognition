import face_recognition
import cv2
import numpy as np
import csv
import psycopg2
import os
from datetime import datetime


video_capture = cv2.VideoCapture(0)

arron_image = face_recognition.load_image_file("photos/arron.jpg")
arron_encoding = face_recognition.face_encodings(arron_image)[0]

elon_image = face_recognition.load_image_file("photos/elon.jpg")
elon_encoding = face_recognition.face_encodings(elon_image)[0]

snowden_image = face_recognition.load_image_file("photos/snowden.png")
snowden_encoding = face_recognition.face_encodings(snowden_image)[0]

assange_image = face_recognition.load_image_file("photos/assange.png")
assange_encoding = face_recognition.face_encodings(assange_image)[0]

known_face_encoding = [
    arron_encoding,
    elon_encoding,
    snowden_encoding,
    assange_encoding
]

known_faces_names = [
    "arron swartz",
    "elon musk",
    "edward snowden",
    "jullian assange"
]

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open('today.csv', 'w+', newline='')
lnwriter = csv.writer(f)

#
# # Connect to the PostgreSQL database
# conn = psycopg2.connect(
#     database="mydatabase",
#     user="postgres",
#     password="kalam",
#     host="localhost",
#     port="5432"
# )



while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor = (255, 0, 0)
                thickness = 3
                lineType = 2

                cv2.putText(frame, name + ' Present',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            thickness,
                            lineType)

                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name, current_time])
    cv2.imshow("attendence system", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




# # Open a cursor to perform database operations
# cur = conn.cursor()
#
# # Define the SQL statement to insert data into a table
# sql = "INSERT INTO mytable ( name, time) VALUES ( %s, %s)"
#
# # Define the values to insert into the table
# values = ('value2', 'value3')
#
# # Execute the SQL statement with the provided values
# cur.execute(sql, values)
#
# # Commit the changes to the database
# conn.commit()
#
# # Close the cursor and connection
# cur.close()
# conn.close()
video_capture.release()
cv2.destroyAllWindows()
f.close()