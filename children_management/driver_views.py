from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
import cv2
import numpy as np
from .models import Driver, RecognitionLog
from .forms import DriverForm
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
import os
import base64
from PIL import Image
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASCADE_PATH = os.path.join(BASE_DIR, 'children_management', 'static', 'children_management', 'haarcascade_frontalface_default.xml')
DATASETFACE_PATH = os.path.join(BASE_DIR, 'children_management', 'static', 'children_management', 'datasetface')
RECOGNIZER_PATH = os.path.join(BASE_DIR, 'children_management', 'static', 'children_management', 'recognizer', 'trainingdata.yml')

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)


def base(request):
    return render(request, 'children_management/register_driver.html')


@login_required(login_url='login')
def main_dashboard(request):
    drivers = Driver.objects.all()
    context = {
        "section": "dashboard",
        "number_of_drivers": drivers.count(), 
    }
    return render(request, 'dashboard.html', context)


def handle_face_image(face_data_uri, driver_id):
    if face_data_uri:
        _, encoded_data = face_data_uri.split(',', 1)
        decoded_data = base64.b64decode(encoded_data)
        image = Image.open(BytesIO(decoded_data))
        image_path = f'driver_faces/{driver_id}.png'
        image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
        image.save(image_full_path)
        return image_path
    return None


def register_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.save()  # Save the driver instance first to generate an ID

            face_data_uri = request.POST.get('face_image')
            image_path = handle_face_image(face_data_uri, driver.id)
            if image_path:
                driver.face_image = image_path

            driver.save()
            return redirect(reverse('capture_and_train_driver', args=[driver.id]))  # Redirect to capture_and_train_driver with driver_id
    else:
        form = DriverForm()

    return render(request, 'children_management/register_driver.html', {'form': form})


@login_required(login_url='login')
def capture_and_train(request, driver_id):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return JsonResponse({"error": "Could not open video device"})

    sample_num = 0
    while True:
        ret, img = cap.read()
        if not ret:
            return JsonResponse({"error": "Failed to capture image"})

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sample_num += 1
            face_img = gray[y:y + h, x:x + w]

            face_img = cv2.GaussianBlur(face_img, (5, 5), 0)
            face_img = cv2.equalizeHist(face_img)

            cv2.imwrite(os.path.join(DATASETFACE_PATH, f"user_{driver_id}_{sample_num}.jpg"), face_img)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Face", img)

        if cv2.waitKey(1) & 0xFF == ord('q') or sample_num >= 50:
            break

    cap.release()
    cv2.destroyAllWindows()

    train_recognizer()
    return JsonResponse({"status": "Training completed"})


def start_recognition(request):
    recognize_faces()
    return redirect('dashboard')


def train_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = get_images_with_id(DATASETFACE_PATH)

    if len(faces) == 0 or len(ids) == 0:
        print("Error: No training data found")
        return

    recognizer.train(faces, ids)
    if not os.path.exists(os.path.dirname(RECOGNIZER_PATH)):
        os.makedirs(os.path.dirname(RECOGNIZER_PATH))
    recognizer.save(RECOGNIZER_PATH)
    cv2.destroyAllWindows()


def get_images_with_id(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    faces = []
    ids = []

    if not image_paths:
        print("No .jpg files found in the specified directory:", path)
        return faces, ids

    for image_path in image_paths:
        face_img = Image.open(image_path).convert('L')
        face_np = np.array(face_img, np.uint8)
        try:
            id = int(os.path.split(image_path)[-1].split(".")[0].split("_")[1])
        except (IndexError, ValueError):
            print("Invalid file name format:", image_path)
            continue

        faces.append(face_np)
        ids.append(id)
        faces.append(cv2.flip(face_np, 1))
        ids.append(id)

        cv2.imshow("Training", face_np)
        cv2.waitKey(10)

    return faces, np.array(ids)


def get_profile(driver_id):
    try:
        return Driver.objects.get(id=driver_id)
    except Driver.DoesNotExist:
        return None


def recognize_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(RECOGNIZER_PATH)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open video device")
        return

    confidence_threshold = 50

    while True:
        ret, img = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            driver_id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < confidence_threshold:
                profile = get_profile(driver_id)
                if profile:
                    if RecognitionLog.log_recognition(profile):
                        cv2.putText(img, f"Name: {profile.first_name} {profile.last_name}", (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (0, 255, 127), 2)
                        cv2.putText(img, f"Email: {profile.email}", (x, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (0, 255, 127), 2)
                        cv2.putText(img, f"Phone: {profile.phone_number}", (x, y + h + 70), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (0, 255, 127), 2)
                        cv2.putText(img, f"Address: {profile.address}", (x, y + h + 95), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (0, 255, 127), 2)
                        cv2.putText(img, f"Child's Unique Number: {profile.childs_unique_number}", (x, y + h + 120), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (0, 255, 127), 2)

                        # Add checkbox and pickup status display
                        pickup_status = 'Child Not Yet Picked'
                        log = RecognitionLog.objects.filter(driver=profile).first()
                        if log:
                            pickup_status = 'Child Picked' if log.child_picked else 'Child Not Yet Picked'
                        cv2.putText(img, pickup_status, (x, y + h + 145), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127), 2)

                        # Draw checkbox
                        checkbox_x = x + 20
                        checkbox_y = y + h + 170
                        checkbox_size = 30
                        cv2.rectangle(img, (checkbox_x, checkbox_y), (checkbox_x + checkbox_size, checkbox_y + checkbox_size), (255, 255, 255), 2)
                        if log:
                            if log.child_picked:
                                cv2.line(img, (checkbox_x, checkbox_y), (checkbox_x + checkbox_size, checkbox_y + checkbox_size), (0, 255, 0), 2)
                                cv2.line(img, (checkbox_x + checkbox_size, checkbox_y), (checkbox_x, checkbox_y + checkbox_size), (0, 255, 0), 2)

                    else:
                        cv2.putText(img, "Face recognized but not logged", (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
            else:
                cv2.putText(img, "Face not recognized", (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("FACE", img)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def recognition_logs(request):
    recent_logs = RecognitionLog.objects.filter(recognition_time__gte=timezone.now() - timedelta(minutes=1000)).order_by('-recognition_time')
    return render(request, 'children_management/recognition_logs.html', {'recent_logs': recent_logs})


def update_pickup_status(request, log_id):
    if request.method == 'POST':
        try:
            log = RecognitionLog.objects.get(id=log_id)
            log.child_picked = not log.child_picked
            log.pickup_time = timezone.now() if log.child_picked else None
            log.save()
            return JsonResponse({
                'child_picked': log.child_picked,
                'pickup_time': log.pickup_time.strftime('%Y-%m-%d %H:%M:%S') if log.pickup_time else None
            })
        except RecognitionLog.DoesNotExist:
            return JsonResponse({'error': 'Log not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def drivers_list(request):
    drivers = Driver.objects.all()
    context = {"section": "drivers_list", 'drivers': drivers}
    return render(request, 'drivers_list.html', context)
