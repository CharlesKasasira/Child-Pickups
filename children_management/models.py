from django.db import models
from django.utils import timezone
from datetime import timedelta


class Parent(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20)
    passport = models.ImageField(upload_to='parent_passports/', blank=True, null=True)
    address = models.TextField()
    face_image = models.ImageField(upload_to='parent_faces/', blank=True, null=True)
    childs_unique_number = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class ParentsLog(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    recognition_time = models.DateTimeField(auto_now_add=True)
    child_picked = models.BooleanField(default=False)
    pickup_time = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def log_recognition(parent):
        current_time = timezone.now()
        ten_minutes_ago = current_time - timedelta(minutes=10)

        if not ParentsLog.objects.filter(parent=parent, recognition_time__gte=ten_minutes_ago).exists():
            ParentsLog.objects.create(parent=parent)
            return True
        return False


class Guardian(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20)
    national_idcard = models.ImageField(upload_to='guardian_national_idcard/', blank=True, null=True)
    face_image = models.ImageField(upload_to='guardian_faces/', blank=True, null=True)
    childs_unique_number = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class GuardiansLog(models.Model):
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    recognition_time = models.DateTimeField(auto_now_add=True)
    child_picked = models.BooleanField(default=False)
    pickup_time = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def log_recognition(guardian):
        current_time = timezone.now()
        ten_minutes_ago = current_time - timedelta(minutes=10)

        if not GuardiansLog.objects.filter(guardian=guardian, recognition_time__gte=ten_minutes_ago).exists():
            GuardiansLog.objects.create(guardian=guardian)
            return True
        return False
    


class Driver(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100,)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    address = models.TextField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    national_idcard = models.ImageField(upload_to='drivers_national_idcard/', blank=True, null=True)
    face_image = models.ImageField(upload_to='driver_faces/', blank=True, null=True)
    # Provide a default value for the field
    childs_unique_number = models.CharField(max_length=100, null=True, unique=True, default='driver_0001')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    child_picked = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name



class RecognitionLog(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    recognition_time = models.DateTimeField(auto_now_add=True)
    child_picked = models.BooleanField(default=False)
    pickup_time = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def log_recognition(driver):
        current_time = timezone.now()
        ten_minutes_ago = current_time - timedelta(minutes=10)

        if not RecognitionLog.objects.filter(driver=driver, recognition_time__gte=ten_minutes_ago).exists():
            RecognitionLog.objects.create(driver=driver)
            return True
        return False


class Child(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    birth_certificate = models.ImageField(upload_to='birth_certificates/', blank=True, null=True)
    childs_unique_number = models.CharField(max_length=100, unique=True)
    face_image = models.ImageField(upload_to='child_faces/', blank=True, null=True)
    classroom_number = models.CharField(max_length=100)
    block_name = models.CharField(max_length=100)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, blank=True, null=True)
    guardian = models.ForeignKey(Guardian, on_delete=models.SET_NULL, blank=True, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    child_picked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ChildrenLog(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    recognition_time = models.DateTimeField(auto_now_add=True)
    child_picked = models.BooleanField(default=False)
    pickup_time = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def log_recognition(child):
        current_time = timezone.now()
        ten_minutes_ago = current_time - timedelta(minutes=10)

        if not ChildrenLog.objects.filter(child=child, recognition_time__gte=ten_minutes_ago).exists():
            ChildrenLog.objects.create(child=child)
            return True
        return False
