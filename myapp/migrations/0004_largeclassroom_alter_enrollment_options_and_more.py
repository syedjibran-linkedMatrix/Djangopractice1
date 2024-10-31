
import django.core.validators
import django.db.models.deletion
import myapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_auto_20241030_1154"),
    ]

    operations = [
        migrations.CreateModel(
            name="LargeClassroom",
            fields=[],
            options={
                "verbose_name": "Large Classroom",
                "verbose_name_plural": "Large Classrooms",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("myapp.classroom",),
        ),
        migrations.AlterModelOptions(
            name="enrollment",
            options={
                "ordering": ["-enrollment_date", "student"],
                "verbose_name": "Enrollment",
                "verbose_name_plural": "Enrollments",
            },
        ),
        migrations.AddField(
            model_name="department",
            name="location",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="classroom",
            name="capacity",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="classroom",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="classrooms",
                to="myapp.department",
            ),
        ),
        migrations.AlterField(
            model_name="classroom",
            name="room_number",
            field=models.CharField(
                max_length=10,
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(10)],
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="code",
            field=models.CharField(
                max_length=10,
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(10)],
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="name",
            field=models.CharField(
                max_length=100,
                validators=[django.core.validators.MaxLengthValidator(100)],
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="teacher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="courses",
                to="myapp.teacher",
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=myapp.models.PhoneNumberField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name="department",
            name="head",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="departments",
                to="myapp.teacher",
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="name",
            field=models.CharField(
                max_length=100,
                validators=[
                    django.core.validators.MaxLengthValidator(
                        100, message="Length is greatter than 100 letters"
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="email",
            field=models.EmailField(
                max_length=254,
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(254)],
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="first_name",
            field=models.CharField(
                max_length=50,
                validators=[django.core.validators.MaxLengthValidator(50)],
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="last_name",
            field=models.CharField(
                max_length=50,
                validators=[django.core.validators.MaxLengthValidator(50)],
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="teachers",
                to="myapp.department",
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="email",
            field=models.EmailField(
                max_length=254,
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(254)],
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="first_name",
            field=models.CharField(
                max_length=50,
                validators=[django.core.validators.MaxLengthValidator(50)],
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="last_name",
            field=models.CharField(
                max_length=50,
                validators=[django.core.validators.MaxLengthValidator(50)],
            ),
        ),
    ]
