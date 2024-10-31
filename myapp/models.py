import re
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 15
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        pattern = r"^\+92-\d{9}-\d{1}$"
        if not re.match(pattern, value):
            raise ValidationError(
                "Phone number must be in the format '+92-XXXXXXXXX-1'."
            )


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
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


class Department(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100, message="Length is greatter than 100 letters")
        ],
        blank=False,
    )
    head = models.ForeignKey(
        "Teacher",
        on_delete=models.SET_NULL,
        null=True,
        related_name="departments",
        blank=True,
    )
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])
    last_name = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])
    email = models.EmailField(
        unique=True,
        validators=[MaxLengthValidator(254)],
        blank=False,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name="teachers",
        blank=True,
    )

    def clean(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValidationError("Invalid email format.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])
    last_name = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])
    email = models.EmailField(unique=True, validators=[MaxLengthValidator(254)])
    enrollment_date = models.DateField()

    def clean(self):
        if self.enrollment_date > timezone.now().date():
            raise ValidationError("Enrollment date cannot be in the future.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    code = models.CharField(
        max_length=10, unique=True, validators=[MaxLengthValidator(10)]
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
        blank=True,
    )

    def clean(self):
        if not re.match(r"^[A-Z]{3}\d{3}$", self.code):
            raise ValidationError("Course code must be in the format 'XXX123'.")

    def __str__(self):
        return self.name


class Classroom(models.Model):
    room_number = models.CharField(
        max_length=10, unique=True, validators=[MaxLengthValidator(10)]
    )
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name="classrooms",
        blank=True,
    )

    def __str__(self):
        return self.room_number


class LargeClassroom(Classroom):
    class Meta:
        proxy = True
        verbose_name = "Large Classroom"
        verbose_name_plural = "Large Classrooms"

    def is_large(self):
        return self.capacity > 50


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrollment_date = models.DateField()

    class Meta:
        unique_together = ("student", "course")
        ordering = ["-enrollment_date", "student"]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

    def clean(self):
        if self.enrollment_date > timezone.now().date():
            raise ValidationError("Enrollment date cannot be in the future.")
