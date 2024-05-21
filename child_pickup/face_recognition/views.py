from django.shortcuts import render
from django.http import JsonResponse
import cv2
import numpy as np
import base64
import os
from child_pickup.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from io import BytesIO
from PIL import Image

def capture_face(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        if image_data:
            # Decode the image
            format, imgstr = image_data.split(';base64,')
            nparr = np.frombuffer(base64.b64decode(imgstr), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Process the image (e.g., face detection)
            face_recognition = FaceRecognition()
            face_id = face_recognition.process_image(img)

            return JsonResponse({'face_id': face_id})
    return render(request, 'face_recognition/camera_feed.html')

class FaceRecognition:
    def __init__(self):
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_id = 2  # Example face ID, modify as needed
        self.sampleNum = 0
        self.dataset_path = os.path.join(BASE_DIR, 'face_recognition', 'dataset')
        self.trainer_path = os.path.join(BASE_DIR, 'face_recognition', 'trainer', 'trainer.yml')

    def process_image(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_img = gray[y:y + h, x:x + w]
                face_file = os.path.join(self.dataset_path, f'user.{self.face_id}.{self.sampleNum}.jpg')
                cv2.imwrite(face_file, face_img)
                self.sampleNum += 1
            return self.face_id
        return None
    

    @staticmethod
    @csrf_exempt
    def register(request):
        if request.method == 'POST':
            image_data = request.POST.get('image')
            name = request.POST.get('name')
            email = request.POST.get('email')

            # print(image_data)

            if not image_data or not name or not email:
                return JsonResponse({'error': 'Image, name, and email are required'}, status=400)

            user_profile = UserProfile(name=name, email=email, image_path=image_data)
            user_profile.save()
            face_id = 3

            img = Image.open(BytesIO(base64.b64decode(image_data)))
            img_np = np.array(img)
            face_recognition = FaceRecognition()
            processed_image, sample_num = face_recognition.process_image(img_np)

            # face_recognition.train()

            return JsonResponse({'message': f'Save for face ID {face_id}', 'face_id': face_id})
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

def list_users(request):
    users = UserProfile.objects.all()
    return render(request, 'face_recognition/list_users.html', {'users': users})
    
def register(request):
    return render(request, 'face_recognition/camera_feed.html')

def login(request):
    return render(request, 'face_recognition/camera_feed.html')

def listParents(request):
    return render(request, 'face_recognition/camera_feed.html')
    
