
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
from .models import Parent
from .forms import ParentForm
from .models import Guardian
from .forms import GuardianForm
from .models import Driver
from .forms import DriverForm
from .models import Child
from .forms import ChildForm
from PIL import Image
import base64
from io import BytesIO
from django.conf import settings
from django.contrib import messages
import africastalking
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm

username = "childpickup"    # use 'sandbox' for development in the test environment
api_key = "510845c968098e21260698ee55cdba8ef4bb7f4a1125e5e7fba46c52ecfffa36"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)

sms = africastalking.SMS

@login_required(login_url='login')
def sendSMS(request):
    response = sms.send("Hello Message!", ["+256750118523"])
    print(response)

@login_required(login_url='login')
def main_dashboard(request):
    children = Child.objects.all()
    parents = Parent.objects.all()
    drivers = Driver.objects.all()
    guardians= Guardian.objects.all()
    context = {
         "section": "dashboard",
         "number_of_children": len(children),
         "number_of_parents": len(parents),
         "number_of_drivers": len(drivers),
         "number_of_guardians": len(guardians),
    }
    return render(request, 'dashboard.html', context)


def register_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)
            
            # Process the captured face image
            face_data_uri = request.POST.get('face_image')
            if face_data_uri:
                # Decode the base64 data URI
                _, encoded_data = face_data_uri.split(',', 1)
                decoded_data = base64.b64decode(encoded_data)
                image = Image.open(BytesIO(decoded_data))
                
                # Save the image to the appropriate location
                image_path = f'driver_faces/{driver.childs_unique_number}.png'
                image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                image.save(image_full_path)
                
                # Update the driver object with the image path
                driver.face_image = image_path
            
            # Process the uploaded passport
            national_idcard = request.FILES.get('national_idcard')
            if national_idcard:
                driver.national_idcard = national_idcard
            
            driver.save()
            messages.success(request, "Driver successfully registered")
            return HttpResponseRedirect('/drivers/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")
    else:
        form = DriverForm()
        context = {
         "section": "drivers_list",
         'form': form
        }
        return render(request, 'register_driver.html', context=context)
    return render(request, 'register_driver.html', {"section": "drivers_list",})


def register_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES)
        if form.is_valid():
            child = form.save(commit=False)
            
            # Process the captured face image
            face_data_uri = request.POST.get('face_image')
            if face_data_uri:
                # Decode the base64 data URI
                _, encoded_data = face_data_uri.split(',', 1)
                decoded_data = base64.b64decode(encoded_data)
                image = Image.open(BytesIO(decoded_data))
                
                # Save the image to the appropriate location
                image_path = f'child_faces/{child.childs_unique_number}.png'
                image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                image.save(image_full_path)
                
                # Update the child object with the image path
                child.face_image = image_path
            
            # Process the uploaded passport
            # national_idcard = request.FILES.get('national_idcard')
            # if national_idcard:
            #     child.national_idcard = national_idcard
            
            child.save()
            messages.success(request, "Child successfully registered")
            return HttpResponseRedirect('/list_children/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error} {field}")
    else:
        form = ChildForm()
        context = {
         "section": "list_children",
         'form': form
        }
        return render(request, 'register_child.html', context)
    return render(request, 'register_child.html', {"section": "list_children",})

    # if request.method == 'POST':
    #     form = ChildForm(request.POST, request.FILES)
    #     print(form)
    #     if form.is_valid():
    #         # Extract the image data and birth certificate from the request
    #         image_data = request.POST.get('face_image')
    #         birth_certificate = request.FILES.get('birth_certificate')  # Extract birth certificate file
    #         if image_data:
    #             format, imgstr = image_data.split(';base64,')
    #             ext = format.split('/')[-1]
    #             data = BytesIO(base64.b64decode(imgstr))
    #             image = Image.open(data)
    #             child = form.save(commit=False)
    #             child.face_image.save(f'child_face.{ext}', image)
    #             if birth_certificate:
    #                 child.birth_certificate = birth_certificate  # Save birth certificate file
    #             child.save()
    #             return HttpResponse('Child registered successfully!')
    #         else:
    #             return HttpResponse('Error: Face image not captured!')
    #     else:
    #         return render(request, 'register_child.html', {'form': form})
    # else:
    #     form = ChildForm()
    #     context = {
    #      "section": "list_children",
    #      'form': form
    #     }
    #     return render(request, 'register_child.html', context)


def register_parent(request):
    if request.method == 'POST':
        form = ParentForm(request.POST, request.FILES)
        if form.is_valid():
            parent = form.save(commit=False)
            
            # Process the captured face image
            face_data_uri = request.POST.get('face_image')
            if face_data_uri:
                # Decode the base64 data URI
                _, encoded_data = face_data_uri.split(',', 1)
                decoded_data = base64.b64decode(encoded_data)
                image = Image.open(BytesIO(decoded_data))
                
                # Save the image to the appropriate location
                image_path = f'parent_faces/{parent.childs_unique_number}.png'
                image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                image.save(image_full_path)
                
                # Update the parent object with the image path
                parent.face_image = image_path
            
            # Process the uploaded passport
            passport = request.FILES.get('passport')
            if passport:
                parent.passport = passport
            
            parent.save()
            messages.success(request, "Parent successfully registered")
            return HttpResponseRedirect('/parents/')
    else:
        form = ParentForm()
        context = {
         "section": "parents_list",
         'form': form
        }
    return render(request, 'register_parent.html', context)
    
def register_guardian(request):
    if request.method == 'POST':
        form = GuardianForm(request.POST, request.FILES)
        if form.is_valid():
            guardian = form.save(commit=False)
            
            # Process the captured face image
            face_data_uri = request.POST.get('face_image')
            if face_data_uri:
                # Decode the base64 data URI
                _, encoded_data = face_data_uri.split(',', 1)
                decoded_data = base64.b64decode(encoded_data)
                image = Image.open(BytesIO(decoded_data))
                
                # Save the image to the appropriate location
                image_path = f'guardian_faces/{guardian.childs_unique_number}.png'
                image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                image.save(image_full_path)
                
                # Update the guardian object with the image path
                guardian.face_image = image_path
            
            # Process the uploaded passport
            national_idcard = request.FILES.get('national_idcard')
            if national_idcard:
                guardian.national_idcard = national_idcard
            
            guardian.save()
            messages.success(request, "Guardian successfully registered")
            return HttpResponseRedirect('/guardians/')
    else:
        form = GuardianForm()
        context = {
         "section": "guardians_list",
         'form': form
        }
    return render(request, 'register_guardian.html', context)

    
    
def search_child(request):
    if request.method == 'POST':
        unique_number = request.POST.get('unique_number')
        try:
            child = Child.objects.get(childs_unique_number=unique_number)
            return render(request, 'child_details.html', {'child': child})
        except Child.DoesNotExist:
            error_message = "Child with unique number '{}' not found.".format(unique_number)
            return render(request, 'search_child.html', {'error_message': error_message})
    else:
        return render(request, 'search_child.html')
    
def list_children(request):
    children = Child.objects.all()
    context = {
         "section": "list_children",
         'children': children
    }
    return render(request, 'list_children.html', context)

def parents_list(request):
    parents = Parent.objects.all()
    context = {
         "section": "parents_list",
         'parents': parents
    }
    return render(request, 'parents_list.html', context)

def drivers_list(request):
    drivers = Driver.objects.all()
    context = {
         "section": "drivers_list",
         'drivers': drivers
    }
    return render(request, 'drivers_list.html', context)

def guardians_list(request):
    guardians= Guardian.objects.all()
    context = {
         "section": "guardians_list",
         'guardians': guardians
    }
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
