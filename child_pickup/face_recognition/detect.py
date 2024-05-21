import cv2
import numpy as np
import os
import sqlite3
from django.db import connection
from django.conf import settings
import django

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingdata.yml")


# Set the settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'child_pickup.settings')
django.setup()


def get_profile(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM face_recognition_userprofile WHERE user_id = %s", [id])
        profile = cursor.fetchone()  # Fetch only one row
    return profile
    # conn = sqlite3.connect("sqlite.db")
    # # cursor = conn.execute("show tables;")
    # cursor = conn.execute("SELECT * FROM face_recognition_userprofile WHERE id=?", (id,))
    # profile = cursor.fetchone()  # Fetch only one row
    # conn.close()
    # return profile


while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, conf = recognizer.predict(gray[y:y + h, x:x + w])
        print("Recognized ID:", id)
        profile = get_profile(id)
        if profile is not None:
            print("Profile:", profile)
            cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127),
                        2)
            cv2.putText(img, "Age: " + str(profile[2]), (x, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127),
                        2)

    cv2.imshow("FACE", img)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
