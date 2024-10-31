from django.db import migrations, models

def add_default_value(apps, schema_editor):
    Department = apps.get_model('myapp', 'Department')
    for obj in Department.objects.all():
        obj.location = 'Lahore' 
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_alter_customuser_managers"),
    ]

    operations = [
        migrations.RunPython(add_default_value)
    ]
