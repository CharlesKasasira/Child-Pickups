from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
# from .models import SyncInterval
import logging
import os
import cv2
import numpy as np
from PIL import Image


# logger = logging.getLogger('')

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = "face_recognition/dataset/"


def schedule_trainer():
    pass
#     sync = 1

#     scheduler = BackgroundScheduler()
#     scheduler.add_job(print("hello"), 'interval', minutes=sync)
#     scheduler.start()


# def get_images_with_id(path):
#     images_paths = [os.path.join("face_recognition/dataset/", f) for f in os.listdir("/Users/charleskasasira/Documents/SEM2/CS Project II/project/Child-Pickups/child_pickup/face_recognition/dataset/")]
#     faces = []
#     Ids = []
#     for single_image_path in images_paths:
#         print(single_image_path)
#         faceImg = Image.open(single_image_path).convert('L')
#         faceNp = np.array(faceImg, np.uint8)
#         id = int(os.path.split(single_image_path)[-1].split(".")[1])
#         print(id)
#         faces.append(faceNp)
#         Ids.append(id)
#         cv2.imshow("Training", faceNp)
#         cv2.waitKey(10)

#     return np.array(Ids), faces 

# def save_recognizer():
#     ids, faces = get_images_with_id(path)
#     recognizer.train(faces, ids)
#     recognizer.save("/Users/charleskasasira/Documents/SEM2/CS Project II/project/Child-Pickups/child_pickup/face_recognition/recognizer/trainingdata.yml")
#     cv2.destroyAllWindows()
#     return "Done"
