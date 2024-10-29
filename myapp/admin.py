from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Department, Teacher, Student, Course, Enrollment, Classroom, CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff', 'is_active', 'delete_button')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)

    def delete_button(self, obj):
        url = reverse('admin:myapp_customuser_delete', args=[obj.id])
        return format_html('<a class="button" href="{}" style="color:red;">Delete User</a>', url)
    delete_button.short_description = "Delete"

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'edit_button', 'delete_button')
    search_fields = ('name',)
    actions = ['make_uppercase']

    def edit_button(self, obj):
        url = reverse('admin:myapp_department_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Edit Department</a>', url)

    def delete_button(self, obj):
        url = reverse('admin:myapp_department_delete', args=[obj.id])
        return format_html('<a class="button" href="{}" style="color:red;">Delete Department</a>', url)

    def make_uppercase(self, request, queryset):
        for department in queryset:
            department.name = department.name.upper()
            department.save()
        self.message_user(request, "Department names updated to uppercase.")

    make_uppercase.short_description = "Make selected departments uppercase"

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'edit_button', 'delete_button')
    search_fields = ('first_name', 'last_name', 'email')
    actions = ['make_uppercase']

    def edit_button(self, obj):
        url = reverse('admin:myapp_teacher_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Edit Teacher</a>', url)

    def delete_button(self, obj):
        url = reverse('admin:myapp_teacher_delete', args=[obj.id])
        return format_html('<a class="button" href="{}" style="color:red;">Delete Teacher</a>', url)

    def make_uppercase(self, request, queryset):
        for teacher in queryset:
            teacher.first_name = teacher.first_name.upper()
            teacher.last_name = teacher.last_name.upper()
            teacher.save()
        self.message_user(request, "Teacher names updated to uppercase.")

    make_uppercase.short_description = "Make selected teachers' names uppercase"

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'enrollment_date', 'edit_button', 'delete_button')
    search_fields = ('first_name', 'last_name', 'email')
    actions = ['make_uppercase']

    def edit_button(self, obj):
        url = reverse('admin:myapp_student_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Edit Student</a>', url)

    def delete_button(self, obj):
        url = reverse('admin:myapp_student_delete', args=[obj.id])
        return format_html('<a class="button" href="{}" style="color:red;">Delete Student</a>', url)

    def make_uppercase(self, request, queryset):
        for student in queryset:
            student.first_name = student.first_name.upper()
            student.last_name = student.last_name.upper()
            student.save()
        self.message_user(request, "Student names updated to uppercase.")

    make_uppercase.short_description = "Make selected students' names uppercase"

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'edit_button', 'delete_button')
    search_fields = ('name', 'code')
    actions = ['make_uppercase']

    def edit_button(self, obj):
        url = reverse('admin:myapp_course_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Edit Course</a>', url)

    def delete_button(self, obj):
        url = reverse('admin:myapp_course_delete', args=[obj.id])
        return format_html('<a class="button" href="{}" style="color:red;">Delete Course</a>', url)

    def make_uppercase(self, request, queryset):
        for course in queryset:
            course.name = course.name.upper()
            course.save()
        self.message_user(request, "Course names updated to uppercase.")

    make_uppercase.short_description = "Make selected courses uppercase"

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'edit_button', 'delete_button')
    search_fields = ('student__first_name', 'course__name')

    def edit_button(self, obj):
        url = reverse('admin:myapp_enrollment_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Edit Enrollment</a>', url)

    def delete_button(self, obj):
        url = reverse('admin:myapp_enrollment_delete', args=[obj.id])
        return format_html('<a class="button" href="{}" style="color:red;">Delete Enrollment</a>', url)

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'capacity', 'department', 'edit_button', 'delete_button')
    search_fields = ('room_number',)

    def edit_button(self, obj):
        url = reverse('admin:myapp_classroom_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Edit Classroom</a>', url)

    def delete_button(self, obj):
        url = reverse('admin:myapp_classroom_delete', args=[obj.id])
        return format_html('<a class="button" href="{}" style="color:red;">Delete Classroom</a>', url)

# Register the models with the custom admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Classroom, ClassroomAdmin)
