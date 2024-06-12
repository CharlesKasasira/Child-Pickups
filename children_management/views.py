from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Parent, Guardian, Driver, Child
from .forms import ParentForm, GuardianForm, DriverForm, ChildForm
from PIL import Image
import base64
from io import BytesIO
import os

@login_required(login_url='login')
def main_dashboard(request):
    children = Child.objects.all()
    parents = Parent.objects.all()
    drivers = Driver.objects.all()
    guardians= Guardian.objects.all()
    context = {
        "section": "dashboard",
        "number_of_children": children.count(),
        "number_of_parents": parents.count(),
        "number_of_drivers": drivers.count(),
        "number_of_guardians": guardians.count(),
    }
    return render(request, 'dashboard.html', context)

def handle_face_image(face_data_uri, unique_number, folder):
    if face_data_uri:
        _, encoded_data = face_data_uri.split(',', 1)
        decoded_data = base64.b64decode(encoded_data)
        image = Image.open(BytesIO(decoded_data))
        image_path = f'{folder}/{unique_number}.png'
        image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
        image.save(image_full_path)
        return image_path
    return None

def register_user(request, form_class, model_name, template_name, redirect_url, folder):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            face_image = request.POST.get('face_image')
            if face_image:
                user.face_image = handle_face_image(face_image, user.childs_unique_number, folder)
            user.save()
            messages.success(request, f"{model_name} successfully registered")
            return HttpResponseRedirect(redirect_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = form_class()
    context = {"section": model_name.lower(), 'form': form}
    return render(request, template_name, context)

def register_driver(request):
    return register_user(request, DriverForm, "Driver", 'register_driver.html', '/drivers/', 'driver_faces')

def register_child(request):
    return register_user(request, ChildForm, "Child", 'register_child.html', '/list_children/', 'child_faces')

def register_parent(request):
    return register_user(request, ParentForm, "Parent", 'register_parent.html', '/parents/', 'parent_faces')

def register_guardian(request):
    return register_user(request, GuardianForm, "Guardian", 'register_guardian.html', '/guardians/', 'guardian_faces')

def search_child(request):
    if request.method == 'POST':
        unique_number = request.POST.get('unique_number')
        try:
            child = Child.objects.get(childs_unique_number=unique_number)
            return render(request, 'child_details.html', {'child': child})
        except Child.DoesNotExist:
            error_message = f"Child with unique number '{unique_number}' not found."
            return render(request, 'search_child.html', {'error_message': error_message})
    else:
        return render(request, 'search_child.html')

def list_children(request):
    children = Child.objects.all()
    context = {"section": "list_children", 'children': children}
    return render(request, 'list_children.html', context)

def parents_list(request):
    parents = Parent.objects.all()
    context = {"section": "parents_list", 'parents': parents}
    return render(request, 'parents_list.html', context)



def guardians_list(request):
    guardians = Guardian.objects.all()
    context = {"section": "guardians_list", 'guardians': guardians}
    return render(request, 'guardians_list.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Successfully logged in")
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login')

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect('/')
