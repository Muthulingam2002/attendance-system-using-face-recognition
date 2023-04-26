# These are import statements in Python that import various libraries and modules that are required
# for the code to run.
import face_recognition
import cv2
import numpy as np
import csv
import psycopg2
import os
from datetime import datetime


# `video_capture = cv2.VideoCapture(0)` is initializing a video capture object that captures video
# from the default camera (index 0) of the device.
video_capture = cv2.VideoCapture(0)

# These lines of code are loading images of known faces from files and encoding them using the
# `face_encodings()` function from the `face_recognition` library. The resulting encodings are stored
# in variables named after the corresponding person's name. These encodings will be used later to
# compare with the encodings of faces detected in the video stream to identify the people present.
arron_image = face_recognition.load_image_file("photos/arron.jpg")
arron_encoding = face_recognition.face_encodings(arron_image)[0]

elon_image = face_recognition.load_image_file("photos/elon.jpg")
elon_encoding = face_recognition.face_encodings(elon_image)[0]

snowden_image = face_recognition.load_image_file("photos/snowden.png")
snowden_encoding = face_recognition.face_encodings(snowden_image)[0]

assange_image = face_recognition.load_image_file("photos/assange.png")
assange_encoding = face_recognition.face_encodings(assange_image)[0]

muthu_image = face_recognition.load_image_file("photos/muthu.jpg")
muthu_encoding = face_recognition.face_encodings(muthu_image)[0]

# `known_face_encoding` is a list of face encodings for known people, which are obtained by using the
# `face_encodings()` function from the `face_recognition` library on their respective images.
known_face_encoding = [
    arron_encoding,
    elon_encoding,
    snowden_encoding,
    assange_encoding,
    muthu_encoding
]

known_faces_names = [
    "arron swartz",
    "elon musk",
    "edward snowden",
    "jullian assange",
    "muthulingam"
]

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

# `now = datetime.now()` is creating a datetime object that represents the current date and time.
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open('today.csv', 'w+', newline='')
lnwriter = csv.writer(f)


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="mydatabase",
    user="postgres",
    password="kalam",
    host="localhost",
    port="5432"
)



# This is the main loop of the program that continuously captures frames from the video stream using
# the `video_capture.read()` function. The captured frame is then resized to a smaller size using
# `cv2.resize()` and converted to RGB format using `[:, :, ::-1]`.
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
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_time])

                    # Open a cursor to perform database operations
                    cur = conn.cursor()

                    # Define the SQL statement to insert data into a table
                    sql = "INSERT INTO mytable ( name, time,date) VALUES ( %s, %s,%s)"

                    # Define the values to insert into the table
                    values = (name, current_time,current_date)

                    # Execute the SQL statement with the provided values
                    cur.execute(sql, values)

                    # Commit the changes to the database
                    conn.commit()

                    # Close the cursor and connection
                    cur.close()
                    conn.close()

    # `cv2.imshow("attendence system", frame)` is displaying the current frame with the detected faces
    # and their names using the OpenCV library. `cv2.waitKey(1) & 0xFF == ord('q')` waits for a key
    # event for 1 millisecond and checks if the key pressed is 'q'. If the 'q' key is pressed, the
    # loop is broken and the program exits.
    cv2.imshow("attendence system", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()