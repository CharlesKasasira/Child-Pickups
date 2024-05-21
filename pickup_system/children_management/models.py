from django.db import models

class Parent(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    passport = models.ImageField(upload_to='parent_passports/', blank=True, null=True)
    address = models.TextField()
    face_image = models.ImageField(upload_to='parent_faces/', blank=True, null=True)
    childs_unique_number = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

class Guardian(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    national_idcard = models.ImageField(upload_to='guardian_national_idcard/', blank=True, null=True)
    face_image = models.ImageField(upload_to='guardian_faces/', blank=True, null=True)
    childs_unique_number = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

class Driver(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    national_idcard = models.ImageField(upload_to='drivers_national_idcard/', blank=True, null=True)
    face_image = models.ImageField(upload_to='driver_faces/', blank=True, null=True)
    childs_unique_number = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

class Child(models.Model):
     GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
     first_name = models.CharField(max_length=100)
     last_name = models.CharField(max_length=100, blank=True, null=True)
     birth_certificate = models.ImageField(upload_to='birth_certificates/', blank=True, null=True)
     childs_unique_number = models.CharField(max_length=100, unique=True)
     face_image = models.ImageField(upload_to='child_faces/')
     classroom_number = models.CharField(max_length=100)
     block_name = models.CharField(max_length=100)
     parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, blank=True, null=True)
     guardian = models.ForeignKey(Guardian, on_delete=models.SET_NULL, blank=True, null=True)
     driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True)
     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
