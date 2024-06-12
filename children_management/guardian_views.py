from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
import cv2
import numpy as np
from .models import Guardian, GuardiansLog
from .forms import GuardianForm
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
import os
import base64
from PIL import Image
import pytz
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARDIAN_CASCADE_PATH = os.path.join(BASE_DIR, 'children_management', 'static', 'children_management', 'haarcascade_frontalface_default.xml')
GUARDIAN_DATASETFACE_PATH = os.path.join(BASE_DIR, 'children_management', 'static', 'children_management', 'guardians', 'datasetface')
GUARDIAN_RECOGNIZER_PATH = os.path.join(BASE_DIR, 'children_management', 'static', 'children_management', 'guardians', 'recognizer', 'trainingdata.yml')

face_cascade = cv2.CascadeClassifier(GUARDIAN_CASCADE_PATH)


def base(request):
    return render(request, 'children_management/register_guardian.html')


@login_required(login_url='login')
def main_dashboard(request):
    guardians = Guardian.objects.all()
    context = {
        "section": "dashboard",
        "number_of_guardians": guardians.count(), 
    }
    return render(request, 'dashboard.html', context)


def handle_face_image(face_data_uri, guardian_id):
    if face_data_uri:
        _, encoded_data = face_data_uri.split(',', 1)
        decoded_data = base64.b64decode(encoded_data)
        image = Image.open(BytesIO(decoded_data))
        image_path = f'guardian_faces/{guardian_id}.png'
        image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
        image.save(image_full_path)
        return image_path
    return None


def register_guardian(request):
    if request.method == 'POST':
        form = GuardianForm(request.POST, request.FILES)
        if form.is_valid():
            guardian = form.save(commit=False)
            guardian.save()  # Save the guardian instance first to generate an ID

            face_data_uri = request.POST.get('face_image')
            image_path = handle_face_image(face_data_uri, guardian.id)
            if image_path:
                guardian.face_image = image_path

            guardian.save()
            return redirect(reverse('capture_and_train_guardian', args=[guardian.id]))  # Redirect to capture_and_train_guardian with guardian_id
    else:
        form = GuardianForm()

    return render(request, 'children_management/register_guardian.html', {'form': form})


@login_required(login_url='login')
def capture_and_train(request, guardian_id):
    cap = cv2.VideoCapture(0)
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

            cv2.imwrite(os.path.join(GUARDIAN_DATASETFACE_PATH, f"user_{guardian_id}_{sample_num}.jpg"), face_img)
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
    faces, ids = get_images_with_id(GUARDIAN_DATASETFACE_PATH)

    if len(faces) == 0 or len(ids) == 0:
        print("Error: No training data found")
        return

    recognizer.train(faces, ids)
    if not os.path.exists(os.path.dirname(GUARDIAN_RECOGNIZER_PATH)):
        os.makedirs(os.path.dirname(GUARDIAN_RECOGNIZER_PATH))
    recognizer.save(GUARDIAN_RECOGNIZER_PATH)
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


def get_profile(guardian_id):
    try:
        return Guardian.objects.get(id=guardian_id)
    except Guardian.DoesNotExist:
        return None


def recognize_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(GUARDIAN_RECOGNIZER_PATH)
    cap = cv2.VideoCapture(0)

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
            guardian_id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < confidence_threshold:
                profile = get_profile(guardian_id)
                if profile:
                    if GuardiansLog.log_recognition(profile):
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
                        log = GuardiansLog.objects.filter(guardian=profile).first()
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



def guardians_logs(request):
    recent_logs = GuardiansLog.objects.filter(recognition_time__gte=timezone.now() - timedelta(minutes=1000)).order_by('-recognition_time')
    
    # Convert time to Uganda timezone and format
    local_tz = pytz.timezone('Africa/Kampala')
    for log in recent_logs:
        log.recognition_time = log.recognition_time.astimezone(local_tz).strftime("%Y-%m-%d %I:%M:%S %p")
        if log.pickup_time:
            log.pickup_time = log.pickup_time.astimezone(local_tz).strftime("%Y-%m-%d %I:%M:%S %p")

    return render(request, 'children_management/guardians_logs.html', {'recent_logs': recent_logs})

def update_pickup_status(request, log_id):
    if request.method == 'POST':
        try:
            log = GuardiansLog.objects.get(id=log_id)
            log.child_picked = not log.child_picked
            log.pickup_time = timezone.now() if log.child_picked else None
            log.save()
            return JsonResponse({
                'child_picked': log.child_picked,
                'pickup_time': log.pickup_time.strftime('%Y-%m-%d %H:%M:%S') if log.pickup_time else None
            })
        except GuardiansLog.DoesNotExist:
            return JsonResponse({'error': 'Log not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def guardians_list(request):
    guardians = Guardian.objects.all()
    context = {"section": "guardians_list", 'guardians': guardians}
    return render(request, 'guardians_list.html', context)
