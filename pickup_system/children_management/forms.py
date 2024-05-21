from django import forms
from .models import Parent, Guardian, Driver,Child

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'phone_number', 'passport', 'address', 'face_image', 'childs_unique_number', 'gender']

class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['first_name', 'last_name', 'phone_number', 'national_idcard', 'face_image', 'childs_unique_number', 'gender']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'phone_number', 'national_idcard', 'face_image', 'childs_unique_number', 'gender']

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'birth_certificate', 'childs_unique_number', 'face_image', 'classroom_number', 'block_name', 'parent', 'guardian', 'driver','gender']