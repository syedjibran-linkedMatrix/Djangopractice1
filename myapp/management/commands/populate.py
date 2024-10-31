# myapp/management/commands/populate.py
import random
from django.core.management.base import BaseCommand
from faker import Faker
from myapp.models import Teacher, Student, Course, Department, Classroom, Enrollment, CustomUser

class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Departments
        departments = []
        for _ in range(5):
            department = Department.objects.create(
                name=fake.company(),
                location=fake.city(),
                head=None 
            )
            departments.append(department)

        # Create Teachers
        teachers = []
        for _ in range(5):
            teacher = Teacher.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                department=random.choice(departments)  
            )
            teachers.append(teacher)

        # Update Departments with a random head
        for department in departments:
            department.head = random.choice(teachers)  
            department.save()

        # Create Students
        students = []
        for _ in range(5):
            student = Student.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                enrollment_date=fake.date_between(start_date='-2y', end_date='today')
            )
            students.append(student)

        # Create Courses
        courses = []
        for _ in range(5):
            course = Course.objects.create(
                name=fake.word(),
                code=fake.unique.bothify(text='???###', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                teacher=None 
            )
            courses.append(course)

        # Update Courses with a random teacher
        for course in courses:
            course.teacher = random.choice(teachers) 
            course.save()

        # Create Classrooms
        classrooms = []
        for _ in range(5):
            classroom = Classroom.objects.create(
                room_number=fake.unique.random_int(min=100, max=999),
                capacity=random.randint(1, 100),
                department=None  
            )
            classrooms.append(classroom)

        # Update Classrooms with a random department
        for classroom in classrooms:
            classroom.department = random.choice(departments)  # Assign a random department
            classroom.save()

        # Create Enrollments
        for student in students:
            num_courses = random.randint(1, 5)  # Set range to 1-5
            selected_courses = random.sample(courses, k=min(num_courses, len(courses)))  

            for course in selected_courses:
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    enrollment_date=fake.date_between(start_date='-1y', end_date='today')
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data.'))
