# Generated by Django 5.1.3 on 2024-12-13 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_schedule_teacher_alter_classes_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]