from django import forms
from .models import Parent, Guardian, Driver,Child

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name','email', 'phone_number', 'passport', 'address', 'childs_unique_number', 'gender']

class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['first_name', 'last_name','email','phone_number', 'national_idcard', 'childs_unique_number', 'gender']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name','email', 'address','phone_number', 'national_idcard', 'childs_unique_number', 'gender']

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'birth_certificate', 'childs_unique_number', 'classroom_number', 'block_name', 'parent', 'guardian', 'driver','gender']