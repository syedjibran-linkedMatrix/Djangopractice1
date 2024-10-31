from django.core.management.base import BaseCommand
from myapp.models import Teacher, Student, Course, Department, Classroom, Enrollment

class Command(BaseCommand):
    help = "Clear all populated data from the database"

    def handle(self, *args, **kwargs):
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.all().delete()
        Department.objects.all().delete()
        Classroom.objects.all().delete()
        Enrollment.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully cleared all populated data.'))
