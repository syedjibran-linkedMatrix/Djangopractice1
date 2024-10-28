from datetime import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
import re

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and return a regular user with the given phone number and password."""
        if not phone_number:
            raise ValueError("The phone number must be set.")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and return a superuser with the given phone number and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() 
    def clean(self):
        if not re.match(r"^\+\d{1,3}-\d{1,3}-\d{1,4}-\d{1,4}-\d{1,4}$", self.phone_number):
            raise ValidationError("Invalid phone number format.")
        super().clean()

    def __str__(self):
        return self.phone_number



class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, related_name='departments')
    
    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='teachers')

    def clean(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValidationError("Invalid email format.")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField()

    def clean(self):
        if self.enrollment_date > timezone.now().date():
            raise ValidationError("Enrollment date cannot be in the future.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='courses')

    def clean(self):
        if not re.match(r"^[A-Z]{3}\d{3}$", self.code):
            raise ValidationError("Course code must be in the format 'XXX123' where X is an uppercase letter.")

    def __str__(self):
        return self.name

    def clean(self):
        if self.enrollment_date > timezone.now().date():
            raise ValidationError("Enrollment date cannot be in the future.")

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"


class Classroom(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='classrooms')

    def clean(self):
        if self.capacity <= 0:
            raise ValidationError("Classroom capacity must be greater than zero.")

    def __str__(self):
        return self.room_number
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField()

    class Meta:
        unique_together = ('student', 'course')